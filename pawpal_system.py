"""PawPal+ logic layer.

Backend classes for the pet care planning assistant. This is the "logic layer"
that the Streamlit UI (app.py) will import and call. Skeleton only — method
bodies are stubs to be implemented in later steps.

Class map (from diagrams/uml_draft.mmd):
    Owner + Pet         -> create a profile
    Task                -> add a task
    Scheduler -> Plan -> ScheduledTask  -> get a plan
"""

from dataclasses import dataclass, field


@dataclass
class Pet:
    """Basic info about the pet being cared for."""

    name: str
    species: str


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, etc.)."""

    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"

    def priority_rank(self) -> int:
        """Return a sortable integer for this task's priority (higher = more urgent)."""
        raise NotImplementedError


@dataclass
class ScheduledTask:
    """A task placed into the plan at a specific time, with a reason."""

    task: Task
    start_time: str
    reason: str


@dataclass
class Plan:
    """The generated daily plan: scheduled tasks plus what got skipped."""

    items: list[ScheduledTask] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)
    total_minutes: int = 0

    def explain(self) -> str:
        """Return a human-readable explanation of why the plan looks the way it does."""
        raise NotImplementedError


@dataclass
class Owner:
    """The pet owner: profile info, constraints, and their tasks."""

    name: str
    available_minutes: int
    preferences: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this owner's list."""
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a task from this owner's list."""
        raise NotImplementedError


class Scheduler:
    """Builds a daily Plan from an owner's tasks and time budget."""

    def __init__(self, tasks: list[Task], available_minutes: int) -> None:
        self.tasks = tasks
        self.available_minutes = available_minutes

    def sort_by_priority(self) -> list[Task]:
        """Return the tasks ordered by priority (most urgent first)."""
        raise NotImplementedError

    def generate_plan(self) -> Plan:
        """Fit tasks into the available time by priority and return a Plan."""
        raise NotImplementedError
