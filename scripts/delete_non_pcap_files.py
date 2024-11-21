import os

def delete_non_pcap_files(folder_path):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            if not file.endswith('.cap'):
                os.remove(file_path)
                print(f"Deleted: {file}")
                
 
if __name__ == "__main__":
	folder = input("Type the name of the folder: ")
	delete_non_pcap_files(folder)
