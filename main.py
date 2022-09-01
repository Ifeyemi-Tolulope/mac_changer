#!/usr/bin/env python

import subprocess
import optparse
import re


# Declare functions
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options


def change_mac_address(interface, mac_address):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])


def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            return "could not read from result provided"
            # print("[-] Could not read MAC address.")
    except subprocess.CalledProcessError:
        return "[-] Could not read MAC address."


# Call functions
options = get_arguments()

current_mac = get_current_mac(options.interface)

print("Current MAC Address = " + current_mac+"\n")

print("Changing MAC Address to " + current_mac + "...\n")

change_mac_address(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] Success!! New MAC address is" + current_mac)
else:
    print("[-] MAC address did not get changed")
