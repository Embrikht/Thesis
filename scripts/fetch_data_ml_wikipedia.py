import requests
import time
import os
import socket

# Making sure each request is not cached by server-side or any proxy
h = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

# Function that returns a list of random URLs
def fetch_urls(number_of_times):
    random_wiki_url = "https://en.wikipedia.org/wiki/Special:Random"
    wikipedia_list = []
    for _ in range(number_of_times):
        response = requests.get(random_wiki_url, headers=h, allow_redirects=True)
        while response.url in wikipedia_list:
            response = requests.get(random_wiki_url, headers=h, allow_redirects=True)
        wikipedia_list.append(response.url)
    return wikipedia_list

def fetch_wikipedia_pages(folder_path, ip_address, port_nr):
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
                wikipedia_urls = fetch_urls(size_k_set)
                folder_counter = 1
                k_counter = 0
                fetched_wikipedia = []

                for w_url in wikipedia_urls:
                    k_counter += 1
                    folder_path_with_counter = f"{folder_path}_{folder_counter}"
                    os.makedirs(folder_path_with_counter, exist_ok=True)

                    for i in range(number_traces):
                        s.sendall(f"START_CAPTURE".encode())
                        time.sleep(1)

                        try:
                            response = requests.get(w_url, headers=h)
                            if response.status_code == 200:
                                print(f"Fetched: {w_url}, nr: {i+1}, subset {k_counter} number: {j+1}")
                                if w_url not in fetched_wikipedia:
                                    s.sendall(f"Answer:{w_url}".encode())
                                    fetched_wikipedia.append(w_url)
                            else:
                                print(f"Failed to fetch {w_url}. Status code: {response.status_code}")
                        except requests.exceptions.RequestException as e:
                            print(f"Error fetching {w_url}: {e}")

                        s.sendall(f"STOP_CAPTURE".encode())
                        time.sleep(1)

                    folder_counter += 1

            s.sendall(f"STOP_SCRIPT".encode())
            print("-----------------------------------")

    except Exception as e:
        print(f"Error occurred while sending data over Ethernet: {e}")


if __name__ == "__main__":
    folder_path_input = input("Enter the folder path: ")
    receiver_ip_address = "192.168.0.56"
    receive_port = 31337
    fetch_wikipedia_pages(folder_path_input, receiver_ip_address, receive_port)
