# MAC Flooding (CAM-Table Overflow)

> ⚠️ Educational / authorized-lab use only. See the [repository README](../README.md).

## Concept

A switch learns which MAC address lives on which port and stores that in a finite
**CAM (content-addressable memory) table**. If the table is filled with thousands of
bogus source MAC addresses, the switch can no longer learn legitimate entries and may
**fail open**, flooding frames out of every port like a hub. That lets an attacker on the
same segment passively see traffic meant for others.

## How to detect it

- A sudden explosion in the number of distinct source MACs seen on a single port.
- CAM-table-full / MAC-move log messages on the switch.
- Unexpected unicast flooding observed by an IDS or a monitoring SPAN port.

## How to defend against it

- **Port security** (e.g. Cisco `switchport port-security`) to cap the number of MACs
  per access port and shut/restrict the port when exceeded.
- **Sticky MAC** learning plus violation actions.
- 802.1X authentication on access ports so unknown devices never reach the data plane.
