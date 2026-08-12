# Streaming and testing xxHash

## Streaming lifecycle

Create one state object per logical ordered byte stream. Read binary chunks,
update in order, finalize once, and discard or explicitly reset the object.
`copy()` is useful for shared-prefix protocols, but test that branch digests do
not mutate one another.

Chunk size is an I/O performance choice, not part of the hash protocol. Empty
input must still produce the algorithm's defined empty digest. Handle read
errors rather than returning the digest of a prefix as if complete.

## Test matrix

- one official/upstream known vector for each supported algorithm;
- empty bytes and representative binary bytes containing zero/non-UTF-8 values;
- one-shot versus every relevant chunk partition;
- same logical text under required normalization and explicit UTF-8;
- different seed and one-byte-changed input produce different expected vectors
  (not a proof of general collision resistance);
- bytes/hex/integer representations agree according to upstream semantics;
- structured framing distinguishes neighboring ambiguous tuples;
- on digest match, application equality verification runs when required.

For cross-language protocols, generate the same vectors in every implementation
and check them into tests with the complete contract metadata. Do not derive the
expected value from the implementation under test in the same assertion.
