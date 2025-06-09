import fitz  # PyMuPDF
from docx import Document
import os

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_text_from_pdf(path):
    with fitz.open(path) as doc:
        return "\n".join(page.get_text() for page in doc)

def extract_text(file_path):
    if file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")
