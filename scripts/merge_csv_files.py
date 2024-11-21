import pandas as pd
import os
import shutil


def sort_pcapfiles(filename):
    parts = filename.split('.')
    first = int(parts[0][8:])
    second = parts[1]
    return first, second

def sort_folder(folder):
    index = int(folder[10:])
    return index

def merge_csv_files(folder, type_value, text_file):
    if os.path.isdir(folder):
        shutil.move(text_file, folder)
        os.chdir(folder)
        subfolders = [subfolder for subfolder in os.listdir('.') if os.path.isdir(subfolder)]
        subfolders.sort(key=sort_folder)
        folder_path = os.getcwd()

        with open(text_file, 'r') as f:
            answer_value = [line.strip() for line in f.readlines()]

        counter = 0
        index = 0
        for subfolder in subfolders:
            subfolder_path = os.path.join(folder_path, subfolder)
            os.chdir(subfolder_path)

            csv_files = [file for file in os.listdir('.') if file.endswith('.csv')]
            csv_files.sort(key=sort_pcapfiles)

            dfs = []
            for file in csv_files:
                if (counter == 20):
                    index += 1
                    counter = 0
                csv_path = os.path.abspath(file)
                df = pd.read_csv(csv_path)
                df['Answer'] = [answer_value[index]] * min(20, len(df))
                counter += 1
                dfs.append(df)


            if type_value == 1:
                output_file = f"{subfolder}_length.csv"
            elif type_value == 2:
                output_file = f"{subfolder}_full.csv"

            merged_df = pd.concat(dfs, ignore_index=True)
            merged_df.to_csv(os.path.join(folder_path, output_file), index=False)

            for file in csv_files:
                os.remove(file)

            os.chdir(folder_path)
        os.chdir('..')
