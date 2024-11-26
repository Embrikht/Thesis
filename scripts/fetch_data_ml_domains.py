import random
import requests
import time
import socket
from math import ceil


# Making sure each request is not cached by server-side or any proxy
h = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

# Function that returns a list of random URLs
def fetch_random_domains(file_name, k):
    with open(file_name, 'r') as file:
        urls = file.readlines()

    urls = [url.strip() for url in urls if url.strip()]
    selected_urls = random.sample(urls, k)

    return selected_urls


def fetch_domain_pages(filename, k, ip_address, port_nr, t):
    print("-----------------------------------")
    print(f"Size of subset k: {k}")
    print(f"Number of traces: 20")
    print(f"Number of times we pick a new subset k: {t}")
    print("-----------------------------------")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, port_nr))
            for times in range(t):
                domains = fetch_random_domains(filename, k)
                k_counter = 0

                for domain in domains:
                    k_counter += 1
                    send_answer = 0
                    for i in range(20):
                        s.sendall(f"START_CAPTURE".encode())
                        time.sleep(1)
                        try:
                            response = requests.get(domain, headers=h, allow_redirects=True)
                            if response.status_code == 200:
                                print(f"Fetched: {domain}, nr: {i+1}, k: {k_counter} trial: {times+1}")
                                if send_answer == 0:
                                    s.sendall(f"Answer:{domain}".encode())
                                    send_answer = 1
                            else:
                                print(f"Failed to fetch {domain}. Status code: {response.status_code}")
                        except requests.exceptions.RequestException as e:
                            print(f"Error fetching {domain}: {e}")

                        s.sendall(f"STOP_CAPTURE".encode())
                        time.sleep(1)

            s.sendall(f"STOP_SCRIPT".encode())
            print("-----------------------------------")

    except Exception as e:
        print(f"Error occurred while sending data over Ethernet: {e}")


if __name__ == "__main__":
    filename_input = input("Enter the textfile to draw from: ")
    k = int(input("Enter the value of k (number of domains to fetch): "))
    receiver_ip_address = "192.168.0.56"
    receive_port = 31337
    t = ceil(4000/(k*20))
    fetch_domain_pages(filename_input, k, receiver_ip_address, receive_port, t)
