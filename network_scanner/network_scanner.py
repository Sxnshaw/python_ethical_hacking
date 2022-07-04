#!/usr/bin/env python
import argparse
import scapy.all as scapy


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip", help="Use -i or --i to specify ip")
    options = parser.parse_args()
    if not options.ip:
        parser.error("[-] Couldn't get IP")
    else:
        return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    client_list = []
    for element in answered_list:
        client = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client)
    return client_list


def print_result(result_list):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_argument()
scan_result = scan(options.ip)
print_result(scan_result)