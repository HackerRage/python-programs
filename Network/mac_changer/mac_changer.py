#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface name for change MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please Specify interface, --help for more details")
    elif not options.new_mac:
        parser.error("Please Specify New MAC Address, --help for more details")
    else:
        return options

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def check_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    get_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if get_mac:
        return get_mac.group(0)
    
options = get_arguments()
get_mac_address = check_mac(options.interface)
print("[+] Current MAC Address = " + str(get_mac_address))
change_mac(options.interface, options.new_mac)
get_mac_address = check_mac(options.interface)
if get_mac_address == options.new_mac:
    print("[+] New MAC Address     = "+get_mac_address)
else:
    print("[-] MAC Address did not get changed.")
