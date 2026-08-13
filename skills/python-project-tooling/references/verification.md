# Quality and build verification

Check the lock without updating it, sync from the lock, then run formatting,
linting, type checking, and tests. For packages, build both artifacts, list
their contents, inspect metadata and entry points, install the wheel in a clean
environment, and import it outside the source tree. Compare sdist-to-wheel
build behavior when generated files or package data are involved.
