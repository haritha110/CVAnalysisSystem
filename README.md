# 📄 CV Analysis Chatbot
The CV Analysis System is a Streamlit-based application that processes multiple CVs (PDF &amp; DOCX) using OCR and LLMs to extract structured information. It allows users to upload resumes and query extracted data via a chatbot interface.

## 🚀 Features

- Upload and process multiple CVs (PDF & DOCX format)

- Extract structured data: Name, Education, Skills, Work Experience, Projects, Certifications

- Query extracted data using an LLM-powered chatbot

- Handle API rate limiting and errors gracefully

- Interactive Streamlit UI

## 🛠️ Installation

1. Clone the Repository

   ```bash
    git clone https://github.com/yourusername/CVAnalysisSystem.git
    cd CVAnalysisSystem

2. Create a Virtual Environment
   
     ```bash
    python -m venv .venv
    source .venv/bin/activate   # On Windows, use: .venv\Scripts\activate

3. Install Dependencies

   ```bash
   pip install -r requirements.txt

5. Set Up API Keys (Optional)

    If you're using OpenAI API, create a .env file and add:
     ```bash
    OPENAI_API_KEY=your_api_key_here

## ▶️ Usage

  Run the Streamlit App

   ```bash
      streamlit run cvsystem.py
  ```

**Upload CVs and Query Data**

1. Open the web interface in your browser.
2. Upload multiple resumes (PDF or DOCX).
3. Query extracted information (e.g., "Find candidates skilled in Python").

## 📂 File Structure

 ```bash
CVAnalysisSystem/
│── cvsystem.py          # Main application
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
│── .env                 # API keys (ignored in .gitignore)
 ```

## 🤖 Tech Stack

- Frontend: Streamlit

- Backend: Python

- Libraries: PyMuPDF, python-docx, openai, streamlit

## 🛠️ Troubleshooting

1. DOCX Processing Error: "File is not a ZIP file"

    - Ensure the uploaded file is a valid DOCX file.

    - Use `uploaded_file.getvalue()` in `extract_text_from_docx()` .

2. LLM Processing Error: "Missing required arguments"

    - Ensure `model` and `prompt` are passed correctly to the OpenAI API.




