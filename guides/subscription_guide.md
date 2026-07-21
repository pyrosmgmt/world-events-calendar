# Subscription & Install Guide

How to add the Pyros World Events calendars to Google Calendar (and Apple/Outlook).

## Two kinds of calendar
1. **Auto-updating feeds** (zero maintenance) — official/third-party feeds we
   subscribe to by URL. They stay current on their own.
2. **Pyros custom calendars** — our curated tentpole calendars, published as
   `.ics` files (hosted or imported). Refreshed once a year.

## A. Subscribe to the auto-updating feeds (recommended for everyone)
In **Google Calendar** (web): left sidebar → **Other calendars** → **＋** →
**From URL** → paste a URL below → **Add calendar**.

| Calendar | URL |
|---|---|
| UK Public Holidays | `https://calendar.google.com/calendar/ical/en.uk%23holiday%40group.v.calendar.google.com/public/basic.ics` |
| US Public Holidays | `https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics` |
| UFC (combat sports) | `https://raw.githubusercontent.com/clarencechaan/ufc-cal/ics/UFC.ics` |
| Formula 1 (per Grand Prix) | `https://files-f1.motorsportcalendars.com/f1-calendar_gp.ics` |

> These update automatically. Google re-checks external URLs on its own schedule
> (typically several hours to a day) — no action needed from you.

## B. Add the Pyros custom calendars
The custom `.ics` files are hosted on GitHub Pages. **Easiest:** open the landing
page and use its copy-link buttons:

**https://pyrosmgmt.github.io/world-events-calendar/**

Or subscribe directly by URL — the pattern is
`https://pyrosmgmt.github.io/world-events-calendar/calendars/<category>.ics`, e.g.
`https://pyrosmgmt.github.io/world-events-calendar/calendars/shopping-events.ics`

**Or** one-time import (does not auto-update): Google Calendar → **Settings** →
**Import & export** → **Import** → choose an `.ics` from the `calendars/` folder →
pick a destination calendar → **Import**.

Custom calendars available: `uk-sporting`, `us-sporting`, `global-sporting`,
`combat-sports` (boxing), `motorsport` (non-F1), `gaming`,
`entertainment-pop-culture`, `music-festivals`, `shopping-events`,
`holidays-awareness` (awareness days), `technology-social-media`, `space-science`.

## C. Apple Calendar / Outlook
- **Apple:** File → New Calendar Subscription → paste the URL.
- **Outlook:** Add calendar → Subscribe from web → paste the URL.

## Notes
- Events marked **[TBC]** in the title have an estimated date not yet officially
  confirmed — verify before building a promotion around them.
- All events include a **Source** link and a **Verified** date in their notes.
