from scapy.all import *
from header_extraction import *
from math import floor
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------
# Plotting size and burstiness of packets
# ---------------------------------------------------

def size_and_interarrival_plot(pcap_file1, pcap_file2, type_of_plot):
    #Checking for retransmission
    processed_packets_first = set()
    timestamp_first = []
    data_size_first = []
    processed_packets_second = set()
    timestamp_second = []
    data_size_second = []

    #Remove duplicates
    def is_retransmission(packet, set):
        frag_nr, seq_nr = sq_extract(packet)
        key = (packet.addr2, packet.addr1, packet.addr3, frag_nr, seq_nr, packet.data)
        if key in set:
            return True
        else:
            set.add(key)
            return False

    try:
        #Used for plotting the first PCAP file
        packets = rdpcap(pcap_file1)
        for packet in packets:
            if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 0 and not is_retransmission(packet, processed_packets_first):
                if type_of_plot == 1 and packet.addr2 != "04:f0:21:1b:61:ba":
                    continue
                else:
                    timestamp_first.append(packet.time)
                    data_size_first.append(len(packet.data))

        interarrival_time_first = [abs(float(diff)) for diff in np.diff(timestamp_first)*1000]
        for i in range(1, len(timestamp_first)):
            timestamp_first[i] = (timestamp_first[i] - timestamp_first[0])*1000
        timestamp_first[0] = 0

        #Used for plotting the second PCAP file if provided
        if pcap_file2 != "":
            try:
                packets_two = rdpcap(pcap_file2)
                for packet in packets_two:
                    if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 0 and not is_retransmission(packet, processed_packets_second):
                        if type_of_plot == 1 and packet.addr2 != "04:f0:21:1b:61:ba":
                            continue
                        else:
                            timestamp_second.append(packet.time)
                            data_size_second.append(len(packet.data))

                interarrival_time_second = [abs(float(diff)) for diff in np.diff(timestamp_second)*1000]
                for i in range(1, len(timestamp_second)):
                    timestamp_second[i] = (timestamp_second[i] - timestamp_second[0])*1000
                timestamp_second[0] = 0

            except FileNotFoundError:
                print("File not found.")

    except FileNotFoundError:
        print("File not found.")

    nr_figures = 1
    if len(processed_packets_second) != 0:
        nr_figures = 2

    #Plotting scatter plot
    plt.subplot(nr_figures,2,1)
    plt.scatter(timestamp_first, data_size_first, marker='o')
    plt.xlabel("Time (ms)")
    plt.ylabel("Size Of The Packet (bytes)")
    plt.title("Time and size of packets")
    plt.grid(True)

    #Plotting interarrival time distribution
    plt.subplot(nr_figures,2,2)
    plt.hist(interarrival_time_first, bins=150, color='blue', alpha=0.7)
    plt.xlabel("Interarrival Time (ms)")
    plt.ylabel("Frequency")
    plt.title("Interarrival Time Distribution")
    plt.grid(True)

    if len(processed_packets_second) != 0:
        #Plotting scatter plot
        plt.subplot(2,2,3)
        plt.scatter(timestamp_second, data_size_second, marker='o')
        plt.xlabel("Time (ms)")
        plt.ylabel("Size Of The Packet (bytes)")
        plt.title("Time and size of packets")
        plt.grid(True)

        #Plotting interarrival time distribution
        plt.subplot(2,2,4)
        plt.hist(interarrival_time_second, bins=150, color='blue', alpha=0.7)
        plt.xlabel("Interarrival Time (ms)")
        plt.ylabel("Frequency")
        plt.title("Interarrival Time Distribution")
        plt.grid(True)

    plt.tight_layout()
    plt.show()
