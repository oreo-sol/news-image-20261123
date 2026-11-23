[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/oreo-sol/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/oreo-sol/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Entry for [Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123) on make.fun.

# news-image-20261123 — The World in One Day, Monday 23 November 2026

One image summing up Monday 23 November 2026: 30 dated stories across
7 regions, 13 illustrated cards, a where-it-happened map, and a date check.
Full-colour broadsheet in the 21 November entry's cover style: warm
newsprint paper, red masthead kicker and red accents, a coloured region
bar (one colour per region), and coloured illustrations. All illustrations
are drawn in code (Python PIL) — no AI image generator.

## The day

NATO's North Atlantic Council meets in Brussels over Russian missiles
landing in Poland, Nepal's prime minister holds talks with Modi in New
Delhi, and the COP31 fallout is labelled the "worst ever" — plus Israeli
strikes in Gaza, a drone-hit ship towed in the Baltic, a South Korean
minister resigning over an AI cheating scandal, and Wall Street sliding
into correction territory.

## Files

- `entry.png` — the image, 1024×1024 RGB PNG (222,947 bytes)
- `main.ts` — validates entry.png (PNG signature, IEND chunk, ≤1 MiB,
  1024×1024 via IHDR, pinned sha256) and copies it to
  `$MAKEFUN_OUTPUT_DIR/entry.png`
- `draw.py` — the renderer that drew the image (run it to reproduce it)
- `LICENSE` — MIT

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
