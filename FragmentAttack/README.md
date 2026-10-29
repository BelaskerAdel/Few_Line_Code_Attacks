# IP Fragmentation Attacks (Tiny / Overlapping / Storm)

> ⚠️ Educational / authorized-lab use only. See the [repository README](../README.md).

## Concept

IP can split a datagram into fragments that the destination reassembles. Historically,
abusing reassembly has been a reliable way to evade filters or exhaust a host:

- **Tiny fragments** split headers so tightly that a filter can't see the full L4 header
  in the first fragment, potentially bypassing simple ACLs.
- **Overlapping fragments** declare offsets that overlap, which old/ambiguous stacks
  reassembled inconsistently (the root of teardrop-style crashes).
- **Fragment storms** flood the target with many large fragmented datagrams to consume
  reassembly buffers and CPU (a denial-of-service pressure test).

## How to detect it

- High rates of fragmented traffic, incomplete fragment sets, or overlapping offsets —
  visible to an IDS/IPS (Suricata/Snort) and to NetFlow anomaly detection.
- Reassembly-timeout and buffer-exhaustion counters rising on the target.

## How to defend against it

- Let a **stateful firewall/IPS reassemble and normalize** fragments before forwarding,
  and drop overlapping or out-of-spec fragment sets.
- Enforce **minimum first-fragment size** so L4 headers can be inspected.
- Cap per-source reassembly memory and set sane reassembly timeouts.
- Keep hosts patched — modern stacks handle malformed fragments safely.
