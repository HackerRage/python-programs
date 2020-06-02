#!/usr/bin/env python

import optparse
import scapy.all as scapy

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t","--target", dest="target_ip", help="Specify the IP or IP range")
    options = parser.parse_args()[0]
    if not options.target_ip:
        parser.error("Please Specify the IP or IP Range, --help for more details")
    else:
        return options.target_ip

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]  #srp() function returns 2 values = answered & unanswered

    client_list = []
    for elements in answered_list:
        client_dist = {"ip":elements[1].psrc, "mac":elements[1].hwsrc}
        client_list.append(client_dist)
    return client_list

def print_result(result_list):
    print("IP\t\t\tMAC Address\n------------------------------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])

ip_address = get_arguments()
scan_result = scan(ip_address)
print_result(scan_result)