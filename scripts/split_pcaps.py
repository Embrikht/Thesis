from scapy.all import *
from header_extraction import *
import os
import shutil

def calculate_midpoints(pcap_file, time_threshold):
    processed_packets = set()
    #Remove duplicates
    def is_retransmission(packet):
        frag_nr, seq_nr = sq_extract(packet)
        key = (packet.addr2, packet.addr1, packet.addr3, frag_nr, seq_nr, packet.data)
        if key in processed_packets:
            return True
        else:
            processed_packets.add(key)
            return False

    split_points = []
    prev_big_packet = None
    packets = rdpcap(pcap_file)
    for packet in packets:
        if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 0:
            if packet.haslayer(Dot11CCMP) and not is_retransmission(packet):
                if (prev_big_packet is not None) and (len(packet) > 1400) and ((packet.time - prev_big_packet) > time_threshold):
                    split_points.append((prev_big_packet+packet.time)/2)
                if len(packet) > 1400:
                    prev_big_packet = packet.time

    return split_points



def itemlist_sort(item):
    return int(item[10:])


def split_pcap_second(folder, time_threshold):
    if os.path.isdir(folder):
        os.chdir(folder)
        itemlist = [item for item in os.listdir('.') if os.path.isdir(item)]
        itemlist.sort(key=itemlist_sort)
        for item in itemlist:
            item_path = os.path.join(folder, item)
            if os.path.isdir(item):
                os.chdir(item)

                #Remove duplicates
                def is_retransmission(packet):
                    frag_nr, seq_nr = sq_extract(packet)
                    key = (packet.addr2, packet.addr1, packet.addr3, frag_nr, seq_nr, packet.data)
                    if key in processed_packets:
                        return True
                    else:
                        processed_packets.add(key)
                        return False

                #Used to update time_threshold if something doesnt work
                #time_threshold = float(input(f"   ---> Type time_threshold for {item}: "))
                for filename in os.listdir('.'):
                    if filename.endswith('.cap'):
                        #Checking for retransmission
                        processed_packets = set()


                        pcap_file = os.path.join('.', filename)

                        #Calculate the midpoints in the PCAP file for splitting later on
                        midpoints = calculate_midpoints(pcap_file, time_threshold)
                        current_output_pcap = None
                        first_packet_time = None
                        nr = 1

                        packets = rdpcap(pcap_file)
                        for packet in packets:
                            if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 0:
                                if packet.haslayer(Dot11CCMP) and not is_retransmission(packet):
                                    if current_output_pcap is None:
                                        output_file_name = f"{filename[:-4]}_{nr}.cap"
                                        current_output_pcap = PcapWriter(output_file_name, append=True)
                                        first_packet_time = packet.time

                                    while midpoints and packet.time > midpoints[0]:
                                        current_output_pcap.close()
                                        nr += 1
                                        output_file_name = f"{filename[:-4]}_{nr}.cap"
                                        current_output_pcap = PcapWriter(output_file_name, append=True)
                                        midpoints.pop(0)

                                    current_output_pcap.write(packet)

                        if current_output_pcap is not None:
                            current_output_pcap.close()

                        os.remove(filename)

                file_count_after_split = sum(1 for file in os.listdir('.') if file.endswith('.cap'))
                print(f"      ---> Number of files in {item}: {file_count_after_split}")
                os.chdir('..')
    os.chdir('..')



def split_pcap_first(folder):
    if os.path.isdir(folder):
        current_directory = os.getcwd()
        os.chdir(folder)

        #Remove duplicates
        def is_retransmission(packet):
            frag_nr, seq_nr = sq_extract(packet)
            key = (packet.addr2, packet.addr1, packet.addr3, frag_nr, seq_nr, packet.data)
            if key in processed_packets:
                return True
            else:
                processed_packets.add(key)
                return False

        time_threshold = 0
        for filename in os.listdir('.'):
            if filename.endswith('.cap'):
                #Checking for retransmission
                processed_packets = set()

                if time_threshold == 0:
                    time_threshold = float(input(f"Type time_threshold for {filename}: "))

                pcap_file = os.path.join('.', filename)
                pcap_name = "pcap"

                #Calculate the midpoints in the PCAP file for splitting later on
                midpoints = calculate_midpoints(pcap_file, time_threshold)
                current_output_pcap = None
                first_packet_time = None
                nr = 1

                packets = rdpcap(pcap_file)
                for packet in packets:
                    if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 0:
                        if packet.haslayer(Dot11CCMP) and not is_retransmission(packet):
                            if current_output_pcap is None:
                                output_file_name = f"{pcap_name}{nr}.cap"
                                current_output_pcap = PcapWriter(output_file_name, append=True)
                                first_packet_time = packet.time

                            while midpoints and packet.time > midpoints[0]:
                                current_output_pcap.close()
                                nr += 1
                                output_file_name = f"{pcap_name}{nr}.cap"
                                current_output_pcap = PcapWriter(output_file_name, append=True)
                                midpoints.pop(0)

                            current_output_pcap.write(packet)

                if current_output_pcap is not None:
                    current_output_pcap.close()

                #first_split_file = f"{pcap_name}_1.cap"
                #if os.path.exists(first_split_file):
                    #os.remove(first_split_file)

        file_count_after_split = sum(1 for file in os.listdir('.') if file.endswith('.cap')) - 1
        print(f"   ---> Number of files in {folder}: {file_count_after_split}")
        shutil.move(filename, current_directory)
        os.chdir('..')
