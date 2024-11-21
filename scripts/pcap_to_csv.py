from scapy.all import *
from header_extraction import *
import csv

# --------------------------------------------------------
# Converting a PCAP file to a CSV file with information
# Also prints the size of packets when run in main.py
# --------------------------------------------------------

def pcap_to_csv(pcap_file_path, output_csv, type_of_csv):
    #Checking for retransmission
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

    with open(output_csv, mode='w', newline='') as csvfile:
        fields = [ "Size",
                   "To DS",
                   "From DS",
                   "More Fragments",
                   "Retry",
                   "Power Management",
                   "More Data",
                   "Protected Frame",
                   "Order",
                   "-----",
                   "Duration/ID",
                   "-----",
                   "Source MAC",
                   "Destination MAC",
                   "MAC AP",
                   "-----",
                   "Fragment number",
                   "Sequence number",
                   "-----",
                   "PN0",
                   "PN1",
                   "Rsvd0",
                   "Rsvd1",
                   "ExtIV",
                   "KeyID",
                   "PN2",
                   "PN3",
                   "PN4",
                   "PN5"]

        #Calculating total number of bytes
        total_bytes = 0

        try:
            packets = rdpcap(pcap_file_path)

            #Creating CSV writer object
            csvwriter = csv.writer(csvfile)

            # Writing the fields
            csvwriter.writerow(fields)

            #Calculating total number of bytes
            tb_rows = []
            total_bytes = 0

            for packet in packets:
                if packet.haslayer(Dot11) and packet.type == 2 and packet.subtype == 0:
                    if packet.haslayer(Dot11CCMP) and not is_retransmission(packet):
                        if type_of_csv == 1 and packet.addr2 != "04:f0:21:1b:61:ba":
                            continue
                        else:
                            #Values to be written to the CSV file
                            rows = []

                            #Empty Variable
                            blank = ""

                            #Size of the packet and number of packets
                            data_size = len(packet.data)
                            rows.extend([data_size])
                            total_bytes += data_size

                            #Frame Control Field, flags
                            order, protected, more_data, pwr_mgt, retry, more_fragments, from_ds, to_ds = flags_extract(packet)
                            rows.extend([to_ds, from_ds, more_fragments, retry, pwr_mgt, more_data, protected, order, blank])

                            #Duration/Connection ID
                            duration = durationID(packet)
                            rows.extend([duration, blank])

                            #Address Field
                            source_mac_sta, dest_mac_sta, mac_ap = addresses_extract(packet)
                            rows.extend([source_mac_sta, dest_mac_sta, mac_ap, blank])

                            #Sequence Control Field
                            fragment_number, sequence_number = sq_extract(packet)
                            rows.extend([fragment_number, sequence_number, blank])

                            #CCMP Header
                            PN0, PN1, rsvd0, rsvd1, extIV, keyID, PN2, PN3, PN4, PN5 = ccmp_extract(packet)
                            rows.extend([PN0, PN1, rsvd0, rsvd1, extIV, keyID, PN2, PN3, PN4, PN5])

                            #Writing the rows to the CSV file
                            csvwriter.writerow(rows)

            tb_rows.extend([total_bytes])
            csvwriter.writerow(tb_rows)
            return total_bytes

        except FileNotFoundError:
            print("File not found.")
