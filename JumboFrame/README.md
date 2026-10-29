# Jumbo Frame / MTU Manipulation

> ⚠️ Educational / authorized-lab use only. See the [repository README](../README.md).

## Concept

Standard Ethernet frames carry a 1500-byte payload (MTU). "Jumbo" frames carry far more
(up to ~9000 bytes) and must be supported end-to-end. This script raises the interface MTU
and sends oversized ICMP packets to probe how a target and the path between handle frames
larger than expected — a way to study MTU handling, fragmentation behavior, and the
robustness of devices to non-standard frame sizes.

## How to detect it

- Oversized frames where they are not expected, or ICMP "fragmentation needed" / PMTUD
  activity, visible on monitoring and switch counters (giant/jumbo frame counters).

## How to defend against it

- Enforce a **consistent, intended MTU** across the L2 domain; drop giants on ports that
  should not carry them.
- Enable storm control and monitor giant-frame counters.
- Keep device firmware current so oversized frames are handled gracefully.
