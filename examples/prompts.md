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
