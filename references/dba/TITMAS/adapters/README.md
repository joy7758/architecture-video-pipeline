# TITMAS Adapter Contributions

An Adapter maps a pinned source framework or service into a TITMAS Development
Profile. It preserves source semantics and unknowns; it does not claim adoption.

Before proposing an Adapter:

1. pin official source, version, package identity and license;
2. define source-owned and TITMAS-bound fields;
3. declare unsupported and unknown semantics;
4. add positive, negative and failure fixtures;
5. assess sensitive payloads and data minimization;
6. prove `Mapping != Adoption` and `Observation != Evidence`;
7. avoid copying external Runtime or governance logic.

Start from [`template.md`](template.md). No external Adapter is implemented or
adopted in this candidate.
