"""PawPal+ logic layer.

Backend classes for the pet care planning assistant. This is the "logic layer"
that the Streamlit UI (app.py) imports and calls.

Structure:
    Owner  has many  Pet  has many  Task
    Scheduler is the "brain" that reaches across all of an Owner's pets to
    retrieve, organize, and manage their tasks.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta


# Sort weight for priorities is not part of this design; tasks are organized by
# frequency and completion. Frequencies we understand, ordered for display.
FREQUENCY_ORDER = {"daily": 0, "weekly": 1, "monthly": 2}

# How far ahead the next occurrence of a recurring task lands. Only these
# frequencies repeat; anything else (e.g. "monthly", one-offs) does not.
RECURRENCE_STEP = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    """A single pet care activity (walk, feeding, meds, grooming, ...)."""

    description: str
    time: str = ""                 # time of day the task happens, e.g. "08:00"
    frequency: str = "daily"       # "daily" | "weekly" | "monthly"
    completed: bool = False        # completion status
    due_date: date = field(default_factory=date.today)  # when this task is due

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Reset this task back to not-done (e.g. for a new day)."""
        self.completed = False

    def next_occurrence(self) -> "Task | None":
        """Build the next occurrence of a recurring task.

        Returns a fresh, not-yet-completed Task whose due_date is advanced by
        the frequency's step (daily -> +1 day, weekly -> +1 week). Using
        timedelta keeps the math calendar-accurate across month and year
        boundaries. Non-recurring frequencies (e.g. "monthly") return None.
        """
        step = RECURRENCE_STEP.get(self.frequency)
        if step is None:
            return None
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            due_date=self.due_date + step,
        )

    def __str__(self) -> str:
        """Return a one-line, human-readable summary of the task."""
        box = "x" if self.completed else " "
        return f"[{box}] {self.time} {self.description} ({self.frequency}) — due {self.due_date}"


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Detach a task from this pet (no error if it isn't there)."""
        if task in self.tasks:
            self.tasks.remove(task)

    def pending_tasks(self) -> list[Task]:
        """Return this pet's tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    """The owner: manages multiple pets and exposes all their tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner (no error if it isn't there)."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> list[Task]:
        """Flatten and return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The 'brain': retrieves, organizes, and manages tasks across all pets."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler bound to a single owner."""
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Retrieve every task from the owner's pets, via the Owner."""
        return self.owner.get_all_tasks()

    def tasks_by_pet(self) -> dict[str, list[Task]]:
        """Group tasks by the pet they belong to (pet name -> tasks)."""
        return {pet.name: list(pet.tasks) for pet in self.owner.pets}

    def pending_tasks(self) -> list[Task]:
        """All not-yet-completed tasks across every pet."""
        return [t for t in self.get_all_tasks() if not t.completed]

    def tasks_for_frequency(self, frequency: str) -> list[Task]:
        """All tasks matching a given frequency (e.g. 'daily')."""
        return [t for t in self.get_all_tasks() if t.frequency == frequency]

    def tasks_for_pet(self, name: str) -> list[Task]:
        """All tasks belonging to a single pet, looked up by name (case-insensitive)."""
        return [
            task
            for pet in self.owner.pets
            if pet.name.lower() == name.lower()
            for task in pet.tasks
        ]

    def complete_task(self, task: Task) -> "Task | None":
        """Mark a task done and auto-schedule its next occurrence.

        If the task recurs (daily/weekly), a fresh Task for the next date is
        added to the same pet's task list and returned. Idempotent: completing
        an already-completed task is a no-op and returns None, so repeated UI
        reruns can't spawn duplicate future tasks.
        """
        if task.completed:
            return None
        task.mark_complete()
        upcoming = task.next_occurrence()
        if upcoming is not None:
            for pet in self.owner.pets:
                if task in pet.tasks:
                    pet.add_task(upcoming)
                    break
        return upcoming

    def organize(self) -> list[Task]:
        """Return all tasks ordered: pending first, then by time of day, then frequency."""
        return sorted(
            self.get_all_tasks(),
            key=lambda t: (
                t.completed,
                t.time,  # zero-padded "HH:MM" strings sort chronologically
                FREQUENCY_ORDER.get(t.frequency, 99),
            ),
        )

    def find_conflicts(self) -> list[str]:
        """Detect tasks that share the same time slot and return warnings.

        Lightweight strategy: group every scheduled task (those with a time
        set) by its "HH:MM" time, across all pets. Any slot holding more than
        one task is a conflict. Returns a list of human-readable warning
        strings (empty if there are none) and never raises — the caller decides
        whether to print, log, or ignore them.
        """
        by_time: dict[str, list[str]] = {}
        for pet in self.owner.pets:
            for task in pet.tasks:
                if not task.time:
                    continue  # unscheduled tasks can't clash on time
                by_time.setdefault(task.time, []).append(
                    f"{task.description} ({pet.name})"
                )

        warnings: list[str] = []
        for time, labels in sorted(by_time.items()):
            if len(labels) > 1:
                warnings.append(
                    f"Conflict at {time}: " + ", ".join(labels)
                )
        return warnings

    def todays_plan(self, day: date | None = None) -> list[Task]:
        """Organized tasks that are due today or overdue.

        Future occurrences (e.g. a daily task's copy spawned for tomorrow when
        you complete today's) are hidden until their day arrives, so the plan
        stays focused on what's actually actionable now. Defaults to today.
        """
        day = day or date.today()
        return [t for t in self.organize() if t.due_date <= day]
