#!/usr/bin/env python
import subprocess
import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change mac")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify new MAC address, use --help for more info")
    return options


def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()
current_mac_address = current_mac(options.interface)
print("[+] Current MAC is > " + str(current_mac_address))

change_mac(options.interface, options.new_mac)
current_mac_address = current_mac(options.interface)

if current_mac_address == options.new_mac:
    print("[+] MAC address successfully changed into: " + str(current_mac_address))
else:
    print("[-] MAC addressed didn't changed")




