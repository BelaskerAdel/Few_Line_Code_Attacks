# VLAN Hopping (Double-Tagging & DTP Trunk Spoofing)

> ⚠️ Educational / authorized-lab use only. See the [repository README](../README.md).

## Concept

VLANs isolate broadcast domains, but two misconfigurations let an attacker reach a VLAN
they shouldn't:

- **Double-tagging:** the attacker sends a frame with two 802.1Q tags. The first switch
  strips the outer tag (if it matches the native VLAN) and forwards the frame on a trunk;
  the next switch acts on the inner tag, delivering the frame into the target VLAN. This
  is one-way.
- **DTP trunk spoofing:** if Dynamic Trunking Protocol is left on, an attacker's port can
  negotiate a **trunk**, giving it access to traffic for all VLANs.

## How to detect it

- 802.1Q frames arriving on access ports, or unexpected DTP negotiation packets.
- Trunk links forming on ports that should be access ports (switchport logs).

## How to defend against it

- **Disable DTP** on access ports (`switchport mode access`, `switchport nonegotiate`).
- Make the **native VLAN** an unused, dedicated VLAN — never the data or management VLAN.
- Explicitly prune allowed VLANs on real trunks (`switchport trunk allowed vlan ...`).
- Shut down unused ports and place them in a black-hole VLAN.
