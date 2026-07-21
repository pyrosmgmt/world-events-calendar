# Workflow: Publish to Pyros Google Calendar

**Objective:** Get all 12 category calendars into the Pyros Google Calendar account
so the team sees them alongside their own calendars.

There are two mechanisms. **Prefer subscription-by-URL** — it stays auto-updating and
never needs re-importing.

## Option A — Subscribe by URL (RECOMMENDED, auto-updating)
Works for every calendar: the official feeds AND our hosted custom feeds.

In Google Calendar (web): **Other calendars → + → From URL → paste the `.ics` URL →
Add calendar.** Repeat per category. Once hosted, our custom feeds live at:
`https://<org>.github.io/world-events-calendar/<category>.ics`

Zero-maintenance official feeds to add directly:
- UK holidays: `https://calendar.google.com/calendar/ical/en.uk%23holiday%40group.v.calendar.google.com/public/basic.ics`
- US holidays: `https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics`
- UFC (combat sports): `https://raw.githubusercontent.com/clarencechaan/ufc-cal/ics/UFC.ics`

**Caveat:** Google refreshes external URL calendars on *its own* schedule (often
8–24h, sometimes longer). Fine here — our data changes at most yearly.

**Note:** A subscribed URL calendar is *read-only* inside Google and cannot be
re-shared to other accounts by URL. For team-wide visibility either (a) have each
team member subscribe to the same URLs, or (b) use Option B into a shared calendar.

## Option B — Insert events via the API (editable, not auto-updating)
Use when the team wants an **editable, shareable** calendar they own. Because the
connector cannot *create* calendars, the calendars must exist first.

1. In Google Calendar, manually create one calendar per category (e.g.
   "Pyros · Shopping Events") and share it with the team. Do this once.
2. `list_calendars` → record each `calendar_id`.
3. For each event in the generated `.ics` / `events.yaml`, call `create_event`:
   - `summary`, `startTime`, `endTime` (ISO 8601), `allDay` for date-only events,
     `timeZone` for timed events, `description` (source + verified date), `calendarId`.
   - Set `availability: AVAILABILITY_FREE` (informational, shouldn't block time).
4. **Idempotency:** the API assigns its own IDs, so re-running duplicates events.
   Only run Option B on first load; for the yearly refresh, either clear the
   calendar first or switch that calendar to Option A.

## Recommendation for Pyros
- Official + hosted custom feeds via **Option A** (subscribe by URL) — auto-updating,
  lowest maintenance, matches the brief's priority.
- Use **Option B** only for any calendar the team wants to actively edit/annotate.
