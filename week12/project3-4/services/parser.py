import pandas as pd
from docx import Document as DocxDocument
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
import mysql.connector
from app.config import DB_CONFIG

def read_pdf(file):
    reader = PdfReader(file)
    return "".join([page.extract_text() or "" for page in reader.pages])

def read_docx(file):
    doc = DocxDocument(file)
    return "\n".join([p.text for p in doc.paragraphs])

def read_csv(file):
    df = pd.read_csv(file)
    return df.to_csv(index=False)

def read_txt(file):
    return file.read().decode("utf-8", errors="ignore")

def read_website(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(separator="\n")
    except:
        return ""

def read_mysql_database(table_name):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        conn.close()
        return df.to_csv(index=False)
    except Exception as e:
        print("DB Error:", e)
        return ""

def detect_department(filename):
    name = filename.lower()
    if "hr" in name: return "HR"
    if "finance" in name: return "Finance"
    if "it" in name: return "IT"
    return "General"
