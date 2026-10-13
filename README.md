# instagram-agent-skills

15 Claude skills that run the @warmnode Instagram ("Warmnode · Deep Talks": rent a friend, free, just talk ☕) for someone with almost no time. They turn the owner's own café photos and videos into finished, ready-to-upload posts.

## The look: espresso & chai
Every post uses the owner's own café, coffee and food photos as the background, graded dark and warm, with cream serif text and a chai-amber accent. The renderer lives in `_shared/warmnode.py` and is copied into each skill that makes files (`_shared/sync.sh` keeps the copies in step).

## Skills
| Command | What it does |
|---|---|
| `/ig-drive` 🆕 | Pulls photos and clips from the Drive folder "warmnode data", picks the best (no faces), reads café names, moves used files to "used" |
| `/ig-tracker` 🆕 | Keeps the "warmnode tracker" Google Sheet: every post and its numbers, plus a 3-line "what's working" summary |
| `/ig-plan` | Plans the week: what to post, when, and the daily routine |
| `/ig-carousel` | Writes a carousel **and renders the 1080x1350 slides** from your photos |
| `/ig-reel` | Writes a reel **and renders the 1080x1920 MP4** from your clips and photos |
| `/ig-story` | Story images plus the exact sticker to add |
| `/ig-caption` | Caption with a strong first line, question and hashtags |
| `/ig-viral` | High-potential post ideas with hooks |
| `/ig-profile` | Scores your profile out of 100 and rewrites what's weak |
| `/ig-comment` | Real comments to leave on bigger accounts |
| `/ig-reply` | Replies to comments on your posts |
| `/ig-dm` | Welcome DMs, collab pitches and follow-ups |
| `/ig-repurpose` | One post into a reel, carousel, stories, Threads, TikTok, Shorts |
| `/ig-human` | Rewrites anything that sounds like AI |
| `/ig-audit` | Reads your insights and tells you what to do next |

## The week
1. **Monday (automatic):** a scheduled task runs `/ig-plan` → `/ig-drive` → `/ig-carousel` ×2 → `/ig-reel` ×2 → `/ig-story`, and delivers one zip + posting guide.
2. **Monday, 10-15 minutes (you):** schedule the carousels in Meta Business Suite; add a soft song to the reels (Audio tab) and schedule them.
3. **Daily, ~10 minutes:** post the day's story from the Instagram app; `/ig-reply` for comments; `/ig-comment` on 5-10 bigger accounts.
4. **Tuesday night:** send insights screenshots → `/ig-audit` + `/ig-tracker`.

## Install in Claude
Each folder that starts with `ig-` is one skill. Zip each folder (the zip should contain the folder, with `SKILL.md` inside it) and upload it in Claude's settings under Skills. Re-upload a skill after it changes here. `_shared/` is not a skill; don't upload it.

## Edit your niche
Every `SKILL.md` has an "Account context" block at the top. Change it there if your bio or niche changes, or just tell Claude in the chat.

## Rules these skills follow
You post and schedule everything yourself. No bots, auto-comments or mass DMs: Instagram restricts accounts for that. Faceless: no recognisable faces in any post.
