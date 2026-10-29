# OS Discovery (Nmap Fingerprinting)

> ⚠️ Educational / authorized-testing use only. See the [repository README](../README.md).

## Concept

Operating-system fingerprinting infers a host's OS from subtle differences in how its TCP/IP
stack responds: TCP options and ordering, initial window sizes, TTLs, how it answers unusual
probes, and so on. **Nmap** maintains a database of these fingerprints; `nmap -O` compares a
target's responses against it. This is reconnaissance — a standard first step in both
attacker and *defender* workflows (asset inventory, vulnerability management).

Unlike the other folders here, this is not an attack: it only observes and classifies.

## Usage

```bash
pip install python-nmap           # plus the Nmap binary from https://nmap.org
sudo python3 OsDiscovery.py 192.168.56.101
```

## How defenders reduce exposure

- Minimize the **attack surface** — close unused ports and services; a host that answers
  little is harder to fingerprint.
- Put assets behind firewalls that drop the unusual probes OS detection relies on.
- Monitor for scan patterns (IDS/IPS, NetFlow) — OS scans are noisy and detectable.
- Note that fingerprint "obfuscation" is weak protection; reducing exposed services is better.
