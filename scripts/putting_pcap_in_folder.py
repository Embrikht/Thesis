import os
import shutil



def sort_pcaps(filename):
    parts = filename.split('-')
    numeric_part = int(parts[1].split('.')[0])
    return numeric_part



def putting_pcap_in_folder(folder, k):
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a directory.")
        return

    files = os.listdir(folder)
    pcap_files = [file for file in files if file.endswith('.cap')]

    # Sort the files to ensure consistent grouping
    pcap_files.sort(key=sort_pcaps)

    # Number of PCAP files per folder
    group_size = k * 20

    # Calculate the number of groups
    num_groups = len(pcap_files) // group_size

    # Print for visual display
    print(f"   ---> Number of PCAP files: {len(pcap_files)}")
    print(f"   ---> Number of folders: {num_groups}")
    print(f"   ---> Number of PCAP files per folder: {group_size}")

    for i in range(num_groups):
        # Create folder for group i
        folder_name = f"pcapfolder{i+1}"
        folder_path_new = os.path.join(folder, folder_name)
        os.makedirs(folder_path_new, exist_ok=True)

        # Move k files to the new folder
        for j in range(group_size):
            source_file = os.path.join(folder, pcap_files[i * group_size + j])
            shutil.move(source_file, folder_path_new)
