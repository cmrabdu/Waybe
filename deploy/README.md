# Deploy WAY-BE on watchy

The site is self-contained: no external API, no CDN, no external fonts.
The data is in `mobility/ugly.csv`. At first start, the app builds the SQLite database from it.

## First install

1. Clone the repo on the server:
   `git clone https://github.com/cmrabdu/Waybe.git /srv/waybe && cd /srv/waybe/deploy`
2. Create `deploy/.env`:
   `echo "WAYBE_SECRET_KEY=$(openssl rand -hex 32)" > .env`
3. Start the container:
   `docker compose up -d --build`
4. Add `Caddyfile.snippet` to the Caddyfile, then reload Caddy.
5. Add a DNS record: `waybe.cmrabdu.com` → IP of watchy.

## Update

`cd /srv/waybe && git pull && cd deploy && docker compose up -d --build`

## Limits and safety

- RAM 256 MB, CPU 0.5, 64 processes max, read-only file system, no Linux capabilities.
- Port 8010 is open on localhost only. Caddy does HTTPS.
- Rate limit: 120 pages per minute per IP (static files excluded). Variable: `WAYBE_RATE_PER_MIN`.
- Strict Content-Security-Policy: the browser loads only files from the site itself.
- Logs rotate (2 × 5 MB).

## Backup

There is no user data to back up. The site writes nothing.
The Git repo is the backup: the database can always be built again from the CSV.
