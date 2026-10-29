# Network Attacks Lab — Scapy

A small, educational collection of classic **Layer 2 / Layer 3 network attack
demonstrations** written in Python with [Scapy](https://scapy.net/). It was built
to *understand and teach* how these attacks work at the packet level — and, just as
importantly, **how to detect and defend against them**.

Each technique is a textbook example from network-security coursework, implemented
compactly so the packet construction is easy to read.

---

## ⚠️ Legal & ethical notice — read before running anything

These scripts generate malicious traffic (spoofing, flooding, malformed fragments).
They are provided **strictly for education and for authorized security testing**.

- Run them **only** inside an **isolated lab network you own** (e.g. VMs on a host-only
  network), or on systems for which you have **explicit, written permission** to test.
- Sending this traffic on networks you do not own may be **illegal** and can disrupt
  services for other users.
- You are solely responsible for how you use this code. The author accepts no liability
  for misuse.

If you don't have a controlled lab, read the code and the explanations below instead of
running it — that's where the learning value is.

---

## Techniques covered

Each folder contains one technique. The table pairs every attack with the control that
defends against it — the defensive side is the point of the exercise.

| Folder | Layer | What it demonstrates | How you defend against it |
|---|---|---|---|
| `ArpAttack` | L2 | ARP cache poisoning for man-in-the-middle | Dynamic ARP Inspection (DAI), static ARP entries, port security |
| `MacFlood` | L2 | Flooding the switch CAM table with random MACs | Port security / MAC limiting on switch ports |
| `VlanAttack` | L2 | VLAN hopping via double-tagging & DTP trunk spoofing | Disable DTP, set access ports, avoid native-VLAN = data VLAN |
| `FragmentAttack` | L3 | Tiny / overlapping / storm IP fragmentation | Fragment reassembly limits, IDS/IPS fragment checks |
| `TearDrop` | L3 | Overlapping-offset fragments (classic DoS) | Patched modern stacks reassemble safely; drop malformed fragments |
| `RoseAttack` | L3 | Sparse high-offset fragments exhausting reassembly | Reassembly timeouts & memory caps, rate limiting |
| `JumboFrame` | L2/L3 | Oversized frame / MTU manipulation probing | Enforce consistent MTU, drop oversized frames |
| `OsDiscovery` | — | OS fingerprinting of a host via Nmap | Limit exposed services, OS-fingerprint obfuscation, firewalling |

## Requirements

- Python 3, [Scapy](https://scapy.net/) (`pip install -r requirements.txt`)
- `OsDiscovery` also needs [`python-nmap`](https://pypi.org/project/python-nmap/) and the
  Nmap binary installed
- A Linux host is recommended; raw packet injection requires **root/administrator**
  privileges

```bash
pip install -r requirements.txt
```

> **Note on status:** this is legacy student code kept as a learning reference. The
> scripts were originally written for Python 2 and an isolated Linux lab, and are
> published here to document the techniques and their defenses rather than as ready-to-run
> tooling. Review and adapt any script to your own authorized lab before use.

## Author

**Adel Belasker** — Cyber Security Architect · [LinkedIn](https://www.linkedin.com/in/belasker/)

*Shared for educational and authorized-testing purposes only.*
