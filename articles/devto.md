---
title: "One command, then an original 2D cartoon from a reference video"
published: false
description: "Sprite Stage is an MIT agent skill. A reference video supplies the premise. Your character sheets supply the cast. OpenVoice speaks. ffmpeg draws the frames."
tags: ai, opensource, python, tutorial
canonical_url: https://github.com/rizwanaabbas/sprite-stage
---

# One command, then an original 2D cartoon

Agents are good at writing code and bad at staying inside a character's clothes. Sprite Stage is a small open-source skill that keeps both jobs in one place.

The repo is [github.com/rizwanaabbas/sprite-stage](https://github.com/rizwanaabbas/sprite-stage). It is MIT. Forks are the point.

## What the agent actually does

You drop the repo into Cursor, Codex, or Claude. The agent reads `SKILL.md` and `AGENTS.md`, then runs:

```bash
bash setup.sh
```

That is the whole setup. It installs ffmpeg if it is missing, makes a Python 3.11–3.13 virtualenv, and installs OpenVoice V2 plus MeloTTS. The sample film is already rendered, so you can watch `renders/long-slide.mp4` before any of that finishes.

A new film has four pieces:

1. A full-body reference image per character.
2. Four-cell sprite sheets on flat magenta `#FF00FF`.
3. Original lines, one voice per person.
4. A timeline where one person climbs and one person slides.

The reference video is a premise, not a script. The sample takes the idea of a very long slide from a public video and writes new lines, new clothes, and new names. Logos, lyrics, and the source's spoken words stay out of the prompts and off the screen.

## Why the sprites survive pink clothes

A loose chroma key eats pink dresses. The loader only clears pixels that are strongly magenta: red above 200, green under 100, blue above 200. Faces stay, because connected regions of about 1800 pixels or more are kept. Walk cycles share one beat, so a group can cross the frame together.

Sample prompts, including a no-key pack for any free image tool, are in `examples/prompts.md`.

```bash
python3 scripts/free_sprites.py --provider prompt --name lina --action walk,front,back,talking,sitting
```

Each text file names the two pictures to attach. The character photo is the identity. The pose guide is the timing. If you already have `GEMINI_API_KEY` in the environment, the same script can call Gemini. The key is never written into the repo. If that image model is outside the key's allowance, switch back to the prompt pack. Those images cost $0.

## What a minute costs

Agent tokens and sprite images are separate. A 1-minute film on sprites you already have is about 300k–500k input tokens and 60k–100k output tokens. Building new sheets and revising once is closer to 1.0M–1.5M input and 200k–300k output.

With a free image tool, add $0 for the pictures. On the paid Gemini image API, 25 sheets (5 people, 5 actions) is about $1.50 on top. The frame render is local. OpenVoice runs on CPU: 8 GB of RAM, Python 3.11–3.13, no GPU required. The full table is `COSTS.md`.

| Agent | Existing cast | New sprites, free image tool |
| --- | ---: | ---: |
| Claude Haiku 5.5 | $0.40 | $1.20 |
| Claude Sonnet 5.5 | $1.60 | $4.90 |
| Codex API | $1.80 | $5.60 |
| Cursor Plus, Grok 4.7 | about $1.30 of the weekly pool | about $3.90 of the weekly pool |

List prices as of 26 October 2026. A long retry loop costs more. One tidy film fits in Cursor Plus or ChatGPT Plus.

## Credits

OpenVoice and MeloTTS are MIT projects from MyShell. ffmpeg cuts the sprites out and encodes the film. PyTorch runs the voices. The picture pipeline in this repo is original.

If you fork it, recast the `characters/` folder and keep the magenta sheets. That is the whole product.
