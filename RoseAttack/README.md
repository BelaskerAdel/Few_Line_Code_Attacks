# Rose Attack (Sparse High-Offset Fragmentation DoS)

> ⚠️ Educational / authorized-lab use only. See the [repository README](../README.md).

## Concept

The Rose attack is a fragmentation denial-of-service. The attacker sends the **first**
fragment of a datagram and then fragments at very **high offsets**, deliberately leaving
the middle missing. The target holds the incomplete datagram in its reassembly buffer,
waiting for fragments that never arrive. Many such partial datagrams tie up reassembly
memory and CPU until the timeout fires — starving legitimate traffic.

## How to detect it

- Large numbers of **incomplete fragment sets** and rising reassembly-timeout counters.
- Many datagrams with a first fragment plus distant high-offset fragments and nothing
  in between — visible to an IDS/IPS.

## How to defend against it

- **Cap per-source reassembly memory** and keep reassembly timeouts short.
- Rate-limit fragmented traffic per source at the perimeter.
- Prefer a firewall/IPS that reassembles centrally and drops incomplete sets.
