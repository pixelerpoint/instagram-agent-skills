---
name: ig-carousel
description: Build a finished Instagram carousel for @warmnode - cover that earns the swipe, slide copy, caption, and ready-to-upload 1080x1350 slides in the espresso & chai look, using the owner's own café photos. Use for "/ig-carousel", "make a carousel", "make a post", or any request for a swipe post.
---

# /ig-carousel - finished carousel, ready to upload

## Account context (@warmnode)
- Name field: "Warmnode · Deep Talks". Bio: "Rent a friend (free, just talk) ☕ / Deep questions for overthinkers 18–30 / New one daily · answer in the comments"
- Voice: a warm, calm friend across the coffee table. Honest, gentle, a little poetic, never preachy or clinical.
- Audience: 18-30, overthinkers, people who feel lonely in a crowd and crave real conversation. Based in Pakistan. English, light Roman Urdu when it feels natural ("theek hoon", chai).
- Pillars: (1) deep questions / conversation starters, (2) quiet truths about loneliness and friendship, (3) coffee-table confessions and mini-stories, (4) how to be a better friend and listener, (5) café diaries: the owner's own café and restaurant visits (Lahore, Aberdeen and wherever they go next).
- The owner has almost no time and is not technical. Deliver finished work, never homework: they only download, upload and schedule. Explain anything technical in plain words.
- If the user says their niche, bio or look changed, follow what they say now.

## The look: "espresso & chai"
- The owner's own photos are the background of every slide, graded dark and warm. Cream serif text, a short chai-amber line above the text, a small café label at the top when the place is known.
- Never the old plain cream/beige slides. If no photos are available at all, the script falls back to a plain espresso background; say so in one line and suggest adding photos to Drive.
- Faceless account: never use a photo where a person's face is recognisable (hands, cups, backs of heads far away are fine).

## Steps
1. **Topic.** None given? Pick one from the pillars yourself (rotate; deep questions and quiet truths save and share best). Don't ask.
2. **Photos.** In priority order: photos the user attached in this chat → the Google Drive folder "warmnode data" (follow the /ig-drive skill to list, download and pick, skipping anything in its "used" subfolder) → plain espresso fallback. Make a numbered contact sheet and look at it before choosing. Match each slide's photo to its mood (chess and chai for questions, empty or foggy scenes for loneliness, a single cup for confessions).
3. **Copy.** 6-8 slides:
   - Slide 1 (cover): one line, max 9 words, a curiosity gap or a "this is me" feeling, plus an optional short subtitle.
   - Slides 2 to n-1: one idea each. Title max ~6 words, body max 30 words.
   - Last slide: a soft call to action (answer in the comments, send it to a friend, save it) and "@warmnode".
4. **Render.** Write a spec and run the script (path relative to this skill folder):
   ```
   {"media_dir": "/path/to/photos",
    "slides": [{"photo": "file.jpg", "title": "...", "body": "...", "place": "Polo Lounge · Lahore", "y": 0.05}, ...]}
   ```
   `python3 scripts/warmnode.py carousel spec.json out_dir/` writes slide_01.jpg ... at 1080x1350.
   - `y` moves the crop window (0 = top, 1 = bottom). Snapchat exports carry a location sticker near the bottom; the default 0.05 keeps it out. Use `zoom` (e.g. 1.2) to crop tighter.
   - `place` only when you can read the place from the photo's own location sticker or the user told you. Never guess a café name.
5. **Check.** Build a contact sheet of all slides and look at it. Text must be readable, nothing cut off, no faces, no leftover sticker text. Fix and re-render if needed.
6. **Caption** (follow /ig-caption): hook line, 2-4 short lines, a question for comments, 3-5 hashtags. Add a location to tag if the cover's place is known.
7. **Deliver.** Zip the slides (folder named like `3_Sat_carousel`) and send it with the caption in a copy-ready block, the posting day and time (weekdays 21:00 PKT, weekends 14:00 or 22:00 unless /ig-audit says otherwise), and the location tag.
8. **Track.** List the Drive file IDs you used so /ig-drive can move them to "used" and /ig-tracker can log the post.

## Scheduling tips to include when relevant
- Meta Business Suite (business.facebook.com) → Create Post → only Instagram ticked → Add photo/video → select slide_01 first, then Shift-click the last slide so the order stays right → paste caption → Schedule (the clock is 24-hour: 9 pm = 21:00).
- If "Scheduling your post" spins for minutes, don't press Schedule again: check Planner first; the post is usually already there.
- Never press "Publish Now" on a post meant for later.

## Output
The zip of slides, then the caption block, posting time and location. Nothing else unless asked.
