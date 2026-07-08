"""Tests for the PawPal+ logic layer."""

import os
import sys

# Make the project root importable so `import pawpal_system` works when
# pytest is run from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task from not-done to done."""
    task = Task(description="Feed Buddy", time="08:00")
    assert task.completed is False  # starts incomplete

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a Pet grows that pet's task list by one."""
    pet = Pet(name="Buddy", species="Dog")
    assert len(pet.tasks) == 0  # starts with no tasks

    pet.add_task(Task(description="Walk Buddy", time="17:30"))

    assert len(pet.tasks) == 1


def test_organize_returns_tasks_in_chronological_order():
    """organize() sorts pending tasks by time of day, regardless of add order."""
    pet = Pet(name="Buddy", species="Dog")
    # Added deliberately out of order.
    pet.add_task(Task(description="Walk Buddy", time="17:30"))
    pet.add_task(Task(description="Feed Buddy", time="08:00"))
    pet.add_task(Task(description="Lunch Buddy", time="12:00"))
    scheduler = Scheduler(owner=Owner(name="Sam", pets=[pet]))

    times = [t.time for t in scheduler.organize()]

    assert times == ["08:00", "12:00", "17:30"]        # earliest first


def test_completing_daily_task_schedules_next_day():
    """Completing a daily task adds a fresh copy due one day later."""
    pet = Pet(name="Buddy", species="Dog")
    task = Task(description="Walk Buddy", frequency="daily", due_date=date(2026, 7, 31))
    pet.add_task(task)
    owner = Owner(name="Sam", pets=[pet])
    scheduler = Scheduler(owner=owner)

    upcoming = scheduler.complete_task(task)

    assert task.completed is True
    assert len(pet.tasks) == 2                      # original + next occurrence
    assert upcoming.completed is False
    assert upcoming.due_date == date(2026, 8, 1)    # timedelta rolls the month over


def test_completing_weekly_task_advances_one_week():
    """Completing a weekly task schedules the next one a week out."""
    pet = Pet(name="Buddy", species="Dog")
    task = Task(description="Bathe Buddy", frequency="weekly", due_date=date(2026, 7, 7))
    pet.add_task(task)
    scheduler = Scheduler(owner=Owner(name="Sam", pets=[pet]))

    upcoming = scheduler.complete_task(task)

    assert upcoming.due_date == date(2026, 7, 7) + timedelta(weeks=1)


def test_completing_is_idempotent():
    """Completing an already-done task is a no-op (no duplicate future tasks)."""
    pet = Pet(name="Buddy", species="Dog")
    task = Task(description="Feed Buddy", frequency="daily")
    pet.add_task(task)
    scheduler = Scheduler(owner=Owner(name="Sam", pets=[pet]))

    scheduler.complete_task(task)
    assert len(pet.tasks) == 2

    scheduler.complete_task(task)                   # second call should do nothing
    assert len(pet.tasks) == 2


def test_monthly_task_does_not_recur():
    """Non-recurring frequencies return None and add nothing."""
    pet = Pet(name="Buddy", species="Dog")
    task = Task(description="Vet visit", frequency="monthly")
    pet.add_task(task)
    scheduler = Scheduler(owner=Owner(name="Sam", pets=[pet]))

    upcoming = scheduler.complete_task(task)

    assert upcoming is None
    assert len(pet.tasks) == 1


def test_todays_plan_hides_future_occurrences():
    """todays_plan shows today + overdue, not tomorrow's spawned occurrence."""
    pet = Pet(name="Buddy", species="Dog")
    today = date(2026, 7, 7)
    pet.add_task(Task(description="Walk Buddy", frequency="daily", due_date=today))
    scheduler = Scheduler(owner=Owner(name="Sam", pets=[pet]))

    scheduler.complete_task(pet.tasks[0])           # spawns a copy due 2026-07-08
    plan = scheduler.todays_plan(day=today)

    assert len(pet.tasks) == 2                      # both exist on the pet
    assert len(plan) == 1                           # but only today's shows
    assert plan[0].due_date == today


def test_find_conflicts_flags_same_time_across_pets():
    """Two tasks at the same time (even on different pets) produce a warning."""
    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Whiskers", species="Cat")
    dog.add_task(Task(description="Feed Buddy", time="08:00"))
    cat.add_task(Task(description="Medicate Whiskers", time="08:00"))
    scheduler = Scheduler(owner=Owner(name="Sam", pets=[dog, cat]))

    conflicts = scheduler.find_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
    assert "Feed Buddy" in conflicts[0] and "Medicate Whiskers" in conflicts[0]


def test_find_conflicts_empty_when_times_differ():
    """Distinct times (and unscheduled tasks) yield no warnings, no crash."""
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(Task(description="Feed", time="08:00"))
    pet.add_task(Task(description="Walk", time="17:30"))
    pet.add_task(Task(description="Someday", time=""))   # unscheduled, ignored
    scheduler = Scheduler(owner=Owner(name="Sam", pets=[pet]))

    assert scheduler.find_conflicts() == []
