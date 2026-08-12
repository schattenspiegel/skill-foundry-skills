# ndarray, axis, dtype, and ownership model

An ndarray combines a data buffer with metadata: `shape`, `ndim`, `dtype`,
`itemsize`, `strides`, order/contiguity flags, and sometimes a `.base` owner.
The array is homogeneous at the dtype level. Object dtype stores Python object
references and changes performance, serialization, and safety assumptions.

## Shapes and axes

Name axes in comments/types/contracts, for example `(batch, time, feature)`.
Length-one dimensions are not decorative; they control broadcasting. `squeeze`
without a specified axis can erase a semantic dimension unexpectedly. A 0-D
array is indexable with `()` and differs from a Python/NumPy scalar.

## Views and copies

- Assignment `b = a` creates another reference to the same array object.
- Basic slicing creates a view in normal cases.
- Transpose and axis moves normally create views with changed strides.
- Advanced indexing creates a copy.
- `reshape` may be a view or copy depending on layout.
- `ravel` returns a view when possible; `flatten` returns a copy.
- `astype` normally allocates for dtype conversion; inspect its current copy/cast contract.

`.base` is a clue, not a complete ownership proof for every external array.
Use `np.shares_memory` for a definitive but potentially expensive check and
`np.may_share_memory` for a conservative possibility check. Public mutation APIs
should document whether inputs may be modified and return owned outputs where
caller isolation matters.

## Dtypes

Specify byte-sized dtypes (`int64`, `float32`) when portability/range matters;
platform integer width can vary. Define casting policy with `can_cast` or the
operation's `casting=` where applicable. For reductions, explicitly choose an
accumulation dtype when input range can overflow or floating precision matters.
