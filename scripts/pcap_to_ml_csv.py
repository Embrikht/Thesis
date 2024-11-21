from scapy.all import *
from header_extraction import *
from collections import OrderedDict
import pandas as pd
import os
import csv

# -------------------------------------------------------------
# Converting a PCAP file to a CSV file with information used
# to train a machine learning algorithm
# This fetches and extracts metadata for later use
# -------------------------------------------------------------



def pcap_to_ml_csv_length(folder, qos_data):
    if os.path.isdir(folder):
        os.chdir(folder)

        subfolders = [subfolder for subfolder in os.listdir('.') if subfolder.startswith('pcapfolder')]
        subfolders.sort(key=lambda x: int(x[len('pcapfolder'):]))

        for name in subfolders:
            if os.path.isdir(name):
                os.chdir(name)
                for filename in os.listdir('.'):
                    if filename.endswith('.cap'):
                        tmp = os.getcwd()
                        csv_path = f"{filename[:-4]}.csv"

                        # Checking for retransmission
                        processed_packets = set()

                        # Initialize columns for packet sizes
                        if qos_data == 1:
                            columns = [f"{i}_up" for i in range(3301)] + [f"{i}_down" for i in range(3301)]
                        else:
                            columns = [f"{i}_up" for i in range(1551)] + [f"{i}_down" for i in range(1551)]

                        # Remove duplicates
                        def is_retransmission(packet):
                            frag_nr, seq_nr = sq_extract(packet)
                            key = (packet.addr2, packet.addr1, packet.addr3, frag_nr, seq_nr)
                            if key in processed_packets:
                                return True
                            else:
                                processed_packets.add(key)
                                return False

                        bursts = 0
                        packet_to = None
                        last_downstream_packet = None
                        first_packet = None

                        # Initialize a dictionary to hold packet sizes
                        packet_sizes = {f"{i}_up": 0 for i in range(3301)} if qos_data == 1 else {f"{i}_up": 0 for i in range(1551)}
                        packet_sizes.update({f"{i}_down": 0 for i in range(3301)} if qos_data == 1 else {f"{i}_down": 0 for i in range(1551)})

                        try:
                            packets = rdpcap(filename)
                            for packet in packets:
                                if qos_data == 0:
                                    if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 0:
                                        if packet.haslayer(Dot11CCMP) and not is_retransmission(packet):
                                            # Change the MAC address based on your own config
                                            if packet.addr2 == "b4:8c:9d:36:3f:fd" and packet.addr1 == "04:f0:21:1b:61:ba":
                                                size = len(packet)
                                                packet_sizes[f"{size}_up"] += 1
                                                if first_packet == None:
                                                    first_packet = packet.time
                                                if packet_to != packet.addr1:
                                                    bursts += 1
                                                    packet_to = packet.addr1

                                            elif packet.addr2 == "04:f0:21:1b:61:ba" and packet.addr1 == "b4:8c:9d:36:3f:fd":
                                                size = len(packet)
                                                packet_sizes[f"{size}_down"] += 1
                                                if first_packet == None:
                                                    first_packet = packet.time
                                                if packet_to != packet.addr1:
                                                    bursts += 1
                                                    packet_to = packet.addr1
                                                last_downstream_packet = packet.time

                                elif qos_data == 1:
                                    if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 8:
                                        if packet.haslayer(Dot11CCMP) and not is_retransmission(packet):
                                            # Change the MAC address based on your own config
                                            if packet.addr2 == "b4:8c:9d:36:3f:fd" and packet.addr1 == "04:f0:21:1b:61:ba":
                                                size = len(packet)
                                                packet_sizes[f"{size}_up"] += 1
                                                if first_packet == None:
                                                    first_packet = packet.time
                                                if packet_to != packet.addr1:
                                                    bursts += 1
                                                    packet_to = packet.addr1

                                            elif packet.addr2 == "04:f0:21:1b:61:ba" and packet.addr1 == "b4:8c:9d:36:3f:fd":
                                                size = len(packet)
                                                packet_sizes[f"{size}_down"] += 1
                                                if first_packet == None:
                                                    first_packet = packet.time
                                                if packet_to != packet.addr1:
                                                    bursts += 1
                                                    packet_to = packet.addr1
                                                last_downstream_packet = packet.time

                        except Exception as e:
                            print(f"Could not read the PCAP file: {filename}")
                            print(f"Error: {e}")

                        # Write to CSV
                        try:
                            with open(csv_path, 'a', newline='') as csvfile:
                                writer = csv.DictWriter(csvfile, fieldnames=columns)
                                if csvfile.tell() == 0:
                                    writer.writeheader()

                                writer.writerow({**packet_sizes})

                        except Exception as e:
                            print(f"Error writing to CSV: {e}")
            os.chdir('..')
        os.chdir('..')



def pcap_to_ml_csv_full(folder, qos_data):
    if os.path.isdir(folder):
        os.chdir(folder)

        subfolders = [subfolder for subfolder in os.listdir('.') if subfolder.startswith('pcapfolder')]
        subfolders.sort(key=lambda x: int(x[len('pcapfolder'):]))

        for name in subfolders:
            if os.path.isdir(name):
                os.chdir(name)
                for filename in os.listdir('.'):
                    if filename.endswith('.cap'):
                        tmp = os.getcwd()
                        csv_path = f"{filename[:-4]}.csv"

                        # Checking for retransmission
                        processed_packets = set()

                        # Remove duplicates
                        def is_retransmission(packet):
                            frag_nr, seq_nr = sq_extract(packet)
                            key = (packet.addr2, packet.addr1, packet.addr3, frag_nr, seq_nr)
                            if key in processed_packets:
                                return True
                            else:
                                processed_packets.add(key)
                                return False

                        nr_packets_up = 0
                        nr_packets_down = 0
                        bytes_up = 0
                        bytes_down = 0
                        bursts = 0
                        bytes_burst = 0
                        packet_to = None
                        trace_time = 0
                        first_packet = None

                        try:
                            packets = rdpcap(filename)
                            for packet in packets:
                                if qos_data == 0:
                                    if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 0:
                                        if packet.haslayer(Dot11CCMP) and not is_retransmission(packet):
                                            # Change the MAC address based on your own config
                                            if packet.addr2 == "b4:8c:9d:36:3f:fd" and packet.addr1 == "04:f0:21:1b:61:ba":
                                                if first_packet == None:
                                                    first_packet = packet.time

                                                if packet_to != packet.addr1:
                                                    bursts += 1
                                                    bytes_burst += len(packet)
                                                    packet_to = packet.addr1

                                                # Counting the different values upstream
                                                nr_packets_up += 1
                                                bytes_up += len(packet)

                                            # Change the MAC address based on your own config
                                            elif packet.addr2 == "04:f0:21:1b:61:ba" and packet.addr1 == "b4:8c:9d:36:3f:fd":
                                                if first_packet == None:
                                                    first_packet = packet.time

                                                if packet_to != packet.addr1:
                                                    bursts += 1
                                                    bytes_burst += len(packet)
                                                    packet_to = packet.addr1

                                                # Counting the different values downstream
                                                nr_packets_down += 1
                                                bytes_down += len(packet)
                                                trace_time = packet.time

                                elif qos_data == 1:
                                    if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 8:
                                        if packet.haslayer(Dot11CCMP) and not is_retransmission(packet):
                                            # Change the MAC address based on your own config
                                            if packet.addr2 == "b4:8c:9d:36:3f:fd" and packet.addr1 == "04:f0:21:1b:61:ba":
                                                if first_packet == None:
                                                    first_packet = packet.time

                                                if packet_to != packet.addr1:
                                                    bursts += 1
                                                    bytes_burst += len(packet)
                                                    packet_to = packet.addr1

                                                # Counting the different values upstream
                                                nr_packets_up += 1
                                                bytes_up += len(packet)

                                            # Change the MAC address based on your own config
                                            elif packet.addr2 == "04:f0:21:1b:61:ba" and packet.addr1 == "b4:8c:9d:36:3f:fd":
                                                if first_packet == None:
                                                    first_packet = packet.time

                                                if packet_to != packet.addr1:
                                                    bursts += 1
                                                    bytes_burst += len(packet)
                                                    packet_to = packet.addr1

                                                # Counting the different values downstream
                                                nr_packets_down += 1
                                                bytes_down += len(packet)
                                                trace_time = packet.time

                            if trace_time is not None and first_packet is not None:
                                trace_time = trace_time - first_packet
                            else:
                                trace_time = 0

                        except Exception as e:
                            print(f"Could not read the PCAP file: {filename}")
                            print(f"Error: {e}")

                        try:
                            with open(csv_path, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                if csvfile.tell() == 0:
                                    writer.writerow(["Nr_packets_up",
                                                     "Nr_packets_down",
                                                     "Bytes_up",
                                                     "Bytes_down",
                                                     "Bursts",
                                                     "Bytes_in_bursts",
                                                     "Trace_time",
                                                     "Answer"])


                                writer.writerow([nr_packets_up, nr_packets_down, bytes_up, bytes_down, bursts, bytes_burst, trace_time])

                        except Exception as e:
                            print(f"Error writing to CSV: {e}")

            os.chdir('..')
        os.chdir('..')
