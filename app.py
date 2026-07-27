import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import PyPDF2

# Load API key
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config(page_title="AI Study Notes Summarizer")

st.title("📚 AI Study Notes Summarizer")

option = st.radio(
    "Choose Input Method",
    ["Paste Notes", "Upload PDF"]
)

text = ""

if option == "Paste Notes":
    text = st.text_area(
        "Paste your study notes",
        height=250
    )

else:
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:
        pdf = PyPDF2.PdfReader(uploaded_file)

        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

if st.button("Generate"):

    if text.strip() == "":
        st.warning("Please enter or upload notes.")

    else:

        prompt = f"""
You are an AI Study Assistant.

Read the following notes carefully.

Generate:

1. Summary
2. Important Points
3. 5 Quiz Questions with Answers

Notes:

{text}
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            st.success("Notes Generated Successfully!")

            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error: {e}")