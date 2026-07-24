import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PyPDF2

# Load API key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("📚 AI Study Notes Summarizer")

option = st.radio(
    "Choose Input Method",
    ["Paste Notes", "Upload PDF"]
)

text = ""

# Paste notes
if option == "Paste Notes":
    text = st.text_area("Paste your study notes", height=250)

# Upload PDF
else:
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:
        pdf = PyPDF2.PdfReader(uploaded_file)

        for page in pdf.pages:
            text += page.extract_text()

if st.button("Generate"):

    if text == "":
        st.warning("Please enter notes.")
    else:

        prompt = f"""
        You are an AI Study Assistant.

        Read the following notes.

        Generate:

        1. Summary
        2. Important Points
        3. 5 Quiz Questions

        Notes:

        {text}
        """

        response = model.generate_content(prompt)

        st.success("Done!")

        st.write(response.text)