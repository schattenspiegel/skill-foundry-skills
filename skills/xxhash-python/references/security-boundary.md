# xxHash security boundary

xxHash is designed for speed and non-cryptographic quality. It does not provide
preimage resistance, collision resistance against an attacker, authenticity,
or password hardness. A seed is not a secret key and does not transform xxHash
into a MAC.

Reject xxHash for:

- password storage or password-derived keys;
- session/API tokens or reset links;
- signatures, HMAC, webhook verification, or artifact attestation;
- security-sensitive deduplication controlled by untrusted inputs;
- tamper detection where an attacker can replace data and digest;
- content addressing whose trust model requires cryptographic collision
  resistance.

Use a standard password KDF for passwords, HMAC with a cryptographic hash for
shared-secret authentication, signatures for public verification, and a
cryptographic digest for adversarial content integrity. Choose the primitive
through the project's security protocol and threat model rather than swapping
names mechanically.

xxHash can still be an internal performance hint before a definitive byte/key
comparison. Keep that second comparison in the algorithm so collisions affect
speed, not correctness.
