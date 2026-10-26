"""British preschool lines for the long slide, spoken with OpenVoice V2.

MeloTTS supplies the British words. OpenVoice shifts each character's tone
color, then a pitch change separates the children from Mama.
"""

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor" / "OpenVoice"
sys.path.insert(0, str(VENDOR))

import torch

_load = torch.load


def _load_ckpt(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _load(*args, **kwargs)


torch.load = _load_ckpt

from melo.api import TTS
from openvoice.api import ToneColorConverter

OUT = HERE / "audio"
CKPT = VENDOR / "checkpoints_v2"
LINES = {
    "ayzel-look": ("ayzel", "Look! The longest slide!"),
    "moiz-high": ("moiz", "It goes right up high!"),
    "mama-one": ("mama", "One by one. We climb, then we slide."),
    "lina-hold": ("lina", "I can hold on."),
    "rafi-fast": ("rafi", "I want a fast one!"),
    "ayzel-turn": ("ayzel", "My turn!"),
    "moiz-turn": ("moiz", "My turn!"),
    "lina-turn": ("lina", "My turn!"),
    "rafi-turn": ("rafi", "My turn!"),
    "mama-turn": ("mama", "My turn!"),
    "ayzel-slide": ("ayzel", "Wheee!"),
    "moiz-slide": ("moiz", "Wheee!"),
    "lina-slide": ("lina", "Wheee!"),
    "rafi-slide": ("rafi", "Whoosh!"),
    "mama-slide": ("mama", "Down I go!"),
    "mama-again": ("mama", "Shall we go again?"),
    "ayzel-again": ("ayzel", "Yes! Again!"),
    "mama-more": ("mama", "One more time!"),
    "ayzel-more": ("ayzel", "One more!"),
    "mama-longest": ("mama", "That was the longest slide."),
    "ayzel-fast": ("ayzel", "I went so fast!"),
    "moiz-too": ("moiz", "Me too!"),
    "lina-tight": ("lina", "I held on tight."),
    "rafi-tomorrow": ("rafi", "Again tomorrow!"),
    "mama-yes": ("mama", "Yes. Again tomorrow."),
}
# British base speaker, a different OpenVoice tone, then pitch for age.
CAST = {
    "ayzel": {"src": "en-br", "tgt": "en-au", "speed": 0.78, "pitch": 1.34},
    "moiz": {"src": "en-br", "tgt": "en-us", "speed": 0.74, "pitch": 1.18},
    "lina": {"src": "en-br", "tgt": "en-default", "speed": 0.76, "pitch": 1.24},
    "rafi": {"src": "en-br", "tgt": "en-india", "speed": 0.80, "pitch": 1.16},
    "mama": {"src": "en-br", "tgt": "en-newest", "speed": 0.68, "pitch": 1.02},
}


def sample_rate(path: Path) -> int:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=sample_rate", "-of", "default=nw=1:nk=1", str(path),
        ],
        text=True,
    )
    return int(out.strip())


def atempo_chain(factor: float) -> str:
    """factor < 1 lengthens the line. Each atempo stage stays inside 0.5–2.0."""
    parts = []
    remaining = factor
    while remaining < 0.5:
        parts.append("atempo=0.5")
        remaining /= 0.5
    while remaining > 2.0:
        parts.append("atempo=2.0")
        remaining /= 2.0
    parts.append(f"atempo={remaining:.4f}")
    return ",".join(parts)


def pace_target(text: str) -> float:
    if text.strip() in {"Wheee!", "Whoosh!"}:
        return 0.95
    words = [word for word in text.replace("!", " ").replace(".", " ").replace("?", " ").split() if word]
    return max(1.05, len(words) * 0.55)


def pitch_shift(src: Path, dest: Path, pitch: float, text: str) -> None:
    rate = sample_rate(src)
    filters = []
    if abs(pitch - 1) >= 0.02:
        filters.append(f"asetrate={rate}*{pitch:.4f},aresample=44100,atempo={1 / pitch:.4f}")
    else:
        filters.append("aresample=44100")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", ",".join(filters), str(dest)],
        check=True,
    )
    heard = duration(dest)
    target = pace_target(text)
    if heard >= target * 0.92:
        return
    slowed = dest.with_suffix(".slow.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(dest), "-af", atempo_chain(heard / target), str(slowed)],
        check=True,
    )
    slowed.replace(dest)


def duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    )
    return float(out.strip())


def main() -> None:
    device = "cpu"
    OUT.mkdir(parents=True, exist_ok=True)
    converter = ToneColorConverter(str(CKPT / "converter" / "config.json"), device=device, enable_watermark=False)
    converter.load_ckpt(str(CKPT / "converter" / "checkpoint.pth"))
    tts = TTS(language="EN", device=device)
    speaker_ids = tts.hps.data.spk2id
    british = speaker_ids["EN-BR"]
    raw = OUT / "_raw.wav"
    colored = OUT / "_colored.wav"
    heard = {}
    for key, (name, text) in LINES.items():
        dest = OUT / f"{key}.wav"
        if dest.exists() and dest.stat().st_size > 1000:
            heard[key] = duration(dest)
            print("keep", key, flush=True)
            continue
        voice = CAST[name]
        src_se = torch.load(CKPT / "base_speakers" / "ses" / f"{voice['src']}.pth", map_location=device)
        tgt_se = torch.load(CKPT / "base_speakers" / "ses" / f"{voice['tgt']}.pth", map_location=device)
        tts.tts_to_file(text, british, str(raw), speed=voice["speed"])
        converter.convert(
            audio_src_path=str(raw),
            src_se=src_se,
            tgt_se=tgt_se,
            output_path=str(colored),
            tau=0.3,
            message="default",
        )
        pitch_shift(colored, dest, voice["pitch"], text)
        heard[key] = duration(dest)
        print(key, f"{heard[key]:.2f}s", text, flush=True)
    (OUT / "durations.json").write_text(json.dumps(heard, indent=2))
    raw.unlink(missing_ok=True)
    colored.unlink(missing_ok=True)
    print(OUT / "durations.json", flush=True)


if __name__ == "__main__":
    main()
