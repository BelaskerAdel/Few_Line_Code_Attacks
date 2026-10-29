# ARP Cache Poisoning (Man-in-the-Middle)

> ⚠️ Educational / authorized-lab use only. See the [repository README](../README.md).

## Concept

ARP has no authentication: a host trusts any ARP reply it receives and updates its
cache accordingly. By sending forged ARP replies that map the **gateway's IP** to the
**attacker's MAC**, an attacker convinces a victim to send its upstream traffic to the
attacker instead of the real gateway — a man-in-the-middle position. To stay transparent
the attacker forwards the traffic on, and on exit restores the correct mapping.

## How to detect it

- Multiple IP addresses suddenly resolving to the **same MAC**, or a gateway's MAC
  changing unexpectedly.
- A burst of unsolicited ARP replies (gratuitous ARP) — tools like **arpwatch**,
  **XArp**, or an IDS (Suricata/Zeek) flag this.
- Duplicate-IP or MAC-change alerts in switch logs.

## How to defend against it

- **Dynamic ARP Inspection (DAI)** on managed switches, tied to a DHCP snooping binding
  table, drops ARP packets that don't match a known IP↔MAC↔port binding.
- **Static ARP entries** for critical hosts (e.g. the default gateway).
- **Port security** limiting MAC addresses per port.
- Encrypt traffic end-to-end (TLS, VPN) so a MITM position yields little.
