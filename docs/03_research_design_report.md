---
title: "Research Design Report — Predictive Early-Warning System for Religious-Minority Crime in Lahore"
subtitle: "Updated Edition — Reflecting What Was Actually Built"
author: "Internship Project — Minorities Early-Warning System"
date: "June 2026"
geometry: margin=2cm
fontsize: 11pt
toc: true
---

# Plain-Language Version First

If you're reading this and you've never seen a research-design document
before, here is the whole thing in 200 words:

> Religious minorities in Pakistan — Christians, Ahmadis, Hindus, Sikhs
> — sometimes get attacked, harassed, or threatened. When they call the
> police helpline, the call gets recorded. We have a record of about
> 4,100 such calls. This project asks: can a computer, having read all
> those past calls, **predict where the next one is likely to come from
> in the next 30 days**? If yes, the police can position a patrol
> there before anything happens, instead of just responding after the
> fact.
>
> To do this, we needed to (a) get the data, (b) figure out which
> features of past calls might predict future ones (we picked six),
> (c) train computer models, (d) test them honestly, and (e) build a
> dashboard for the police to actually use.
>
> This document explains the choices we made, *why* we made them, and
> what limits we know about. The rest of the project (the data, the
> models, the dashboard) is the result of executing on this design.

# 1. The Origin of This Project

This project came out of fieldwork at the **Punjab Safe Cities
Authority (PSCA)** command centre in Lahore. PSCA operates an
emergency-call ecosystem covering all of Punjab's 120 million people:

- The **Emergency-15** helpline (Pakistan's equivalent of 911 / 1122),
 which takes calls from the public.
- **AI-assisted call routing** that sends calls to the right operator.
- **GPS-based first-responder dispatch** that finds the nearest police
 unit.
- **Specialised virtual centres** for women, children, and minorities.

The **Virtual Center for Minorities (VCM)** is the relevant one for
this project. It is a dedicated helpline staffed by call-takers from
minority backgrounds, so a Christian or Ahmadi caller is sure to speak
to someone culturally aware.

Sitting through these calls during fieldwork, the researcher noticed
something. Calls were **not random**. They had patterns:

- Some neighbourhoods showed up over and over.
- Calls clustered around predictable dates — Christmas, Eid, Muharram,
 Holi.
- Sometimes multiple calls came from the *same* area within hours of
 each other — coordinated incidents, not isolated ones.
- Spikes in **social-media negativity** about a community seemed to
 precede physical incidents on the ground.

If patterns exist, a computer can be taught to spot them. That's the
heart of this project.

# 2. The Research Question

Stated formally:

> **What combination of social, political, economic, and digital
> signals most reliably precedes minority-targeted violent incidents
> in Lahore, and can these signals be formalized into a predictive
> risk index capable of generating early warnings?**

Stated for a non-expert:

> Looking at the messy collection of things that happen before a
> minority-targeted attack — a misinformation post, an election, a
> religious holiday, a previous attack in the same neighbourhood — can
> we use them together to predict where and when the *next* attack will
> happen?

# 3. What Counts as a "Risk Event"?

We need a precise definition before we can predict anything.

> A **risk event** is any incident reported through Emergency-15 or
> VCM channels where one of the following is true:
>
> 1. The incident involves **physical violence**, **property
> destruction**, **threats**, or **forced displacement** AND the
> victim's identity as a religious minority is a factor.
> 2. The incident is a **protest gathering** or **public
> confrontation** with sectarian meaning that has potential to
> escalate.

Practically, in the database we approximate this with a strict
boolean label called `is_minority_targeted`. A call satisfies this
when:

- The Emergency-15 operator tagged the call as a *Religious Offence*
 in the Level-2 case-nature hierarchy, AND
- The caller mentioned one of: Christian, Ahmadi, Hindu, Sikh
 (or multiple) in the free-text description of the incident.

Out of 4,110 minority-related calls in our dataset, **312 (7.6%)**
satisfy this strict definition. These are the "positive examples" the
prediction models learn from.

# 4. Geographic and Temporal Scope

## 4.1 Geographic — why Lahore

We focus on **Lahore** for three reasons:

1. **Data accessibility.** The research originated in PSCA Lahore.
2. **Demographic complexity.** Lahore has all four target minority
 communities present in significant numbers — Christian, Ahmadi,
 Hindu, Sikh — spread across both working-class and mixed-income
 neighbourhoods. This makes pattern-learning meaningful.
3. **Largest share of the data.** Lahore alone produces **22.6% of all
 minority-related Emergency-15 calls in Punjab** (928 out of 4,110).

Other districts — Faisalabad, Sheikhupura, Sialkot, Gujranwala — are
also covered but get less focus in the dashboard.

## 4.2 Temporal — what time period

The data covers **January 2024 through June 2026**. That's about 30
months. The split we use for training and testing the models is:

- **Training data:** 2024 + 2025 (full years)
- **Test data:** 2026 year-to-date (about 6 months)

This is a *temporal* split — we don't randomly mix train and test
together. The model is trained on the past and tested on the future.
That mirrors what happens in real deployment: we never know the
future when making a prediction.

# 5. The Six Predictor Variables (Features)

The original Research Design proposed six families of predictors. We
implemented five and left one as a placeholder. Each is described in
detail in the detailed report, but here is the design rationale.

## 5.1 Social media sentiment (placeholder in v1)

**Hypothesis:** A rise in negative posts about a particular community,
in the period just before an incident, should predict that incident.

**Why we picked it:** Documented in the academic literature on
hate-speech-to-violence pipelines. Globally, social media often
precedes physical confrontations.

**Implementation status:** The infrastructure (column definitions, the
loader interface) is in place. We did not connect a social-media feed
because we don't have authorized access to one. When PSCA adds one,
the feature activates with no code change.

## 5.2 Misinformation propagation

**Hypothesis:** A single viral false claim — *"a Christian burned the
Quran"*, *"an Ahmadi is preaching"* — can trigger violence within
days.

**Why:** The 2023 Jaranwala incident, the 2024 Sargodha mob attack,
several Dijkot and Sialkot-Moutra clusters in our own data — all
followed documented misinformation events.

**Implementation:** A small hand-curated CSV (9 events) of known
misinformation incidents, with district and target community. Features
ask: did a misinformation event happen in the same district within
the last 7 days? In any district? Targeting this case's community?

## 5.3 Political calendar events

**Hypothesis:** Periods of political instability — elections,
by-elections, major announcements, anniversaries of contested events
— raise community tensions.

**Why:** During elections, especially, religious identity often gets
mobilized politically, and the political conflict bleeds into community
relations.

**Implementation:** A pre-populated political calendar (19 events
2024-2026), with features for days-to-next-event, days-since-last-
event, "in election period" flag.

## 5.4 Religious calendar density

**Hypothesis:** Periods where major festivals from different
communities overlap, or where multiple religious gatherings occur in
mixed neighbourhoods, have elevated incident risk.

**Why:** Visibly confirmed in the data: **18.9% of all minority-
related calls happen within ±1 day of a major religious event** —
about one in five.

**Implementation:** A 51-event calendar covering Islamic, Christian,
Hindu, and Sikh observances 2024-2026, with per-community
days-to-next-event features, multi-community overlap flag, density
score for ±7-day windows.

## 5.5 Prior incident density

**Hypothesis:** A rolling count of past minority-related calls in the
same neighbourhood is a strong predictor of future calls.

**Why:** Tensions don't usually appear out of nowhere. They build.
Areas with recent incidents are at elevated risk.

**Implementation:** Self-contained — computed directly from the
`minority_incidents` table itself. We count incidents in the same
police station for windows of 7, 30, 60, 90 days back, and similarly
for the whole district. Plus a clever "escalation ratio" that
compares the recent 7-day rate to the 30-day baseline.

## 5.6 Police responsiveness

**Hypothesis:** Areas where the police are slow to respond have
**structural vulnerability** — perpetrators learn that response is
slow and act accordingly.

**Why:** This is a *non-trigger* variable — it doesn't change quickly
day-to-day, but it shapes which areas perpetrators target.

**Implementation:** For each call, we look at the local police
station's average response time over the previous 3 months (across
ALL calls, not just minority-related), and compute decile rank
across Punjab.

# 6. The Data Source

The base data is PSCA's **`<source_call_log_table>` table** — the master
database of every Emergency-15 call across Punjab. It currently has
~5.7 million rows. We filter down to minority-related rows using a
two-clause filter (operator tag OR description keyword), arriving at
4,110 working rows.

The Research Design originally proposed using a separate **VCM case
database** of 4,508 cases. That database was not accessible at the
time of building this system. Using `<source_call_log_table>` instead gives us:

- More cases (4,110 from the broader filter vs ~1,500 Lahore VCM cases)
- Geographic coverage (lat/long for every call)
- A common spine to join other features (response time, calendar
 events, etc.)

The trade-off is we don't have VCM's specific outcome / feedback
fields. When VCM data becomes available, a follow-up phase can
supplement.

# 7. Three Models, Three Questions

We deliberately built **three models** answering three different
questions:

| Question | Model | When you'd use it |
|---|---|---|
| Is *this* call (already logged) minority-targeted? | Per-case classifier (LR + RF) | Triage as calls come in |
| Will an attack happen at *this PS* in the next 30 days? | PS-week forecaster (LR) | Weekly deployment planning |
| How many total attacks should Punjab expect next month? | Volume forecaster (Prophet) | Quarterly resource planning |

These are complementary, not competitive. A modern security operation
needs all three.

# 8. Methodological Boundaries

## 8.1 Under-reporting is irreducible

The model predicts **reports**, not incidents. If a community doesn't
trust the police, it doesn't call them. That community will look
"low-risk" in the data — even if real attacks are happening.

There is no way to fully fix this without a separate ground-truth
data source. The mitigation is to *say so loudly, in every output*.

## 8.2 The model is Lahore-biased

22.6% of training data is from Lahore. The model's confidence in
Lahore predictions is higher. Other districts get lower-confidence
predictions even when known clusters exist (Sialkot-Moutra, Faisalabad-
Dijkot are ranked above the median but not in the top-50).

The mitigation is to communicate clearly: don't only look at top-50.
For each district, look at the *top within that district*.

## 8.3 Feedback loops

If the police deploy heavily to areas the model flags, those areas
generate more reports (more police = more reporting). The next
iteration of the model then flags those areas even harder. This is a
known failure mode of predictive policing.

The mitigation: retrain on **raw** Emergency-15 data only, on a fixed
quarterly cadence — not on the system's own outputs.

## 8.4 Selection of what counts as "minority-targeted"

The filter we use to define a "minority-related" case is based on
operator tag + description keywords. It misses:

- Anti-Shia incidents that don't name a sect (Shia are not in our
 target list because Shia is not a religious minority — it's a Muslim
 sub-community).
- Gendered minority violence — a Christian woman attacked for being
 both Christian and female. We don't distinguish.
- Sectarian disputes within a community (intra-Christian, intra-
 Ahmadi, etc.).

The strict label (`is_minority_targeted`) is conservative; the broader
set captures more but with noise. A future iteration could refine the
definition with help from community organizations.

# 9. Ethics Embedded in the Design

From day one, three principles were built in:

1. **No individual targeting.** The unit of prediction is *(place,
 time)*. Never *(person)*.
2. **Privacy by default.** Phone numbers, addresses, names, CNICs in
 call descriptions are all auto-redacted before they reach any
 display. The toggle to show descriptions defaults to OFF.
3. **Community review required.** Before deployment, representatives of
 the affected communities should review predictions, false
 positives, and recommendations.

These are encoded in `<see project ethics doc>` in the project
folder.

# 10. What Success Looks Like

Per the methodology, we set three thresholds before we started training:

| Model | Success threshold | Result |
|---|---|---|
| Logistic Regression baseline | ROC AUC ≥ 0.65 | **0.841** (per-case) / **0.715** (PS-week) — both pass |
| Random Forest | ROC AUC ≥ 0.75 AND Precision@20 ≥ 0.30 | **0.814 + 0.35** — passes |
| Fairness check | No community AUC < 0.55 (where evaluable) | Passes where evaluable (Christian, n=213). Ahmadi (n=10) and Hindu (n=11) also pass but their samples are too small to be reliable. |
| Prophet volume forecaster | MAPE < 20% on Punjab | **9.54%** — comfortably passes |

The system meets all the success thresholds set at design time.

# 11. The Twelve Weeks of Build (Cross-Reference)

| Weeks | Phase | Output |
|---|---|---|
| 1 | Data pipeline | `minority_incidents` table, 4,110 rows |
| 2-3 | EDA | 8 figures, district-severity CSV, summary JSON |
| 3-4 | Heatmap | 3 HTML heatmaps |
| 5-6 | Feature engineering | 6 feature families, merged 62-column table |
| 7-8 | Models | Per-case LR + RF, PS-week LR + RF, Prophet — all evaluated |
| 9-10 | Dashboard | HTML dashboard + Streamlit app |
| 11-12 | Documentation | Policy brief, detailed report, this document, data dictionary, timeline — all in markdown + Word + PDF |

# 12. What Should Happen After This

The system as delivered is a **research prototype**. To move it to
operational use:

1. **PSCA pilots it for a quarter.** Compare top-15 forecasts to
 actual incidents.
2. **Build access controls.** Login required, role-based access, audit
 log of every page view (documented but not built).
3. **Refresh schedule.** Nightly cron to refresh `minority_incidents`,
 re-run features, re-train models, regenerate dashboards.
4. **Connect a social-media feed.** Activate the sentiment predictor.
5. **Quarterly community review.** Schedule sit-downs with
 community organizations.
6. **Replicate in other provinces.** If it works in Punjab, the same
 pattern can be applied in Sindh, KP, Balochistan.

# 13. Closing

A predictive system for minority-targeted crime in Pakistan is a
sensitive thing to build. It has the potential to *protect*
communities — and the same machinery has the potential to *target*
them if misused.

This project tries to thread that needle:

- Be honest about what the model can and cannot do.
- Build privacy in from day one, not as an afterthought.
- Document every decision in plain language.
- Treat the dashboard as a *human decision-support tool*, not as a
 judge.

The 4,110 cases in our dataset represent 4,110 real moments where a
real person was scared enough to call the police. The least we can do
with that data is use it carefully, transparently, and toward the goal
of fewer such moments in the future.

---

*This document is an updated edition of the original Research Design
Report from PSCA, reflecting what was
actually built across the project. For implementation details, see
`02_detailed_report` and the model cards in the full project archive.*
