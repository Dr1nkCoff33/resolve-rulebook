# New project routine

Trigger: "new project <ID> <name>". Rules come from `_TEMPLATE/CLAUDE.md`; this file is only the order of operations. Current template: `RESOLVE_TEMPLATE_v01` (assets: `_TEMPLATE/assets/`).

1. **Folder.** If `<projects root>/<ID>_<name>/` exists, stop and ask. Otherwise copy `_TEMPLATE/_folder_skeleton/` to it, and copy the template's assets into `<ID>_<name>/assets/`. Create only; never overwrite. (`scripts/new_project.py` does exactly this.)
2. **Import.** Import `_TEMPLATE/RESOLVE_TEMPLATE_v01.drp` as a new Resolve project named `<ID>_<name>`. If a project with that name exists, stop and ask. Record the template version used.
3. **Rename and relink.** Rename `TPL_LONG_v01` to `<ID>_LONG_v01` and `TPL_S01_v01` to `<ID>_S01_v01`. Run `ReplaceClip` on every bumper and music clip so each points at the matching file in `<ID>_<name>/assets/`. Confirm nothing is offline. Change nothing else from the template.
4. **Place the content by hand.** The scripting API cannot ripple-insert. The human puts the playhead on the edit point between the intro and the outro, locks the music track, selects the content clip in the Media Pool and presses F9 (Insert), which pushes the outro right. Then unlocks the music and fits it to the new end. After the human confirms, list the V1 clips in order; the outro must be last. If it is not, stop and say so.
5. **Report.** What was created, the folder tree, the bin names, the clip paths, anything offline, and any step skipped. Tell the human to press Cmd+S.
