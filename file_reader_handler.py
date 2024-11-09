import os
import pdfplumber
from docx import Document
from Final_Summary_Ai import get_Finalresponse
from OpenAi_embedding import get_openai_embedding
from Summary_Ai import get_response
from milvus_handler import create_milvus_collection, insert_into_milvus

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

def add_to_data_dict(file_data, file_name, content):
    if file_name in file_data:
        index = 1
        new_name = f"{file_name}_{index}"
        while new_name in file_data:
            index += 1
            new_name = f"{file_name}_{index}"
        file_data[new_name] = content
    else:
        file_data[file_name] = content

def process_child_folder(child_folder_path, user_id):
    print(f"Processing folder: {child_folder_path}")
    file_data = getFilepath(child_folder_path)
    process_and_insert_data(file_data, user_id)

def getFilepath(folderpath):
    file_data = {}

    extensions = [
        ".doc", ".rtf", ".odt", ".tex",
        ".xls", ".xlsx", ".csv", ".ods",
        ".ppt", ".pptx", ".odp",
        ".py", ".java", ".cpp", ".c", ".cs", ".js", ".html", ".css", ".md", ".rb", ".php", ".sh", ".sol", ".go", ".rs",
        ".json", ".yaml", ".yml", ".xml", ".ini", ".cfg", ".conf",
        ".sql", ".db", ".dbf", ".log", ".dat", ".sqlite",
        ".bat", ".ps1", ".vbs", ".ts", ".tsx", ".jsx", ".txt", ".toml"
    ]

    delete_drawio_files(folderpath)

    for file_path in find_files(folderpath, ['.docx']):
        file_name = os.path.basename(file_path)
        content = docx_to_text(file_path)
        add_to_data_dict(file_data, file_name, content)

    for pdf_file_path in find_files(folderpath, ['.pdf']):
        file_name = os.path.basename(pdf_file_path)
        content = pdf_to_text(pdf_file_path)
        add_to_data_dict(file_data, file_name, content)

    for file_path in find_files(folderpath, extensions):
        file_name = os.path.basename(file_path)
        content = read_txt_file(file_path)
        add_to_data_dict(file_data, file_name, content)
        
    print(f"Processed {len(file_data)} files in folder '{folderpath}'.")
    return file_data

def process_and_insert_data(file_data, user_id):
    if not isinstance(file_data, dict):
        print("The data is not a dictionary.")
        return
    
    # Create Milvus collection if not already present
    create_milvus_collection(user_id, dimension=1536)

    embedding_data = []
    id_counter = 1
    summary = ""

    for key, value in file_data.items():
        if isinstance(value, str):
            summary += (get_response(value)) + "\n"
        else:
            print(f"Value for '{key}' is not a string and was skipped.")
    
    final_summary = get_Finalresponse(summary)

    if final_summary:
        print(f"Generated summary for '{key}': {final_summary}...")
        embedding = get_openai_embedding(final_summary)
        if embedding is not None:
            embedding_data.append({
                "id": id_counter,
                "vector": embedding.tolist(),
                "title": key,
                "text": final_summary,
                "subject": f"Source:"
            })
            id_counter += 1
        else:
            print(f"Summary for '{key}' exceeds the maximum token limit; embedding was not generated.")
    else:
        print(f"Could not generate a summary for '{key}'.")
    
    if embedding_data:
        insert_into_milvus(embedding_data, user_id)
        print("Data has been successfully processed and inserted into Milvus.")
    else:
        print("No valid data to insert.")

def extract_and_process_main_folder(parent_folder, user_id):
    for item in os.listdir(parent_folder):
        item_path = os.path.join(parent_folder, item)
        if os.path.isdir(item_path):  # Check if it is a directory
            process_child_folder(item_path, user_id)

# Main execution
if __name__ == '__main__':
    user_id = "user123"
    parent_folder = "extracted"
    extract_and_process_main_folder(parent_folder, user_id)
