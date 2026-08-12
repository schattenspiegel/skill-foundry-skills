# Streamlit caching and forms

Use `st.cache_data` for data values that can be recomputed from explicit
arguments. Include user/tenant, query, filters, source version, and other
semantic inputs unless cross-user reuse is intentionally safe. Set TTL for
remote freshness and `max_entries` for cardinality/memory. Never cache a secret
in rendered output or share user-specific data through an under-keyed cache.

Use `st.cache_resource` for connections, models, and clients whose lifetime is
global and whose implementation is safe for concurrent sessions. It returns a
shared mutable instance; put per-session cursors/configuration elsewhere.

Forms batch widget updates until `st.form_submit_button`. Use a form for search
criteria, settings, or mutations that need atomic input. Widgets inside cannot
drive backend-dependent dynamic changes before submit. Keep an explicit draft
versus committed state when unrelated reruns must not apply unsubmitted values.

Do not put side effects inside cached functions: cache hits skip execution and
cache misses can recur. Cache retrieval and external mutation are separate
operations with separate verification.
