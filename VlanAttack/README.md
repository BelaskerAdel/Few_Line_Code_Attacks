# VLAN Attacks :   
## VLAN Spoofing : 

Simulate the VLAN spoofing attack by sending multiple DTP (Dynamic Trunking Protocol) Packets in order to impersonate a trunking switch and to form a trunk link and gain traffic from all VLANs
## Example : 
``` Spoofing("192.168.254.25","eth0",11:22:33:44:55:66,10)```

## Double Tagging : 
Sending a double VLAN tagged packet . 
## Example : 
```DoubleTagging("192.168.254.25","eth0",11:22:33:44:55:66,10)```
