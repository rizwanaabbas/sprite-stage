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

## 3. A new story with the same cast

```text
Use the Sprite Stage skill.

New film in its own folder. Ayzel, Moiz, Lina, Rafi, and Mama have a picnic
and then fly a kite. Use characters/ as identity references and the sprite
sheets already in sprites/.
One action at a time. Original dialogue. British OpenVoice lines, each
character a different pitch. Mouth open only while that character speaks.
No logos, no on-screen words, no copied song lyrics.
```
