#!/usr/bin/env python3
"""OS fingerprinting of a host using Nmap.

This is a thin wrapper around Nmap's OS-detection (``-O``) and service/version
detection (``-sV``) features, exposed through the ``python-nmap`` library. It is
reconnaissance: it reports Nmap's best guess at the target's operating system.

EDUCATIONAL / AUTHORIZED-TESTING USE ONLY. Only scan hosts you own or have
explicit written permission to scan - unsolicited scanning may be against the
law or the acceptable-use policy of the network. See the README in this folder
for how OS fingerprinting works and how defenders reduce their exposure to it.

Requirements:
    - The Nmap binary installed and on PATH (https://nmap.org/)
    - python-nmap  (pip install python-nmap)
    - OS detection generally requires root/administrator privileges.

Usage:
    sudo python3 OsDiscovery.py 192.168.56.101
"""

import argparse
import sys

import nmap  # python-nmap


def discover_os(target: str) -> list[dict]:
    """Run an Nmap OS/service scan against *target* and return the OS matches.

    Returns the list of ``osmatch`` dictionaries Nmap produced (name, accuracy,
    and the underlying OS classes). The list is empty when Nmap could not make
    a confident guess.
    """
    scanner = nmap.PortScanner()
    # -O : OS detection, -sV : service/version detection, --osscan-guess :
    # fall back to the closest match when there is no perfect fingerprint.
    scanner.scan(hosts=target, arguments="-O -sV --osscan-guess")

    if target not in scanner.all_hosts():
        return []
    return scanner[target].get("osmatch", [])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Guess a host's operating system with Nmap (authorized use only).",
    )
    parser.add_argument("target", help="IP address or hostname to fingerprint")
    args = parser.parse_args(argv)

    try:
        matches = discover_os(args.target)
    except nmap.PortScannerError as exc:
        # Most often: Nmap not installed, or insufficient privileges for -O.
        print(f"[!] Nmap error: {exc}", file=sys.stderr)
        return 1

    if not matches:
        print(f"[*] No confident OS match for {args.target}.")
        return 0

    print(f"[*] OS matches for {args.target}:")
    for match in matches:
        print(f"    - {match.get('name')} (accuracy: {match.get('accuracy')}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
