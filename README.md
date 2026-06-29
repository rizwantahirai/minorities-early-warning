# Minorities Early-Warning System — Internship Handoff

Welcome 👋 — this folder is everything you need for the **Minorities
Early-Warning** internship project at the Punjab Safe Cities
Authority. Read this README top to bottom before doing anything else;
it tells you what's in the box, how to receive it on your laptop, how
to run the dashboard locally, how to put it online behind a password,
and what to read for your internship submission.

This is the **safe-to-share** version: caller personal data has been
stripped out, database credentials are not included, real schema
column names have been genericised, and only material safe for
external eyes is included.

---

# 🚀 The complete intern playbook — from "received zip" to "live URL"

Step-by-step, no skipped detail. Follow this once and you'll have a
public, password-protected dashboard your supervisor and reviewers
can visit on the internet. End-to-end this takes about **30 minutes**
the first time — half of that is waiting.

## Step 0 — What you should already have

Three things, before you start:

1. **This folder** — either as a zipped archive (`.zip` or `.tar.gz`)
   from your supervisor, or pulled from a Google Drive / shared
   location. After unzipping, the folder is called
   `minorities_ews_intern_handoff/` (about 2.2 MB).
2. **A laptop with internet access.**
3. **About 30 minutes** for the first-time setup.

If you don't yet have the folder, ask your supervisor — it usually
arrives by email, Google Drive, or USB stick.

## Step 1 — Receive and unpack the folder

If your supervisor gave you a `.zip` file:

- **Windows:** right-click the file → *Extract All…* → pick a
  destination → click *Extract*.
- **macOS:** double-click the file. macOS unpacks it automatically.
- **Linux:** open a terminal in the download folder and run
  `unzip minorities_ews_intern_handoff.zip`.

If your supervisor gave you a `.tar.gz` file:

- **macOS / Linux:** in a terminal, run
  `tar -xzf minorities_ews_intern_handoff.tar.gz`.
- **Windows:** use 7-Zip (free) — right-click the file → *7-Zip* →
  *Extract Here*.

After unpacking you should see a folder called
`minorities_ews_intern_handoff/` containing `app/`, `docs/`,
`reference_data/`, `README.md`, and `.gitignore`.

## Step 2 — Install Python

If you don't already have Python 3.10 or newer:

- **Windows / macOS:** go to <https://www.python.org/downloads/> and
  install the latest stable Python 3. **Important on Windows:** tick
  the box that says *"Add python.exe to PATH"* in the installer.
- **Linux:** Python 3 is usually already installed. Check with
  `python3 --version`.

Verify it works by opening a terminal (PowerShell on Windows,
Terminal on macOS, any terminal on Linux) and typing:

```bash
python3 --version
```

You should see something like `Python 3.11.5`.

## Step 3 — Run the dashboard on your laptop

Open a terminal **inside the `app/` folder** of the unpacked handoff.
On Windows you can do this by `Shift + Right-click` in the folder and
choosing *Open PowerShell window here*. Then run, **one line at a
time**:

```bash
# Create a private Python environment for this project
python3 -m venv venv

# Turn on the environment
source venv/bin/activate          # macOS / Linux
# .\venv\Scripts\Activate.ps1     # Windows PowerShell

# Install Streamlit (the only library we need)
pip install -r requirements.txt

# Set your login password
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# (Windows PowerShell:  Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml)

# Open .streamlit/secrets.toml in any text editor and set:
#   username = "admin"
#   password = "your-test-password"

# Launch the dashboard
streamlit run app.py
```

A browser window opens at `http://localhost:8501`. You see a
**login screen**. Type the username and password you set in
`secrets.toml` and click *Log in*. The dashboard appears.

To stop the app: go back to the terminal and press `Ctrl + C`.

> **If something goes wrong:** look at the line printed in the
> terminal. The most common errors are *"command not found: python3"*
> (Python isn't installed or isn't on PATH) and *"port 8501 is
> already in use"* (another Streamlit app is already running — close
> it or change the port with `--server.port 8502`).

## Step 4 — Create a free GitHub account

You'll publish the folder to GitHub so Streamlit Cloud can host the
live version.

1. Go to <https://github.com/signup>.
2. Sign up with your email. Pick a username you're comfortable
   showing (it appears in the public URL).
3. **Verify your email** — GitHub sends a code; enter it on the site.

If you already have a GitHub account, log in. Skip to Step 5.

## Step 5 — Create a personal-access token (so git can push)

GitHub doesn't let you push with a password anymore — you need a
**Personal Access Token (PAT)**:

1. Logged into GitHub, go to <https://github.com/settings/tokens>.
2. Click *Generate new token (classic)*.
3. Give it a name (e.g. `minorities-ews`) and an expiration (90 days
   is fine).
4. Tick the box for the **`repo`** scope.
5. Click *Generate token* at the bottom.
6. **Copy the token immediately** — GitHub shows it once, you'll
   never see it again. Save it somewhere safe (e.g. your password
   manager). Treat it like a password.

You'll paste this token whenever git asks for "Password" in the next
step.

## Step 6 — Create a GitHub repository for the handoff

1. Go to <https://github.com/new>.
2. **Repository name:** `minorities-early-warning` (or any name you
   like — lowercase, no spaces).
3. Set it to **Public**. Streamlit Community Cloud's free tier only
   works on public repos. (Your password gate will keep the dashboard
   private even though the code repo is public.)
4. **Do not** check "Initialize this repository with a README" — the
   handoff folder already has its own.
5. Click *Create repository*.

GitHub shows a page with a URL like
`https://github.com/YOUR_USERNAME/minorities-early-warning.git`.
Copy that URL — you need it in the next step.

## Step 7 — Push the handoff folder to GitHub

Open a terminal **at the root of the handoff folder** (the folder
that directly contains `app/`, `docs/`, and `reference_data/`) and
run, one line at a time:

```bash
# Tell git this folder is a repository
git init
git branch -M main

# (Only the first time you ever use git on this laptop:)
git config --global user.name  "Your Name"
git config --global user.email "your-email@example.com"

# Stage every file and create the first commit
git add .
git commit -m "Initial commit — Minorities Early-Warning handoff"

# Connect this folder to the GitHub repo you just created
git remote add origin https://github.com/YOUR_USERNAME/minorities-early-warning.git

# Push the commit
git push -u origin main
```

When git asks for **Username**, type your GitHub username.
When git asks for **Password**, paste the **personal-access token**
you copied in Step 5 (not your GitHub login password).

If the push succeeds you'll see something like
`Branch 'main' set up to track 'origin/main'`. Reload your repo's
page on GitHub — all your files should be there.

## Step 8 — Sign in to Streamlit Community Cloud

1. Go to <https://share.streamlit.io/>.
2. Click *Continue with GitHub* — you'll already be logged in to
   GitHub from Step 4.
3. Streamlit asks for permission to read your repos. Click
   *Authorize*.

You land on a dashboard that says you have no apps yet.

## Step 9 — Deploy the app

1. Click the big **New app** button (top right).
2. Fill the form:
   - **Repository:** `YOUR_USERNAME/minorities-early-warning`
   - **Branch:** `main`
   - **Main file path:** `app/app.py` ← **note the `app/` prefix**.
     This tells Streamlit Cloud where to find the script inside the
     repo.
   - **App URL** (optional but useful): pick something memorable
     like `minorities-ews` so your live URL becomes
     `https://minorities-ews.streamlit.app`.
3. Click **Advanced settings → Secrets** and paste:

   ```
   username = "admin"
   password = "PICK_A_STRONG_PASSWORD"
   ```

   Replace `PICK_A_STRONG_PASSWORD` with something you'd actually
   use — this is what anyone visiting the public URL will need to
   type. **Don't reuse the password from your laptop's `secrets.toml`
   — that one is local only.**
4. Click **Save** on the secrets pane, then **Deploy**.

Streamlit Cloud now builds your app: it pulls the repo, installs the
single dependency, and starts the server. **First boot takes
2–3 minutes.** Watch the build log in your browser — it scrolls live.

When it's done you'll see the dashboard's login screen at the URL
you picked. Try logging in with the username/password you set in the
Secrets pane.

🎉 **Your dashboard is live on the internet.** Share the URL + the
password with whoever needs to see it.

## Step 10 — Sharing safely

To share:

- **The URL alone** = anyone who clicks it lands on the login screen.
- **The URL + password** = they can see the dashboard.

Don't post the password in the same channel as the URL. (Send the
URL by email, password by WhatsApp; or URL on a slide, password
verbally.)

If you ever want to rotate the password:
Streamlit Cloud → your app page → kebab menu → *Settings* →
*Secrets* → change the line → Save. The app reboots in ~30 seconds
and any active sessions are kicked out to the login screen.

## Step 11 — Making changes after deployment

Every push to GitHub auto-redeploys the live app, within about a
minute. To make a change later:

```bash
# Pull the latest version of the repo
git pull

# Edit any file (app.py, dashboard.html, the docs — anything)

# Stage, commit, push
git add .
git commit -m "Describe what you changed"
git push
```

That's it. Refresh the live URL after ~60 seconds and your changes
are live.

---

# 📂 What's in the handoff folder

```
minorities_ews_intern_handoff/
├── README.md                    ← you are here
├── .gitignore                   ← tells git to ignore venv/, secrets, etc.
│
├── app/                         ← the runnable Streamlit dashboard
│   ├── app.py                   ← entry point: login screen + embed
│   ├── dashboard.html           ← the actual dashboard (sanitised)
│   ├── requirements.txt         ← one line: streamlit
│   ├── README.md                ← what each file in app/ does
│   ├── DEPLOY.md                ← deeper deploy reference + troubleshooting
│   ├── .streamlit/
│   │   ├── config.toml          ← theme settings
│   │   └── secrets.toml.example ← copy → secrets.toml & set your password
│   └── scripts/
│       └── sanitize.py          ← rebuild dashboard.html when data refreshes
│
├── docs/                        ← documentation for learning + submission
│   ├── 01_policy_brief.{md,pdf,docx}        ← 2 pages, non-technical
│   ├── 02_detailed_report.{md,pdf,docx}     ← 15 pages, full write-up
│   ├── 03_research_design_report.{md,pdf,docx}
│   ├── 04_data_dictionary.{md,pdf,docx}
│   ├── 05_timeline.{md,pdf,docx}            ← phase-by-phase build log
│   └── how_to_do_this.{md,pdf,docx}         ← the big learning guide
│
└── reference_data/              ← non-sensitive calendar CSVs
    ├── religious_calendar.csv
    ├── political_calendar.csv
    └── misinformation_events.csv
```

Three subfolders, two top-level files. Small and focused.

---

# 📖 What to read, in what order

You don't need to read every doc at once. They build on each other —
read them in this order and the next one always makes sense in the
context of the previous:

| # | Read | Why |
|---|---|---|
| 1 | `docs/01_policy_brief.md` | 2 pages, plain English. The whole project in one go. |
| 2 | `docs/02_detailed_report.md` | The full write-up. ~15 pages. The story of what was built and why. |
| 3 | `docs/03_research_design_report.md` | The academic framing — research question, hypotheses, methodology. |
| 4 | `docs/05_timeline.md` | Phase-by-phase build log. Useful for your internship submission's project-management section. |
| 5 | `docs/how_to_do_this.md` | **The big learning guide.** Every technique unpacked, every choice explained, with code snippets inline. Read this when you want to understand HOW it was built. |
| 6 | `docs/04_data_dictionary.md` | Reference. Every field of the working table described. Read when you need to look up a detail. |

Every doc is in three formats:

- `.md` — source (open in any editor)
- `.pdf` — read-only, looks the same on any device
- `.docx` — editable in Microsoft Word

---

# 🎓 What to submit for your internship

The deliverable documents are submission-ready. Pick by the type of
evaluator:

| Evaluator | Submit |
|---|---|
| Technical reviewer | `02_detailed_report.pdf` + `04_data_dictionary.pdf` |
| Policy reviewer | `01_policy_brief.pdf` |
| Academic reviewer | `03_research_design_report.pdf` |
| Project-management section | `05_timeline.pdf` |
| Personal portfolio / methodology depth | `how_to_do_this.pdf` |

The `.docx` versions are there if you want to add your own
introduction, acknowledgements, or institutional cover page before
printing.

---

# 📸 Capturing dashboard screenshots for your portfolio

The dashboard is the headline visual artefact of this project — get
clean screenshots once you have it running.

Recommended shots:

1. **The login screen** — the centred login card with the project
   title. Take this *before* you log in.
2. **The full dashboard, default view** — header KPI showing the
   forecast, map with the heatmap + orange forecast circles.
3. **The 🔮 Next 30 Days panel** — close-up of the right sidebar
   with the top-15 forecast police stations.
4. **A map detail** — zoomed in on Lahore showing the orange
   forecast circles sitting over the historical heatmap. Hover one
   to capture the tooltip showing case identifiers + score.
5. **The trend chart** — bottom-right, showing cases-per-month.

Tools:

- **macOS:** `Cmd + Shift + 4` then drag to capture an area, or
  `Cmd + Shift + 5` for a window.
- **Windows:** *Snipping Tool* (built in), or `Win + Shift + S`.
- **Browser full-page capture:** in Chrome / Firefox dev tools,
  `Ctrl + Shift + P` → *Capture full size screenshot*.

Use these screenshots in your internship presentation, portfolio
slides, or in the `.docx` deliverable documents (insert via
*Insert → Pictures*).

---

# 🛡️ Privacy posture (read this before sharing the URL)

- The dashboard's caller free-text descriptions are **replaced with a
  placeholder** in every embedded record. There is no caller PII in
  this handoff.
- The dashboard is **gated behind a username + password** set in
  `secrets.toml` (locally) or in Streamlit Cloud's Secrets pane
  (when deployed).
- Real internal column names from the source database have been
  **replaced with generic placeholders** in every document.
- The `.gitignore` excludes `secrets.toml`, so your real password
  never gets committed.

If you deploy publicly, set a strong password and never put the
password in any file you commit. Streamlit Cloud's Secrets pane is
the right place for it — never inside `app/` or `docs/`.

---

# ❓ Common questions & troubleshooting

**`git push` rejects my credentials**
→ Use your personal-access token (Step 5), not your GitHub login
password. If your token expired, regenerate it.

**Streamlit Cloud says "Could not find app.py"**
→ The main file path in Step 9 needs to be `app/app.py` (with the
`app/` prefix), not just `app.py`.

**The live app shows "No password is configured"**
→ Add `username = "..."` and `password = "..."` in Streamlit Cloud →
your app → Settings → Secrets. Save. Wait ~30 seconds.

**The dashboard map is blank**
→ Open your browser's developer console (F12). If you see "Mixed
Content" errors, the dashboard uses CDNs over `https://`; your
school/institution proxy may be blocking them. Try a different
network.

**`streamlit: command not found` when running locally**
→ You forgot to activate the venv. Run
`source venv/bin/activate` (macOS / Linux) or
`.\venv\Scripts\Activate.ps1` (Windows) again.

**Pip install is super slow**
→ Try `pip install -i https://pypi.org/simple -r requirements.txt`
to force PyPI's main index.

**I want to delete the deployment**
→ Streamlit Cloud → your app → kebab menu → *Delete*. The GitHub
repo is untouched; you can redeploy any time.

---

# What's NOT in this folder (and why)

To keep this bundle safe to share publicly, the following are
deliberately **not included**:

- **Raw incident data** with caller descriptions, phone numbers,
  addresses — lives in the full project archive, not shared publicly.
- **Database credentials** — never committed anywhere.
- **Source Python code** (training scripts, feature builders, etc.) —
  not needed for running the dashboard, and the educational walk-
  through is already inline in `docs/how_to_do_this.md` with code
  snippets at every step.
- **Trained model `.pkl` files** — predictions are already baked into
  `dashboard.html`, so the dashboard works without them.
- **Original PSCA reference PDFs** — institute documents; not for
  public redistribution.

If you need any of these for advanced work, contact the project
supervisor.

---

# Where to get help

- **Anything dashboard-related** → check `app/DEPLOY.md` for deeper
  troubleshooting, then ask the supervisor.
- **A document doesn't open** → use the `.pdf` version; every doc is
  in `.md`, `.pdf`, and `.docx`.
- **You're stuck on a concept** → open `docs/how_to_do_this.md` and
  search for the term. Every technique is explained from first
  principles, with code snippets inline.

Good luck with your internship 🚀 — the dashboard works, the docs are
complete, the deployment path is well-trodden. You've got this.
