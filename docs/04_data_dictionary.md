---
title: "District Dataset and Data Dictionary Report"
subtitle: "Updated Edition — Every Column Explained in Plain Language"
author: "Internship Project — Minorities Early-Warning System"
date: "June 2026"
geometry: margin=2cm
fontsize: 11pt
toc: true
---

# A note on the placeholders in this document

This is the **public release** of the data dictionary. Internal PSCA
schema details (source database names, exact column names of the
Emergency-15 case log) have been replaced with generic placeholders
in angle brackets — for example `<source_call_log_table>`,
`<category_lvl2>`, `<case_id>`. The methodology, structure, and
field meanings are unchanged; only the institutional names have been
genericized so the document is safe to share publicly.

If you receive the full project bundle as a trusted recipient, the
internal data dictionary in that bundle uses the real names.

# Plain-Language Summary First

If you're new to this kind of document, here's what it is:

> A **data dictionary** is just a list of every column in a table,
> what's in it, what it means, and where it came from. It's like the
> table of contents at the front of a book — you can look up anything
> without reading the whole book.
>
> This document is the data dictionary for the working table at the
> heart of the Minorities Early-Warning System. The table is called
> `minority_incidents`, and it has **4,110 rows** (one row per phone
> call to PSCA's Emergency-15 helpline involving a religious minority)
> and **23 columns** (different pieces of information about each call).
>
> The document also explains the **district-level severity dataset**
> — a summary CSV that aggregates the 4,110 calls up to the district
> level and assigns each district a severity rating (Low / Medium /
> High / Critical).

# 1. The Working Table — `minority_incidents`

## 1.1 Where it lives

| Field | Value |
|---|---|
| Database | `<analytics_db>` (PostgreSQL) |
| Table name | `minority_incidents` |
| Rows | 4,110 |
| Columns | 23 |
| Built from | `<source_call_log_table>` (a 5.7-million-row source) |
| Build script | the incidents-table build script |

## 1.2 What's in it

Each row is one phone call to Emergency-15 where the call satisfies
**either** of these two filters:

1. The operator tagged the call as a **"Religious Offence"** in the
 case-nature hierarchy, **OR**
2. The caller's description **mentions a minority community by name**
 (Christian, Ahmadi, Hindu, Sikh) or a place of worship (church,
 temple, gurdwara) or a religious-accusation keyword (blasphemy).

This is a deliberately wide filter — we'd rather pick up too many
cases than miss real ones. A stricter label (`is_minority_targeted`)
is provided as a column so downstream code can filter to only the
high-confidence positives.

## 1.3 Quick numbers

| Slice | Count | % of total |
|---|---|---|
| All rows | 4,110 | 100% |
| Rows from Lahore | 928 | 22.6% |
| Strict-label minority-targeted | 312 | 7.6% |
| With valid GPS coordinates | 3,281 | 79.8% |
| Year 2024 | 1,450 | 35% |
| Year 2025 | 2,117 | 52% |
| Year 2026 (Jan–June) | 525 | 13% |

# 2. Column-by-Column Walkthrough

There are 23 columns. We group them into 6 logical buckets to make it
easier to follow.

## 2.1 Identifier columns (3)

These uniquely identify each row in the table.

### `id` — Internal database ID

| Property | Value |
|---|---|
| Type | Integer (auto-increment) |
| Example | `1234` |
| What it means | A unique number assigned to each row when it was loaded. Has no meaning outside this table — it's just a row-counter. |
| Why it's here | So that other tables (predictions, features) can link back to a specific row. |

### `<case_id>` — Official PSCA case reference

| Property | Value |
|---|---|
| Type | Text |
| Example | `LHR-20260615-323147436` |
| What it means | The official case identifier assigned by Emergency-15 when the call was logged. Same format as PSCA uses elsewhere. |
| Why it's here | So a human analyst can look up the same case in PSCA's other systems. |
| Privacy note | **This is internal PSCA reference data. Do not share publicly.** |

### `<dispatch_id>` — PSCA system lead ID

| Property | Value |
|---|---|
| Type | Text |
| Example | `15612345` |
| What it means | Another PSCA-internal identifier, used for cross-referencing with the lead-management system. |

## 2.2 Time columns (4)

When did the incident happen?

### `incident_date` — The day the case was reported

| Property | Value |
|---|---|
| Type | Date (YYYY-MM-DD) |
| Example | `2026-06-15` |
| What it means | The calendar date the call was placed. |
| Source | `<source_call_log_table>.date` (parsed from text) |

### `<received_time>` — Exact timestamp the call was accepted

| Property | Value |
|---|---|
| Type | Timestamp (YYYY-MM-DD HH:MM:SS) |
| Example | `2026-06-15 14:23:08` |
| What it means | The exact second the call was picked up by an operator. |
| Used for | Computing "prior 30 days" counts — we use this for strict temporal ordering. |

### `incident_year`, `incident_month` — Numeric breakouts

| Property | Value |
|---|---|
| Type | Integer |
| Example | `2026`, `6` |
| What it means | Year (4 digits) and month (1–12) extracted from `incident_date`. Convenience columns to make grouping by year/month easy. |

## 2.3 Location columns (7)

Where did the incident happen?

### `district_id` — Numeric district identifier

| Property | Value |
|---|---|
| Type | Text (numeric string) |
| Example | `40` (Lahore), `25` (Multan) |
| What it means | The Emergency-15 system's district identifier. The same system is used across PSCA, the police boundaries database, and Emergency-15 dispatch. |
| Lookup | Use `<station_boundaries_ref>.district_id` to resolve. |

### `district_name` — Human-readable district name

| Property | Value |
|---|---|
| Type | Text |
| Example | `Lahore`, `Multan`, `Faisalabad` |
| Source | Resolved from `district_id` via the `<station_boundaries_ref>` table |

### `police_station_id` — Specific police station code

| Property | Value |
|---|---|
| Type | Text (numeric string) |
| Example | `657` |
| What it means | The Emergency-15 identifier for the specific police station responsible for this geographic area. Punjab has 656 such police stations. |

### `police_station` — Human-readable PS name

| Property | Value |
|---|---|
| Type | Text |
| Example | `Mughalpura`, `Old Anarkali`, `Garhi Shahu` |

### `lat`, `long` — GPS coordinates of the incident

| Property | Value |
|---|---|
| Type | Floating-point number |
| Example | `lat: 31.5615`, `long: 74.3095` |
| What it means | Latitude and longitude where the caller's phone said they were. Some are exact incident locations; some are police-station centroids (when the caller location couldn't be determined). |
| Coverage | About 80% of rows have valid coordinates. The rest have `NULL` for these fields. |
| Privacy note | These are precise to ~3 decimal places, about 100 meters. Anyone with the lat/long can pinpoint a house. For external presentation, consider rounding to 3 decimals (~110m) to reduce precision. |

### `is_lahore` — Quick boolean: is this row from Lahore?

| Property | Value |
|---|---|
| Type | Boolean (TRUE / FALSE) |
| Derived from | `district_id = '40'` |
| Why it exists | Lahore is the focal city of the project. Having a boolean makes filtering trivially fast. |

## 2.4 Case-nature taxonomy (3)

What kind of case is this?

PSCA's case-nature hierarchy has 3 levels — broad to specific.

### `<category_lvl1>` — Top-level category

| Property | Value |
|---|---|
| Type | Text |
| Examples | `Crime Against Person`, `Crime Against Property`, `Law & Order`, `Other Help` |
| Notes | A handful of high-level buckets, ~12 distinct values. |

### `<category_lvl2>` — Mid-level category

| Property | Value |
|---|---|
| Type | Text |
| Most relevant example | `Religious Offences` |
| Other examples | `Theft`, `Robbery/Snatching`, `Assault`, `Public Disorder` |
| Notes | Roughly 40 distinct values. **`Religious Offences` is the critical one for this project.** |

### `<category_lvl3>` — Most specific category

| Property | Value |
|---|---|
| Type | Text |
| Examples (under Religious Offences) | `Any Other Religious Issue`, `Defiling of Holy Book`, `Derogation of Holy Persons`, `Distribution / Display of hateful sectarian material`, `Hate Speech`, `Attack/Damage of Religious Places (Church/Mosque/Gurdwara/Mundar/Imambargah/Mazzar)` |
| Notes | ~150 distinct values. The 6 listed above are all the Level-3 sub-categories of "Religious Offences". |

## 2.5 Free text + derived signals (5)

The caller's verbatim words and the things we extracted from them.

### `description` — Caller's verbatim words

| Property | Value |
|---|---|
| Type | Text (up to 2000 characters) |
| Example | `"caller reported some persons broke the Christmas decorations need help"` |
| What it is | The operator's verbatim transcription of what the caller said. Often a mix of English, Urdu (transliterated), and operational shorthand. |
| Privacy warning | **Contains phone numbers, addresses, individual names, CNIC numbers, and call-center metadata.** It is auto-redacted before reaching any dashboard, but the raw column in this table is **the original unredacted text**. Do not share publicly. |
| What's done with it | The system extracts community keywords from this field to derive `minority_community`. The dashboard displays a redacted preview (and only when explicitly toggled on). |

### `match_source` — How did this row qualify?

| Property | Value |
|---|---|
| Type | Text (enum) |
| Possible values | `religious_offence`, `desc_keyword`, `both` |
| What it means | Tells you *which* of the two filter clauses this row satisfied. `religious_offence` = formally tagged. `desc_keyword` = caught only by description text. `both` = both — the highest-confidence subset. |
| Distribution | religious_offence: 2,463 (60%) · desc_keyword: 1,312 (32%) · both: 335 (8%) |

### `matched_keywords` — Which words triggered the keyword filter

| Property | Value |
|---|---|
| Type | Text array |
| Example | `{christian, blasphemy}` |
| What it means | Every minority-community or blasphemy-related word the regex found in the description. |

### `minority_community` — Inferred community

| Property | Value |
|---|---|
| Type | Text (enum) |
| Possible values | `christian`, `ahmadi`, `hindu`, `sikh`, `multiple`, `unspecified` |
| Distribution | unspecified: 2,530 · christian: 1,305 · ahmadi: 166 · hindu: 58 · sikh: 47 · multiple: 4 |
| How it's inferred | A case-insensitive regex over the description. `christian` matches "christian", "christians", "church", "pastor", "masihi". `ahmadi` matches "ahmadi", "qadiani", "ahmedi". And so on. |
| `unspecified` meaning | The description doesn't name a community. It doesn't mean the case is *not* minority-related — it might just not say the community out loud. |

### `is_minority_targeted` — The STRICT label

| Property | Value |
|---|---|
| Type | Boolean (TRUE / FALSE) |
| Definition | `<category_lvl2> = 'Religious Offences' AND minority_community IN ('christian', 'ahmadi', 'hindu', 'sikh', 'multiple')` |
| Distribution | TRUE: 312 (7.6%) · FALSE: 3,798 (92.4%) |
| Why it matters | **This is the target the prediction models learn from.** It's the high-confidence "yes, this is minority-targeted" subset. |

## 2.6 Metadata (1)

### `loaded_at` — When this row was loaded

| Property | Value |
|---|---|
| Type | Timestamp |
| Example | `2026-06-22 12:33:45.428463` |
| What it means | When the build script populated this row. Useful for audit ("when did we last refresh?"). |

# 3. The District-Level Severity Dataset

Alongside the case-level `minority_incidents` table, the system
produces a smaller summary CSV: `<see project intermediate data>`.
This aggregates all 4,110 cases up to the district level and assigns
each district a severity rating.

## 3.1 What's in it

| Column | Type | Example |
|---|---|---|
| District | Text | `Lahore`, `Faisalabad` |
| Total Cases | Integer | `928`, `381` |
| Severity_level | Text | `Critical`, `High`, `Medium`, `Low` |
| Reporting Period | Text | `Current Dataset (2024 → 2026 YTD)` |

## 3.2 How severity is assigned

| Cases | Severity |
|---|---|
| 0 – 50 | Low |
| 51 – 150 | Medium |
| 151 – 300 | High |
| 300 + | Critical |

These bands come from the original Research Design Report. We use
them unchanged for compatibility.

## 3.3 What it shows

| District | Cases | Severity |
|---|---|---|
| **Lahore** | 928 | **Critical** |
| **Faisalabad** | 381 | **Critical** |
| **Sheikhupura** | 282 | **High** |
| **Sialkot** | 258 | **High** |
| **Gujranwala** | 233 | **High** |
| Bahawalpur, Multan, Rahim Yar Khan… | 50–150 | Medium |
| Smaller districts | < 50 | Low |

## 3.4 Caveat about the severity bands

These bands are **count-based**, not intensity-based. A district with
194 minor public-disorder calls is rated the same severity as a
district with 194 mosque attacks — even though those are operationally
very different.

The policy brief explicitly flags this as a recommendation for the
next version: split "volume severity" from "intensity severity".

# 4. Six More Tables Derived From This One

The case-level `minority_incidents` table is the foundation. Six
feature tables, one per predictor family, are derived from it (and
from external calendars):

| Table | Rows | Cols | What it adds |
|---|---|---|---|
| `minority_features_prior_density` | 4,110 | 11 | Rolling case counts at PS and district level |
| `minority_features_religious_calendar` | 4,110 | 12 | Days to / since major religious events |
| `minority_features_political_calendar` | 4,110 | 7 | Political event proximity |
| `minority_features_misinformation` | 4,110 | 7 | Misinformation event flags |
| `minority_features_responsiveness` | 4,110 | 6 | Local PS response-time baseline |
| `minority_features_sentiment` | 4,110 | 6 | Placeholder (all NULL until a feed is connected) |
| `minority_features_merged` | 4,110 | **62** | All six joined together — what the models train on |

Each feature table has its own schema file (the per-family schema files)
and its own builder script (the per-family builder scripts).

# 5. Two More Tables For Predictions

| Table | Rows | What it stores |
|---|---|---|
| `minority_predictions` | 4,110 | LR and RF model scores for every case in `minority_incidents` |
| `minority_psweek_train` | 82,000 | Training data for the PS-week forecaster: one row per (police station × week) for 2024-2026 |
| `minority_psweek_forward` | 656 | Current forward prediction for every PS — risk of an incident in the next 30 days |

# 6. Known Data-Quality Issues

We catalog these honestly:

1. **The descriptions are operational, not analytical.** They mix
 English, Urdu, Roman Urdu, and operator shorthand. Spelling is
 inconsistent. The keyword extractor catches the obvious patterns
 but will miss creative spellings.

2. **"Unspecified" doesn't equal "not minority-related".** Many cases
 have a generic description without a community name — the operator
 was busy, the caller didn't say, or they used "they/those people"
 instead of naming a community. These cases are still in the table.

3. **About 20% of rows have NULL or invalid lat/long.** These are kept
 in the count tables but excluded from the map.

4. **Some older lat/longs are police-station centroids, not incident
 locations.** This is a known upstream issue in `<source_call_log_table>`.
 Recent rows (2025-onwards) have better GPS data.

5. **24 rows had coordinates outside Pakistan entirely** (data-entry
 errors — swapped lat/long, zero coords, etc.). These are filtered
 out at the dashboard layer.

6. **Reporting bias is irreducible.** A community that under-reports
 will be under-represented in this dataset. We say this loudly
 throughout the documentation.

# 7. How to Refresh This Table

To re-pull the latest data from the source `<source_call_log_table>` table:

```bash
cd minorities_project
python3 the incidents-table build script
```

The script drops and recreates the table from scratch. It is
**idempotent** — running it twice in a row produces the same table.

To export the latest version to CSV (for the portable bundle):

```bash
python3 the CSV export script
```

# 8. How to Query It Yourself

In `psql`:

```sql
\c db_predictive_policing

-- All Lahore strict-targeted cases this year
SELECT <case_id>, incident_date, police_station, minority_community
FROM minority_incidents
WHERE is_lahore = TRUE
 AND is_minority_targeted = TRUE
 AND incident_year = 2026
ORDER BY incident_date DESC;

-- Top 10 police stations by case count
SELECT police_station, COUNT(*) AS n
FROM minority_incidents
WHERE is_lahore
GROUP BY police_station
ORDER BY n DESC
LIMIT 10;

-- Community breakdown for the strict-label set
SELECT minority_community, COUNT(*)
FROM minority_incidents
WHERE is_minority_targeted
GROUP BY minority_community;
```

In Python:

```python
import pandas as pd
df = pd.read_csv('<see project CSV exports>',
 parse_dates=['incident_date'])
df_lahore = df[df['is_lahore'] == True]
print(df_lahore['minority_community'].value_counts())
```

# 9. References

- **Builder script:** the incidents-table build script
- **DDL (table schema):** the incidents-table schema
- **CSV snapshot:** `<see project CSV exports>`
- **Source table:** `<source_call_log_table>`
- **Boundaries (district / police-station resolution):** `<analytics_db>.<station_boundaries_ref>`

---

*This is the updated edition of the original PSCA "District Dataset
and Data Dictionary Report", reflecting the case-level working table
that powers the Minorities Early-Warning System.*
