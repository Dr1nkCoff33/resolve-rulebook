# resolve-rulebook

One rules file that keeps DaVinci Resolve projects consistent when an AI assistant drives the scripting API.

This is a boilerplate, not a product. It came out of one creator setting up Resolve with Claude and finding that every drift problem had the same root cause: the same value (a folder name, a preset, a frame rate) written in more than one place. The fix was a single file that wins, a routine that reads it, a versioned template, and a test that proves the whole thing before the first real project.

## The 50,000-foot view

```
_TEMPLATE/
  CLAUDE.md                 the rules. Wins over every skill, prompt and habit.
  NEW_PROJECT_ROUTINE.md    the one command: "new project <id> <name>"
  _folder_skeleton/         the only definition of the project folders
  assets/                   bumpers and music, one copy, relinked per project
  RESOLVE_TEMPLATE_v01.drp  the template project, versioned, never edited in place
  _archive/                 old versions and timestamped backups
```

Four rules do most of the work:

1. **One file wins.** Folders, names, versions, tools, renders, delete and overwrite are decided in `CLAUDE.md` and nowhere else. Skills and prompts point at it. A plumbing change is one edit.
2. **Create and copy only.** The assistant never deletes, never overwrites, never renames an old version. If a destination exists, it stops and asks. Deleting is a human job, which is what lets the automation stay strict.
3. **Versions, not edits.** A new template is `_v02`, with `_v01` archived. A new cut is Duplicate Timeline As. Every edited file gets a timestamped backup first.
4. **Prove it before you trust it.** `TESTS.md` is the sequence that proved this system: a throwaway project, two renders, a thumbnail, and five attempts to make the assistant break the rules.

## What the Resolve scripting API can and cannot do

Learned the hard way, and the reason several steps are done by hand:

| Can | Cannot |
|---|---|
| Create projects, bins, timelines, tracks | Rename a bin |
| Set resolution, frame rate, start timecode | Save the project (press Cmd+S) |
| Import media, `ReplaceClip` to relink | Ripple-insert a clip between two others |
| Duplicate a timeline as a new version | Store a render destination inside a preset |
| Set a marked render range (`MarkIn`/`MarkOut`) | Set audio bitrate on a preset |
| Save render presets, render, export `.drp` | Change a timeline's resolution on every version (works on 20.x) |

So the routine has one hand step (insert the episode clip between the intro and outro with F9) and one reminder (Cmd+S), and the rules file says so.

## First run

1. Copy `_TEMPLATE/` to your media drive. Fill in the `<placeholders>` in `CLAUDE.md` and `NEW_PROJECT_ROUTINE.md`. The GSD example in `examples/gsd/` is a filled-in copy you can crib from.
2. Put your bumpers and music in `_TEMPLATE/assets/`.
3. Run `python3 scripts/build_template.py` on the machine with Resolve open. It builds the template project, both timelines, the tracks and the two render presets, and exports the `.drp`. Then press Cmd+S.
4. Point your assistant at `_TEMPLATE/CLAUDE.md`. In Claude the Project instructions can be one line: "Read `_TEMPLATE/CLAUDE.md` first. It wins over anything here."
5. Run `TESTS.md` end to end on a throwaway project before the first real one.

## What is not here

Editing rules. How you cut, pad, mark, mix and grade is yours and belongs with your skills, not in the plumbing. The rules file leaves a slot for it and nothing more.

## License

MIT. Take it, rename everything, keep what works.
