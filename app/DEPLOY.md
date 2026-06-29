# DEPLOY.md — Push to GitHub + Streamlit Community Cloud

Step-by-step. End-to-end takes about 10 minutes. No prior Streamlit
Cloud experience needed.

The goal: push the **entire handoff folder** (this folder's parent —
`minorities_ews_intern_handoff/`) to a GitHub repo, then point
Streamlit Community Cloud at `app/app.py` as the main file.

---

## Phase 1 — Create a GitHub repository

1. Go to <https://github.com/new>.
2. Repository name: `minorities-early-warning` (or whatever you like).
3. Set it to **Public** (Streamlit Community Cloud free tier needs
 public repos). If you have Streamlit Teams (paid), private is fine.
4. **Do not** initialise with a README, .gitignore, or licence — the
 handoff folder already has its own.
5. Click *Create repository*.

GitHub gives you a URL like
`https://github.com/<your-username>/minorities-early-warning.git`.
Copy that URL.

## Phase 2 — Push the handoff folder

In a terminal, from the **handoff root** (not inside `app/`):

```bash
cd minorities_ews_intern_handoff # the folder containing app/, docs/, 

git init
git branch -M main

git config user.name "Your Name"
git config user.email "you@example.com"

git add .
git commit -m "Initial commit — Minorities Early-Warning handoff"

git remote add origin https://github.com/<your-username>/minorities-early-warning.git
git push -u origin main
```

If git asks for credentials, use a **personal access token** (not
your password). Create one at <https://github.com/settings/tokens>
with the `repo` scope and paste it when prompted.

## Phase 3 — Deploy to Streamlit Community Cloud

1. Go to <https://share.streamlit.io/> and sign in with GitHub.
2. Click **New app** (top right).
3. Fill in:
 - **Repository**: `<your-username>/minorities-early-warning`
 - **Branch**: `main`
 - **Main file path**: `app/app.py` ← **important — the `app/` prefix**
 - **App URL** (optional): pick a subdomain like `minorities-ews`
 so the URL becomes `https://minorities-ews.streamlit.app`
4. **Advanced settings → Secrets**:
 `
 username = "admin"
 password = "pick-a-strong-shared-password"
 `
 Save.
5. Click **Deploy**.

Streamlit builds the environment from `app/requirements.txt`,
installs Streamlit, and starts the app. First boot takes 2-3 minutes.

When the app is live you will see the URL at the top of the page.
That URL is public — anyone lands on the login screen, but only
someone with the password can see the dashboard.

### Rotating the password later

App page on share.streamlit.io → kebab menu → *Settings* → *Secrets*.
Change the `password = "..."` line. Save. The app reboots in
~30 seconds. Anyone with an active session gets booted to the
login screen.

### Running locally with the password

In the `app/` folder, create `.streamlit/secrets.toml` (the
gitignored file, NOT the `.example` template):

```toml
username = "admin"
password = "your-local-test-password"
```

Then `streamlit run app.py`. Without this file the login screen
will show a warning.

## Phase 4 — Share with a collaborator

Send your collaborator three things:

1. **The repo URL** — `https://github.com/<your-username>/minorities-early-warning`
2. **The live app URL** — `https://minorities-ews.streamlit.app`
3. **Collaborator access** — on GitHub:
 repo → *Settings* → *Collaborators* → *Add people* → their
 GitHub username → they accept the invitation.

After that, both of you can edit the code and push — every push to
`main` triggers an automatic redeploy.

## Phase 5 — Collaborator workflow

```bash
git clone https://github.com/<your-username>/minorities-early-warning.git
cd minorities-early-warning/app

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Edit app.py or dashboard.html …

streamlit run app.py # test locally

# When happy:
git add .
git commit -m "Added a new chart"
git push
```

Within ~60 seconds Streamlit Community Cloud picks up the push and
redeploys the live app at the same URL.

## Troubleshooting

**"Could not find `app.py`" during deploy**
→ Set Main file path to `app/app.py`, not just `app.py`.

**Dependencies fail to install**
→ Streamlit Cloud reads `app/requirements.txt`. If you added a new
library, make sure you added it there. Push again.

**Want a specific Python version**
→ Add a file at the repo root called `runtime.txt` with one line:
```
python-3.11
```

**Custom domain**
→ Streamlit Community Cloud (free tier) only supports
`*.streamlit.app` URLs. For a custom domain you'd need Streamlit
Teams (paid) or self-host on Render / Railway / Fly.io.

## Quick reference

| What | Where |
|---|---|
| GitHub repo | `https://github.com/<your-username>/minorities-early-warning` |
| Live app | `https://<subdomain>.streamlit.app` |
| Streamlit Cloud dashboard | <https://share.streamlit.io/> |
| Main file Streamlit watches | `app/app.py` |
| Dependency file Streamlit reads | `app/requirements.txt` |
| Theme file | `app/.streamlit/config.toml` |
| Trigger redeploy | `git push` to `main` |
