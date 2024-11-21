import csv
from collections import Counter
import math

def analyze_pdf_sizes(file_path):
    sizes = []

    # Read sizes from the CSV file
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            size = int(row[2])  # Get the size from the third column
            sizes.append(size)

    # Task 1: Analysis without size adjustments
    size_counts = Counter(sizes)
    largest_identical_set = max(size_counts.values())
    unique_sizes = len(size_counts)
    uniquely_identifiable_pdfs = sum(1 for count in size_counts.values() if count == 1)

    print("Task 1:")
    print(f"Largest set of PDF files of identical size: {largest_identical_set}")
    print(f"Number of different lengths: {unique_sizes}")
    print(f"Number of uniquely identifiable PDF files: {uniquely_identifiable_pdfs}")

    # Task 2: Analysis with padding to multiples of each value in `multiples` times 3, 6, and 9
    multiples = [6, 56, 72, 1433]
    scaling_factors = [3, 6, 9]

    for multiple in multiples:
        for scale in scaling_factors:
            padded_multiple = multiple * scale
            adjusted_sizes = []
            total_size_before = sum(sizes)  # Total size before padding
            total_size_after = 0  # Initialize total size after padding

            # For each size, calculate the padded size to the next multiple of padded_multiple
            for size in sizes:
                adjusted_size = math.ceil(size / padded_multiple) * padded_multiple
                adjusted_sizes.append(adjusted_size)
                total_size_after += adjusted_size  # Accumulate the total size after padding

            adjusted_size_counts = Counter(adjusted_sizes)
            largest_identical_set_adjusted = max(adjusted_size_counts.values())
            unique_sizes_adjusted = len(adjusted_size_counts)
            uniquely_identifiable_pdfs_adjusted = sum(1 for count in adjusted_size_counts.values() if count == 1)

            # Calculate overhead
            overhead = (total_size_after / total_size_before - 1) * 100  # Percentage increase

            print(f"\nTask 2 (padded to nearest multiple of {padded_multiple}):")
            print(f"Largest set of PDF files of identical size: {largest_identical_set_adjusted}")
            print(f"Number of different lengths: {unique_sizes_adjusted}")
            print(f"Number of uniquely identifiable PDF files: {uniquely_identifiable_pdfs_adjusted}")
            print(f"Total overhead: {overhead:.2f}%")

file_path = 'website_pdf_size_ordered.csv'  # Replace with your actual CSV file path
analyze_pdf_sizes(file_path)
