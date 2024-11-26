import requests
import time
import socket
from math import ceil

# Define headers to avoid caching
h = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}


def fetch_data_amsdu(k, filename, ip_address, port_nr):
    print("-----------------------------------")
    print(f"Size of subset k: {k}")
    print(f"Number of traces: 20")
    print("-----------------------------------")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port_nr))
            try:
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    number_lines = 0
                    for line in lines:
                        fetched = 0
                        line = line.strip()
                        number_lines += 1

                        if number == 1: #WFS1
                            pdf_name = line
                            pdf_url = f"https://uioencryptedtraffic.no/master_files/{pdf_name}"
                            for i in range(20): 
                                s.sendall(f"START_CAPTURE".encode())
                                time.sleep(1)
                                try:
                                    response = requests.get(pdf_url, headers=h)
                                    if response.status_code == 200:
                                        print(f"Fetched: {pdf_url}, nr: {i+1}, file nr: {number_lines}")
                                        if fetched == 0:
                                            s.sendall(f"Answer:{pdf_name}".encode())
                                            fetched = 1
                                    else:
                                        print(f"Failed to fetch {pdf_url}. Status code: {response.status_code}")
                                except requests.exceptions.RequestException as e:
                                    print(f"Error fetching {pdf_url}: {e}")
                                s.sendall(f"STOP_CAPTURE".encode())
                                time.sleep(1)
                            
                        elif number == 2: #WFS2
                            wiki_url = line
                            for i in range(20):
                                s.sendall(f"START_CAPTURE".encode())
                                time.sleep(1)
                                try:
                                    response = requests.get(wiki_url, headers=h)
                                    if response.status_code == 200:
                                        print(f"Fetched: {wiki_url}, nr: {i+1}, file nr: {number_lines}")
                                        if fetched == 0:
                                            s.sendall(f"Answer:{wiki_url}".encode())
                                            fetched = 1
                                    else:
                                        print(f"Failed to fetch {wiki_url}. Status code: {response.status_code}")
                                except requests.exceptions.RequestException as e:
                                    print(f"Error fetching {wiki_url}: {e}")
                                s.sendall(f"STOP_CAPTURE".encode())
                                time.sleep(1)

                        elif number == 3: #WFS3
                            domain_url = line
                            for i in range(20):
                                s.sendall(f"START_CAPTURE".encode())
                                time.sleep(1)
                                try:
                                    response = requests.get(domain_url, headers=h)
                                    if response.status_code == 200:
                                        print(f"Fetched: {domain_url}, nr: {i+1}, file nr: {number_lines}")
                                        if fetched == 0:
                                            s.sendall(f"Answer:{domain_url}".encode())
                                            fetched = 1
                                    else:
                                        print(f"Failed to fetch {domain_url}. Status code: {response.status_code}")
                                except requests.exceptions.RequestException as e:
                                    print(f"Error fetching {domain_url}: {e}")
                                s.sendall(f"STOP_CAPTURE".encode())
                                time.sleep(1)

            except FileNotFoundError:
                print(f"Error: File '{filename}' not found.")

            s.sendall(f"STOP_SCRIPT".encode())
            print("-----------------------------------")

    except Exception as e:
        print(f"Error occurred while sending data over Ethernet: {e}")


if __name__ == "__main__":
    number = int(input("Press '1' for WFS1, '2' for WFS2 and '3' for WFS3:\n     [-->] "))
    k = int(input("Type the size of the private set:\n"))
    filename = input("Type the name of the textfile with the answers:\n     [-->] ")
    ip_address = "192.168.0.56"
    port_nr = 31337
    fetch_data_amsdu(k, filename, ip_address, port_nr)
