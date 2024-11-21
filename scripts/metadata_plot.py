import pandas as pd
import os
import matplotlib.pyplot as plt

# ---------------------------------------------------
# Script for plotting specific metadata information
# ---------------------------------------------------

def csv_to_metadata_plot(directory):
    trace_number = 0
    file_info = {}

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_file = os.path.join(directory, filename)

            #Read CSV file
            df = pd.read_csv(csv_file)

            #Fetching the wanted information
            total_bytes_upstream = df['Bytes_up'].sum() / 1024
            total_bytes_downstream = df['Bytes_down'].sum() / 1024
            bursts = df['Bursts']
            last_packet_time = df['Trace_time']

            #Increment trace number for dictionary
            trace_number += 1

            #Write to dictionary
            file_info[trace_number] = (total_bytes_upstream,
                                       total_bytes_downstream,
                                       bursts,
                                       last_packet_time,
                                       trace_number)

    return file_info


def plot_metadata(dict, colors, markers):
    key_list = list(dict.keys())
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    for i in range(len(key_list)):
        #Defining variables for plotting
        bytes_upstream = []
        bytes_downstream = []
        burst_session = []
        last_packet_session = []
        trace_session = []

        #Getting the correct sessions in order based on converted CSV file
        temp_dict = dict[key_list[i]]
        pdf_key_list = list(temp_dict.keys())
        pdf_key_list.sort()

        #Getting the correct data within a PDF file
        for j in range(len(pdf_key_list)):
            upstream = temp_dict[pdf_key_list[j]][0]
            downstream = temp_dict[pdf_key_list[j]][1]
            burststream = temp_dict[pdf_key_list[j]][2]
            time_packet = temp_dict[pdf_key_list[j]][3]
            number_of_trace = temp_dict[pdf_key_list[j]][4]
            bytes_upstream.append(upstream)
            bytes_downstream.append(downstream)
            burst_session.append(burststream)
            last_packet_session.append(time_packet)
            trace_session.append(number_of_trace)

        #Plotting all information from 1 PDF file into the three plots
        axs[0].scatter(last_packet_session, trace_session, color=colors[i], marker=markers[i])
        axs[1].scatter(bytes_upstream, bytes_downstream, color=colors[i], marker=markers[i])
        axs[2].scatter(trace_session, burst_session, color=colors[i], marker=markers[i])

    axs[0].set_xlabel("Last Downstream packet (seconds)")
    axs[0].set_ylabel("Trace Number")
    axs[0].grid(True)

    axs[1].set_xlabel("Upstream (kilobytes)")
    axs[1].set_ylabel("Downstream (kilobytes)")
    axs[1].grid(True)

    axs[2].set_xlabel("Trace Number")
    axs[2].set_ylabel("Burst per Trace")
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()
