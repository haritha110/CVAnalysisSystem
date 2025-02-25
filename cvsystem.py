import streamlit as st
import fitz  # PyMuPDF for PDFs
import docx
import openai
import json
import os
from io import BytesIO

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")


# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf_doc:
        text += page.get_text("text") + "\n"
    return text


# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    try:
        # Convert uploaded file to a readable stream
        file_stream = BytesIO(uploaded_file.getvalue())  # Use getvalue() instead of read()
        doc = docx.Document(file_stream)  # Open DOCX from BytesIO
        extracted_text = "\n".join([para.text for para in doc.paragraphs])  # Extract text

        if not extracted_text.strip():
            return "Error: No text found in the DOCX file."

        return extracted_text
    except Exception as e:
        return f"Error reading DOCX file: {str(e)}"


# Function to process multiple CVs
def process_cv_files(uploaded_files):
    extracted_data = {}
    for uploaded_file in uploaded_files:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension == "pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif file_extension == "docx":
            extracted_text = extract_text_from_docx(uploaded_file)
        else:
            extracted_text = "Unsupported file format."

        extracted_data[uploaded_file.name] = extracted_text
    return extracted_data


# Function to analyze text with OpenAI LLM
def analyze_cv(text):
    prompt = f"Extract structured information from this CV:\n{text}\n\nFormat: JSON with keys - name, email, phone, skills, education, experience."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI assistant for CV parsing."},
                      {"role": "user", "content": prompt}]
        )
        return json.loads(response["choices"][0]["message"]["content"])
    except Exception as e:
        return {"error": str(e)}


# Streamlit UI
st.title("📄 CV Analysis Chatbot")

# Upload multiple CV files
uploaded_files = st.file_uploader("Upload CVs (PDF & DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

cv_data = {}

if uploaded_files:
    with st.spinner("Extracting text from CVs..."):
        extracted_texts = process_cv_files(uploaded_files)

    for file_name, text in extracted_texts.items():
        if text and text != "Unsupported file format.":
            with st.spinner(f"Analyzing {file_name}..."):
                structured_data = analyze_cv(text)

            if "error" not in structured_data:
                cv_data[file_name] = structured_data
            else:
                st.error(f"Error in {file_name}: {structured_data['error']}")
        else:
            st.error(f"Failed to extract text from {file_name}")

    # Display structured CV data
    if cv_data:
        st.success("CVs processed successfully!")
        st.json(cv_data)

# Query CV Data
query = st.text_input("🔍 Enter your query:")
if st.button("Submit") and query:
    if cv_data:
        with st.spinner("Searching CVs for relevant data..."):
            formatted_data = "\n".join([f"{name}: {json.dumps(data, indent=2)}" for name, data in cv_data.items()])
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are an AI assistant for analyzing CVs."},
                          {"role": "user",
                           "content": f"From this structured CV data, answer this query: {query}\n\n{formatted_data}"}]
            )
            st.write(response["choices"][0]["message"]["content"])
    else:
        st.error("Please upload at least one CV first.")
