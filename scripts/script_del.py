import os
import sys

def remove_pcap_files(folder, k):
    if k == 30:
        j = 1
    else:
        j = 0

    # Calculate the limit for files to keep
    keep_count = 4000 + (200 * j)

    # Ensure the folder exists
    if not os.path.exists(folder):
        print(f"Error: The folder '{folder}' does not exist.")
        sys.exit(1)

    # List all files in the folder
    all_files = os.listdir(folder)

    # Filter out files that are not PCAP files with the correct naming format "capture-x.cap"
    pcap_files = [file for file in all_files if file.startswith("capture-") and file.endswith(".cap")]

    # Sort the PCAP files based on the number in the filename without using regex
    def extract_number(file_name):
        # Split by '-' and '.' and get the middle part (the number x in capture-x.cap)
        try:
            return int(file_name.split('-')[1].split('.')[0])
        except (IndexError, ValueError):
            return 0

    # Sort the list based on the extracted number
    pcap_files.sort(key=extract_number)

    # Check if we have more files than we need to keep
    if len(pcap_files) <= keep_count:
        print(f"Folder has {len(pcap_files)} PCAP files, which is less than or equal to {keep_count}. No files will be removed.")
        return

    # Identify files to be removed
    files_to_remove = pcap_files[keep_count:]

    # Remove the files
    for file in files_to_remove:
        file_path = os.path.join(folder, file)
        try:
            os.remove(file_path)
            print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")

if __name__ == "__main__":
    # Get input from the user
    k = int(input("Enter the value of k: "))
    folder = input("Enter the folder path: ")

    # Remove excess PCAP files
    remove_pcap_files(folder, k)
