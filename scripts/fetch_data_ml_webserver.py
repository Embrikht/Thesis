import os
import requests
from bs4 import BeautifulSoup
import time
import random
import socket

# Making sure each request is not cached by server-side or any proxy
h = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

# Extracting the PDF files on the website in a list
def extract_pdf_links(url, header):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_links = soup.find_all('a', href=True)
    pdf_links = [link['href'] for link in all_links]
    return pdf_links

def download_for_ml_pdf(url, folder_path, ip_address, port_nr):
    # Getting a list of all PDFs on the website
    pdf_list = extract_pdf_links(url, h)

    number_traces = 20
    size_k_set = 30
    fetch_nr_times = 7

    print("-----------------------------------")
    print(f"Size of subset k: {size_k_set}")
    print(f"Number of traces: {number_traces}")
    print(f"Number of times we pick a new subset k: {fetch_nr_times}")
    print("-----------------------------------")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port_nr))
            
            for j in range(fetch_nr_times):
                k_counter = 0
                k_variable = size_k_set
                folder_counter = 1
                fetched_pdfs = set()

                while k_counter < k_variable:
                    # Create the folder if it doesn't exist
                    folder_path_with_counter = f"{folder_path}_{folder_counter}"
                    os.makedirs(folder_path_with_counter, exist_ok=True)

                    if len(pdf_list) > k_variable:
                        # Defining the PDF file to download and the URL to fetch the PDF
                        random_pdf = random.choice(pdf_list)[15:]
                        while random_pdf in fetched_pdfs:
                            random_pdf = random.choice(pdf_list)[15:]
                        pdf_path = os.path.join(folder_path_with_counter, random_pdf)
                        pdf_url = f"{url}/master_files/{random_pdf}"

                        for i in range(number_traces):
                            s.sendall(f"START_CAPTURE".encode())
                            time.sleep(1)

                            try:
                                pdf_response = requests.get(pdf_url, headers=h)
                                if pdf_response.status_code == 200:
                                    with open(pdf_path, 'wb') as pdf_file:
                                        pdf_file.write(pdf_response.content)
                                    print(f"Downloaded: {pdf_path}, nr: {i+1}, subset {k_counter+1} number: {j+1}")
                                    if random_pdf not in fetched_pdfs:
                                        s.sendall(f"Answer:{random_pdf}".encode())
                                        fetched_pdfs.add(random_pdf)
                                else:
                                    random_pdf = random.choice(pdf_list)[15:]
                                    print(f"Failed to download {pdf_url}. Status code: {pdf_response.status_code}")
                            except requests.exceptions.RequestException as e:
                                random_pdf = random.choice(pdf_list)[15:]
                                print(f"PDF response: {e}")

                            s.sendall(f"STOP_CAPTURE".encode())
                            time.sleep(1)

                        folder_counter += 1
                        k_counter += 1

            s.sendall(f"STOP_SCRIPT".encode())
            print("-----------------------------------")

    except Exception as e:
        print(f"Error occurred while sending answer over Ethernet: {e}")

if __name__ == "__main__":
    folder_path_input = input("Enter the folder path: ")
    receiver_ip_address = "192.168.0.56"
    receive_port = 31337
    download_for_ml_pdf("https://uioencryptedtraffic.no", folder_path_input, receiver_ip_address, receive_port)