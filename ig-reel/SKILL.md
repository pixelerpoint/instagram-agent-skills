---
name: ig-reel
description: Make a finished Instagram Reel for @warmnode - the 3-second hook, timed on-screen text, and a ready-to-upload 1080x1920 MP4 built from the owner's own café clips and photos in the espresso & chai look, plus audio advice and caption. Use for "/ig-reel", "reel idea", "script a reel", or "make a video".
---

# /ig-reel - a finished reel, not a filming task

## Account context (@warmnode)
- Name field: "Warmnode · Deep Talks". Bio: "Rent a friend (free, just talk) ☕ / Deep questions for overthinkers 18–30 / New one daily · answer in the comments"
- Voice: a warm, calm friend across the coffee table. Honest, gentle, never preachy.
- Audience: 18-30 overthinkers who feel lonely in a crowd and crave real conversation. Pakistan. English, light Roman Urdu when natural.
- Pillars: deep questions, quiet truths about loneliness/friendship, coffee-table confessions, being a better friend/listener, café diaries (the owner's own café and restaurant visits).
- Faceless account, owner has almost no time and is not technical. Deliver a finished video, not a shot list to film, whenever media exists.
- If the user says their niche changed, follow what they say now.

## Steps
1. **Topic.** None given? Pick one from the pillars yourself. Don't ask.
2. **Media.** Photos/clips the user attached → the Google Drive folder "warmnode data" via /ig-drive (prefer short clips under ~3 MB; skip the "used" subfolder; skip clips with people's faces or with on-screen text/clocks baked in) → if nothing exists, fall back to the old way: write the script and a shot list they can film in 5 minutes.
3. **Script.** 7-9 text beats, 18-25 seconds total:
   - **Hook (first 2-3 s):** max 8 words, a feeling they recognise or a question they can't ignore. Open on a moving clip if you have one; motion holds people in the first second.
   - Beats of 2-3.2 s, max ~12 words each. End on a line that makes people comment or rewatch ("Which one will you ask tonight?").
4. **Render.** Spec (path relative to this skill folder):
   ```
   {"media_dir": "/path/to/media",
    "segments": [{"video": "clip.mp4", "start": 0.5, "secs": 2.8, "big": true, "text": "Stop asking “how are you?”"},
                 {"photo": "cup.jpg", "secs": 3.0, "text": "..."}]}
   ```
   `python3 scripts/warmnode.py reel spec.json out.mp4` → 1080x1920 MP4 with a silent audio track. Photos get a slow push-in, clips are graded to match.
5. **Check.** Pull 4-6 frames with ffmpeg into a contact sheet and look at it: text readable, no faces, no sticker or clock overlays from the source clips.
6. **Audio.** Music is never baked in, because Instagram's own audio gets more reach. Tell the owner, in plain words:
   - In Meta Business Suite → Create Reel → **Audio** tab → search `lofi`, `piano`, `acoustic` or `chill` → pick something slow and soft (not filmi/dance tracks) → keep the volume low.
   - Or in the Instagram app → Reel → Audio.
   - Audio can't be added after the reel is published, so it has to be done before scheduling.
7. **Caption** (follow /ig-caption) and **cover**: the first frame is the cover by default; say if a later frame is better.
8. **Deliver** the MP4, the caption block, the posting day and time (PKT), and the audio steps. List the Drive file IDs used so /ig-drive can move them to "used" and /ig-tracker can log it.

## Output
The MP4 file, caption block, posting time, audio steps. Copy-ready, no extra commentary.
