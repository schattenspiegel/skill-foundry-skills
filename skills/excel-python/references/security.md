# Untrusted text and security

Classify every external/user-controlled field as text, number, date, boolean,
formula, or hyperlink before writing. A string beginning with `=`, `+`, `-`, or
`@` may be interpreted dangerously by spreadsheet consumers; XlsxWriter's
generic `write()` converts leading `=` strings to formulas by default and also
auto-detects URLs.

For semantically textual data, use `write_string()` or construct the workbook
with `strings_to_formulas=False` and, when links are not intended,
`strings_to_urls=False`. Do not escape by silently changing the user's value
unless the output contract defines that representation. Test leading formula
characters, URL-like strings, tabs/newlines, long IDs, and empty strings.

Never execute VBA, refresh external connections, follow workbook hyperlinks,
or dereference external formulas during file inspection. Treat embedded files,
ActiveX, OLE objects, custom XML, and unknown package parts as untrusted opaque
content. Do not expose cell values, source paths, author metadata, or embedded
content in logs unless required by the task.
