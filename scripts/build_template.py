#!/usr/bin/env python3
"""Build the Resolve template project from the values in a small config block.

Run this on the machine where DaVinci Resolve is open, with the scripting API
enabled (Preferences > System > General > External scripting using: Local).
It creates one project with two timelines (a landscape LONG timeline and a
portrait Shorts timeline), names the tracks, sets the start timecode, imports
the bumpers and music from _TEMPLATE/assets/, places intro then outro on the
LONG timeline, saves two render presets, and exports the .drp.

It never overwrites: if the project or the .drp already exists it stops.
It cannot save the project (the API has no save), so press Cmd+S when it
finishes, and it cannot rename bins, so it creates them with the final names.

    python3 scripts/build_template.py --version 1
    python3 scripts/build_template.py --version 2 --dry-run

Edit CONFIG below once. Everything the script does comes from it.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

CONFIG = {
    "template_home": os.environ.get("TEMPLATE_HOME", ""),   # e.g. /Volumes/video/Projects/_TEMPLATE
    "name_prefix": "RESOLVE_TEMPLATE_v",
    "frame_rate": "23.976",
    "start_timecode": "01:00:00:00",
    "long": {"timeline": "TPL_LONG_v01", "width": 3840, "height": 2160},
    "shorts": {"timeline": "TPL_S01_v01", "width": 2160, "height": 3840},
    "bins": ["01_CAMERA_A", "02_AUDIO", "03_GFX", "04_STILLS", "05_PROJECT",
             "06_EXPORTS", "07_TIMELINES", "08_BUMPERS", "09_MUSIC"],
    "video_tracks": ["A-roll and bumpers", "B-roll A", "B-roll B", "Cards", "FX"],
    "audio_tracks": ["VOICE", "Bleeps", "SFX and music", "SYNC (muted)"],
    "mute_audio_track": 4,
    "intro": "intro.mov",     # file names inside _TEMPLATE/assets/bumpers/
    "outro": "outro.mov",
    "music": "music.wav",     # inside _TEMPLATE/assets/music/
    "presets": {
        "LONG_PRESET": {"width": 3840, "height": 2160, "bitrate_kbps": 40000},
        "SHORTS_PRESET": {"width": 2160, "height": 3840, "bitrate_kbps": 40000},
    },
}


def get_resolve():
    try:
        import DaVinciResolveScript as dvr  # type: ignore
    except ImportError:
        sys.path.append("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")
        try:
            import DaVinciResolveScript as dvr  # type: ignore
        except ImportError:
            sys.exit("error: DaVinciResolveScript not importable. Enable external scripting in Resolve and run this on that machine.")
    resolve = dvr.scriptapp("Resolve")
    if resolve is None:
        sys.exit("error: Resolve is not running or scripting is not enabled.")
    return resolve


def check(ok, what):
    print(("  ok   " if ok else "  FAIL ") + what)
    return bool(ok)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--version", type=int, required=True, help="template version number, e.g. 1")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and touch nothing")
    args = ap.parse_args(argv)

    cfg = CONFIG
    if not cfg["template_home"]:
        sys.exit("error: set TEMPLATE_HOME to your _TEMPLATE folder.")
    home = Path(cfg["template_home"])
    name = f"{cfg['name_prefix']}{args.version:02d}"
    drp = home / f"{name}.drp"
    bumpers = home / "assets" / "bumpers"
    music = home / "assets" / "music"
    media = [bumpers / cfg["intro"], bumpers / cfg["outro"], music / cfg["music"]]

    print(f"template: {name}")
    print(f"export:   {drp}")
    for m in media:
        print(f"asset:    {m} {'(found)' if m.exists() else '(MISSING)'}")
    if drp.exists():
        sys.exit(f"error: {drp} exists. A new version is a new number; nothing was changed.")
    if any(not m.exists() for m in media):
        sys.exit("error: put the bumpers and music in _TEMPLATE/assets/ first.")
    if args.dry_run:
        print("dry run: nothing created.")
        return 0

    resolve = get_resolve()
    pm = resolve.GetProjectManager()
    if name in (pm.GetProjectListInCurrentFolder() or []):
        sys.exit(f"error: a Resolve project named {name} already exists. Nothing was changed.")
    project = pm.CreateProject(name)
    if not project:
        sys.exit("error: CreateProject failed.")
    print(f"created project {name}")

    fr = cfg["frame_rate"]
    L, S = cfg["long"], cfg["shorts"]
    check(project.SetSetting("timelineFrameRate", fr), f"project frame rate {fr}")
    check(project.SetSetting("timelineResolutionWidth", str(L["width"])), f"project width {L['width']}")
    check(project.SetSetting("timelineResolutionHeight", str(L["height"])), f"project height {L['height']}")

    pool = project.GetMediaPool()
    root = pool.GetRootFolder()
    bins = {}
    for b in cfg["bins"]:
        bins[b] = pool.AddSubFolder(root, b)
        check(bins[b] is not None, f"bin {b}")

    pool.SetCurrentFolder(bins["08_BUMPERS"])
    bumper_items = pool.ImportMedia([str(media[0]), str(media[1])]) or []
    pool.SetCurrentFolder(bins["09_MUSIC"])
    music_items = pool.ImportMedia([str(media[2])]) or []
    check(len(bumper_items) == 2, "imported intro and outro")
    check(len(music_items) == 1, "imported music")
    for it in bumper_items:
        fps = it.GetClipProperty("FPS")
        check(str(fps).startswith(fr[:5]), f"{it.GetName()} is {fps} fps (template is {fr})")

    pool.SetCurrentFolder(bins["07_TIMELINES"])

    def make_timeline(spec):
        tl = pool.CreateEmptyTimeline(spec["timeline"])
        if not tl:
            sys.exit(f"error: could not create timeline {spec['timeline']}")
        check(tl.SetSetting("useCustomSettings", "1"), f"{spec['timeline']} custom settings on")
        check(tl.SetSetting("timelineResolutionWidth", str(spec["width"])), f"{spec['timeline']} width {spec['width']}")
        check(tl.SetSetting("timelineResolutionHeight", str(spec["height"])), f"{spec['timeline']} height {spec['height']}")
        check(tl.SetSetting("timelineFrameRate", fr), f"{spec['timeline']} frame rate {fr}")
        check(tl.SetStartTimecode(cfg["start_timecode"]), f"{spec['timeline']} start {cfg['start_timecode']}")
        while tl.GetTrackCount("video") < len(cfg["video_tracks"]):
            tl.AddTrack("video")
        while tl.GetTrackCount("audio") < len(cfg["audio_tracks"]):
            tl.AddTrack("audio")
        for i, n in enumerate(cfg["video_tracks"], 1):
            check(tl.SetTrackName("video", i, n), f"V{i} {n}")
        for i, n in enumerate(cfg["audio_tracks"], 1):
            check(tl.SetTrackName("audio", i, n), f"A{i} {n}")
        m = cfg["mute_audio_track"]
        if m:
            check(tl.SetTrackEnable("audio", m, False), f"A{m} muted")
        return tl

    long_tl = make_timeline(L)
    make_timeline(S)
    project.SetCurrentTimeline(long_tl)

    # Intro then outro, adjacent. Content is inserted between them by hand (F9).
    start = long_tl.GetStartFrame()
    intro, outro = bumper_items[0], bumper_items[1]
    i_frames = int(intro.GetClipProperty("Frames") or 0)
    o_frames = int(outro.GetClipProperty("Frames") or 0)
    placed = pool.AppendToTimeline([
        {"mediaPoolItem": intro, "startFrame": 0, "endFrame": i_frames, "recordFrame": start, "trackIndex": 1},
        {"mediaPoolItem": outro, "startFrame": 0, "endFrame": o_frames, "recordFrame": start + i_frames, "trackIndex": 1},
    ]) or []
    check(len(placed) == 2, f"intro ({i_frames} fr) then outro ({o_frames} fr) on V1")
    order = [it.GetName() for it in long_tl.GetItemListInTrack("video", 1) or []]
    check(order == [intro.GetName(), outro.GetName()], f"V1 order {order}")

    # Render presets. Destination is never stored in a preset; the routine sets it per render.
    for pname, p in cfg["presets"].items():
        ok = project.SetCurrentRenderFormatAndCodec("mp4", "H264")
        ok = project.SetRenderSettings({
            "SelectAllFrames": 1, "FormatWidth": p["width"], "FormatHeight": p["height"],
            "FrameRate": float(fr), "VideoQuality": p["bitrate_kbps"] * 1000, "ExportVideo": True, "ExportAudio": True,
        }) and ok
        ok = project.SaveRenderPreset(pname) and ok
        check(ok, f"render preset {pname} {p['width']}x{p['height']}")

    check(pm.ExportProject(name, str(drp), False), f"exported {drp}")
    print()
    print("Press Cmd+S in Resolve now. Then run the proof: import the .drp as a throwaway")
    print("project and read back both timelines, every clip path, and the preset list.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
