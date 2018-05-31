
# Compiled at: 2018-04-11 16:43:14
import sys
from scapy.all import *
import nmap


# Try to guess the OS of the target by examining some of its footprints using nmap .
def OsDiscovery(Ip, Interface):
    nmapInstance = nmap.PortScanner()
    nmapInstance.scan(hosts=Ip, arguments='-O --fuzz -sV')
    return str(nmapInstance[Ip]['osmatch'])

