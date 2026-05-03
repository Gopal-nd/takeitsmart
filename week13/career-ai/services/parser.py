from io import BytesIO
from docx import Document
import PyPDF2
from fastapi import UploadFile, HTTPException

def extract_text(file: UploadFile) -> str:
    filename = file.filename.lower()
    content = file.file.read()

    if filename.endswith(".txt"):
        return content.decode("utf-8")

    elif filename.endswith(".docx"):
        doc = Document(BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs])

    elif filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(BytesIO(content))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type (.pdf, .docx, .txt only)"
        )
