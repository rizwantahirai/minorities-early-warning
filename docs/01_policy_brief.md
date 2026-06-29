---
title: "Policy Brief — A Computer System That Warns the Police *Before* Religious-Minority Crime Happens"
subtitle: "Punjab Safe Cities Authority · Minorities Early-Warning System"
author: "Internship Project — Minorities Early-Warning System"
date: "June 2026"
geometry: margin=2cm
fontsize: 11pt
---

## What this is, in one paragraph

Imagine that every time someone in Punjab calls the police because a
minority community (a Christian, an Ahmadi, a Hindu, or a Sikh family)
is being threatened or attacked, that phone call is recorded in a big
notebook. We have access to **about 4,100 such phone calls** from
January 2024 onwards. This project is a computer system that **reads
those past phone calls and learns the pattern** of when and where these
incidents happen. Once it has learned the pattern, it can do two useful
things:

1. **Score every new phone call**, telling the police *"this one looks
 like a minority-targeted attack — pay extra attention"*.
2. **Look ahead at the next 30 days**, telling the police *"this
 particular police-station's area is at higher risk — send a patrol
 there even before any call comes in"*.

This brief explains what the system does, what it found, and what we
recommend the Punjab Safe Cities Authority (PSCA) do next.

---

## Why we built this

Today, the police react. Someone calls the **Emergency-15 helpline**
(Punjab's equivalent of "dialling 911" in the US or "1122" elsewhere in
Pakistan), an operator takes the details, and a response unit is sent
to the location. This is reactive — the incident has already happened
by the time the system gets involved.

Researchers at PSCA noticed a pattern: incidents involving religious
minorities **don't happen randomly**. They cluster:

- **Around specific neighbourhoods** — the same police-station areas
 show up over and over (for example: *Mughalpura* and *Garhi Shahu* in
 Lahore, *Dijkot* in Faisalabad, *Moutra* in Sialkot).
- **Around specific dates** — religious holidays like Christmas,
 Muharram, Eid, Holi, and Diwali see spikes in calls.
- **Around political events** — elections and major announcements seem
 to coincide with rising community tensions.
- **After misinformation goes viral** — a fake claim spreading on
 social media often precedes a real incident on the ground.

If incidents follow these patterns, then in principle, a computer can
*detect* the patterns and **warn the police a few days early**. That is
exactly what this system does.

---

## What we did, step by step

### Step 1 — Collected the data

We extracted **4,110 phone calls** from the Emergency-15 database where
the call involved one of these:

- The operator tagged the call as a *Religious Offence*
- OR the caller mentioned a minority community by name in their
 description of the incident
- OR the caller mentioned a place of worship (a church, a temple, a
 *gurdwara*) or a religious accusation (like *blasphemy*)

About **928 of these 4,110 calls came from Lahore alone** — which is
why Lahore is the focus of this project.

### Step 2 — Labelled each call

For each of the 4,110 calls, we asked: *was this incident clearly a
minority-targeted attack, or could it have been something else?* When
the operator tagged it as Religious Offence AND the caller named a
specific minority community (Christian / Ahmadi / Hindu / Sikh), we
called it **"strict-label minority-targeted"** — meaning we are
confident it was. **312 calls** fall into this strict category.

### Step 3 — Built features (clues) the computer can use

For each call, we collected six kinds of clues:

1. **History of nearby calls** — how many similar calls came from the
 same neighbourhood in the last 30, 60, 90 days? (If a place has been
 tense recently, that's a clue.)
2. **Religious calendar** — how many days until the next Christmas /
 Eid / Muharram / Holi? (Incidents spike near these dates.)
3. **Political calendar** — was there a recent election or protest? (Politics raises tensions.)
4. **Misinformation events** — was there a recent fake viral claim in
 the same district? (These often precede violence.)
5. **Police response speed in that area** — how fast does the local
 police station usually respond? (Slow response = more vulnerable.)
6. **Social media sentiment** — how negative are recent posts about
 minorities in that area? (Currently a placeholder — we don't have a
 feed connected yet, but the system is ready to use it when one is
 available.)

### Step 4 — Trained three computer models

A "model" is a math program that learns patterns from past data. We
built three of them, each answering a different question:

| Model | Question it answers |
|---|---|
| **Per-case classifier** | *"This call just came in. Is it likely a minority-targeted attack?"* |
| **PS-week forecaster** | *"For each police-station area, will an attack happen there in the next 30 days?"* (This is the actual *early warning*.) |
| **Volume forecaster (Prophet)** | *"How many minority-related cases should we expect across Punjab next month?"* |

Each model was trained on calls from 2024 and 2025, then tested on 2026
calls (data the model had never seen) to make sure it actually works on
fresh examples.

---

## What the system found

### Finding 1 — The model works

On the 2026 test data (which the model never saw during training):

- The per-case classifier ranks cases well on held-out 2026 test data
 (**ROC AUC 0.84**) and **catches about 93% of the cases that were truly
 minority-targeted** (recall). Because such cases are rare it casts a wide
 net, so only a minority of everything it flags is targeted — about **1 in
 5 of its top-ranked cases** (precision@20), several times the base rate.
 It is a triage aid a human reviews, not an autonomous decider.
- The early-warning forecaster, when it ranks all 656 Punjab police
 stations by 30-day risk, picks **about 18× more true high-risk areas
 than random guessing would** in its top-50 list.
- The volume forecaster predicts next-month total Punjab volume with
 **9.54% average error** — the best precision of any of the three.

### Finding 2 — Religious dates really do drive incidents

**1 in 5 minority-related incidents (18.9%)** happen within ±1 day of a
major religious holiday. The single biggest spike we saw was on
**December 25, 2025 (Christmas Day)** — five different districts logged
Christian-targeted incidents the same day.

### Finding 3 — The same neighbourhoods keep appearing

Six police-station areas account for an outsized share of incidents:

| Police Station | District | Why it matters |
|---|---|---|
| Mughalpura | Lahore | Largest cluster of strict-label cases |
| Chung | Lahore | Repeat incidents over months |
| Kahna | Lahore | Repeat incidents, model gives it 0.99 risk for next 30 days |
| Garhi Shahu | Lahore | Same |
| Dijkot | Faisalabad | Cited in the original Research Design Report |
| Moutra | Sialkot | Same |

### Finding 4 — Top driving signals

When we asked the model *"which clues were most important?"*, the answer
was:

1. The category the operator assigned the call (the strongest signal,
 but obvious — if the operator already tagged it as religious, that
 tells us a lot)
2. How quickly the local police station has been responding in the last
 3 months (slower response → higher risk area)
3. The number of similar calls from the same area in the last 90 days
 (history repeats)
4. Days until the next major religious or political event

---

## What we recommend

For **Punjab Safe Cities Authority (PSCA)**:

1. **Use the system weekly.** Every Monday, take the top-15 highest-risk
 police-station areas the forecaster identifies and brief the field
 commanders. Position extra patrols there for the week.
2. **Pre-position force for known calendar dates.** Christmas, Eid, Holi,
 Diwali, Muharram, Ashura, and Easter — these are the days when
 minority-targeted incidents spike. Build a standing "festive
 security plan" using the model's per-event risk scores.
3. **Track the model's predictions over time.** Each quarter, compare
 what the model predicted to what actually happened. If accuracy
 drops, retrain.

For **the Information and Media authorities**:

4. **Treat viral misinformation about minorities as a measurable
 predictor.** The model already uses this signal. Building a small
 monitoring desk (1-2 staff) to flag known patterns — fake blasphemy
 accusations, false claims about minority community businesses, etc.
 — would feed the early-warning system in real time.

For **PSCA's Virtual Center for Minorities (VCM)**:

5. **Keep recording the free-text descriptions of every call.** They are
 the single most valuable signal — more useful than the formal
 category tag. The model uses keywords from the descriptions to
 classify cases.
6. **Establish a monthly data-sharing handshake** with the early-warning
 system. Right now data is exported manually; a monthly automated
 refresh would keep the model current.

For **minority community organizations**:

7. **Engage with how the model is built and reviewed.** The system is
 designed to *protect* minority communities, but a model trained on
 crime reports can also be misused. Civil-society review of how
 results are used is essential.

---

## What we need to be honest about (limitations)

This system has real limitations that anyone using it must know:

1. **It predicts *reports*, not *incidents*.** Communities that have
 low trust in the police report fewer incidents. The model will
 therefore under-warn for those very communities. **A "low risk
 score" does NOT mean "low actual risk" — it means "low reported risk".**
2. **It is Lahore-heavy.** Because 22.6% of our training data comes
 from Lahore, the model's top picks lean toward Lahore. Other districts
 like Sialkot and Faisalabad show up further down the list, even though
 incidents there have been historically severe.
3. **It is a triage and planning tool — not evidence.** A high risk
 score for a place or a person is a *hypothesis*, not a finding. Any
 operational action based on these scores must be reviewed by a human
 analyst.
4. **It must never be used against minorities.** The whole purpose is
 to *protect* communities, not to target them. Risk scores must never
 be used as a basis for suspecting or detaining members of a minority
 community.

---

## Next steps

1. **Pilot for one quarter** — run the system in parallel with current
 PSCA operations for 3 months. Compare the system's top-15 weekly
 recommendations with where incidents actually happen.
2. **Quarterly review** — sit down with minority-community
 representatives, look at false positives, look at what was missed,
 and adjust.
3. **Open-source the methodology** (not the underlying case data) so
 other provinces and similar systems globally can learn from it.
4. **Connect a social-media monitoring feed** to activate the sentiment
 predictor we already have wired up.

---

## A note for the reader who isn't technical

If you've never seen a "model" or "machine learning" before, here is
the simplest way to understand what we did:

> Imagine you are a teacher who has read every minority-related
> Emergency-15 call for two years. You start to notice that calls from
> a certain neighbourhood spike near Christmas. You start to notice
> that one police-station area is mentioned more often than others.
> Over time, your gut becomes good at predicting: *"there's going to be
> trouble in this area next month."*
>
> A computer model is like that teacher — except the computer can read
> all 4,110 calls in five minutes, can spot subtle patterns across many
> dimensions at once, and can give you a numeric confidence score for
> every prediction.
>
> The model doesn't *replace* a human analyst. It does the heavy
> lifting of pattern-spotting so the analyst can focus on the decisions
> that need human judgement.

---

*Authors: Internship project, Minorities Early-Warning System.*
*Last updated: June 2026.*
*For the underlying methodology, see the detailed report and the
model cards in the full project archive.*
