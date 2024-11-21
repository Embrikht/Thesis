import urllib.request
import gzip
import sqlite3
import os
from bs4 import BeautifulSoup
import requests
import sys

def extract_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_links = soup.find_all('a', href=True)
    pdf_links = [link['href'] for link in all_links]
    return pdf_links

def create_database(url, filename):
    pdf_links = extract_pdf_links(url)
    totalpapers = len(pdf_links)
    print("Total: %d pdfs" % totalpapers)

    if os.path.isfile(filename):
        exit("Database file exists!")

    db = sqlite3.connect(filename)
    db.execute("CREATE TABLE papers (nr, name UNIQUE, pdf_size)")
    db.commit()

    number = 1
    for i in range(len(pdf_links)):
        pdf_name = pdf_links[i][15:]
        print(pdf_name)
        pdf_url = f"{url}/master_files/{pdf_name}"
        print("Retrieving %s" % pdf_name)

        #Fetching the PDF file and defining the values of the variables
        try:
            r = urllib.request.urlopen(pdf_url)
            pdf = r.read()
            lenpdf = len(pdf)
        except:
            print(f"Could not fetch PDF: {pdf_url}")
            continue

        #Insert into database
        db.execute("INSERT OR IGNORE INTO papers (nr, name, pdf_size) VALUES (?,?,?)",
                   (number, pdf_name, lenpdf))
        number += 1

    db.commit()
    db.close()


if __name__ == "__main__":
    database_input = input("Enter the database name: ")
    website = "https://uioencryptedtraffic.no"
    create_database(website, database_input)
