---
name: sprite-stage
description: >-
  Builds original 2D sprite cartoons from character reference sheets and a
  reference video. Use when someone asks for a 2D cartoon, sprite film,
  character animation, OpenVoice preschool voices, or to set up Sprite Stage.
---

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
