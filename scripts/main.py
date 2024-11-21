from scapy.all import *
from header_extraction import *
from size_interarrival_plot import *
from pcap_to_ml_csv import *
from metadata_plot import *
from delete_non_pcap_files import *
from putting_pcap_in_folder import *
from merge_csv_files import *

import matplotlib.pyplot as plt
import csv
import os

# ---------------------------------------------------
# Main script for running PCAP to CSV and plotting
# ---------------------------------------------------

if __name__ == "__main__":
    first_choice = int(input("Press '1': Filter prior to processing\nPress '2': PCAPs to CSVs\nPress '3': Merge CSV files\nPress '4': Plot figures\n     [-->] "))
    folder = input("Type the name of the folder containing sniffed traffic:\n     [-->] ")
    if first_choice == 1:
        size_of_private_set = int(input("Type the size of the private set:\n"))
        print("---------------------------------------------")
        print("---> Running delete_non_pcap_files")
        delete_non_pcap_files(folder)
        print("---> Running putting_pcap_in_folder")
        putting_pcap_in_folder(folder, size_of_private_set)
        print("---------------------------------------------")

    elif first_choice == 2:
        type_of_ml_csv = int(input("Press '1' for lengths for each packet, '2' for full session:\n     [-->] "))
        aggregation = int(input("Press '0' for not considering aggregation, '1' for aggregation:\n     [-->] "))
        print("---------------------------------------------")
        print("---> Running pcap_to_ml_csv")
        if (type_of_ml_csv == 1):
            pcap_to_ml_csv_length(folder, aggregation)
        elif (type_of_ml_csv == 2):
            pcap_to_ml_csv_full(folder, aggregation)
        print("---------------------------------------------")

    elif first_choice == 3:
        type_of_ml_csv = int(input("Press '1' for lengths for each packet, '2' for full session:\n     [-->] "))
        text_file = input("Type the name of the textfile with the answers:\n     [-->] ")
        print("---------------------------------------------")
        print("---> Running merge_csv_files")
        merge_csv_files(folder, type_of_ml_csv, text_file)
        print("---------------------------------------------")

    elif first_choice == 4:
        kind_of_plot = int(input("Press '1' for peek-a-boo figure given directory with .cap files\nPress '2' for plotting a PCAP file\nPress '3' for plotting two files against each other\n     [-->] "))
        if kind_of_plot == 1:
            plot_dict = {}
            nr_folders = int(input("Type the number of directories to iterate:\n     [-->] "))
            for i in range(nr_folders):
                folder = input("Type the name of the folder:\n     [-->] ")
                try:
                    plot_dict[i+1] = csv_to_metadata_plot(folder)
                except Exception as e:
                    print("Unable to run csv_to_metdata_plot for folder:", folder)
                    print(f"Exception: {e}")

            #Must be expanded if nr_folders > 5
            colors = ['blue', 'red', 'green', 'orange', 'purple']
            markers = ["^","s","P","x","d"]
            plot_metadata(plot_dict, colors, markers)

        elif kind_of_plot == 2:
            pcap_file1 = input("What PCAP file you want to use to plot?\n     [-->] ")
            pcap_file2 = ""
            plot_choice = int(input("Press '1': Only downstream\nPress '2': Both directions\n     [-->] "))
            size_and_interarrival_plot(pcap_file1, pcap_file2, plot_choice)

        elif kind_of_plot == 3:
            pcap_file1 = input("What PCAP file you want to use to plot?\n     [-->] ")
            pcap_file2 = input("What second PCAP file you want to use to plot?\n     [-->] ")
            plot_choice = int(input("Press '1': Only downstream\nPress '2': Both directions\n     [-->] "))
            size_and_interarrival_plot(pcap_file1, pcap_file2, plot_choice)
