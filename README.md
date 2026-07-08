# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Daily plan:
  [ ] 08:00 Feed Buddy (daily)
  [ ] 12:00 Groom Whiskers (weekly)
  [ ] 17:30 Walk Buddy (daily)
  [x] 07:15 Feed Whiskers (daily)

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
$ python -m pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.11.3, pytest-9.0.3, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /Users/raabiahazeez/AI110/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 10 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 10%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 20%]
tests/test_pawpal.py::test_organize_returns_tasks_in_chronological_order PASSED [ 30%]
tests/test_pawpal.py::test_completing_daily_task_schedules_next_day PASSED [ 40%]
tests/test_pawpal.py::test_completing_weekly_task_advances_one_week PASSED [ 50%]
tests/test_pawpal.py::test_completing_is_idempotent PASSED               [ 60%]
tests/test_pawpal.py::test_monthly_task_does_not_recur PASSED            [ 70%]
tests/test_pawpal.py::test_todays_plan_hides_future_occurrences PASSED   [ 80%]
tests/test_pawpal.py::test_find_conflicts_flags_same_time_across_pets PASSED [ 90%]
tests/test_pawpal.py::test_find_conflicts_empty_when_times_differ PASSED [100%]

============================== 10 passed in 0.01s ==============================

confidence in system's reliability: 4, handles more edge cases such as weekly recurrence, idempotent completion (no duplicates), monthly tasks not recurring, today's-plan filtering, and the no-conflict case.
```

## 📐 Smarter Scheduling

These are the scheduling features PawPal+ adds on top of just storing tasks. All of
them live in the `Scheduler` (and `Task`) classes in `pawpal_system.py`.

| Feature | Method | What it does |
|---------|--------|--------------|
| Sorting | `Scheduler.organize()` | Puts the day's tasks in a sensible order |
| Filtering | `Scheduler.pending_tasks()`, `tasks_for_pet()`, `tasks_for_frequency()` | Pulls out just the tasks you care about |
| Conflict detection | `Scheduler.find_conflicts()` | Warns when two tasks are set for the same time |
| Recurring tasks | `Scheduler.complete_task()` + `Task.next_occurrence()` | Auto-schedules the next daily/weekly task |
| Today's view | `Scheduler.todays_plan()` | Shows only what's due today or overdue |

### Sorting

`Scheduler.organize()` sorts all of an owner's tasks into a daily plan. Things still
to do come first, then earliest time of day, then by how often the task repeats. It
works by sorting on the task's `"HH:MM"` time string — because the times are written
zero-padded (like `08:00`), plain text order already matches clock order, so no fancy
time parsing is needed.

### Filtering

There are a few small methods that each return just a slice of the tasks:

- `pending_tasks()` — only the tasks that aren't done yet.
- `tasks_for_pet(name)` — only one pet's tasks (name matching ignores upper/lowercase).
- `tasks_for_frequency("daily")` — only tasks that repeat at a given frequency.

Each one just walks the full task list and keeps the ones that match.

### Conflict detection

`Scheduler.find_conflicts()` checks whether two tasks are scheduled for the same time,
even across different pets. It groups every task by its time slot, and if any slot has
more than one task it returns a friendly warning message (for example, *"Conflict at
08:00: Feed Buddy (Buddy), Medicate Whiskers (Whiskers)"*). It only returns text — it
never stops the program — so the app can print the warning and keep going. It's a
lightweight check: it looks for exact same-time matches, not overlapping durations.

### Recurring tasks

When you finish a daily or weekly task, PawPal+ sets up the next one for you.
`Scheduler.complete_task()` marks the task done and then calls `Task.next_occurrence()`,
which builds a fresh copy with its due date pushed forward (one day for daily, one week
for weekly, using Python's `timedelta` so month and year rollovers are correct). One-off
or monthly tasks don't repeat. Completing a task twice won't create duplicates.

### Today's view

`Scheduler.todays_plan()` shows only the tasks due today or already overdue, so a
freshly scheduled "tomorrow" task stays hidden until tomorrow and the list doesn't pile up.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
