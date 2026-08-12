# xxHash contract and framing

A reproducible digest needs this complete tuple:

```text
(algorithm/version family, digest width, seed, exact input bytes, output form)
```

For structured input, exact bytes additionally depend on field order, type
tags, lengths, text normalization/encoding, integer signedness/width/endianness,
float policy, and missing-value representation.

## Stable text protocol

Choose whether Unicode-equivalent strings should be distinct. If not, name a
normalization form such as NFC before UTF-8 encoding and apply it everywhere.
Case-fold only when identifiers are semantically case-insensitive. Do not trim
whitespace merely for convenience.

## Numeric protocol

Do not hash `str(number)` when different runtimes must agree unless that textual
grammar is explicitly specified. For integers, fix signedness, width, and byte
order or use a canonical structured encoding. For floats, define handling for
negative zero, NaN payloads, infinities, and precision; otherwise cross-system
reproducibility is not established.

## Migration

Changing algorithm, seed, normalization, framing, or output representation
invalidates existing hashes. Version the digest column/key, support dual read
or recomputation as needed, and backfill with verification. Never label a new
algorithm under an old generic field named only `hash`.
