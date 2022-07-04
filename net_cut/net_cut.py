#!/usr/bin/env python
import subprocess
import netfilterqueue


def create_queue():
    subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "0"])


def process_packet(packet):
    packet.drop()


create_queue()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

try:
    queue.run()
except KeyboardInterrupt:
    print("[+] Ctrl+C detected exiting...")

