#!/usr/bin/env bash
# One-shot setup. An agent runs this once. It is safe to run again.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(pwd)"

say() { printf '\n== %s\n' "$1"; }

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  say "Installing ffmpeg"
  if command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
  elif command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y ffmpeg
  else
    echo "ffmpeg is required. Install it, then run bash setup.sh again."
    exit 1
  fi
fi

PY=""
for candidate in python3.12 python3.11 python3.13 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    ver="$("$candidate" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')"
    major="${ver%%.*}"
    minor="${ver#*.}"
    if [[ "$major" -eq 3 && "$minor" -ge 11 && "$minor" -le 13 ]]; then
      PY="$candidate"
      break
    fi
  fi
done
if [[ -z "$PY" ]]; then
  echo "Python 3.11, 3.12, or 3.13 is required for voices."
  exit 1
fi

say "Python $($PY -c 'import sys; print(sys.version.split()[0])')"
if [[ ! -x .venv/bin/python ]]; then
  "$PY" -m venv .venv
fi

say "Voice libraries"
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -q -r requirements-voice.txt

if [[ ! -d vendor/OpenVoice/.git ]]; then
  say "OpenVoice"
  git clone https://github.com/myshell-ai/OpenVoice.git vendor/OpenVoice
  git -C vendor/OpenVoice checkout 74a1d147b17a8c3092dd5430504bd83ef6c7eb23
fi
if [[ ! -d vendor/MeloTTS/.git ]]; then
  say "MeloTTS"
  git clone https://github.com/myshell-ai/MeloTTS.git vendor/MeloTTS
  git -C vendor/MeloTTS checkout 209145371cff8fc3bd60d7be902ea69cbdb7965a
fi

.venv/bin/python -m pip install -q --no-deps -e vendor/OpenVoice -e vendor/MeloTTS
.venv/bin/python scripts/apply_voice_patches.py

CKPT="vendor/OpenVoice/checkpoints_v2"
mkdir -p "$CKPT/converter" "$CKPT/base_speakers/ses"
BASE="https://huggingface.co/myshell-ai/OpenVoiceV2/resolve/main"
if [[ ! -s "$CKPT/converter/checkpoint.pth" ]]; then
  say "OpenVoice checkpoints"
  curl -L --fail -o "$CKPT/converter/checkpoint.pth" "$BASE/converter/checkpoint.pth"
  curl -L --fail -o "$CKPT/converter/config.json" "$BASE/converter/config.json"
  for name in en-au en-br en-default en-india en-newest en-us; do
    curl -L --fail -o "$CKPT/base_speakers/ses/${name}.pth" "$BASE/base_speakers/ses/${name}.pth"
  done
fi

touch .ready
say "Sprite Stage is ready"
echo "Replay the sample: python3 render.py"
echo "New voices:        .venv/bin/python voices.py"
