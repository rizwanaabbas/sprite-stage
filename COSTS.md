# Cost of a 1-minute film, and what OpenVoice needs

Prices below are public list rates checked on 26 October 2026. A real bill moves with retries, image generation, and how long the agent keeps the repo in context. Rendering the frames is local and costs nothing extra.

## Agent tokens for 1 minute

These counts are the language-model work: reading the skill, writing the timeline, writing the lines, and one or two picture fixes. They do not include sprite-image calls. A new cast of sprite sheets is a separate image-model bill.

| Film | Input tokens | Output tokens |
| --- | ---: | ---: |
| Cast and sprite sheets already in the repo. New 1-minute story. | 300,000–500,000 | 60,000–100,000 |
| Reference video, new sprite sheets, one revision of motion and sync | 1,000,000–1,500,000 | 200,000–300,000 |

The dollar table uses the middle of each range: **400k input / 80k output** for a film on the existing cast, and **1.2M input / 250k output** when the agent also builds sprites and revises once.

## Rough cost

| Where you run the agent | Existing cast, 1 minute | New sprites plus one revision |
| --- | ---: | ---: |
| Claude Haiku 5.5 (API, prompts over 100k tokens) | $0.40 | $1.20 |
| Claude Sonnet 5.5 (API) | $1.60 | $4.90 |
| Claude Opus 5.5 (API) | $3.20 | $9.80 |
| Codex, `gpt-5.3-codex` API | $1.80 | $5.60 |
| Codex inside ChatGPT Plus ($20/month) | inside the plan | inside the plan for a single film |
| Cursor Plus ($8/month), Grok 4.7 | about $1.30 of the weekly pool | about $3.90 of the weekly pool |
| Cursor Premium ($30/month), Claude or Codex | same as that model's API row, from prepaid credit | same as that model's API row |

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
