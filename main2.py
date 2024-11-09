import os
import zipfile
import shutil
import signal
import subprocess

from file_reader_handler import extract


def run_python_script(script_name):
    try:
        subprocess.run(["python3", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        exit(1)


run_python_script("github.py")
run_python_script("downloader.py")


# Define timeout handler
def handler(signum, frame):
    raise TimeoutError("Extraction took too long")


# Set the timeout handler
signal.signal(signal.SIGALRM, handler)

# Define directories
zip_dir = "downloads"
extract_dir = "extracted"

# Clean up extract_dir if it exists
if os.path.exists(extract_dir):
    shutil.rmtree(extract_dir)

# Create a new directory to extract files
if not os.path.exists(extract_dir):
    os.makedirs(extract_dir)

print("Extracting files")

# Extract ZIP files
for subdir, dirs, files in os.walk(zip_dir):
    for zipp in files:
        if zipp.endswith(".zip"):
            filepath = os.path.join(subdir, zipp)
            print(f"Processing file: {filepath}")

            # Set the timer to 5 seconds before raising TimeoutError
            signal.alarm(20)

            try:
                with zipfile.ZipFile(filepath, "r") as zip_ref:
                    zip_ref.testzip()  # Check for any issues in the ZIP file
                    zip_ref.extractall(extract_dir)
                    print(f"Extracted {zipp} to {extract_dir}")
                signal.alarm(0)  # Disable the alarm if extraction is successful

            except TimeoutError:
                print(f"Skipped {zipp}: Extraction took too long")
            except zipfile.BadZipFile:
                print(f"Error: {zipp} is not a valid ZIP file.")
            except Exception as e:
                print(f"Error extracting {zipp}: {e}")

print("Extraction complete!")
extract()

