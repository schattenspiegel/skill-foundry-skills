# Projects and dependencies

An application may need only project metadata and dependencies; a distributable
library needs a build backend and package discovery. A workspace shares one
lockfile but each member retains its own package metadata. Runtime dependencies,
optional extras, and dependency groups have different consumers. Use exact
Python compatibility and markers where platform behavior differs.
