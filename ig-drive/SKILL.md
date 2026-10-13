---
name: ig-drive
description: Pull the owner's café, coffee and food photos and videos for @warmnode from the Google Drive folder "warmnode data", pick the best ones for a post (no faces, readable, right mood), read café names from the location stickers, and move used files into a "used" subfolder so nothing repeats. Use for "/ig-drive", "use my Drive photos", "pick photos", "new photos added", or whenever another /ig-* skill needs media.
---

# /ig-drive - the owner's photo library, sorted

## Account context (@warmnode)
- The owner visits cafés and restaurants (Lahore, Aberdeen and wherever they go next) and drops photos and short videos into the Google Drive folder **"warmnode data"** (account pixelerpoint@gmail.com). Many are Snapchat exports: 1242x2208 portrait, with a location sticker near the bottom (e.g. "POLO LOUNGE · Lahore, Pakistan").
- Faceless account: never pick media where a person's face is recognisable. Hands, cups, tables, interiors, streets are perfect.
- The owner is not technical: never ask them to rename or sort files.

## Steps
1. **Find the folder.** Google Drive `search_files` with `title contains 'warmnode data' and mimeType = 'application/vnd.google-apps.folder'`. Note its ID. Inside it, also find (or create, see step 7) the subfolder **"used"**.
2. **List the files.** `search_files` with `parentId = '<folder id>'`, `excludeContentSnippets: true`, `pageSize: 100`, following `nextPageToken` until it runs out. Large results are saved to a file: read them with `jq` (id, title, mimeType, fileSize). Files in "used" have a different parent, so they're excluded automatically.
3. **Download.** `download_file_content` per file, in parallel batches of about 10. Big results land in a saved JSON file: decode with `jq -r .content FILE | base64 -d > "<dir>/<title>"`. Start with all images; for videos, take the smaller clips (under ~3 MB, 5-10 s) and only as many as the reels need.
4. **Look before choosing.** Build a numbered contact sheet (PIL, ~220x300 thumbs, 6 per row) and view it. For videos, grab 3 frames each (30%, 50%, 80%) into a sheet. Note per item: mood (cosy, moody, foggy, night, chai, chess, cards, latte art, food), any face (skip), any baked-in text, clock or sticker (crop around it with `y`/`zoom`, or skip), and the place name if a location sticker shows it.
5. **Pick for the job.** Match mood to message: chess/cards + chai → questions; empty chairs, fog, night streets → loneliness; one cup in the dark → confessions; busy warm interiors → friendship; latte art and food → café diaries. Prefer variety across a week: different cafés, light and dark, top-down and wide.
6. **Hand over** a short list to the calling skill: local path, Drive file ID, mood, place (only if read from the sticker or told by the owner, never guessed), suggested `y`/`zoom`.
7. **Mark as used** once the week's content is built and delivered:
   - If "used" doesn't exist: `create_file` with title `used`, `contentMimeType`/type `application/vnd.google-apps.folder`, `parentId` = warmnode data folder.
   - Move each used file: `update_file` with `fileId` and `parentId` = the "used" folder ID. Nothing is deleted; say in one line how many files moved.
8. **Reuse rule.** A "used" photo may come back after 6 weeks, recropped or in a different format (a carousel photo can become a reel segment). When the main folder runs low (fewer than ~15 unused photos), tell the owner in one line to add new café photos.

## Output
For the owner: one line ("Picked 8 photos and 2 clips from your Drive; 23 photos still unused."). For other skills: the pick list from step 6.
