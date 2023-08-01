import os
from pathlib import Path

files_bp = Blueprint("files", __name__)

# Sample data (in real-world, this would come from a database)
files = [
    {"id": 1, "name": "File 1", "size": 50, "priority": 3},
    {"id": 2, "name": "File 2", "size": 30, "priority": 2},
    # Add more files here
]

@files_bp.route("/files", methods=["GET"])
def get_files():
    return jsonify(files)

# Additional API endpoints for adding, updating, and deleting files
# Example of specifying a single folder
target_folder = "/path/to/your/folder"

# Example of specifying multiple folders
target_folders = ["/path/to/folder1", "/path/to/folder2", "/path/to/folder3"]

def scan_folder(folder_path):
    for entry in os.scandir(folder_path):
        if entry.is_file():
            # Process the file
            print("File:", entry.name)
        elif entry.is_dir():
            # Process the subdirectory
            print("Directory:", entry.name)
            scan_folder(entry.path)  # Recursive call to scan subfolder if desired

# For scanning a single folder
scan_folder(target_folder)

# For scanning multiple folders
for folder in target_folders:
    scan_folder(folder)
