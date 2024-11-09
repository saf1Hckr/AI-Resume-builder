import os
import pdfplumber
from docx import Document

def find_files(base_dir, included_extensions):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(tuple(included_extensions)):
                yield os.path.join(root, file)

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def pdf_to_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

def docx_to_text(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def delete_drawio_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.drawio'):
                os.remove(os.path.join(root, file))
                print(f"Deleted {os.path.join(root, file)}")

def getFilepath2(folderpath):
    base_dir = folderpath  # Replace with the actual path
    combined_text = ""

    extensions = [
        ".doc", ".rtf", ".odt", ".tex",
        ".xls", ".xlsx", ".csv", ".ods",
        ".ppt", ".pptx", ".odp",
        ".py", ".java", ".cpp", ".c", ".cs", ".js", ".html", ".css", ".md", ".rb", ".php", ".sh", ".sol", ".go", ".rs",
        ".json", ".yaml", ".yml", ".xml", ".ini", ".cfg", ".conf",
        ".sql", ".db", ".dbf", ".log", ".dat", ".sqlite",
        ".bat", ".ps1", ".vbs", ".ts", ".tsx", ".jsx", ".txt", ".toml"
    ]

    delete_drawio_files(base_dir)

    for file_path in find_files(base_dir, ['.docx']):
        content = docx_to_text(file_path)
        combined_text += content + "\n"

    for pdf_file_path in find_files(base_dir, ['.pdf']):
        content = pdf_to_text(pdf_file_path)
        combined_text += content + "\n"

    for file_path in find_files(base_dir, extensions):
        content = read_txt_file(file_path)
        combined_text += content + "\n"
    
    print(f"Processed files and combined text.")
    return combined_text  # Return a single concatenated string of all file contents
