#!usr/bin/env python
import sys
from scapy.all import *
#only for linux and python < 3
import commands




# Sending a Jumbo ICMP packet :
# 1) get the current MTU
# 2) set the required MTU
# 3) send an ICMP request with a Jumbo Payload
# 4) reset the normal MTU
# 5) return the number of received ICMP reply packets - in case we received a response
def JumboFrame(Ip,Interface,mtu):

    #get the current MTU
    current_mtu=commands.getstatusoutput("cat /sys/class/net/"+Interface+"/mtu")[1]
    #set the required jumbo mtu
    commands.getstatusoutput("ifconfig "+Interface+" mtu "+str(mtu)+" up")

    ans,uans=sr(Ether(type=0x8870)/IP(dst=Ip)/ICMP()/Raw(load="a"*(mtu-28)),timeout=1,iface=Interface,verbose=0)
    ansPck_nbr=len(ans)

    #reset the old MTU
    commands.getstatusoutput("ifconfig "+Interface+" mtu "+str(current_mtu)+" up")


    return ansPck_nbr



