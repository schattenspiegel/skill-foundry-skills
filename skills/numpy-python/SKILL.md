---
name: numpy-python
description: Use for writing, reviewing, debugging, testing, or optimizing Python NumPy ndarray code. Trigger on array construction, shape/axis reasoning, dtypes and casting, broadcasting, indexing, copies/views, ufuncs, reductions, vectorization, random Generator, linear algebra, FFT, masked/structured arrays, memory layout, or NumPy interoperability. Do not use for pandas/Polars table semantics, JAX/CuPy-only arrays, symbolic SymPy, or pure Python sequences without a NumPy boundary.
argument-hint: "[NumPy array task, shape contract, code, or error]"
---

# NumPy Python

Produce NumPy code whose array shape, axis meaning, dtype, broadcasting,
ownership, mutation, missing/nonfinite policy, and numerical accuracy are
explicit and tested.

## Know the array contract

| Concept | Runtime meaning | Required decision |
|---|---|---|
| `ndarray` | Homogeneous, fixed-size multidimensional elements plus shape/strides/dtype metadata. | Define every axis and dtype. |
| scalar / 0-D array | Python/NumPy scalar or `shape == ()` array. | Preserve the caller's return type deliberately. |
| view | New array metadata sharing an underlying buffer. | Mutation can affect another array. |
| copy | Independently owned data buffer. | Pay allocation cost when ownership isolation is needed. |
| ufunc | Elementwise operation supporting broadcasting, dtype loops, `out`, and reductions. | Check promotion and nonfinite behavior. |
| `Generator` | Explicit random stream. | Inject it; never depend on ambient global RNG state. |

Shape is not just dimensions: assign a semantic name to each axis. A vector
`(n,)`, a column `(n, 1)`, and a row `(1, n)` broadcast and multiply
differently. Dtype governs range, precision, missing representation, byte order,
and memory. Read [the ndarray, axis, dtype, and ownership model](references/object-model.md).

## Ordered workflow

1. Recover input/output shape, named axis meaning, dtype, units, mutability,
   ownership, and nonfinite/missing policy from callers and tests.
2. Normalize with `np.asarray` when copying is unnecessary, or `np.array(...,
   copy=True)` when independent ownership is part of the API.
3. State the intended broadcast using shape algebra; insert axes explicitly
   with `None`/`np.newaxis`, `expand_dims`, or reshape.
4. Use ufuncs, reductions, indexing, matrix operations, or an operation family
   matched to the semantic axis; avoid `np.vectorize` as a performance fix.
5. Control accumulation/result dtype when overflow or precision matters.
6. Make copy/view and mutation behavior explicit at every slice, reshape,
   transpose, fancy index, `astype`, and boundary conversion.
7. Test empty axes, singleton axes, noncontiguous views, integer limits,
   mixed dtypes, `NaN`/infinity, aliasing, and invalid shapes.

## Choose by intent

| Intent | Prefer | Guard |
|---|---|---|
| Convert array-like | `asarray` / `array` | Copy, dtype, ragged input, and subclass policy. |
| Elementwise transform | ufunc/operator | Broadcasting, promotion, `where`, `out`. |
| Aggregate | `sum`, `mean`, `min`, etc. | Axis, `keepdims`, empty input, accumulation dtype. |
| Matrix product | `@` / `matmul` | Batch axes and 1-D special cases. |
| Elementwise product | `*` | Never substitute for matrix multiplication. |
| Rearrange without changing elements | transpose/moveaxis/reshape | View/copy possibility and axis mapping. |
| Select by slices | basic indexing | Usually a view. |
| Select by integer/boolean arrays | advanced indexing | A copy; boolean shape must match its indexed axes. |
| Join/split arrays | concatenate/stack/block/split families | Existing versus newly inserted axis. |
| Random sampling | injected `np.random.Generator` | Seed/stream/shape and distribution parameterization. |

Read [operations, broadcasting, and numerical rules](references/operations.md).

## Canonical anchor

```python
import numpy as np
import numpy.typing as npt


def standardize_columns(values: npt.ArrayLike) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 2:
        raise ValueError(f"expected (rows, features), got {array.shape}")
    mean = array.mean(axis=0, keepdims=True)
    scale = array.std(axis=0, keepdims=True)
    if np.any(scale == 0) or not np.all(np.isfinite(scale)):
        raise ValueError("every feature must have finite, nonzero scale")
    return (array - mean) / scale
```

`axis=0` aggregates rows to one statistic per feature; `keepdims=True` makes the
subsequent `(rows, features) - (1, features)` broadcast auditable. The function
returns a new floating array and rejects constant/nonfinite scale by policy.

## High-risk rules

- Broadcasting compares trailing dimensions; dimensions match when equal or
  one is `1`. Use `np.broadcast_shapes` in validation when shape compatibility
  is a public contract. Avoid a broadcast that creates a huge intermediate.
- Basic slicing normally returns a view; advanced integer/boolean indexing
  returns a copy. Chained indexing can therefore mutate—or fail to mutate—the
  original unexpectedly. Assign with one indexed operation when mutation is intended.
- `reshape` returns a view where possible and a copy otherwise. Never promise
  zero-copy without checking layout/strides or enforcing a contiguous contract.
- Dtype promotion can overflow integers, lose precision, or convert mixed data
  to object/string. Declare input, accumulation, and output dtypes for critical code.
- `NaN`, positive/negative infinity, masked values, and absence are different
  policies. Integer arrays cannot represent `NaN` without changing dtype.
- `np.empty` is uninitialized. Write every element before reading it.
- `np.vectorize` is a convenience loop, not native vectorized performance.
  Prefer ufunc/array algebra, generalized ufuncs, compiled kernels, or a clear
  outer loop that controls memory.
- Use `default_rng`/`Generator` injected into functions. Test invariants and
  fixed-stream reproducibility, not one global `np.random.seed` trace.
- For linear algebra, validate shapes, rank/conditioning, and residuals. Prefer
  solving systems to explicit inverse multiplication.
- Do not mutate `.shape` or `.dtype` attributes to reinterpret data. Use reshape,
  `astype`, or `view(dtype=...)` only when their different semantics are intended.

## Performance and interoperability

Before optimizing, measure allocations and representative shapes. Prefer array
operations but control temporaries with staged computation or `out=` only when
aliasing/casting is safe. Memory order, strides, and contiguity affect native
libraries; copying once at a boundary may beat repeated strided work.

At pandas, Polars, Arrow, JAX, CuPy, Torch, or buffer boundaries, define device,
ownership, writable state, dtype, shape, zero-copy claim, and lifetime. “Array
like” does not guarantee a NumPy-owned CPU buffer.

## Version grounding and completion

The stable online docs currently identify NumPy 2.5, while NumPy is absent from
the foundry environment. Check the installed version with `np.__version__`, then
inspect the migration guide and signature before relying on promotion, string dtype, copy keyword,
random, or Array API behavior. Read [verification](references/verification.md).

Completion requires exact shape/axis/dtype/ownership contracts; broadcast and
mutation behavior proven on adversarial shapes/views; nonfinite and overflow
policy tested; numeric algorithms checked by residual/tolerance; and no hidden
object dtype, unintended copy, or global RNG dependency.

## References

- [ndarray, axis, dtype, and ownership model](references/object-model.md)
- [Operations, broadcasting, and numerical rules](references/operations.md)
- [Verification and API grounding](references/verification.md)
