import os
import shutil

def move_pcap_files(subfolder):
    # Check if the provided folder exists
    if not os.path.isdir(subfolder):
        print(f"Error: '{subfolder}' is not a directory.")
        return

    # Iterate over subsubfolders in the subfolder
    for subsubfolder in os.listdir(subfolder):
        subsubfolder_path = os.path.join(subfolder, subsubfolder)

        # Ensure it's a directory
        if os.path.isdir(subsubfolder_path):
            # Iterate over files in the subsubfolder
            for file in os.listdir(subsubfolder_path):
                # Only move files with .cap extension
                if file.endswith('.cap'):
                    source_path = os.path.join(subsubfolder_path, file)
                    destination_path = os.path.join(subfolder, file)

                    # Move the PCAP file to the subfolder
                    shutil.move(source_path, destination_path)
                    print(f"Moved: {file} from {subsubfolder} to {subfolder}")

            # Once files are moved, delete the empty subsubfolder
            os.rmdir(subsubfolder_path)
            print(f"Deleted empty folder: {subsubfolder}")

if __name__ == "__main__":
    subfolder_path = input("Enter the path to the subfolder: ")
    move_pcap_files(subfolder_path)
