"""Tests for the PawPal+ logic layer."""

import os
import sys

# Make the project root importable so `import pawpal_system` works when
# pytest is run from anywhere.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Pet, Task


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
