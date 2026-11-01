# WAY-BE

A website about **mobility in Belgium**, with a **Y2K** look (pink neon, XP windows, pixels, LCD screens).
End of 1st year project: **UCLouvain EPL**, **group C02**, 2024. The students wrote it by hand, before AI tools.

In 2026, we fixed and redesigned the site with **Claude Code** (Anthropic's AI coding agent).

## What the site does

- **Data**: select a city, a street and a period. The site shows Telraam counts (cars, bikes, pedestrians, trucks).
- **Stats**: a short story told with the data, with charts.
- **Memory**: a card game. Match each vehicle to its real share of the traffic in a city.
- **Moon**: the moon phase for any date. Does the full moon bring more bikes?
- **Team**: trading cards of the 4 students.
- **Radio**: a small Y2K MP3 player.

## Stack

- Flask + SQLite (`mobility/`). At first start, the app builds the database from `mobility/ugly.csv`.
- HTML, CSS and vanilla JavaScript. Chart.js and the fonts are served by the site itself.
- No external API, no CDN, no tracking.

## Run it locally

```bash
python3 -m venv .venv && .venv/bin/pip install flask
.venv/bin/flask --app mobility --debug run
```

Then open http://127.0.0.1:5000.

## Deploy

See [`deploy/README.md`](deploy/README.md): Docker + Caddy, with hard limits on RAM and CPU.

## Repository

```
mobility/        Flask app (templates, static, SQL, moon calculation)
deploy/          Docker Compose, Caddy snippet, deploy guide
docs/            Old static showcase (GitHub Pages)
rapport WAY-BE/  LaTeX report of the 2024 project
```

## Team

| Name |
|------|
| Noah Moussaoui |
| Houari Boumeddien Benkechida |
| Abdullah Camur (Abdu) |
| Guillaume Sablon (Guigui) |
