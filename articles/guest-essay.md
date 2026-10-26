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
