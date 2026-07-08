import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Plan your pets' daily care: build a profile, add tasks, get a plan.")

# --- Session state: create the Owner once, then reuse it across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

owner: Owner = st.session_state.owner


# --- 1. Create a profile (owner + pets) ---
st.header("1. Profile")

owner.name = st.text_input("Owner name", value=owner.name or "Jordan")

with st.form("add_pet_form", clear_on_submit=True):
    st.markdown("**Add a pet**")
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if pet_name.strip():
            owner.add_pet(Pet(name=pet_name.strip(), species=species))
            st.success(f"Added {pet_name}.")
        else:
            st.warning("Give your pet a name first.")

if owner.pets:
    st.write("**Your pets:** " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")


# --- 2. Add a task (to a chosen pet) ---
st.header("2. Add a task")

if not owner.pets:
    st.info("Add a pet before adding tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_names = [p.name for p in owner.pets]
        chosen_pet = st.selectbox("For which pet?", pet_names)
        description = st.text_input("Task description", value="Morning walk")
        col1, col2 = st.columns(2)
        with col1:
            task_time = st.time_input("Time of day")
        with col2:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
        if st.form_submit_button("Add task"):
            if description.strip():
                pet = next(p for p in owner.pets if p.name == chosen_pet)
                pet.add_task(
                    Task(
                        description=description.strip(),
                        time=task_time.strftime("%H:%M"),
                        frequency=frequency,
                    )
                )
                st.success(f"Added '{description}' for {chosen_pet}.")
            else:
                st.warning("Describe the task first.")


# --- 3. Get a plan (Scheduler organizes tasks across all pets) ---
st.header("3. Daily plan")

scheduler = Scheduler(owner=owner)
plan = scheduler.todays_plan()

if not plan:
    st.info("No tasks yet. Add some above, then your plan will appear here.")
else:
    st.caption(
        "Today and overdue only, still-to-do first then by time of day. "
        "Completing a daily/weekly task schedules the next one automatically."
    )
    for i, task in enumerate(plan):
        done = st.checkbox(str(task), value=task.completed, key=f"task_{i}")
        # Keep the underlying Task in sync with the checkbox. Completing via the
        # scheduler auto-adds the next occurrence for recurring tasks; it's
        # idempotent, so reruns while the box stays checked won't duplicate.
        if done:
            scheduler.complete_task(task)
        else:
            task.mark_incomplete()

    pending = scheduler.pending_tasks()
    st.metric("Tasks remaining today", len(pending))
