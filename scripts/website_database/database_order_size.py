import sqlite3

def export_paper_sizes(database_path, output_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve rows sorted by PDF size
    cursor.execute("SELECT * FROM papers ORDER BY pdf_size DESC")
    with open(output_file, 'w') as file:
        for row in cursor.fetchall():
            nr = row[0]
            name = row[1]
            pdf_size = row[2]
            pdf_size_compressed = row[2]
            file.write(','.join((str(nr), str(name), str(pdf_size))) + '\n')

    conn.close()

if __name__ == "__main__":
    database = input("Enter the database name: ")
    export_paper_sizes(database, "website_pdf_size_ordered.csv")
