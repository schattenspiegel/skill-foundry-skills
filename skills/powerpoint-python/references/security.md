# Security

Treat presentations as potentially active and untrusted packages. Never execute
macros, add-ins, actions, programs, file-open commands, OLE verbs, or media;
never follow external links merely to inspect them; never refresh embedded or
linked content.

Report external hyperlinks, internal slide links, external relationships,
`OPEN_FILE`, `RUN_PROGRAM`, `RUN_MACRO`, OLE objects, and embedded packages.
Preserve or remove active content only under an explicit contract, with a
before/after inventory.

Parse ZIP/XML defensively: reject malformed archives, bound detail output,
avoid extraction to attacker-controlled paths, and do not resolve external XML
entities or relationship targets.
