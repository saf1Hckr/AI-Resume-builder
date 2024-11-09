#downloader.py
import os
import requests
import shutil

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {url} to {save_path}")
    else:
        print(f"Failed to download {url}: {response.status_code}")


def download_files_from_text_file(text_file_path, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with open(text_file_path, "r") as file:
        lines = file.readlines()

    project_name = None

    for line in lines:
        line = line.strip()

        if line.startswith("http"):  
            if project_name:
                file_extension = line.split("/")[
                    -1
                ]  
                save_path = os.path.join(save_dir, f"{project_name}_{file_extension}")
                download_file(line, save_path)
                project_name = None  
        else:
            project_name = line


text_file_path = "download_links.txt"
save_dir = "downloads"

if os.path.exists(save_dir):
    shutil.rmtree("downloads")

download_files_from_text_file(text_file_path, save_dir)
