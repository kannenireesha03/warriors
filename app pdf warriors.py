import os
import google.generativeai as genai
import fitz  # PyMuPDF
import streamlit as st

# Directly configure the Gemini API key (replace with your actual API key)
api_key = "AIzaSyAATUQu36TEQSAWMp-tIpT9bC290x1jYoI"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Set up Gemini model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",  # Specify your model name here
    generation_config=generation_config,
)

# Function to extract text from PDF using PyMuPDF (fitz)
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

# Function to summarize the document using Gemini API
def summarize_with_gemini(text):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "pdf summarizer",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Okay, I'm ready to help you summarize a PDF! Please provide the PDF content or the file itself.",
                ],
            },
        ]
    )
    response = chat_session.send_message(text)
    return response.text

# Streamlit UI and functionality
def main():
    st.title("Gemini Powered PDF Summarizer")

    # File uploader for PDF
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded PDF
        file_path = f"temp_pdf.pdf"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract text from the uploaded PDF
        extracted_text = extract_text_from_pdf(file_path)

        # Option to summarize the document
        if st.button("Summarize PDF"):
            summary = summarize_with_gemini(extracted_text)
            st.subheader("Summary:")
            st.write(summary)

if __name__ == "__main__":
    main() 