# makefun-news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/phothan26/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/phothan26/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image summing up Wednesday 25 November 2026 in six stories: Iran says two oil tankers struck naval mines in the Strait of Hormuz and caught fire; a fuel tanker blast kills 31 on Cairo's Ring Road; Ukrainian drones set two Russian refineries ablaze in Samara; the US proposes tariffs of up to 20% on 14 economies; Pakistan's first astronaut docks at China's Tiangong station; and Asian shares plunge on AI doubts, with the Kospi down 6.2%. A footer strip adds the Bogor mine flood (9 dead, 17 trapped), Australia's inflation jumping to 4.9%, and the Australia–Solomon Islands security treaty.

The image is a light broadsheet front page, drawn flat with PIL: a black lead panel for Hormuz, four illustrated cards, a markets strip, and an "also" line. It ships as `entry.png.b64` (the PNG base64-encoded so it travels as plain text); `main.ts` decodes it and writes `/output/entry.png`, then verifies the copy byte for byte.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=t7e39kme&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
