#!/usr/bin/env python
import scapy.all as scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered[0][1].hwdst

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffer_packet)

def process_sniffer_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                print("[+] You are Under Attack !!!")
            # else:
            	# print("[+] System is Safe")
        except IndexError:
            pass

sniff("wlan0")
