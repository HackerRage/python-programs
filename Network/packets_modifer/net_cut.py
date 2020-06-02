#!/usr/bin/env python
import netfilterqueue

def process_packet(packet):
    print(packet)
    packet.drop()
    # packet.accept()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()