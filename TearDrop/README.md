# Teardrop (Overlapping-Offset Fragmentation DoS)

> ⚠️ Educational / authorized-lab use only. See the [repository README](../README.md).

## Concept

Teardrop is a classic late-1990s denial-of-service technique. It sends IP fragments whose
**offsets overlap** in a way the reassembly code did not expect. Vulnerable stacks computed
a negative or oversized length during reassembly and crashed or hung. It is of historical
and educational interest: it illustrates why input validation during reassembly matters.

## How to detect it

- Overlapping fragment offsets for a single datagram — a textbook IDS/IPS signature.
- Spikes in malformed-fragment counters on the target or perimeter device.

## How to defend against it

- **Modern, patched operating systems are not vulnerable** — they reassemble defensively.
- Have a firewall/IPS **drop overlapping fragments** before they reach end hosts.
- Enforce fragment normalization at the perimeter.
