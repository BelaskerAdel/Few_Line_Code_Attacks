# Sending Jumbo Frame with the configuration of a desired MTU

Sending a Jumbo ICMP packet : <br/>
1) get the current MTU <br/>
2) set the required MTU <br/>
3) send an ICMP request with a Jumbo Payload <br/>
4) reset the normal MTU <br/>
5) return the number of received ICMP reply packets - in case we received a response <br/>

# Example :
```response = JumboFrame("192.168.254.250","eth0",9000)```
if response > 0 then we got response from the target else the target didn't respond 
