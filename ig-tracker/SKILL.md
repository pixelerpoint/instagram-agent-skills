---
name: ig-tracker
description: Keep the @warmnode post tracker - a Google Sheet "warmnode tracker" in the Drive folder "warmnode data" logging every post (date, time, format, hook, pillar, photos, café) and its results (reach, likes, comments, saves, shares, follows) - and summarise what works. Use for "/ig-tracker", "log this post", "update my tracker", "add my numbers", or after /ig-plan, scheduling, or sharing insights screenshots.
---

# /ig-tracker - every post, and what it did

## Account context (@warmnode)
- Instagram @warmnode, Creator account, started October 2026. Pakistan time (PKT).
- Pillars: deep questions, quiet truths, confessions, better friend/listener, café diaries.
- The owner is not technical: they send screenshots; you do the typing.

## The sheet
Google Sheet **"warmnode tracker"** inside the Drive folder **"warmnode data"**. Columns, in this order:
`Date | Day | Time (PKT) | Format | Hook / cover line | Pillar | Café / place | Photos & clips used | Status | Reach | Likes | Comments | Saves | Shares | Follows | Notes`
- Format: Carousel, Reel, Story. Status: planned → scheduled → live.
- One row per post. Stories only when they carried a sticker worth tracking (log replies in Notes).

## How to update (the Drive connector can't edit cells in place)
1. Find the current sheet: `search_files` `title = 'warmnode tracker'` with parent = the warmnode data folder. Read it with `read_file_content`.
2. Merge your changes into the rows in memory: add planned rows after /ig-plan, flip to scheduled once the owner confirms, fill numbers from insights screenshots.
3. Write the full table as CSV and `create_file` it with `title: "warmnode tracker"`, `textContent: <csv>`, `contentMimeType: "text/csv"`, `parentId: <warmnode data id>`. It converts to a Google Sheet.
4. Keep the old version: `update_file` it with `title: "warmnode tracker (old YYYY-MM-DD)"` and `parentId` = the "used" folder (create "used" as in /ig-drive if missing). So there's only ever one live "warmnode tracker".
5. If Drive isn't connected, give the CSV as a file instead and say so in one line.

## Reading the numbers
When insights screenshots arrive: read each post's Reach, Likes, Comments, Saves, Shares, Follows (and for reels, average watch time in Notes). Small accounts swing a lot: compare posts to each other, not to big creators.

## Summary to give after every update (3 lines, plain words)
- Best post this week and why (rank by saves + shares, then follows).
- Which pillar and format are winning so far (averages, once there are 6+ posts).
- One thing to repeat next week. Hand this to /ig-audit and /ig-plan when they run.

## Output
Link to the updated sheet + the 3-line summary.
