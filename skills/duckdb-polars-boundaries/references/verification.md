# Verification

Test empty, null, timestamp, decimal, categorical, and nested inputs. Compare
schema plus values before/after, assert grain and row count, and make order
explicit. Test object/connection lifetime and repeated executions to expose
stale registration. Measure copies and memory only when performance matters.
