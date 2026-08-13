# Render verification

Use the Agg backend in headless tests. Assert line/bar/image collections and
their data, text labels, limits, scale, legend entries, and output dimensions.
Use image comparison only after semantic assertions and with controlled fonts,
backend, DPI, and tolerance. Close figures to prevent state leakage.
