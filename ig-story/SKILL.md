---
name: ig-story
description: Make Instagram Stories for @warmnode - ready 1080x1920 story images from the owner's café photos in the espresso & chai look, plus the exact sticker (poll, question box, slider) and its wording. Use for "/ig-story", "story ideas", "make today's story", or "what should I put on my story".
---

# /ig-story - stories that start conversations

## Account context (@warmnode)
- Name field: "Warmnode · Deep Talks". Bio: "Rent a friend (free, just talk) ☕ / Deep questions for overthinkers 18–30 / New one daily · answer in the comments"
- Voice: warm, calm, honest, a friend who listens. English, light Roman Urdu when natural.
- Audience: 18-30 overthinkers who crave real conversation. Pakistan.
- Faceless. The owner has almost no time and is not technical: give them a finished image and one sticker instruction.
- If the user says their niche changed, follow what they say now.

## Why stories matter here
Stories are where followers turn into friends. Sticker replies and DMs tell Instagram people care about this account, which pushes its posts to them more.

## Steps
1. **Which day?** If the user says "today's story" and a weekly plan exists (from /ig-plan or the tracker), use that day's idea. Otherwise plan 1-3 frames, mixing:
   - **Question box:** "Ask me anything you can't ask your friends" / "Tell me a small confession, anonymously".
   - **Poll:** a light either/or ("Do you overthink texts? Yes / Always").
   - **Emoji slider:** "How heavy is your mind today? ☕"
   - **Share-back:** reshare the latest post with one line.
2. **Photos.** Attached photos → Drive "warmnode data" via /ig-drive → plain espresso background.
3. **Render.** Spec: `{"media_dir": "...", "frames": [{"photo": "file.jpg", "text": "Do you overthink a text before sending it?", "name": "Thu_story"}]}` then `python3 scripts/warmnode.py story spec.json out_dir/` (path relative to this skill folder). Text sits in the top third; the middle-lower area stays clear for the sticker.
   - Never print sticker instructions on the image itself; followers would see them.
4. **Tell the owner exactly what to do**, in plain words: open Instagram app → + → Story → pick the image → sticker icon → which sticker → the exact wording (and poll options) → place it in the empty middle area → Your story.
5. Stories can't carry poll/question stickers when scheduled from Business Suite, so they're posted from the app on the day. Keep it under a minute of work.
6. Add one follow-up idea: how to answer the question-box replies next day (anonymously, warmly), and which Highlight to save it in ("Deep talks", "Ask me").

## Output
The image(s), then numbered steps with the sticker wording. Copy-ready.
