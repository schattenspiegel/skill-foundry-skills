# Streamlit fragments and interaction testing

Use a fragment after the app is correct under full reruns and profiling shows a
region should update independently. Fragment widgets trigger that fragment
rather than the whole script; an automatic `run_every` adds repeated execution.
Keep state transitions idempotent and shared-resource access thread-safe.

Render inside the fragment's own region. Writing to a container created outside
the fragment can accumulate elements across fragment reruns rather than clear
them as a normal full rerun would. Define whether a fragment-triggered action
needs a fragment rerun or full-app rerun and use the installed API explicitly.

## Test sequences, not functions only

Use Streamlit's installed app-testing API when available to run:

1. first load and default state;
2. each widget change or form draft without submit;
3. form submit and committed output;
4. callback state visible in the following render;
5. fragment-local update versus full-app update;
6. error/empty/loading branch;
7. two sessions proving state isolation;
8. cache hit, TTL/invalidation, and user-key separation;
9. repeated mutation trigger proving idempotency.

Static import/compile checks cannot prove rerun order, browser widget identity,
WebSocket/session behavior, or rendering. Retain a real `streamlit run` browser
smoke test for release-critical interactions.
