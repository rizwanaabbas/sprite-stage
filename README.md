# Sprite Stage

**One-shot agent skill for original 2D cartoons.**

Drop this repo into an agent. The agent runs one command. Character sheets and a reference video come out as a finished sprite film, with a different voice for each person.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
Forks are welcome.

![Ayzel on the long slide](examples/poster.jpg)

Sample film: [`renders/long-slide.mp4`](renders/long-slide.mp4) (2 min 16 sec). Ayzel, Moiz, Lina, Rafi, and Mama climb and slide one at a time.

## One-shot setup

From the repo root, the agent runs:

```bash
bash setup.sh
```

That installs ffmpeg if needed, creates a Python 3.11–3.13 virtualenv, installs PyTorch, OpenVoice, and MeloTTS, and downloads the public voice checkpoints. When it prints `Sprite Stage is ready`, setup is done. Run it again any time. It skips work that is already finished.

Replay the sample:

```bash
python3 render.py
```

Agents should follow [`SKILL.md`](SKILL.md) and [`AGENTS.md`](AGENTS.md). Do not commit API keys. This repo has none.

A 1-minute film on the included cast is roughly **$0.40–$3** of agent tokens on Claude Haiku, Sonnet, or Cursor Plus, and about **$2–$6** on Codex or Opus if the agent also draws new sprites and revises once. The frame render is free and local. Full table, plus the OpenVoice machine requirements, is below. A free image tool sets the sprite-image line to **$0**.

## Make your own

1. Add a full-body reference image per character in [`characters/`](characters/).
2. Ask the agent for sprite sheets. Prompts are below and in [`examples/prompts.md`](examples/prompts.md).
3. Hand the agent a reference video. It keeps the premise and writes an original script. Names, logos, lyrics, and the source's spoken lines stay out of the prompts and off the screen.
4. The agent renders a new film and mixes voices so each line lasts as long as the mouth is open.

## What is in the box

- `characters/` — reference sheets for the whole cast
- `sprites/` — walk, front, back, talking, sitting, and action sheets, plus magenta pose guides
- `renders/long-slide.mp4` — the sample, picture and voices together
- `render.py` — the film. One climber, one rider, palms, smooth per-frame motion
- `voices.py` — British OpenVoice lines, one tone per character


## Agents

# Sprite Stage

On the first use of this repo, run `bash setup.sh` yourself and wait until it prints `Sprite Stage is ready.`

Do not ask the person to install Python packages, ffmpeg, PyTorch, OpenVoice, or checkpoints. `setup.sh` is the whole setup and it is safe to run again.

Then follow `SKILL.md`.

## Skill

# Sprite Stage

One setup command. Then make an original 2D film from character sheets and a reference video.

## First action

If `.ready` is missing, run this and wait for `Sprite Stage is ready.`

```bash
bash setup.sh
```

Do that yourself. Do not hand the person a list of packages to install. The script is safe to run again.

Picture replay uses system Python. New voices use the virtualenv the script creates.

```bash
python3 render.py
.venv/bin/python voices.py
python3 render.py
```

The finished sample is `renders/long-slide.mp4`.

## What you keep original

A reference video supplies the premise only: the place, the order of actions, and the feeling. Write a new script in the user's own character names. Do not copy the source title, character names, logos, lyrics, or spoken lines into prompts, on-screen text, or the soundtrack.

Wardrobe and voice locks for the included cast are in [characters/CAST.md](characters/CAST.md). Prompt examples are in [examples/prompts.md](examples/prompts.md).

## Make a new film

1. Put each character's reference image in `characters/`. One person per file. Front view, full body, plain background.
2. Generate sprite sheets into `sprites/{name}-{action}.png`. Actions used by the sample renderer: `walk`, `front`, `talking`, `back`, `sitting`. Sheets are four cells side by side on magenta (`#FF00FF`).

## Free sprites

Default to a free image tool. That makes the sprite images **$0**. The agent-token table in [COSTS.md](COSTS.md) still applies.

```bash
python3 scripts/free_sprites.py --provider prompt --name lina --action walk,front,back,talking,sitting
```

Each file in `sprites/prompts/` names the two pictures to attach and the prompt to paste. Sample prompts are in [examples/prompts.md](examples/prompts.md). Save the tool's image as `sprites/{name}-{action}.png`.

Use Gemini only when `GEMINI_API_KEY` is already in the environment. Never ask for the key, never print it, and never write it into the repo.

```bash
python3 scripts/free_sprites.py --provider gemini --name lina --action walk
```

If that model is outside the key's free allowance, stop and use `--provider prompt`.

3. Write original lines in `voices.py`, then `.venv/bin/python voices.py`. Pitch uses the file's real sample rate, then each line is slowed to about two words a second so the mouth can stay open for the whole line.
4. Point `render.py` `NAMES` and `HEIGHT` at the cast. Build the timeline so only one person climbs and only one person slides. Call `python3 render.py`. Mouths open for `duration + 0.2s`. The slide cheer starts when the slide starts.

## Sprite rules that keep clothes intact

- Key only strong magenta: red > 200, green < 100, blue > 200. A loose chroma key punches holes in pink cloth.
- Do not delete a connected region just because it is a face. Keep components of about 1800 pixels or more.
- Walk cells share one timing: long stride, feet together, opposite stride, feet together.
- Side view faces right. Mirror it in the renderer when the character walks left.
- Sit the rider on the chute path and cover the legs with the near lip of the slide. Do not float the body above the chute.

## Voices

OpenVoice V2 shifts tone. MeloTTS speaks the words with a British English base. Children are higher and a little quicker than the adult. Give each person a different target tone. Do not give the whole cast one pitch.

If a line is still shorter than its mouth window, lower the MeloTTS speed or stretch with `atempo` below 1. Do not speed a line up to fill a gap.

## Cost and machine

A 1-minute film is about 300k–500k input tokens and 60k–100k output tokens when the sprites already exist, or about 1.0M–1.5M input and 200k–300k output when you also make sprites and revise once. Dollar figures for Claude, Codex, and Cursor, and the OpenVoice CPU requirements (8 GB RAM, Python 3.11–3.13, no GPU required), are in [COSTS.md](COSTS.md).

## Credits

OpenVoice and MeloTTS are MIT software from MyShell. ffmpeg draws the frames. PyTorch runs the voice models. Checkpoints come from the public `myshell-ai/OpenVoiceV2` model. Full links are in the README.

## Cast

# Cast

Reference images live next to this file. Ignore any labels or color dots on a sheet. The clothes below are the lock.

| Name | Reference | Clothes |
| --- | --- | --- |
| Ayzel | `ayzel.jpg` | Voluminous curly brown hair, no bow. Plain pink short-sleeve dress, white ankle socks, pink sneakers with white toes and laces. |
| Moiz | `moiz.jpg` | Short side-swept brown hair. Plain blue crewneck, blue sweatpants, white sneakers with orange stripes and orange laces. |
| Mama | `mama.jpg` | Shoulder-length wavy brown hair. Light pink open cardigan, white dress, light blue leggings, lavender sneakers with white laces. |
| Lina | `lina.jpg` | Straight black bob, no bow. Teal short-sleeve shirt, cream shorts, white sneakers. |
| Rafi | `rafi.jpg` | Short curly black hair. Green polo with no logo, navy shorts, green sneakers. |
| Baba | `baba.jpg` | Completely bald crown, sides, and back. Beard on the cheeks, jaw, and chin only. Front or back only. Not in the sample film. |
| Granny | `granny.jpg` | Grey hair. |
| Grandpa | `grandpa.jpg` | Grey hair. |
| Auntie | `auntie.jpg` | Adult woman from the sheet. |
| Uncle | `uncle.jpg` | Has hair and a fuller beard than Baba. |
| Chloe | `chloe.jpg` | Child from the sheet. |
| Bittu | `bittu.jpg` | Baby from the sheet. Fully clothed. |

Children stay fully clothed. No logos, letters, or watermarks.

## Voices

British English. Ayzel is a bright high little girl. Moiz is softer and shorter. Lina is calmer and a little lower than Ayzel. Rafi is quicker than Moiz. Mama is a warm medium voice, never a deep adult voice. Baba, if used later, is a friendly medium voice, never deep, and must not sound like Uncle.

## Sample prompts

# Prompts for an agent

Paste one block. The agent already has this skill, so it should run `bash setup.sh` itself if `.ready` is missing.

## 1. Sprite sheet from a reference character

```text
Use the Sprite Stage skill.

Create a 4-cell sprite sheet for Lina from characters/lina.jpg.
Action: walk, side view, facing right.
Cells left to right:
1. long stride, both feet down
2. feet together, back foot lifted
3. opposite long stride
4. feet together, the other foot lifted
Same clothes as the reference. Fully clothed. No logos, letters, or watermarks.
Background of every cell is flat magenta #FF00FF.
Save sprites/lina-walk.png, four equal cells in one row.

Then make sprites/lina-front.png, sprites/lina-back.png, sprites/lina-talking.png,
and sprites/lina-sitting.png the same way. Front shows the face. Back shows the
back of the head and no face. Talking is a front view with the mouth open.
Sitting is a side view in the chute pose.
```

## 2. A reference video becomes an original 2D film

```text
Use the Sprite Stage skill.

Watch this reference video and keep only the premise:
https://www.youtube.com/watch?v=9qShcQMq1cA

Make a new 2 minute 2D sprite film with the characters in characters/.
Mama leads. The children climb the stairs one at a time, then slide one at a time.
Keep the slide fast, but keep each spoken line slow enough that the mouth
is open for the whole line.

Write original lines. Do not copy names, logos, lyrics, or the spoken script
from the reference. Do not put words on screen.
Use the included wardrobe. Add palm trees. Render renders/long-slide.mp4
and mix the OpenVoice lines onto the same pictures.
```

## 3. Free sprite sheets, no image bill

```text
Use the Sprite Stage skill.

Make free sprite sheets for Lina. Do not spend money on an image API.
Run:
python3 scripts/free_sprites.py --provider prompt --name lina --action walk,front,back,talking,sitting

Then send each prompt file in sprites/prompts/ to a free image tool, with the
two attached pictures named in that file. Save the results as
sprites/lina-walk.png, sprites/lina-front.png, sprites/lina-back.png,
sprites/lina-talking.png, and sprites/lina-sitting.png.
Magenta background #FF00FF. Four equal cells. Same clothes as characters/lina.jpg.
```

## 4. Sample prompt for any free image tool

Attach `characters/lina.jpg`, then `sprites/pose-guide.png`, then paste:

```text
IMAGE 1 is the identity reference for Lina. IMAGE 2 is a four-cell pose map.
Ignore every word, label, color dot, and extra pose on IMAGE 1.
Paint a new sprite sheet of that same character only. Copy the clothes and hair from IMAGE 1.
Fully clothed. No logos, letters, or watermarks.
ONE wide image, exactly four equal cells in a single horizontal row, matching IMAGE 2 cell for cell.
Side view, facing right, walking in place.
Cell 1 long stride, both feet down.
Cell 2 feet together, one foot lifted.
Cell 3 the opposite long stride, both feet down.
Cell 4 feet together, the other foot lifted.
Same height and the same foot line in every cell.
Background outside the figure is flat pure magenta #FF00FF.
No white frame, no ground line, no text, no numbers, no grid, no second person.
```

Swap the pose guide and the cell lines for the other actions:

- Front: attach `sprites/pose-guide-front.png`. Both eyes visible. Same walk beat.
- Back: attach `sprites/pose-guide-back.png`. Back of the head, no face.
- Talking: attach `sprites/pose-guide-talking.png`. Body still. Mouth closed, a little open, wide open, a little open.
- Sitting: attach `sprites/pose-guide-sitting.png`. Already sitting, fully clothed, four small shifts.

## 5. Gemini, only if the user already has a key

```text
Use the Sprite Stage skill.

The user has set GEMINI_API_KEY in the environment. Do not ask them to paste it.
Do not write it into any file.
Run:
python3 scripts/free_sprites.py --provider gemini --name lina --action walk,front,back,talking,sitting

If the call says the image model is not on the free tier, stop and switch to the
free prompt pack in section 3. Sprite images from that path cost $0.
```

## 6. A new story with the same cast

```text
Use the Sprite Stage skill.

New film in its own folder. Ayzel, Moiz, Lina, Rafi, and Mama have a picnic
and then fly a kite. Use characters/ as identity references and the sprite
sheets already in sprites/.
One action at a time. Original dialogue. British OpenVoice lines, each
character a different pitch. Mouth open only while that character speaks.
No logos, no on-screen words, no copied song lyrics.
```

## Costs and OpenVoice requirements

# Cost of a 1-minute film, and what OpenVoice needs

Prices below are public list rates checked on 26 October 2026. A real bill moves with retries, image generation, and how long the agent keeps the repo in context. Rendering the frames is local and costs nothing extra.

## Agent tokens for 1 minute

These counts are the language-model work: reading the skill, writing the timeline, writing the lines, and one or two picture fixes. Sprite images are a separate line in the table under this one. A free image tool sets that line to $0.

| Film | Input tokens | Output tokens |
| --- | ---: | ---: |
| Cast and sprite sheets already in the repo. New 1-minute story. | 300,000–500,000 | 60,000–100,000 |
| Reference video, new sprite sheets, one revision of motion and sync | 1,000,000–1,500,000 | 200,000–300,000 |

The dollar table uses the middle of each range: **400k input / 80k output** for a film on the existing cast, and **1.2M input / 250k output** when the agent also builds sprites and revises once.

## Rough cost

| Where you run the agent | Existing cast, 1 minute | New sprites, free image tool | New sprites, paid Gemini image API |
| --- | ---: | ---: | ---: |
| Claude Haiku 5.5 (API, prompts over 100k tokens) | $0.40 | $1.20 | $2.70 |
| Claude Sonnet 5.5 (API) | $1.60 | $4.90 | $6.40 |
| Claude Opus 5.5 (API) | $3.20 | $9.80 | $11.30 |
| Codex, `gpt-5.3-codex` API | $1.80 | $5.60 | $7.10 |
| Codex inside ChatGPT Plus ($20/month) | inside the plan | inside the plan for a single film | plan plus about $1.50 of images |
| Cursor Plus ($8/month), Grok 4.7 | about $1.30 of the weekly pool | about $3.90 of the weekly pool | about $3.90 of the pool plus $1.50 of images |
| Cursor Premium ($30/month), Claude or Codex | same as that model's API row, from prepaid credit | same as that model's API row | API row plus about $1.50 of images |

The free-tool column is the agent only. `scripts/free_sprites.py --provider prompt` writes the prompts, and a free image tool paints the sheets, so the images add **$0**.

The paid column adds about **$1.50** for 25 sheets (5 people × walk, front, back, talking, sitting). Gemini 3.1 Flash Image list price is about $0.045–$0.067 per image. Source: [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing). Those image models show no free API tier. A key in `GEMINI_API_KEY` is billed unless that project includes the model. Google AI Studio itself can still be used with the same sample prompts at no charge when the project is on the free studio allowance.

Rates used:

- Claude Haiku 5.5, prompts over 100,000 tokens: $0.50 / $2.50 per million input / output tokens. Shorter prompts are $0.10 / $0.50. Source: [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing).
- Claude Sonnet 5.5: $2 / $10. Claude Opus 5.5: $4 / $20. Same page.
- Codex `gpt-5.3-codex`: $1.75 / $14 per million input / output tokens. Source: [OpenAI API pricing](https://developers.openai.com/api/docs/pricing). ChatGPT Plus is $20/month and includes Codex. Source: [Codex pricing](https://developers.openai.com/codex/pricing/).
- Cursor Plus is $8/month and spends the weekly pool on Cursor models. Grok 4.7 list rate is $2 input and $6 output per million tokens. Premium is $30/month and bills Claude or Codex at their API list price from prepaid credit. Source: [Cursor models and pricing](https://cursor.com/docs/models-and-pricing).

A tidy 1-minute film on the included cast usually fits in Cursor Plus or ChatGPT Plus. Opus, or a long retry loop, is the path that climbs toward $10.

## OpenVoice system requirements

`bash setup.sh` installs OpenVoice V2 plus MeloTTS. Voices run on the CPU. A GPU is optional.

| | Minimum | Comfortable |
| --- | --- | --- |
| OS | macOS 13 or Ubuntu 22.04 | Apple Silicon Mac, or Linux |
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| GPU | none | optional NVIDIA with 4 GB VRAM, or Apple MPS |
| Free disk | 8 GB | 15 GB |
| Python | 3.11, 3.12, or 3.13 | 3.11 |
| Also | ffmpeg, git, curl | same |

The converter checkpoint is about 125 MB. One MeloTTS language plus the English BERT weights adds a few hundred megabytes. The PyTorch virtualenv is the large part, so leave several gigabytes free.

On CPU, a minute of short preschool lines finishes in about a minute after the models have loaded the first time. The first line also downloads the English MeloTTS checkpoint and BERT. CUDA runs the same voices with about 1.3 GB of VRAM. Official install notes: [OpenVoice usage](https://github.com/myshell-ai/OpenVoice/blob/main/docs/USAGE.md).

## Where to post

# Where Sprite Stage can be seen

These are the places that actually surface a new agent-skill repo. The articles next to this file are written for them. Post each one once, in your own account. Do not cross-post the same text on the same day.

| Place | File | Why it gets seen |
| --- | --- | --- |
| Dev.to | [devto.md](devto.md) | Tags `ai`, `opensource`, `python` land in the daily feed. Set `published: true` in the front matter, then publish from your Dev.to account. |
| Hashnode | [devto.md](devto.md) | Same essay. Add the GitHub repo as the canonical URL so search engines keep one copy. |
| Hacker News | [show-hn.md](show-hn.md) | Show HN posts that include a setup command and a real sample get comments. Title is already in the file. https://news.ycombinator.com/submit |
| Reddit r/cursor | [reddit.md](reddit.md) | People there install skills. |
| Reddit r/LocalLLaMA | [reddit.md](reddit.md) | OpenVoice on CPU is the hook. Post a day after the Cursor post, not the same hour. |
| Reddit r/SideProject | [show-hn.md](show-hn.md) | Short version. Lead with the film, then the link. |
| Indie Hackers | [guest-essay.md](guest-essay.md) | Product thread. Cost table is the useful part. |
| AI newsletters | [guest-essay.md](guest-essay.md) | Send the essay as the draft, not a "please feature me" note. Ben's Bites, The Neuron, and TLDR AI take short tools pieces. |

## Already published from this repo

- The README, skill, sample film, and these drafts are on https://github.com/rizwanaabbas/sprite-stage
- GitHub topics: `ai-agents`, `cursor`, `agent-skill`, `2d-animation`, `openvoice`

Guest posts on Dev.to, Hacker News, and Reddit have to come from your login. This repo does not contain an account token, and it should stay that way.

## Guest article for Dev.to and Hashnode

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

## Show HN

# Show HN: Sprite Stage — an agent skill that turns a reference video into an original 2D cartoon

https://github.com/rizwanaabbas/sprite-stage

I kept losing character clothes and voice sync when I asked an agent to "make a cartoon of this video." The agent would copy names, drift the wardrobe, and finish a sentence while the mouth was still opening.

Sprite Stage is one MIT repo an agent can set up with `bash setup.sh`. A reference video supplies the premise only. Character sheets supply the cast. Sprite sheets are four cells on magenta, keyed tightly enough that pink clothes survive. OpenVoice V2 plus MeloTTS speak, one tone per person, stretched so the line lasts as long as the mouth is open. ffmpeg draws the frames on CPU.

The sample is a 2 minute 16 second film, `renders/long-slide.mp4`, of five original characters taking turns on a long slide.

A free image tool makes the new sprite sheets $0. The agent-token cost of a 1-minute film on an existing cast is roughly $0.40 on Claude Haiku, $1.60 on Sonnet, $1.80 on the Codex API, or about $1.30 of a Cursor Plus weekly pool. Figures and the OpenVoice machine notes (8 GB RAM, Python 3.11–3.13, GPU optional) are in `COSTS.md`.

I would like feedback on the sprite key and on whether the one-shot setup survives a clean machine.

## Reddit

# r/cursor and r/LocalLLaMA

**Title:** I packed a 2D cartoon pipeline into one agent skill (MIT, one setup command)

An agent can clone https://github.com/rizwanaabbas/sprite-stage and run `bash setup.sh`. After that it can take a reference video as a premise, keep your own character sheets, and render an original sprite film.

What is included:

- The sample film (`renders/long-slide.mp4`, 2:16)
- Reference sheets and the sprite PNGs
- Sample prompts for a free image tool, so new sheets can cost $0
- Optional Gemini only if `GEMINI_API_KEY` is already in the environment. The key is not in the repo
- OpenVoice voices, CPU is enough (8 GB RAM, Python 3.11–3.13)
- A cost table for a 1-minute film on Claude, Codex, and Cursor

The reference video is not copied. New names, new lines, no logos on screen.

If you try the setup on a clean machine, I want to know where it stops.

## Newsletter guest essay

# Guest essay: the cheap part of a cartoon is the picture

*For an AI newsletter or a tools column. About 800 words. Suggested subject: "A 1-minute 2D cartoon for the price of a coffee, if the sprites are free."*

Editors keep asking what an agent is actually for, besides a pull request. One honest answer is a film a preschooler can watch, made from a reference video the family already loves and from characters that belong to the family.

The trap is the reference. Hand an agent a popular episode and it will reach for the names, the song, and the clothes. Those are not yours to ship. The useful split is smaller. The video lends the premise: a long slide, a picnic, a kite. The character sheet lends the person. The script is written fresh.

[Sprite Stage](https://github.com/rizwanaabbas/sprite-stage) is an MIT skill built around that split. An agent clones it and runs `bash setup.sh`. One command installs the voice stack and checks for ffmpeg. The sample in the repo is two minutes and sixteen seconds. Five original characters climb a slide one at a time and slide one at a time. Palm trees sit at the edges. Each line lasts about as long as that character's mouth is open.

The pictures are sprites, not a video model. A video model bills every second and still changes a dress between shots. A sprite sheet is four cells on flat magenta. The loader deletes only real magenta, so a pink dress stays pink. Walks share one beat. The renderer is a few hundred lines of Python and ffmpeg. A minute of 720p frames is a local CPU job.

Voices are OpenVoice V2 and MeloTTS, both MIT, from MyShell. They run on CPU. Eight gigabytes of RAM and Python 3.11, 3.12, or 3.13 are enough. A GPU is optional. The first run downloads the checkpoints. After that, a minute of short lines takes about a minute.

The bill people ask about is the agent, not the frames. A 1-minute film on sprites you already have is a few hundred thousand tokens. On public list prices in late October 2026, that is about $0.40 on Claude Haiku, $1.60 on Claude Sonnet, $1.80 on the Codex API, or a couple of dollars of a Cursor Plus weekly pool. Drawing new sheets and revising the motion once pushes the agent toward $1–$10 depending on the model.

The image line is the one you can zero out. A free image tool, pointed at the sample prompts in the repo, adds $0. The paid Gemini image API is about $1.50 for 25 sheets, and those image models are not on the free API tier. Google AI Studio can still run the same prompts when the project is on the free studio allowance. The repo never stores an API key.

That is the shape I want other agent skills to copy. One setup command. A worked sample in the repo. A cost table that separates the language model from the pictures. A license that lets the next person delete the cast and put their own family in.

The sample film is here: https://github.com/rizwanaabbas/sprite-stage/blob/main/renders/long-slide.mp4

— rizwanaabbas

## Credits

This project stands on tools you can fork:

- [OpenVoice](https://github.com/myshell-ai/OpenVoice) by MyShell, MIT. Tone color for each character.
- [MeloTTS](https://github.com/myshell-ai/MeloTTS) by MyShell, MIT. The spoken words.
- [OpenVoice V2 checkpoints](https://huggingface.co/myshell-ai/OpenVoiceV2) on Hugging Face.
- [PyTorch](https://pytorch.org/) for the voice models.
- [ffmpeg](https://ffmpeg.org/) for sprite keys, frames, and the soundtrack mix.

The picture pipeline is original. Sprite sheets are generated from the reference images in `characters/`, cut out with a strict magenta key so pink clothes stay intact.

The sample story takes its premise from a public long-slide video, [youtube.com/watch?v=9qShcQMq1cA](https://www.youtube.com/watch?v=9qShcQMq1cA). The script, names, clothes, and pictures here are original. This project is not affiliated with that video or its rightsholders.

## License

MIT. Fork it, recast it, and ship your own films. See [LICENSE](LICENSE).
OpenVoice and MeloTTS keep their own MIT notices when `setup.sh` clones them.
