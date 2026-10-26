"""Make a 4-cell sprite sheet with Gemini or any other image tool.

Gemini reads GEMINI_API_KEY from the environment and never prints it.
With no key, this writes a prompt pack the agent can feed to a free image tool.
"""

import argparse
import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARACTERS = ROOT / "characters"
SPRITES = ROOT / "sprites"
PROMPTS = SPRITES / "prompts"

ACTIONS = {
    "walk": (
        "pose-guide.png",
        "Side view, facing right, walking in place. "
        "Cell 1 long stride, both feet down. "
        "Cell 2 feet together, one foot lifted. "
        "Cell 3 the opposite long stride, both feet down. "
        "Cell 4 feet together, the other foot lifted.",
    ),
    "front": (
        "pose-guide-front.png",
        "Front view in every cell. Both eyes visible. Same walk beat as the side view.",
    ),
    "back": (
        "pose-guide-back.png",
        "Back view in every cell. Back of the head, no face. Same walk beat as the side view.",
    ),
    "talking": (
        "pose-guide-talking.png",
        "Front view. Body stays still. Only the mouth changes: closed, a little open, wide open, a little open.",
    ),
    "sitting": (
        "pose-guide-sitting.png",
        "Already sitting, fully clothed, legs bent, outfit covering the lap. Four small seated shifts.",
    ),
    "catching": (
        "pose-guide-catching.png",
        "Catching one plain ball with no logo. The ball stays inside its own cell.",
    ),
    "holding": (
        "pose-guide-holding.png",
        "Holding one plain ball at the waist in every cell. No logo.",
    ),
    "taking": (
        "pose-guide-taking.png",
        "Taking one plain ball that starts in front of the character and ends at the chest.",
    ),
    "throwing": (
        "pose-guide-throwing.png",
        "Throwing one plain ball. The ball never enters the next cell.",
    ),
}


def prompt_for(name: str, action: str) -> str:
    _guide, beat = ACTIONS[action]
    return (
        f"IMAGE 1 is the identity reference for {name}. IMAGE 2 is a four-cell pose map. "
        "Ignore every word, label, color dot, and extra pose on IMAGE 1. "
        "Paint a new sprite sheet of that same character only. Copy the clothes and hair from IMAGE 1. "
        "Fully clothed. No logos, letters, or watermarks. "
        "ONE wide image, exactly four equal cells in a single horizontal row, matching IMAGE 2 cell for cell. "
        f"{beat} "
        "Same height and the same foot line in every cell. "
        "Background outside the figure is flat pure magenta #FF00FF. "
        "No white frame, no ground line, no text, no numbers, no grid, no second person."
    )


def write_pack(name: str, action: str) -> Path:
    guide_name, _beat = ACTIONS[action]
    PROMPTS.mkdir(parents=True, exist_ok=True)
    dest = PROMPTS / f"{name}-{action}.txt"
    identity = next(CHARACTERS.glob(f"{name}.*"))
    dest.write_text(
        "\n".join(
            [
                f"Save the image as sprites/{name}-{action}.png",
                f"Attach image 1: {identity.relative_to(ROOT)}",
                f"Attach image 2: sprites/{guide_name}",
                "",
                prompt_for(name, action),
                "",
            ]
        )
    )
    print(dest.relative_to(ROOT), flush=True)
    return dest


def gemini(name: str, action: str, model: str) -> None:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise SystemExit("Set GEMINI_API_KEY in the environment. Do not paste it into the chat or the repo.")
    identity = next(CHARACTERS.glob(f"{name}.*"))
    guide = SPRITES / ACTIONS[action][0]
    parts = []
    for path in (identity, guide):
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(path.read_bytes()).decode()}})
    parts.append({"text": prompt_for(name, action)})
    body = json.dumps(
        {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}},
        }
    ).encode()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    request.add_header("x-goog-api-key", key)
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        detail = error.read().decode()[:500]
        raise SystemExit(f"Gemini image call failed ({error.code}). {detail}") from None
    for candidate in payload.get("candidates") or []:
        for part in ((candidate.get("content") or {}).get("parts") or []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                dest = SPRITES / f"{name}-{action}.png"
                dest.write_bytes(base64.b64decode(inline["data"]))
                print(dest.relative_to(ROOT), dest.stat().st_size, flush=True)
                return
    raise SystemExit(f"Gemini returned no image for {name} {action}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Free or Gemini sprite sheets")
    parser.add_argument("--name", required=True)
    parser.add_argument("--action", default="walk,front,back,talking,sitting")
    parser.add_argument("--provider", choices=("prompt", "gemini"), default="prompt")
    parser.add_argument("--model", default=os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-image"))
    args = parser.parse_args()
    actions = [item.strip() for item in args.action.split(",") if item.strip()]
    unknown = [item for item in actions if item not in ACTIONS]
    if unknown:
        raise SystemExit(f"Unknown action: {', '.join(unknown)}")
    if not any(CHARACTERS.glob(f"{args.name}.*")):
        raise SystemExit(f"Missing characters/{args.name}.jpg")
    for action in actions:
        if args.provider == "gemini":
            gemini(args.name, action, args.model)
        else:
            write_pack(args.name, action)


if __name__ == "__main__":
    main()
