"""PawPal+ logic layer.

Backend classes for the pet care planning assistant. This is the "logic layer"
that the Streamlit UI (app.py) imports and calls.

Structure:
    Owner  has many  Pet  has many  Task
    Scheduler is the "brain" that reaches across all of an Owner's pets to
    retrieve, organize, and manage their tasks.
"""

from dataclasses import dataclass, field


# Sort weight for priorities is not part of this design; tasks are organized by
# frequency and completion. Frequencies we understand, ordered for display.
FREQUENCY_ORDER = {"daily": 0, "weekly": 1, "monthly": 2}


@dataclass
class Task:
    """A single pet care activity (walk, feeding, meds, grooming, ...)."""

    description: str
    time: str = ""                 # time of day the task happens, e.g. "08:00"
    frequency: str = "daily"       # "daily" | "weekly" | "monthly"
    completed: bool = False        # completion status

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Reset this task back to not-done (e.g. for a new day)."""
        self.completed = False

    def __str__(self) -> str:
        """Return a one-line, human-readable summary of the task."""
        box = "x" if self.completed else " "
        return f"[{box}] {self.time} {self.description} ({self.frequency})"


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
