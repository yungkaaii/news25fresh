# THE WORLD TODAY — Wednesday 25 November 2026

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/yungkaaii/news25fresh/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/yungkaaii/news25fresh/reward.svg)](https://make.fun/bounty/news-image-20261125)

A newspaper front page that sums up the world's news of
**Wednesday 25 November 2026** in a single 1024x1024 image.

`main.py` (Python 3.13, standard library only) draws the poster itself —
its own PNG encoder and its own 5x7 bitmap font, both written from
scratch in this file. No network, no randomness, no clock reads: every
run writes the exact same bytes to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`).

## What the poster shows

- A masthead with the date, **WEDNESDAY 25 NOVEMBER 2026**, and the
  line "30 STORIES FROM ONE DAY | IN ONE IMAGE".
- One lead story, drawn large with an illustration of the Pacific:
  the Solomon Islands–Australia treaty, with the two flags over the sea.
- The other 29 stories in a three-column grid, each with its number,
  section and headline — 30 stories in total, across war and diplomacy,
  the Pacific, markets, tech, health, science, sport and climate.

## Lead story

**01 — Solomon Islands signs a landmark treaty with Australia.**
Canberra is named the islands' primary security partner, no foreign
military base will be built on the islands, and the pact replaces a
2022 security deal with China. Signed in Canberra on Wednesday.

## The 30 stories

1. **LEAD — THE PACIFIC:** Solomon Islands signs landmark treaty with Australia
2. **SPACE:** Shenzhou-24 carries Pakistan's first astronaut
3. **TECH:** US jury convicts Huawei of stealing trade secrets
4. **WAR:** Ukraine drones sink Russian ship in Libya
5. **WAR:** Zelensky: Ukraine needs €115bn aid for 2027
6. **MIDEAST:** Fresh attacks on shipping in Strait of Hormuz
7. **MIDEAST:** Israeli strikes in Gaza kill 7, including official
8. **MIDEAST:** Houthi attack in Riyadh injures 11 people
9. **MIDEAST:** Iran vows 'all means' to counter US blockade
10. **ECONOMY:** Eurozone inflation rises to 4.0%
11. **ECONOMY:** Australian inflation rises to 4.9%
12. **ECONOMY:** UK energy bills to rise 26% from January
13. **MARKETS:** AI fears drag markets lower across Asia, Wall St
14. **MARKETS:** Anthropic shares fall below IPO price
15. **TECH:** Amazon buys Decart to challenge Nvidia
16. **TECH:** Hackers' AI agents break into university server
17. **TECH:** Tidal bans AI music, deletes 27m tracks
18. **USA:** Abrego Garcia leaves US for Spain
19. **LATAM:** Colombia frees hostages in supermarket siege
20. **SPORT:** Court restores AFCON title to Senegal
21. **HEALTH:** Roche breast cancer pill wins 2nd FDA nod
22. **HEALTH:** UN: funding cuts threaten HIV progress
23. **USA:** Six killed in plane crash off Mississippi
24. **ASIA:** Dozens trapped in flooded Indonesia gold mine
25. **CHINA:** Xi's purge takes down Shanghai chief Chen Jining
26. **ASIA:** North Korea expels Swiss diplomat
27. **UK:** Two held after break-in at Prince William's home
28. **BUSINESS:** EasyJet profit falls 89% as fuel costs soar
29. **USA:** San Francisco Bay braces for record flooding
30. **CLIMATE:** Bowen: geopolitics hurt COP31 consensus

Every headline above is a real event reported on 25 November 2026,
researched from live news sources on the day. Nothing is invented.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs produce byte-identical `entry.png` files
(1024x1024 PNG, well under the 1 MiB limit).

## License

MIT — see `LICENSE`.
