# Streamlit rerun and state model

Normal widget interaction updates frontend/widget state and triggers a
top-to-bottom script run. A widget callback, when configured, executes first;
then the script runs. Therefore every top-level side effect is repeatable unless
guarded by an event and idempotency rule.

Session state belongs to one connected browser session and is lost when that
session ends or the server state resets. It is not durable persistence. Widget
keys link frontend identity to session-state entries; changing key/defining
parameters can create a new widget identity.

Initialize keys before use:

```python
if "page" not in st.session_state:
    st.session_state.page = "overview"
```

Use stable record IDs in dynamic keys, not list positions that change after
sorting/filtering. Separate a trigger (`button` clicked this run) from durable
workflow state (`job_status == "submitted"`).

Callbacks should make a short state transition. Main page output belongs in the
normal render flow because callback-rendered elements appear before and can
disappear on the next rerun. External writes need a stable operation ID and a
stored receipt/transaction so refresh or duplicate clicks cannot repeat them.
