# Show HN: Sprite Stage — an agent skill that turns a reference video into an original 2D cartoon

https://github.com/rizwanaabbas/sprite-stage

I kept losing character clothes and voice sync when I asked an agent to "make a cartoon of this video." The agent would copy names, drift the wardrobe, and finish a sentence while the mouth was still opening.

Sprite Stage is one MIT repo an agent can set up with `bash setup.sh`. A reference video supplies the premise only. Character sheets supply the cast. Sprite sheets are four cells on magenta, keyed tightly enough that pink clothes survive. OpenVoice V2 plus MeloTTS speak, one tone per person, stretched so the line lasts as long as the mouth is open. ffmpeg draws the frames on CPU.

The sample is a 2 minute 16 second film, `renders/long-slide.mp4`, of five original characters taking turns on a long slide.

A free image tool makes the new sprite sheets $0. The agent-token cost of a 1-minute film on an existing cast is roughly $0.40 on Claude Haiku, $1.60 on Sonnet, $1.80 on the Codex API, or about $1.30 of a Cursor Plus weekly pool. Figures and the OpenVoice machine notes (8 GB RAM, Python 3.11–3.13, GPU optional) are in `COSTS.md`.

I would like feedback on the sprite key and on whether the one-shot setup survives a clean machine.
