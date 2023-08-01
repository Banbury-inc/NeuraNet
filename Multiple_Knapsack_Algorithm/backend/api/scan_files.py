import os

target_folder = "//Users/michaelmills/Pictures/Final_Project"
def scan_folder(folder_path):
    file_list = []  # Initialize an empty list to store file information

    for entry in os.scandir(folder_path):
        if entry.is_file():
            # Process the file
            file_info = get_file_info(entry.path, priority="high")
            if file_info is not None:
                file_list.append(file_info)  # Add file_info dictionary to the list

        elif entry.is_dir():
            # Process the subdirectory
            print("Directory:", entry.name)
            # Recursive call to scan subfolder and extend the file_list with its result
            file_list.extend(scan_folder(entry.path))

    return file_list

def get_file_info(file_path, priority="normal"):
    if not os.path.exists(file_path):
        return None

    file_id = hash(file_path)  # You can use a hash of the file path as an identifier
    file_name = os.path.basename(file_path)
    file_size_bytes = os.path.getsize(file_path)
    file_size = file_size_bytes / (1024 * 1024)  # Convert bytes to megabytes
    priority_level = priority

    return {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
        "file_path": file_path,
        "priority_level": priority_level,
    }

# For scanning a single folder
file_info_list = scan_folder(target_folder)

# Print the list of file information
for file_info in file_info_list:
    print(f"File ID: {file_info['file_id']}, File Name: {file_info['file_name']}, "
          f"File Size: {file_info['file_size']}, File Path: {file_info['file_path']}, "
          f"Priority Level: {file_info['priority_level']}")

def get_file_sizes(file_info_list):
    file_sizes = []  # Initialize an empty list to store file sizes

    for file_info in file_info_list:
        file_size = file_info["file_size"]
        file_sizes.append(file_size)

    return file_sizes

