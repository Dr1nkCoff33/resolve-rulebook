# GSD Production Rules (worked example)

A filled-in copy of the template, as used on a two-videos-a-week YouTube channel. Gear names are left out on purpose; the lanes are generic.

This file wins over any skill, prompt or habit for folders, tools, naming, versions, Shorts, renders, delete and overwrite.

Read this file first, every project. The brief in the project's `05_PROJECT/brief.md` is the memory for that project.

## Commands
- "new episode EP### name": follow `_TEMPLATE/NEW_EPISODE_ROUTINE.md` exactly. Do not restate its steps.

## Naming and versions
- Project folder and Resolve project: `EP###_<name>` (lowercase, hyphens, no version).
- Timelines: `EP###_LONG_v##` and `EP###_S##_v##` (one `S##` per Short). New version only via Duplicate Timeline As. Never rename an old timeline version.
- Template: `GSD_TEMPLATE_v##`. A change is a new version; the old one is copied into `_archive/`. Never edit a template in place. A template version carries its own `assets/` copy only when the bumpers or music changed; otherwise the routine reads `_TEMPLATE/assets/`.
- Graphics: `gfx_<name>_v##` in `03_GFX`, thumbnails `gfx_thumb_<name>_v##`. A re-render is the next version. Never overwrite an earlier version.
- Screen recordings: `cap_<name>.<ext>` in `03_GFX`.

## Folders (`EP###_<name>/`)
`01_CAMERA_A`, `02_AUDIO`: originals, read-only. `03_GFX`: add new files only. `04_STILLS`: still frames and reference images. `05_PROJECT`: brief, cards, cutlists, transcripts. `06_EXPORTS`: renders only. `assets/`: the bumpers and music copied for this project. `_TEMPLATE/_folder_skeleton/` is the only definition of these lanes; add a lane there, not here.

Camera clips for real projects are recorded at 24p (23.976), never 30p; a 30p source on a 23.976 timeline judders. If a clip in `01_CAMERA_A` is at another rate, say so before importing it.

## Tools
- Allowed tools: Canva, Epidemic Sound, Cap, Claude in Chrome, Resolve tools. Anything else is off.
- Resolve: use the scripting API. Never use an unsafe or unrestricted script runner. Never open, save or modify any project other than the one named in the current task. The API cannot save: after any change, tell me to press Cmd+S before reporting the step as done.
- Transcription: whisper-cli on the Mac, run by me. If the assistant cannot run it, it prints the exact command instead.
- Thumbnails: Canva, thumbnails only. Never build from scratch; copy the design named `GSD Thumbnail MASTER` and change only its text, 1 to 3 words, 16 characters or fewer. If the text is longer, propose a shorter title and ask. Never wrap, shrink or resize to make text fit. Export 1280x720 PNG to `03_GFX` as `gfx_thumb_<name>_v##`.
- Music: Epidemic Sound. Its license likely covers my own channels only. Check what the license covers before using a track in client work.
- Renders: presets do not store a destination. Load `GSD_LONG_4K_2398` for a LONG timeline and `GSD_SHORTS_2160x3840_2398` for a Shorts timeline. Before every render: (1) set the render target folder to the project's `06_EXPORTS` and the file name to the timeline name; (2) find the last frame of the last video clip and set a marked range from the timeline start to that frame (SelectAllFrames off, MarkIn and MarkOut set), so audio can never run past the picture; (3) list any audio clip that ends after the last video frame. After the render, read the file with ffprobe and compare the video and audio stream durations. If they differ by more than 3 frames (AAC padding adds about 2), or the resolution is not 3840x2160 for LONG or 2160x3840 for Shorts, say so plainly and do not report the render as done. Never overwrite an existing export.
- Bumpers: on every LONG timeline the intro is the first video clip and the outro is always the last, after all content. Never place anything after the outro. Before every render, list the video clips in order; if the outro is not last, stop and say so.
- Brand: use the locked brand system. Look it up where it lives; do not retype it here.

## Safety
Create and copy only. Never delete. Back up a file before editing it. If a destination exists, stop and ask. Backups are named `<file>.<YYYYMMDD-HHMM>` and are never overwritten.

## Shorts
Target 2 to 4 Shorts per 10-minute episode, each 30 to 60 seconds. Shorts timelines are 2160x3840, 23.976, inside the same project. A 16:9 clip on a Shorts timeline uses Scaling = Fill (crop to the frame), then Transform position to keep the subject inside the phone-safe area. Never Smart Reframe. One clip card per Short, filled one at a time from the transcript.

## Editorial
Cut, pad, marker, mix and grade rules are not plumbing and do not live here. They live in the gsd-* edit skills in the private content repo, which this file wins over only where the two disagree on folders, tools, naming, versions, Shorts, renders, delete or overwrite.
