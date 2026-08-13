# Migration safeguards

Establish current commands and artifacts before replacing requirements files,
setup configuration, Poetry, or another manager. Preserve markers, extras,
indexes, editable/path/git dependencies, workspace membership, entry points,
package data, and CI deployment behavior. Regenerate rather than hand-edit the
lock, diff resolved packages, and test a clean clone/build before removing the
old path.
