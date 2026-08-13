# Existing workbooks

1. Copy or retain the source and inspect it without mutation.
2. Recover the workbook contract and package preservation requirements.
3. Run OOXML preflight before openpyxl. If required unsupported or unknown
   features exist, stop before load/save.
4. Load with formula text. Add `keep_vba=True` for macro-enabled files and keep
   external links unless the contract explicitly removes them. Use a separate
   `data_only=True` load only for cached-result evidence.
5. Reassert the target Table/name/range and expected old value immediately
   before mutation. Change the smallest region; do not rebuild unaffected
   sheets or normalize styles globally.
6. Save to a temporary sibling with the correct extension, close, reopen, and
   compare against the before snapshot. Move to the requested destination only
   after all required invariants pass.

Never overwrite the source by default. Never use `read_only=True` for mutation.
Do not assume `keep_vba=True` preserves non-VBA Excel objects. Do not delete an
unknown defined name, relationship, or hidden sheet merely because it appears
unused.
