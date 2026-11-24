#!/usr/bin/env python3
"""Jumbo-frame / MTU manipulation probe.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

This is a legacy learning exercise, refactored to modern Python 3 for
readability (the original used the Python 2 ``commands`` module). Linux only:
changing the interface MTU requires root privileges.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from scapy.layers.inet import ICMP, IP
from scapy.layers.l2 import Ether
from scapy.packet import Raw
from scapy.sendrecv import sr

JUMBO_ETHERTYPE = 0x8870         # Ethernet type signalling a jumbo frame
IP_ICMP_HEADER_BYTES = 28        # 20 (IP) + 8 (ICMP) subtracted from the MTU
REPLY_TIMEOUT_S = 1


def _read_mtu(interface: str) -> int:
    return int(Path(f"/sys/class/net/{interface}/mtu").read_text().strip())


def _set_mtu(interface: str, mtu: int) -> None:
    subprocess.run(["ifconfig", interface, "mtu", str(mtu), "up"], check=True)


def jumbo_frame(target_ip: str, interface: str, mtu: int) -> int:
    """Raise the interface MTU, send an oversized ICMP echo, then restore the MTU.

    Returns the number of ICMP replies received (0 if the target/path dropped it).
    """
    original_mtu = _read_mtu(interface)
    _set_mtu(interface, mtu)
    try:
        payload = b"a" * (mtu - IP_ICMP_HEADER_BYTES)
        answered, _unanswered = sr(
            Ether(type=JUMBO_ETHERTYPE) / IP(dst=target_ip) / ICMP() / Raw(load=payload),
            timeout=REPLY_TIMEOUT_S,
            iface=interface,
            verbose=0,
        )
        return len(answered)
    finally:
        _set_mtu(interface, original_mtu)   # always restore, even on error
