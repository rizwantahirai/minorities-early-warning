# `app/` — The runnable Streamlit dashboard

This subfolder is the **runnable web app**. Everything else in this
handoff (docs, code reference) is documentation; this is the live
piece you can launch.

## Run it locally

```bash
# from this app/ directory:
python3 -m venv venv
source venv/bin/activate # macOS / Linux
# .\venv\Scripts\Activate.ps1 # Windows

pip install -r requirements.txt

cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit secrets.toml and set username + password

streamlit run app.py
```

Browser opens at `http://localhost:8501`. Log in. The dashboard
appears in the page.

Stop with `Ctrl+C`.

## What each file does

| File | What it does |
|---|---|
| `app.py` | Streamlit script. Shows the login form, checks credentials against `.streamlit/secrets.toml`, then loads `dashboard.html` and embeds it. |
| `dashboard.html` | The actual dashboard — Leaflet map, Chart.js charts, all data baked in. Sanitized: every caller description has been replaced with a placeholder. |
| `requirements.txt` | One line: `streamlit`. |
| `.streamlit/config.toml` | Theme (red primary colour, light background). |
| `.streamlit/secrets.toml.example` | Template for the login credentials. Copy to `secrets.toml` and edit. |
| `scripts/sanitize.py` | Regenerates `dashboard.html` from the full project (if you have access to it — see the bundle README). |

## Deploy it to the internet

Push the whole handoff folder to GitHub, then connect Streamlit
Community Cloud to it. Set the password in the Secrets pane.

Full step-by-step is in `DEPLOY.md`.
