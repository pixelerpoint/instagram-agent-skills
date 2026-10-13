---
name: ig-carousel
description: Build a finished Instagram carousel for @warmnode - cover that earns the swipe, slide copy, caption, and ready-to-upload 1080x1350 PNG slides. Use for "/ig-carousel", "make a carousel", "make a post", or any request for a swipe post.
---

# /ig-carousel - finished carousel, ready to upload

## Account context (@warmnode)
- Bio: "Rent a friend for coffee & deep talks."
- Voice: a warm, calm friend across the coffee table. Honest, gentle, a little poetic, never preachy or clinical.
- Audience: 18-30, overthinkers, people who feel lonely in a crowd and crave real conversation. English, light Roman Urdu is fine when it feels natural.
- Pillars: (1) deep questions / conversation starters, (2) quiet truths about loneliness and friendship, (3) coffee-table confessions and mini-stories, (4) how to be a better friend and listener.
- The owner has almost no time. Deliver finished work, never homework. They should only need to download and post.
- If the user says their niche or bio changed, follow what they say now.

## Steps
1. If no topic is given, pick one from the pillars yourself (rotate; favour deep questions and quiet truths, they save and share best). Don't ask.
2. Write 6-8 slides:
   - Slide 1 (cover): one line, max 9 words, that creates a curiosity gap or a "this is me" feeling. E.g. "The friends who check on you are rare."
   - Slides 2 to n-1: one idea per slide, max 30 words each. Short lines. Each slide should make the next swipe feel necessary.
   - Last slide: a soft call to action: save it, send it to the friend it reminds you of, or answer a question in the comments. Include "@warmnode".
3. Render the slides:
   - Save slide text as JSON: `{"slides": [{"title": "...", "body": "..."}, ...]}`. `title` is optional; use it for the cover and short headers.
   - Run `python3 scripts/make_carousel.py slides.json out/` (path relative to this skill folder). It writes slide_01.png ... at 1080x1350 in the warmnode style.
   - Look at at least the cover and one inner slide to check nothing overflows; shorten text and re-render if it does.
   - Give the user the PNG files.
4. Write the caption (see /ig-caption rules): hook line, 2-4 short lines, a question for comments, 3-5 hashtags.
5. Give a posting tip in one line (best time: 8-10 pm Pakistan time on weekdays unless their insights say otherwise).

## Output
The slide images, then the caption in a copy-ready block. Nothing else unless asked.
