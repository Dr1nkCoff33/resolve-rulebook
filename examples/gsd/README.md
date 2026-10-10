# Worked example: GSD Media

The template filled in for one channel: two videos a week, a long 16:9 episode plus 2 to 4 vertical Shorts cut from it, Resolve driven by an AI assistant through the scripting API.

Choices this example made, and why:
- **Episode IDs** (`EP###`) rather than ISO weeks, so a project name never changes if a video slips a week.
- **23.976 everywhere.** The bumpers and the camera both produce 23.976; switching the timeline to true 24 would have meant a dropped frame every 41 seconds for nothing.
- **Shorts at 2160x3840** inside the same project as the long timeline. One template, one media pool, no second project to keep in step.
- **Thumbnails are a copy of one master design** with only the text changed, 1 to 3 words. The first test used a six-word title and the text spilled out of the frame; the rule was added the same day.
- **Marked-range renders.** The first test render was 218 s long because the music bed ran past a 52 s picture. The render range now ends at the last video frame, and the exported durations are checked afterwards.
- **One copy of the media.** Each template version used to carry its own 186 MB of bumpers and music; five versions meant five copies. Now the shared folder is the default and a version gets its own copy only when the files change.

Not included: the camera, mic and lighting rig, the brand system, and the editing rules (cuts, pads, markers, audio chain). Those are the part worth keeping to yourself.
