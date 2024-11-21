from scapy.all import *
from math import *

# ------------------------------------------------------
# Extracting information from headers, used in main.py
# ------------------------------------------------------
        
#Frame control Field, flags
def flags_extract(packet):
    fcfield_int = int(packet.FCfield)
    fcfield_binary = bin(fcfield_int)[2:]
    order = 0
    protected = 0
    more_data = 0
    pwr_mgt = 0
    retry = 0
    more_fragments = 0
    from_ds = 0
    to_ds = 0

    #Making sure that the format is correct
    while len(fcfield_binary) < 8:
        fcfield_binary = '0' + fcfield_binary

    #Setting the frame control fields
    for i in range(len(fcfield_binary)):
        if i == 0:
            order = fcfield_binary[i]
        elif i == 1:
            protected = fcfield_binary[i]
        elif i == 2:
            more_data = fcfield_binary[i]
        elif i == 3:
            pwr_mgt = fcfield_binary[i]
        elif i == 4:
            retry = fcfield_binary[i]
        elif i == 5:
            more_fragments = fcfield_binary[i]
        elif i == 6:
            from_ds = fcfield_binary[i]
        elif i == 7:
            to_ds = fcfield_binary[i]

    return order, protected, more_data, pwr_mgt, retry, more_fragments, from_ds, to_ds


#Duration/ID Field
def durationID(packet):
    temp = int(packet.ID)
    duration = bin(temp)[2:]

    while len(duration) < 16:
        duration = '0' + duration

    return duration



#Mac Addresses in the header
def addresses_extract(packet):
    source_mac = packet.addr2
    dest_mac = packet.addr1
    mac_ap = packet.addr3

    return source_mac, dest_mac, mac_ap


#Sequence Control field
def sq_extract(packet):
    sq_number = int(packet.SC)
    sq_binary = bin(sq_number)[2:]

    #Making sure the format is correct
    while len(sq_binary) < 16:
        sq_binary = '0' + sq_binary

    #Calculating both fragment number and sequence number
    fragment_number = sq_binary[12:]
    sequence_number = sq_binary[:12]

    return fragment_number, sequence_number


#CCMP Header Extraction
def ccmp_extract(packet):
    list = [packet.PN0, packet.PN1, packet.PN2, packet.PN3, packet.PN4, packet.PN5]
    PN0 = bin(int(list[0]))[2:]
    PN1 = bin(int(list[1]))[2:]
    PN2 = bin(int(list[2]))[2:]
    PN3 = bin(int(list[3]))[2:]
    PN4 = bin(int(list[4]))[2:]
    PN5 = bin(int(list[5]))[2:]

    rsvd0 = bin(int(packet.res0))[2:]
    rsvd1 = bin(int(packet.res1))[2:]
    extIV = bin(int(packet.ext_iv))[2:]
    keyID = bin(int(packet.key_id))[2:]

    while len(PN0) < 8:
        PN0 = '0' + PN0
    while len(PN1) < 8:
        PN1 = '0' + PN1
    while len(rsvd0) < 8:
        rsvd0 = '0' + rsvd0
    while len(rsvd1) < 5:
        rsvd1 = '0' + rsvd1
    while len(keyID) < 2:
        keyID = '0' + keyID
    while len(PN2) < 8:
        PN2 = '0' + PN2
    while len(PN3) < 8:
        PN3 = '0' + PN3
    while len(PN4) < 8:
        PN4 = '0' + PN4
    while len(PN5) < 8:
        PN5 = '0' + PN5

    return PN0, PN1, rsvd0, rsvd1, extIV, keyID, PN2, PN3, PN4, PN5
