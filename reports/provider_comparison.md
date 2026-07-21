# Provider Comparison

Verified on 2026-07-21. Feeds with a URL were fetched live and parsed as valid iCalendar.

| Category | Provider | Strategy | Official | Price | Cadence | Confidence | Live URL |
|---|---|---|---|---|---|---|---|
| holidays-awareness | Google Official — UK Holidays | subscribe | yes | free | auto (zero maintenance) | high | yes |
| holidays-awareness | Google Official — US Holidays | subscribe | yes | free | auto (zero maintenance) | high | yes |
| holidays-awareness | gov.uk Bank Holidays (JSON) — validation source | reference | yes | free | auto | high | yes |
| combat-sports | clarencechaan/ufc-cal (UFC, scraped from ufc.com) | subscribe | no | free | auto (updated multiple times daily) | high | yes |
| uk-sporting | Custom curated (seed: sporting-events.org + VisitBritain + official sites) | custom | no | free | yearly refresh (~1-2h) | high | — |
| us-sporting | Custom curated (seed: ESPN public API + official event sites) | custom | no | free | yearly refresh + mid-season playoff check | high | — |
| global-sporting | Custom curated (seed: governing bodies + Wikipedia '202X in sport') | custom | no | free | yearly refresh (~30 min) | high | — |
| gaming | Custom curated (seed: IGDB API + Wikipedia '20XX in video games') | custom | no | free (IGDB non-commercial only — ToS flag for agency use) | yearly + quarterly launch re-pull | medium | — |
| entertainment-pop-culture | Custom curated + AddEvent award feed (feeder) | hybrid | no | free | yearly refresh | medium | yes |
| music-festivals | Custom curated (seed: official festival sites + Music Festival Wizard) | custom | no | free | yearly refresh + mid-year check | high | — |
| shopping-events | Custom generated (deterministic weekday rules) | custom | no | free | yearly (mostly rule-based, near-zero effort) | high | — |
| technology-social-media | Custom curated + Techmeme events feed (radar) | hybrid | no | free | yearly refresh | high | yes |
| space-science | Custom curated (astronomy) + Launch Library 2 (launches) | hybrid | no | free | yearly (astronomy) + weekly launch check if included | high | yes |
| motorsport | f1calendar.com — F1 race-only feed | hybrid | no | free | auto (F1) + yearly refresh (other series) | high | yes |
