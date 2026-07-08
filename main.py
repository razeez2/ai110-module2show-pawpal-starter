import pawpal_system

if __name__ == "__main__":
    # Create an owner and some pets
    owner = pawpal_system.Owner(name="Alice")
    dog = pawpal_system.Pet(name="Buddy", species="Dog")
    cat = pawpal_system.Pet(name="Whiskers", species="Cat")

    # Add pets to the owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create some tasks for the pets, each at a different time of day
    task1 = pawpal_system.Task(description="Feed Buddy", time="08:00", frequency="daily")
    task2 = pawpal_system.Task(description="Walk Buddy", time="17:30", frequency="daily")
    task3 = pawpal_system.Task(description="Feed Whiskers", time="07:15", frequency="daily", completed=True)
    task4 = pawpal_system.Task(description="Groom Whiskers", time="12:00", frequency="weekly")
    # Deliberate clash: this cat task shares 08:00 with "Feed Buddy" (task1).
    task5 = pawpal_system.Task(description="Medicate Whiskers", time="08:00", frequency="daily")

    # Add tasks to the pets
    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)
    cat.add_task(task4)
    cat.add_task(task5)

    # Create a scheduler for the owner
    scheduler = pawpal_system.Scheduler(owner=owner)

    # Retrieve and print all tasks across all pets, ordered into a daily plan
    print(f"Daily plan:")
    for task in scheduler.organize():
        print(f"  {task}")

    # Warn (don't crash) about tasks competing for the same time slot.
    conflicts = scheduler.find_conflicts()
    if conflicts:
        print("\nScheduling warnings:")
        for warning in conflicts:
            print(f"  ⚠️  {warning}")
    else:
        print("\nNo scheduling conflicts.")
