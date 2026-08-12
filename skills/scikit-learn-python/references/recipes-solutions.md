# Evaluated solution recipes

## Recipe `sklearn.pipeline-cross-validation`
**Use when:** cross-validate preprocessing and classification as one unit.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def evaluate(X, y):
    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, random_state=7)),
        ]
    )
    split = StratifiedKFold(5, shuffle=True, random_state=7)
    scores = cross_validate(model, X, y, cv=split, scoring=("accuracy", "neg_log_loss"))
    model.fit(X, y)
    return model, scores
```
**Do not use when:** The requested abstraction or lifecycle differs from
`leakage-safe-pipeline`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `sklearn.verify-no-preprocessing-leakage`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline
from solution import evaluate


def test_pipeline_is_evaluated_as_unit() -> None:
    X, y = make_classification(n_samples=100, n_features=6, random_state=3)
    model, scores = evaluate(X, y)
    assert isinstance(model, Pipeline)
    assert len(scores["test_accuracy"]) == 5
    assert np.isfinite(scores["test_neg_log_loss"]).all()
    assert model.predict(X[:3]).shape == (3,)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`leakage-safe-pipeline`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `sklearn.group-aware-splitting`
**Use when:** prevent entity leakage across validation folds.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
from sklearn.model_selection import GroupKFold


def group_splits(X, y, groups, n_splits: int = 3):
    if len(np.unique(groups)) < n_splits:
        raise ValueError("not enough unique groups")
    result = list(GroupKFold(n_splits=n_splits).split(X, y, groups))
    for train, test in result:
        if set(np.asarray(groups)[train]) & set(np.asarray(groups)[test]):
            raise RuntimeError("group leakage")
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`group-isolated-splits`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `sklearn.verify-group-disjointness`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
import pytest
from solution import group_splits


def test_groups_are_disjoint() -> None:
    X = np.arange(24).reshape(12, 2)
    y = np.array([0, 1] * 6)
    groups = np.repeat(np.arange(6), 2)
    for train, test in group_splits(X, y, groups):
        assert set(groups[train]).isdisjoint(groups[test])
    with pytest.raises(ValueError):
        group_splits(X[:4], y[:4], [1, 1, 2, 2], 3)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`group-isolated-splits`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `sklearn.inference-schema-guard`
**Use when:** reject drifted feature schemas at inference.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np


def predict_checked(model, frame):
    if not frame.columns.is_unique:
        raise ValueError("duplicate feature columns")
    expected = list(model.feature_names_in_)
    if list(frame.columns) != expected:
        raise ValueError(f"expected ordered features {expected}")
    classes = np.asarray(model.classes_)
    if not np.array_equal(classes, np.array([0, 1])):
        raise ValueError("positive-class contract requires classes [0, 1]")
    return model.predict_proba(frame)[:, 1]
```
**Do not use when:** The requested abstraction or lifecycle differs from
`schema-checked-predict`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `sklearn.verify-feature-and-class-contract`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from solution import predict_checked


def test_schema_and_class_mapping() -> None:
    frame = pd.DataFrame({"a": [0, 1, 2, 3], "b": [1, 0, 1, 0]})
    model = LogisticRegression().fit(frame, [0, 0, 1, 1])
    assert predict_checked(model, frame).shape == (4,)
    with pytest.raises(ValueError):
        predict_checked(model, frame[["b", "a"]])
```
**Do not use when:** The requested abstraction or lifecycle differs from
`schema-checked-predict`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
