# Cost of a 1-minute film, and what OpenVoice needs

Prices below are public list rates checked on 26 October 2026. A real bill moves with retries, image generation, and how long the agent keeps the repo in context. Rendering the frames is local and costs nothing extra.

## Agent tokens for 1 minute

These counts are the language-model work: reading the skill, writing the timeline, writing the lines, and one or two picture fixes. Sprite images are a separate line in the table under this one. A free image tool sets that line to $0.

| Film | Input tokens | Output tokens |
| --- | ---: | ---: |
| Cast and sprite sheets already in the repo. New 1-minute story. | 300,000–500,000 | 60,000–100,000 |
| Reference video, new sprite sheets, one revision of motion and sync | 1,000,000–1,500,000 | 200,000–300,000 |

The dollar table uses the middle of each range: **400k input / 80k output** for a film on the existing cast, and **1.2M input / 250k output** when the agent also builds sprites and revises once.

## The route that stays at $0

Use [OpenCode](https://opencode.ai) and pick a model whose price is **Free**. The OpenCode app is free. Those models are $0 per token and work without an account. Pair them with a free image tool and the local renderer:

1. In OpenCode, stay on a Free model for the whole film. On 26 October 2026 the free list includes Big Pickle, GLM-5.3-Flash Free, DeepSeek V4.1 Flash Free, Beam Free, Flint 40B Free, MiMo-V2.6-Flash Free, Nemotron 3 Ultra Free, Nemotron 3.5 Lightning Free, and Nemotron 3.5 Super VL Free. The list is limited-time and each free model has a daily request quota.
2. Make the sheets with `python3 scripts/free_sprites.py --provider prompt`, then a free image tool. Google AI Studio on its free allowance is the other $0 picture path.
3. Run `bash setup.sh`, then `python3 render.py`. Frames and OpenVoice voices stay on your machine.

That combination is **$0** while the film fits the daily free-model quota. If the quota runs out, wait until the next day. Switching to Claude, Codex, Cursor, or OpenCode Zen starts that provider's bill. OpenCode Go is a separate $10/month plan.

## Rough cost

| Where you run the agent | Existing cast, 1 minute | New sprites, free image tool | New sprites, paid Gemini image API |
| --- | ---: | ---: | ---: |
| OpenCode, a model marked Free | $0 | $0 | about $1.50 of images |
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
- OpenCode the app is free, and models marked Free are $0. They work without an account, with a daily request quota, and the free lineup changes. Source: [OpenCode](https://opencode.ai/) and the model table on [OpenCode Zen](https://opencode.ai/docs/zen/).

The **$0** route is OpenCode on a Free model, a free image tool, and the local frame render. A tidy 1-minute film on the included cast also fits in Cursor Plus or ChatGPT Plus. Opus, or a long retry loop, is the path that climbs toward $10.

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
