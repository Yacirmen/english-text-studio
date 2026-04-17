from __future__ import annotations

from typing import Any


SCENARIOS: list[dict[str, Any]] = [
    {
        "title": "Morning Bus Routine",
        "topic": "Daily Life",
        "keywords": ["morning", "bus", "coffee", "routine"],
        "person": "Lina",
        "setting": "the bus stop near her apartment",
        "routine": "She carries a small coffee and checks her plan for the day before the bus arrives",
        "goal": "start the day with a calmer mind",
        "problem": "the first hour used to feel rushed and messy",
        "change": "she now leaves home a little earlier and uses the ride to slow down",
        "detail": "On the way, she notices familiar faces, quiet streets, and the same corner bakery opening its door",
        "result": "she arrives more focused and less irritated by small problems",
        "reflection": "A modest routine can improve the tone of the whole day",
    },
    {
        "title": "Evening Table Talk",
        "topic": "Daily Life",
        "keywords": ["dinner", "family", "evening", "conversation"],
        "person": "Can",
        "setting": "his family's kitchen table",
        "routine": "He helps prepare dinner and listens while everyone shares one detail from the day",
        "goal": "keep evenings warm instead of distracted",
        "problem": "people often ate quickly and moved back to their own screens",
        "change": "he suggested a slower dinner with a short conversation before anyone stood up",
        "detail": "The meal itself is simple, but the talk makes the room feel fuller and more relaxed",
        "result": "the family now remembers small stories that would otherwise disappear",
        "reflection": "Attention can make ordinary moments feel surprisingly rich",
    },
    {
        "title": "Saturday Market Walk",
        "topic": "Daily Life",
        "keywords": ["market", "street", "bag", "weekend"],
        "person": "Mina",
        "setting": "the neighborhood market on Saturday morning",
        "routine": "She walks with a fabric bag, compares prices, and chooses food for the next few days",
        "goal": "turn a basic errand into a slower weekly habit",
        "problem": "shopping used to feel like a chore she wanted to finish immediately",
        "change": "she began going earlier, walking instead of driving, and talking with the same sellers",
        "detail": "Because she pays attention, she notices seasonal fruit, new smells, and the changing pace of the street",
        "result": "the trip feels lighter and more personal than before",
        "reflection": "A repeated task becomes easier when it also gives something back",
    },
    {
        "title": "Library Research Hour",
        "topic": "School",
        "keywords": ["library", "student", "research", "notes"],
        "person": "Eren",
        "setting": "the school library after class",
        "routine": "He gathers two books, opens his notebook, and summarizes the clearest ideas in short lines",
        "goal": "understand the topic instead of copying information",
        "problem": "his first notes were crowded and difficult to review later",
        "change": "he now separates facts, questions, and examples into different sections",
        "detail": "The quieter space helps him notice where his understanding is weak and where it is already solid",
        "result": "studying later takes less time because the notes already have structure",
        "reflection": "Good preparation often begins with better organization, not more pressure",
    },
    {
        "title": "Group Presentation Draft",
        "topic": "School",
        "keywords": ["presentation", "class", "teacher", "draft"],
        "person": "Selin",
        "setting": "a classroom during group work",
        "routine": "She and her classmates build a first draft before deciding which points deserve more space",
        "goal": "make the final presentation clear for the whole class",
        "problem": "each student collected useful material, but their ideas did not connect well",
        "change": "they started with one shared outline and assigned each section more carefully",
        "detail": "Once the structure improved, even nervous students knew what to say and when to say it",
        "result": "the group sounded more confident because the parts finally worked together",
        "reflection": "Collaboration improves when structure arrives early enough to guide the work",
    },
    {
        "title": "Lab Notebook Habit",
        "topic": "School",
        "keywords": ["lab", "notebook", "experiment", "teacher"],
        "person": "Bora",
        "setting": "the science lab at school",
        "routine": "He records each step of the experiment before moving to the next one",
        "goal": "avoid confusion when the class reviews the process later",
        "problem": "he once trusted his memory and forgot the order of an important step",
        "change": "his teacher showed him how a careful notebook can protect accuracy",
        "detail": "Now he writes short observations, marks changes in color or temperature, and dates each page clearly",
        "result": "his lab reports feel more reliable and easier to explain",
        "reflection": "Discipline in small details often prevents larger mistakes",
    },
    {
        "title": "Late Check-In",
        "topic": "Travel",
        "keywords": ["hotel", "travel", "night", "arrival"],
        "person": "Asya",
        "setting": "the lobby of a small hotel after a late flight",
        "routine": "She confirms her booking, asks about transport, and checks the city map before sleeping",
        "goal": "begin the trip without unnecessary confusion",
        "problem": "late arrivals usually leave her too tired to think clearly",
        "change": "she now prepares the first morning in advance instead of improvising when exhausted",
        "detail": "A few minutes of planning gives the unfamiliar place a sense of order before the real exploring begins",
        "result": "the next morning feels calm rather than chaotic",
        "reflection": "Travel becomes easier when decisions are made before stress grows",
    },
    {
        "title": "Rainy City Walk",
        "topic": "Travel",
        "keywords": ["city", "rain", "street", "travel"],
        "person": "Yusuf",
        "setting": "a city center during light afternoon rain",
        "routine": "He walks slowly, changes his route, and lets weather shape the day instead of fighting it",
        "goal": "see the city as it really feels, not only as it appears in guides",
        "problem": "he used to believe a good trip required perfect conditions and a strict plan",
        "change": "he now treats small interruptions as part of the experience",
        "detail": "Rain turns shop windows brighter, quiets the traffic, and reveals a different rhythm in public spaces",
        "result": "the afternoon becomes more memorable because it feels less controlled",
        "reflection": "Unexpected conditions often reveal the strongest parts of a place",
    },
    {
        "title": "Platform Change",
        "topic": "Travel",
        "keywords": ["train", "station", "ticket", "platform"],
        "person": "Duru",
        "setting": "a crowded train station",
        "routine": "She reads the departure board, checks her ticket, and moves quickly when information changes",
        "goal": "handle the journey without panic",
        "problem": "a last-minute platform change once made her miss an important train",
        "change": "since then, she arrives earlier and watches for updates more carefully",
        "detail": "She also studies the station layout in advance so movement feels less confusing under pressure",
        "result": "even busy stations now feel manageable instead of overwhelming",
        "reflection": "Preparation does not remove uncertainty, but it changes how uncertainty feels",
    },
    {
        "title": "Monday Agenda",
        "topic": "Work Life",
        "keywords": ["meeting", "agenda", "office", "team"],
        "person": "Deniz",
        "setting": "a small office on Monday morning",
        "routine": "She writes a short agenda before each meeting and sends it to the team early",
        "goal": "turn discussion into clearer action",
        "problem": "without structure, people left meetings with different ideas about the next step",
        "change": "she limited each session to a few decisions and one visible list of responsibilities",
        "detail": "The work did not become lighter, but the team stopped wasting time on repeated confusion",
        "result": "people now begin the week with sharper focus and better follow-through",
        "reflection": "Clarity is often the fastest form of efficiency",
    },
    {
        "title": "Client Call Preparation",
        "topic": "Work Life",
        "keywords": ["client", "call", "notes", "project"],
        "person": "Arda",
        "setting": "his desk before a client call",
        "routine": "He reviews key decisions, opens the latest project notes, and writes two questions he must not forget",
        "goal": "lead the conversation with confidence instead of reacting at the last second",
        "problem": "earlier calls felt stressful because he depended too much on memory",
        "change": "he now prepares a small briefing page for every important conversation",
        "detail": "That page includes deadlines, unresolved points, and one line about the client's main concern",
        "result": "the call feels more balanced because he can listen without losing direction",
        "reflection": "Preparation creates space for better thinking in real time",
    },
    {
        "title": "Shared Deadline Board",
        "topic": "Work Life",
        "keywords": ["deadline", "project", "board", "team"],
        "person": "Melis",
        "setting": "a project room used by a cross-functional team",
        "routine": "She keeps one shared board with deadlines, owners, and visible blockers",
        "goal": "reduce hidden delays before they become serious",
        "problem": "people were working hard, yet problems often stayed invisible until the last moment",
        "change": "she asked everyone to update the board before the daily check-in",
        "detail": "Once the board became reliable, meetings became shorter because the real issues were already visible",
        "result": "the team still faced pressure, but the pressure stopped feeling shapeless",
        "reflection": "Shared visibility often matters more than constant urgency",
    },
    {
        "title": "School Garden Experiment",
        "topic": "Science",
        "keywords": ["plant", "science", "light", "experiment"],
        "person": "Elif",
        "setting": "a small school garden used for class projects",
        "routine": "She compares how plants respond to different light conditions over several days",
        "goal": "understand how one variable can shape a living system",
        "problem": "at first, the changes seemed too small to say anything useful",
        "change": "she started measuring the same details at the same hour every day",
        "detail": "That consistency made small differences easier to notice and easier to trust",
        "result": "the experiment became clearer because observation became more disciplined",
        "reflection": "Science often depends on patient attention before it produces strong conclusions",
    },
    {
        "title": "Moon Observation Log",
        "topic": "Science",
        "keywords": ["moon", "observation", "night", "pattern"],
        "person": "Kerem",
        "setting": "his apartment balcony at night",
        "routine": "He records the moon's shape, the sky conditions, and the date in a simple log",
        "goal": "see how a pattern becomes visible over time",
        "problem": "single observations felt interesting, but they did not explain much on their own",
        "change": "he turned casual watching into a repeated record with dates and comparisons",
        "detail": "As the pages filled, what once looked random started to look structured and easier to interpret",
        "result": "the night sky felt less distant because it now had a history he could follow",
        "reflection": "Repeated observation can transform curiosity into understanding",
    },
    {
        "title": "Water Filter Test",
        "topic": "Science",
        "keywords": ["water", "test", "material", "result"],
        "person": "Mert",
        "setting": "a classroom table during a science activity",
        "routine": "He compares how different materials affect the clarity of water moving through a simple filter",
        "goal": "learn how method shapes the value of a result",
        "problem": "his first trial mixed too many variables and produced a confusing outcome",
        "change": "he changed only one material at a time and repeated the process more carefully",
        "detail": "The second set of notes was easier to compare because the conditions were more stable",
        "result": "the class could discuss the result with more confidence",
        "reflection": "A result becomes useful when the path toward it is clear enough to examine",
    },
    {
        "title": "Sleep Reset Week",
        "topic": "Health",
        "keywords": ["sleep", "habit", "energy", "routine"],
        "person": "Zeynep",
        "setting": "her evening routine during a busy week",
        "routine": "She puts her phone away earlier, lowers the lights, and reads for a short time before sleep",
        "goal": "wake up with more steady energy",
        "problem": "late scrolling made her mornings heavy and unfocused",
        "change": "she replaced that habit with a smaller, calmer sequence of steps",
        "detail": "The change looked simple from the outside, but it made her body expect rest instead of stimulation",
        "result": "after several days, mornings became easier to start",
        "reflection": "Health improves more reliably when habits are realistic enough to repeat",
    },
    {
        "title": "Lunch Habit Shift",
        "topic": "Health",
        "keywords": ["lunch", "health", "meal", "energy"],
        "person": "Can",
        "setting": "his workday lunch break",
        "routine": "He prepares a simple meal at home and takes water instead of buying something random each day",
        "goal": "feel less tired in the second half of the afternoon",
        "problem": "fast, heavy lunches left him distracted and uncomfortable",
        "change": "he built a routine around smaller portions and more regular timing",
        "detail": "Because the meal became predictable, it stopped demanding attention and started supporting the rest of the day",
        "result": "his focus in the afternoon improved without any dramatic program",
        "reflection": "A good health decision often looks ordinary once it becomes sustainable",
    },
    {
        "title": "Screen Break Routine",
        "topic": "Health",
        "keywords": ["screen", "break", "eyes", "focus"],
        "person": "Asli",
        "setting": "a long study session with her laptop",
        "routine": "She takes short breaks to move, stretch, and look away from the screen at regular times",
        "goal": "protect both focus and comfort during long tasks",
        "problem": "when she worked without pauses, her eyes grew tired and her thinking became dull",
        "change": "she began setting a gentle timer instead of waiting until discomfort forced her to stop",
        "detail": "The pause is brief, but it resets attention before fatigue becomes the main influence on decisions",
        "result": "she now studies longer with less strain",
        "reflection": "Rest can support performance rather than interrupt it",
    },
    {
        "title": "Team Practice Review",
        "topic": "Sport",
        "keywords": ["team", "practice", "coach", "review"],
        "person": "Yusuf",
        "setting": "the gym after team practice",
        "routine": "He stays a few minutes to review what the coach corrected during the session",
        "goal": "turn feedback into progress instead of forgetting it by the next day",
        "problem": "he used to repeat the same mistake because he left practice thinking only about the score",
        "change": "he now writes one note about timing, one about movement, and one about focus",
        "detail": "This tiny review helps him see training as a process rather than a series of isolated drills",
        "result": "improvement feels slower but more reliable",
        "reflection": "Sport rewards reflection when reflection is tied to repeated action",
    },
    {
        "title": "Recovery After the Match",
        "topic": "Sport",
        "keywords": ["match", "recovery", "team", "discipline"],
        "person": "Derya",
        "setting": "the hour after a demanding match",
        "routine": "She cools down properly, drinks water, and listens carefully during the team's short recovery talk",
        "goal": "treat recovery as part of performance rather than an afterthought",
        "problem": "after difficult matches, everyone wanted to leave quickly and ignore what their bodies needed",
        "change": "the new coach made recovery non-negotiable and linked it to the next training session",
        "detail": "Once the team respected that routine, players arrived at later sessions in better condition and with sharper concentration",
        "result": "the quality of practice improved because fatigue was handled more intelligently",
        "reflection": "Discipline after effort is often what protects future performance",
    },
    {
        "title": "New Coach Drill",
        "topic": "Sport",
        "keywords": ["coach", "drill", "focus", "timing"],
        "person": "Kerem",
        "setting": "the first month with a new coach",
        "routine": "He repeats a difficult drill until timing, movement, and attention begin to work together",
        "goal": "understand why precision matters before speed",
        "problem": "the drill seemed frustrating because progress was almost invisible at first",
        "change": "the coach broke the movement into smaller parts and explained the reason behind each one",
        "detail": "That explanation changed the mood of practice because players were no longer imitating a shape they did not understand",
        "result": "the drill became demanding in a useful way instead of a random source of pressure",
        "reflection": "Good coaching often makes discipline feel meaningful rather than merely strict",
    },
    {
        "title": "Quiet Cafe Reflection",
        "topic": "Open",
        "keywords": ["quiet", "cafe", "thought", "focus"],
        "person": "Mina",
        "setting": "a quiet cafe near a side street",
        "routine": "She sits with a notebook, watches the room, and writes a few honest lines before work begins",
        "goal": "create a small space for thought inside a crowded week",
        "problem": "without a pause, her ideas blurred together and lost shape",
        "change": "she stopped expecting a perfect mood and started protecting a short reflective habit instead",
        "detail": "The cafe is not magical, yet its stillness helps her notice which concerns are real and which are only noise",
        "result": "she returns to work with clearer priorities and less emotional clutter",
        "reflection": "A deliberate pause can restore proportion to the rest of the day",
    },
    {
        "title": "Neighborhood Change Walk",
        "topic": "Open",
        "keywords": ["street", "change", "walk", "memory"],
        "person": "Bora",
        "setting": "the neighborhood where he grew up",
        "routine": "He walks the same streets and compares what remains familiar with what has changed",
        "goal": "understand how memory and place influence each other",
        "problem": "he expected the walk to feel comforting, yet parts of it felt strangely distant",
        "change": "instead of resisting that feeling, he paid closer attention to what exactly had shifted",
        "detail": "Old shops were gone, new buildings stood in unexpected places, and even the sounds of the street carried a different mood",
        "result": "the walk became less nostalgic and more revealing",
        "reflection": "Places do not simply hold memory; they also test it",
    },
    {
        "title": "Source Mapping Session",
        "topic": "Academic",
        "keywords": ["source", "research", "argument", "evidence"],
        "person": "Elif",
        "setting": "a university study room",
        "routine": "She groups sources by claim, method, and usefulness before writing the first paragraph",
        "goal": "build an argument that is easier to support and revise",
        "problem": "when she collected sources without structure, the writing felt crowded and repetitive",
        "change": "she started mapping how each source contributed to the larger argument",
        "detail": "That map made it easier to see gaps, weak links, and places where evidence repeated itself without adding insight",
        "result": "the draft became clearer because the research was already organized by purpose",
        "reflection": "Academic confidence often begins with better source relationships, not stronger vocabulary alone",
    },
    {
        "title": "Evidence and Interpretation",
        "topic": "Academic",
        "keywords": ["evidence", "analysis", "claim", "interpretation"],
        "person": "Arda",
        "setting": "a late-stage revision session for an academic paper",
        "routine": "He checks whether each claim is supported by evidence and whether each citation is doing real argumentative work",
        "goal": "separate interpretation from unsupported assertion",
        "problem": "earlier drafts sounded confident, but some passages moved too quickly from fact to conclusion",
        "change": "he revised the structure so that analysis followed evidence more transparently",
        "detail": "As the links became clearer, the paper sounded less decorative and more intellectually trustworthy",
        "result": "revision improved not only style but also the honesty of the argument",
        "reflection": "Academic writing becomes stronger when reasoning is visible enough to examine",
    },
]


TOPIC_REFLECTIONS = {
    "Daily Life": "small structure can make everyday life feel more manageable",
    "School": "steady preparation supports better learning",
    "Travel": "calm planning changes how unfamiliar places feel",
    "Work Life": "clear routines protect attention under pressure",
    "Science": "careful observation turns curiosity into understanding",
    "Health": "simple habits support health when they are repeatable",
    "Sport": "repetition becomes useful when it is linked to reflection",
    "Open": "quiet attention often reveals meaning hidden inside ordinary moments",
    "Academic": "stronger structure usually leads to stronger thinking",
}


def _make_generated_scenario(
    topic: str,
    title: str,
    person: str,
    setting: str,
    keywords: list[str],
    routine: str,
    goal: str,
) -> dict[str, Any]:
    keyword_a = keywords[0]
    keyword_b = keywords[1]
    keyword_c = keywords[2]
    keyword_d = keywords[3]
    return {
        "title": title,
        "topic": topic,
        "keywords": keywords,
        "person": person,
        "setting": setting,
        "routine": routine,
        "goal": goal,
        "problem": "the first version of the habit often felt rushed, unclear, or harder to repeat than expected",
        "change": f"{person} adjusted the timing, simplified the order of the steps, and treated {keyword_a} and {keyword_b} as fixed anchors",
        "detail": f"That shift made details related to {keyword_c} and {keyword_d} easier to notice and use well inside the setting",
        "result": "the routine now feels clearer, calmer, and easier to trust from one day to the next",
        "reflection": TOPIC_REFLECTIONS[topic],
    }


GENERATED_TOPIC_ITEMS = {
    "Daily Life": [
        ("Laundry Timing Reset", "Sena", "the apartment laundry room", ["laundry", "schedule", "basket", "evening"], "She sorts clothes before dinner and starts the machines before the building gets busy", "protect a calmer evening at home"),
        ("Balcony Plant Check", "Mert", "the narrow balcony outside his kitchen", ["plant", "water", "balcony", "sunlight"], "He checks the soil, waters the plants, and turns the pots toward the light", "keep a small home habit alive during busy weeks"),
        ("Shared Breakfast Notes", "Leyla", "the family table before work and school", ["breakfast", "family", "table", "plan"], "She writes one task for the day while everyone finishes breakfast together", "begin the morning with a clearer shared rhythm"),
        ("Sunday Room Reset", "Baris", "his bedroom on Sunday afternoon", ["room", "shelf", "window", "weekend"], "He opens the window, clears the desk, and returns books to the right shelf", "start the new week with less visual clutter"),
        ("Bus Card Habit", "Aylin", "the station entrance near her office", ["card", "station", "line", "morning"], "She checks her transport card and enters the station a few minutes earlier than before", "reduce small sources of morning stress"),
        ("Corner Bakery Pause", "Kaan", "the bakery near his street", ["bread", "queue", "street", "routine"], "He stops for bread, watches the short queue, and uses the wait to review the day", "turn an errand into a more deliberate pause"),
        ("Closet Planning Minute", "Defne", "the closet area beside her room", ["shirt", "closet", "choice", "night"], "She prepares the next day's clothes before sleeping instead of deciding in the morning", "save attention for more important decisions later"),
        ("Kitchen Counter Reset", "Emre", "the kitchen counter after dinner", ["kitchen", "counter", "dish", "order"], "He washes the last dish and wipes the counter before leaving the room", "keep the home feeling lighter at night and easier in the morning"),
        ("Window Seat Reading", "Ipek", "the window seat in her living room", ["book", "window", "tea", "quiet"], "She reads for fifteen minutes with tea before opening any social app", "create a quieter transition into the evening"),
        ("Grocery Shelf Review", "Onur", "the grocery aisle near the corner market", ["grocery", "list", "shelf", "price"], "He compares shelves carefully and follows a list instead of choosing in a hurry", "keep shopping practical without feeling scattered"),
        ("Phone Charger Spot", "Deniz", "the small table near the apartment door", ["phone", "charger", "table", "habit"], "She leaves her phone in one place at night instead of carrying it room to room", "reduce distraction before sleep and after waking"),
    ],
    "School": [
        ("Outline Before Homework", "Arda", "his desk after school", ["homework", "outline", "desk", "notebook"], "He lists the steps of the assignment before writing the first answer", "make homework less confusing to start and easier to finish"),
        ("Hallway Vocabulary Review", "Selin", "the quiet hallway outside the classroom", ["vocabulary", "hallway", "card", "review"], "She reviews small cards for five minutes before the lesson begins", "keep difficult words active without waiting for exam week"),
        ("Math Error Journal", "Kerem", "the study table in the library", ["math", "error", "journal", "practice"], "He writes down one mistake pattern after each practice set", "turn repeated errors into something he can actually improve"),
        ("After Class Summary", "Dila", "a bench near the school garden", ["summary", "class", "bench", "memory"], "She writes three summary lines before the details of class begin to fade", "remember the real point of the lesson later in the evening"),
        ("Project Role Check", "Ece", "the group project corner in class", ["project", "role", "group", "plan"], "She checks who is responsible for each part before the team goes home", "avoid confusion the next time the group meets"),
        ("Reading Log Session", "Tolga", "the school library reading room", ["reading", "log", "page", "question"], "He keeps a small log of pages, questions, and new ideas while reading", "build deeper understanding instead of passive completion"),
        ("Exam Week Calendar", "Mina", "the notice board near her bed", ["exam", "calendar", "week", "subject"], "She marks exam dates and matches each subject to a short study block", "keep exam week visible enough to manage calmly"),
        ("Lab Cleanup Order", "Yigit", "the science lab sink area", ["lab", "cleanup", "order", "table"], "He cleans tools in the same order after each class experiment", "finish lab sessions without losing notes or materials"),
        ("Teacher Question List", "Sude", "the front row before the lesson starts", ["teacher", "question", "lesson", "clarity"], "She keeps one small question list ready so she can ask at the right time", "use class time more actively when something remains unclear"),
        ("Citation Card Habit", "Merve", "the history project folder on her laptop", ["citation", "source", "folder", "history"], "She records each source as soon as she uses it rather than searching later", "avoid messy revision when the final draft is due"),
        ("Notebook Margin Signals", "Can", "his main notebook during long lessons", ["notebook", "margin", "signal", "topic"], "He marks examples, definitions, and questions with small symbols in the margin", "make review faster without rewriting every page"),
    ],
    "Travel": [
        ("Hostel Locker Routine", "Nisa", "the hostel room during a city break", ["hostel", "locker", "passport", "morning"], "She checks her passport, locker key, and map before leaving the room", "start each travel day without avoidable stress"),
        ("Airport Gate Review", "Firat", "the airport gate area before boarding", ["airport", "gate", "ticket", "time"], "He reviews the gate number, boarding time, and travel documents once more", "stay calm when airports become noisy and crowded"),
        ("Station Cafe Pause", "Eylul", "the cafe inside a train station", ["station", "cafe", "ticket", "route"], "She uses a short cafe break to check the route and next transfer", "keep the journey organized without rushing every moment"),
        ("Museum Entry Plan", "Berk", "the entrance line of a busy museum", ["museum", "entry", "line", "guide"], "He studies the floor plan before following the crowd inside", "see the most important rooms without wandering aimlessly"),
        ("Rainy Map Detour", "Zehra", "a central square during light rain", ["map", "rain", "square", "detour"], "She adjusts the route instead of forcing the original plan through bad weather", "treat interruptions as part of the trip rather than failure"),
        ("Hotel Desk Check", "Pelin", "the hotel desk on the first night", ["hotel", "desk", "check", "transport"], "She confirms transport options and breakfast hours before going upstairs", "make the first morning in a new city simpler"),
        ("Beach Bag Routine", "Bora", "the small hotel room before a beach day", ["beach", "bag", "water", "towel"], "He packs the same items in the same order before leaving", "avoid forgetting basic things when the day starts early"),
        ("Old Town Walk Notes", "Asli", "the old town district at sunset", ["town", "walk", "street", "memory"], "She takes short notes after each stop instead of trusting memory alone", "remember the trip as a series of details instead of a blur"),
        ("Bus Platform Double Check", "Cem", "the intercity bus station", ["bus", "platform", "board", "bag"], "He checks the platform board again after setting down his bag", "prevent small mistakes from becoming missed departures"),
        ("Neighborhood Food Search", "Lara", "a side street near the rental apartment", ["food", "street", "menu", "choice"], "She compares two local places before choosing where to eat", "find something practical without wasting too much time"),
        ("Sunrise Ferry Start", "Mete", "the ferry dock before sunrise", ["ferry", "dock", "morning", "view"], "He arrives early, watches the water, and lets the journey begin slowly", "give the trip a steadier emotional start"),
    ],
    "Work Life": [
        ("Desk Opening Checklist", "Melis", "her desk during the first ten minutes of work", ["desk", "checklist", "task", "focus"], "She checks the day's first task, open files, and deadlines before answering messages", "protect the best focus of the morning"),
        ("Inbox Block Session", "Arda", "the office inbox at mid-morning", ["inbox", "reply", "block", "priority"], "He answers messages in one defined block instead of reacting all day", "stop email from shaping the whole workday"),
        ("Client Summary Note", "Zeynep", "the notes page after a client call", ["client", "summary", "call", "note"], "She writes a five-line summary right after the conversation ends", "keep agreements visible before memory becomes fuzzy"),
        ("Meeting Room Reset", "Burak", "the meeting room after the team leaves", ["meeting", "room", "board", "action"], "He clears the board and writes the next actions before walking out", "prevent discussion from ending without a usable record"),
        ("Deadline Radar Board", "Sila", "the shared project board near the design team", ["deadline", "board", "project", "update"], "She updates one visible board with deadlines and blockers every afternoon", "make risk easier to see before it becomes urgent"),
        ("Lunch Walk Reset", "Onur", "the street around the office during lunch", ["lunch", "walk", "office", "reset"], "He takes a short walk after lunch before opening the next set of tasks", "restore attention for the second half of the day"),
        ("Proposal Draft Window", "Derya", "her laptop during a quiet early shift", ["proposal", "draft", "window", "editing"], "She drafts the first proposal paragraph before meetings start to interrupt her", "do difficult writing while the mind is still fresh"),
        ("Shared Folder Ritual", "Kaan", "the project folder used by the whole team", ["folder", "version", "team", "clarity"], "He names files carefully and moves final versions to one trusted folder", "avoid confusion caused by scattered documents"),
        ("Friday Review Notes", "Ekin", "the office on late Friday afternoon", ["review", "friday", "week", "progress"], "She reviews what moved forward and what still needs attention next week", "close the week with clearer priorities"),
        ("Call Agenda Minute", "Merve", "the call window before an important discussion", ["agenda", "call", "question", "goal"], "She writes two questions and one desired outcome before pressing join", "keep calls purposeful instead of reactive"),
        ("Workstation Calm Start", "Tolga", "the workstation at the start of a long day", ["workstation", "calm", "screen", "start"], "He opens only the tools he needs for the first task and closes the rest", "reduce digital clutter before it steals momentum"),
    ],
    "Science": [
        ("Seed Jar Comparison", "Elif", "the classroom windowsill with small seed jars", ["seed", "jar", "light", "growth"], "She compares how similar seeds change under slightly different light conditions", "understand how one condition influences growth over time"),
        ("Weather Graph Habit", "Mert", "the balcony where he checks the morning sky", ["weather", "graph", "temperature", "pattern"], "He records temperature and cloud cover at the same time each day", "see whether a larger pattern appears through repeated notes"),
        ("Sound Echo Trial", "Lina", "the school corridor during a physics activity", ["sound", "echo", "corridor", "distance"], "She measures how sound changes when the speaker moves through the corridor", "connect observation with a simple physical explanation"),
        ("Leaf Surface Check", "Bora", "the garden bed behind the school", ["leaf", "surface", "water", "observation"], "He compares how water behaves on different leaves after a short rain", "notice how material surfaces change what we see"),
        ("Magnet Sorting Table", "Kerem", "a table covered with mixed classroom objects", ["magnet", "metal", "table", "test"], "He sorts materials by how they respond to a small magnet", "understand the difference between guesswork and direct testing"),
        ("Shadow Length Record", "Ayca", "the open yard at school", ["shadow", "yard", "time", "record"], "She records shadow length at several points in the day", "see how movement in the sky becomes visible on the ground"),
        ("Paper Bridge Trial", "Can", "the lab table during a design challenge", ["paper", "bridge", "weight", "trial"], "He tests how folding changes the strength of a paper bridge", "see how structure can matter more than material amount"),
        ("Ice Melt Timing", "Irem", "the kitchen table during a home experiment", ["ice", "melt", "surface", "timing"], "She compares how quickly ice melts on different surfaces", "observe how the same object changes under different conditions"),
        ("Moon Sketch Sequence", "Deniz", "the apartment roof in the evening", ["moon", "sketch", "sequence", "night"], "He sketches the moon over several nights in the same notebook", "turn curiosity into a visible sequence of observations"),
        ("Soil Moisture Check", "Yusuf", "the community garden after watering", ["soil", "moisture", "garden", "measure"], "He checks soil moisture at the same depth each time", "replace vague impressions with more careful observation"),
        ("Bottle Air Pressure Demo", "Sude", "the lab sink during a short demonstration", ["bottle", "air", "pressure", "demo"], "She repeats a simple bottle demonstration and watches how pressure changes the result", "see how invisible forces still leave visible signs"),
    ],
    "Health": [
        ("Morning Stretch Window", "Nehir", "the living room before breakfast", ["stretch", "morning", "breath", "energy"], "She stretches for a few minutes after waking and before checking her phone", "start the day with steadier physical energy"),
        ("Water Bottle Habit", "Baris", "his desk during long work hours", ["water", "bottle", "desk", "habit"], "He keeps one bottle in the same place and refills it at regular times", "make hydration easier than forgetting"),
        ("Quiet Walk Break", "Ece", "the park path near her building", ["walk", "park", "break", "mind"], "She takes a short walk after sitting for too many hours indoors", "clear mental heaviness before it grows"),
        ("Fruit Prep Sunday", "Lara", "the kitchen counter on Sunday evening", ["fruit", "prep", "kitchen", "week"], "She prepares fruit boxes in advance instead of deciding in a hurry each day", "make better food choices easier to repeat"),
        ("Screen Sunset Rule", "Can", "his room during the last hour before sleep", ["screen", "sleep", "light", "night"], "He lowers screen brightness and stops scrolling at a fixed time", "protect sleep quality without a dramatic routine change"),
        ("Desk Posture Check", "Mina", "the home study desk", ["posture", "desk", "chair", "comfort"], "She checks the chair, screen height, and shoulder position before long study blocks", "avoid small physical strain becoming constant discomfort"),
        ("Lunch Box Rhythm", "Pelin", "the office kitchen at noon", ["lunch", "box", "meal", "timing"], "She brings a simple lunch box so the middle of the day feels less random", "keep energy steadier in the afternoon"),
        ("Breathing Reset Minute", "Arda", "the quiet corner outside the meeting room", ["breathing", "reset", "calm", "minute"], "He takes one minute for slower breathing before a stressful task", "reduce tension without losing momentum"),
        ("Tea Instead of Soda", "Ipek", "the shared break room at work", ["tea", "soda", "break", "choice"], "She changes one daily drink choice and watches how the habit feels after a week", "make health improvement feel realistic instead of extreme"),
        ("Backpack Weight Review", "Yigit", "the school entrance before the walk home", ["backpack", "weight", "school", "balance"], "He removes what he does not need before carrying the bag home", "reduce daily physical strain caused by small repeated habits"),
        ("Weekend Sleep Note", "Dila", "her bedside notebook on Saturday morning", ["sleep", "note", "weekend", "pattern"], "She writes down when she slept and how she felt after waking", "notice patterns before guessing about causes"),
    ],
    "Sport": [
        ("Warm-Up Ladder", "Kaan", "the side of the training field", ["warmup", "ladder", "field", "timing"], "He follows the same short warm-up ladder before every intense drill", "prepare the body before speed becomes the focus"),
        ("Penalty Practice Notes", "Mert", "the goal area after football practice", ["penalty", "practice", "goal", "angle"], "He writes one note about body angle after each set of penalty shots", "turn repetition into clearer learning"),
        ("Swim Turn Review", "Selin", "the end of the swimming lane", ["swim", "turn", "lane", "timing"], "She reviews each wall turn with the coach before repeating the next round", "improve movement through precise correction rather than speed alone"),
        ("Coach Marker Routine", "Yusuf", "the court during a team drill", ["coach", "marker", "court", "focus"], "He uses the coach's floor markers to repeat the same movement path accurately", "build cleaner movement under pressure"),
        ("Recovery Bottle Plan", "Derya", "the bench after training", ["recovery", "water", "bench", "discipline"], "She follows a recovery order with water, stretching, and short notes after practice", "protect the next session instead of only surviving the last one"),
        ("Sprint Interval Board", "Kerem", "the track during sprint practice", ["sprint", "interval", "track", "breath"], "He watches the interval board and keeps breathing controlled between runs", "treat pacing as part of performance"),
        ("Volleyball Serve Sequence", "Asli", "the volleyball court before the match", ["serve", "sequence", "court", "match"], "She repeats the same serve sequence so nerves do not change her timing", "keep technique steady when pressure rises"),
        ("Gym Grip Adjustment", "Baris", "the weight room during strength training", ["gym", "grip", "weight", "form"], "He changes grip slowly and checks form before increasing weight", "let control lead progress instead of impatience"),
        ("Running Shoe Log", "Sena", "the shelf where her running gear stays", ["running", "shoe", "log", "distance"], "She tracks distance and comfort in each pair of shoes", "understand how small equipment choices affect training quality"),
        ("Match Video Pause", "Tolga", "the team video room after a game", ["match", "video", "pause", "decision"], "He pauses the match video to review one repeated decision mistake", "learn from competition instead of only remembering emotion"),
        ("Captain Huddle Habit", "Elif", "the sideline before the second half", ["captain", "huddle", "sideline", "message"], "She gives one short message in the team huddle instead of many scattered words", "help the group regain focus quickly"),
    ],
    "Open": [
        ("Second-Hand Book Search", "Leyla", "the used bookstore near the tram line", ["book", "shelf", "tram", "idea"], "She looks for one overlooked book and notes why it caught her eye", "make curiosity part of her weekly routine"),
        ("Rooftop Sunset Notes", "Berk", "the apartment rooftop at sunset", ["sunset", "roof", "note", "quiet"], "He watches the skyline for ten minutes and writes one honest observation", "make the end of the day feel more intentional"),
        ("Street Photo Limit", "Defne", "a familiar street in the old neighborhood", ["street", "photo", "frame", "memory"], "She takes only a few photos and pays more attention to what each frame means", "replace endless collecting with stronger noticing"),
        ("Record Store Pause", "Onur", "the back corner of a record shop", ["record", "music", "corner", "mood"], "He listens to short samples and writes what kind of mood each one creates", "understand taste more clearly instead of choosing at random"),
        ("Sketchbook Bench", "Irem", "a public bench near the river", ["sketch", "bench", "river", "shape"], "She sketches one scene without worrying about perfect technique", "let observation matter more than performance"),
        ("Cafe Margin Draft", "Pelin", "a quiet cafe before the lunch crowd arrives", ["cafe", "margin", "draft", "thought"], "She drafts one paragraph in the margins of her notebook before work begins", "protect a small creative rhythm inside a practical week"),
        ("Archive Box Sorting", "Arda", "the storage room in his family home", ["box", "archive", "photo", "memory"], "He sorts old papers and labels what is worth keeping", "understand family memory without drowning in clutter"),
        ("Map of Old Routes", "Mina", "the desk where she keeps old city maps", ["map", "route", "city", "change"], "She compares old routes with current ones and marks what has changed", "see how places and habits shape each other"),
        ("Rain on the Window", "Can", "the window seat during a rainy evening", ["rain", "window", "evening", "reflection"], "He watches the rain and lets one question stay longer than usual", "make room for reflection without forcing a result"),
        ("Gallery Return Visit", "Sude", "the small local gallery downtown", ["gallery", "visit", "painting", "response"], "She returns to one gallery to see whether the same works feel different later", "test how attention changes over time"),
        ("Pocket Notebook Walk", "Kaan", "the neighborhood streets after dark", ["notebook", "walk", "street", "detail"], "He carries a pocket notebook and records one surprising detail from the walk", "train attention to notice more than the obvious"),
        ("Late Archive Walk", "Bora", "the quiet blocks near the old cinema", ["cinema", "block", "walk", "memory"], "He takes the same route after dark and notices what feels altered by memory", "see how familiar places become new again when viewed carefully"),
    ],
    "Academic": [
        ("Method Section Map", "Ece", "the university library method desk", ["method", "section", "library", "draft"], "She outlines the method section before writing full paragraphs", "make the paper easier to defend and revise later"),
        ("Citation Chain Review", "Mert", "the research folder on his laptop", ["citation", "chain", "source", "claim"], "He checks how each citation supports a specific claim instead of sitting passively in the notes", "make evidence work harder inside the argument"),
        ("Theory Comparison Grid", "Elif", "a graduate study room", ["theory", "comparison", "grid", "concept"], "She compares two theories in a grid before deciding how to frame the discussion", "avoid vague contrasts in the final paper"),
        ("Abstract Compression Pass", "Yusuf", "the final revision stage of an article draft", ["abstract", "revision", "article", "precision"], "He rewrites the abstract to remove broad claims and keep only the necessary signals", "make the argument legible from the first paragraph"),
        ("Source Gap Audit", "Derya", "the reading list beside her main draft", ["source", "gap", "audit", "evidence"], "She audits where the draft still lacks evidence or overuses the same kind of source", "see weakness before submission pressure hides it"),
        ("Seminar Response Notes", "Kerem", "the seminar room after discussion ends", ["seminar", "response", "notes", "argument"], "He records objections from the seminar while they are still fresh", "use criticism to strengthen the next version of the argument"),
        ("Paragraph Logic Pass", "Asli", "the printed paper spread across a desk", ["paragraph", "logic", "paper", "sequence"], "She checks whether each paragraph logically prepares the next one", "make the argument easier to follow without extra explanation"),
        ("Keyword Database Habit", "Baris", "the literature database search screen", ["keyword", "database", "search", "literature"], "He tracks which search terms produced strong academic sources and which did not", "make research more efficient and transparent"),
        ("Counterargument Slot", "Ipek", "the outline page of a new essay", ["counterargument", "outline", "essay", "position"], "She decides early where the counterargument belongs instead of adding it too late", "make the final structure more convincing and honest"),
        ("Annotated Quote File", "Mina", "the quote file linked to her thesis notes", ["quote", "annotation", "thesis", "context"], "She annotates each quote with why it matters before pasting it into any chapter", "stop quotations from replacing actual thinking"),
        ("Revision Heat Map", "Tolga", "the final week before paper submission", ["revision", "heat", "paper", "focus"], "He marks which sections need conceptual revision and which need only language repair", "spend revision energy where it changes the argument most"),
    ],
}


for topic_name, items in GENERATED_TOPIC_ITEMS.items():
    for title, person, setting, keywords, routine, goal in items:
        SCENARIOS.append(
            _make_generated_scenario(
                topic=topic_name,
                title=title,
                person=person,
                setting=setting,
                keywords=keywords,
                routine=routine,
                goal=goal,
            )
        )


def title_for(base: str, level: str) -> str:
    return f"{base} · {level}"


def build_a1(item: dict[str, Any]) -> str:
    return (
        f"{item['person']} spends time at {item['setting']}. "
        f"{item['routine']}. "
        f"{item['person']} wants to {item['goal']}. "
        f"At first, {item['problem']}. "
        f"So {item['change']}. "
        f"{item['detail']}. "
        f"In the end, {item['result']}. "
        f"{item['reflection']}."
    )


def build_a2(item: dict[str, Any]) -> str:
    return (
        f"{item['person']} often works on this part of life at {item['setting']}. "
        f"{item['routine']}. "
        f"The main goal is to {item['goal']}, but {item['problem']}. "
        f"Because of that problem, {item['change']}. "
        f"After a few days, {item['detail']}. "
        f"The change is not dramatic, yet {item['result']}. "
        f"This shows that {item['reflection'].lower()}."
    )


def build_b1(item: dict[str, Any]) -> str:
    return (
        f"In {item['setting']}, {item['person']} follows a routine that now feels more intentional than automatic. "
        f"{item['routine']}. "
        f"The deeper aim is to {item['goal']}, although {item['problem']}. "
        f"Instead of waiting for the situation to improve on its own, {item['change']}. "
        f"That decision matters because {item['detail']}. "
        f"Over time, the difference becomes easier to notice, and {item['result']}. "
        f"For {item['person']}, the lesson is simple but important: {item['reflection'].lower()}."
    )


def build_b2(item: dict[str, Any]) -> str:
    return (
        f"At {item['setting']}, {item['person']} has developed a routine that looks modest from the outside but has become surprisingly meaningful. "
        f"{item['routine']}. "
        f"The goal is to {item['goal']}, yet this was not easy at the beginning because {item['problem']}. "
        f"Rather than treating that difficulty as a fixed condition, {item['change']}. "
        f"What makes the shift effective is not speed or intensity, but the way it changes attention from moment to moment. "
        f"{item['detail']}. "
        f"As a result, {item['result']}. "
        f"In a quiet way, the experience suggests that {item['reflection'].lower()}."
    )


def build_c1(item: dict[str, Any]) -> str:
    return (
        f"In {item['setting']}, {item['person']} has come to understand that routine can be a method of thought rather than merely a repeated behavior. "
        f"{item['routine']}. "
        f"The central aim is to {item['goal']}, although earlier attempts failed because {item['problem']}. "
        f"Instead of interpreting that tension as proof that the effort was misguided, {item['change']}. "
        f"This shift matters because it transforms the situation from something reactive into something deliberately structured. "
        f"{item['detail']}. "
        f"Over time, {item['result']}, not through a dramatic breakthrough but through a more intelligent relation to repetition. "
        f"The broader implication is that {item['reflection'].lower()}."
    )


def build_academic(item: dict[str, Any]) -> str:
    return (
        f"Seen analytically, the situation at {item['setting']} illustrates how repeated practice can reorganize attention, judgment, and performance. "
        f"{item['person']} begins from a recognizable pattern: {item['routine'].lower()}. "
        f"The stated aim is to {item['goal']}, yet the effort initially encounters difficulty because {item['problem']}. "
        f"The critical intervention occurs when {item['change']}. "
        f"From that point forward, the process becomes easier to evaluate because the relevant details are no longer hidden inside habit. "
        f"{item['detail']}. "
        f"Consequently, {item['result']}. "
        f"Rather than treating the outcome as accidental, it is more useful to read it as evidence that {item['reflection'].lower()}."
    )


BUILDERS = {
    "A1": build_a1,
    "A2": build_a2,
    "B1": build_b1,
    "B2": build_b2,
    "C1": build_c1,
    "Academic": build_academic,
}


READING_SEEDS: list[dict[str, Any]] = []
for scenario in SCENARIOS:
    for level, builder in BUILDERS.items():
        READING_SEEDS.append(
            {
                "title": title_for(scenario["title"], level),
                "level": level,
                "topic": scenario["topic"],
                "keywords": list(scenario["keywords"]),
                "text": builder(scenario),
            }
        )


def normalize_topic(topic: str) -> str:
    topic_map = {
        "Open": "Open",
        "Serbest": "Open",
        "Daily Life": "Daily Life",
        "G??nl??k Hayat": "Daily Life",
        "Daily Life": "Daily Life",
        "School": "School",
        "Okul": "School",
        "Travel": "Travel",
        "Seyahat": "Travel",
        "Work Life": "Work Life",
        "??Work Life?": "Work Life",
        "Work Life": "Work Life",
        "Academic": "Academic",
        "Akademik": "Academic",
        "Science": "Science",
        "Health": "Health",
        "Sport": "Sport",
    }
    return topic_map.get(topic, topic)
