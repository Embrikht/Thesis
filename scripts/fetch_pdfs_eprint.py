import os
import random
import requests
from urllib.parse import urljoin
import urllib.request

# ---------------------------------------------------
# Downloading the PDF files from ePrint
# The files are incrementally downloaded for each
# year, given the information in the list
# ---------------------------------------------------

list = [
    (2010, 660, 616),   # 616 PDF files
    (2011, 714, 659),   # 659 PDF files
    (2012, 733, 699),   # 699 PDF files
    (2013, 881, 850),   # 850 PDF files
    (2014, 1029, 974),  # 974 PDF files
    (2015, 1255, 1208), # 1208 PDF files
    (2016, 1195, 1167), # 1167 PDF files
    (2017, 1262, 1228), # 1228 PDF files
    (2018, 1249, 1222)  # 1222 PDF files
    ]

def file_number_to_correct_format(access_file):
    if access_file < 100:
        if access_file < 10:
            access_file = f"00{access_file}"
        else:
            access_file = f"0{access_file}"
    return access_file

def download_pdf(url, folder_path, list, nr_pdfs):
    #Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    fetched_pdfs = set()

    for y in range(2010,2019):
        year = y
        i = 0
        while i < nr_pdfs:
            #Choosing the year uniformly at random given nr of PDFs within a year
            chosen_year = year
            total_files = list[int(year)-2010][1]

            #Choosing the file uniformly at random and then checking if PDF
            access_file = file_number_to_correct_format(random.randint(1,total_files))

            #Used to fetch a valid PDF file
            fetched_file = False

            while not fetched_file:
                #Construct the page URL
                page_url = f"{url}{year}/{access_file}"
                try:
                    with urllib.request.urlopen(page_url) as response:
                        if response.getcode() != 200:
                            print(f"Failed to fetch the page. Status code: {response.getcode()}")
                            return

                        #Draw a new file if the accessed file does not contain a PDF file
                        pdf_base_name = os.path.basename(page_url)
                        pdf_name = f"{year}_{pdf_base_name}"
                        pdf_path = os.path.join(folder_path, pdf_name)

                        #Fetching the PDF file if it exists
                        pdf_url = f"{url}{year}/{access_file}.pdf"
                        if pdf_url in fetched_pdfs:
                            access_file = file_number_to_correct_format(random.randint(1,total_files))
                            continue
                        try:
                            pdf_response = requests.get(pdf_url)
                            if pdf_response.status_code == 200:
                                with open(pdf_path, 'wb') as pdf_file:
                                    pdf_file.write(pdf_response.content)
                                i += 1
                                fetched_pdfs.add(pdf_url)
                                fetched_file = True
                                print(f"Downloaded: {pdf_path}, nr: {i+1}")
                            else:
                                access_file = file_number_to_correct_format(random.randint(1,total_files))
                                print(f"Failed to download {pdf_url}. Status code: {pdf_response.status_code}")
                        except:
                            access_file = file_number_to_correct_format(random.randint(1,total_files))
                            print(f"PDF response: {pdf_response.status_code}")

                except requests.exceptions.RequestException as e:
                    access_file = file_number_to_correct_format(random.randint(1,total_files))
                    print(f"Failed to download {pdf_url}: {e}")

if __name__ == "__main__":
    folder_path_input = input("Enter the folder path: ")
    number = int(input("Enter number of PDFs to fetch: "))
    download_pdf("https://eprint.iacr.org/", folder_path_input, list, number)
