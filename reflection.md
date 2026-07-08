# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
-   My initial UML design was based on three core actions: adding a profile, adding a task, and getting a plan. I asked AI to help me create classes based on these user actions.
- What classes did you include, and what responsibilities did you assign to each?
    The classes I included include :
    %% Three core user actions map onto the classes below:
    %%   1. Create a profile  -> Owner + Pet
    %%   2. Add a task        -> Task
    %%   3. Get a plan        -> Scheduler produces a Plan

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, i had a classes for "plan' and "scheduledtask" that were deleted/ never used in the final implementation. I had added these classes initially because it seemed like they would have their own individual features before reading the later stage directions. When I got to the later phase, I realized I had too many unneccesary classes. I made owners have pets and pets have tasks, instead of owners having tasks directly because the pets technically need the task.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler mainly considers time , frequency, and pets. I decided which constraint mattered most based on the three core user actions I had planned out.Time and frequency seemd to be the most important for filtering and sorting. The app's purpose was to create an organized plan so these constrains seemed simplest to implement while getting the job done.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
 
 One trade-off is that it sorts tasks by the start time and not duration. So a 30 min task of walking could overlap with a 15 min task of feeding if they have close enough start times. This is reasonable for this scenario because tasks for pets are not generally time-sensitive in terms of duration & may be different everyday depending on the owner's schedule. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    I used claude to help me verify if my brainstorming ideas seemed accurate or valid for what the project was expecting. I also used it to help with logic, debugging, and verification. The prompts that were most helpful were asking it to do something that the assignment instruction said but in a simpler way. It really helped break down backend logic as well.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - it told me to write over the uml.mmd file for the draft uml but I told it to just add draft file as a new file.
    - the "simpler" algorithm change was just one line and the output for the warning of two tasks being at the same times was made friendlier and didnt sound like a warning so I kept the original algorithm.
- How did you evaluate or verify what the AI suggested?
    - testing and consistently re-reading the assignment instructions to see if it was suggesting something expected or unexpected.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested the expected output of scheduling tasks that didn't overlap, overlapped, with different pets, completed tasks, non completed tasks, etc.
- Why were these tests important?
These tests were important as they directly related to the three core user actions and handled major edge cases .

**b. Confidence**

- How confident are you that your scheduler works correctly?
    Im 80% confident it works correctly in the simplest way in terms of filtering and sorting and completing the barebones of the user tasks related to scheduling.
- What edge cases would you test next if you had more time?
    I want to test if duration was implemented & how that would create conflicts. I would also test removing pets or removing tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    I am satisifed with the sorting and filtering part. I think the logic for those took the most time and understanding.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would definitely re design the UI to be more appealing & bold. I would also add more edge cases and options for the tasks and pets.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    AI may oversimplify things sometimes. It may suggest something that doesn't align with your expectations. It is best to be specific when you are prompting AI and not use generic phrases like " simplify " or "making it human-readable".
