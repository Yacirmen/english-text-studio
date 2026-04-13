from __future__ import annotations

from typing import Any


SCENARIOS: list[dict[str, Any]] = [
    {
        "title": "Morning Bus Routine",
        "topic": "Günlük Hayat",
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
        "topic": "Günlük Hayat",
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
        "topic": "Günlük Hayat",
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
        "topic": "Okul",
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
        "topic": "Okul",
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
        "topic": "Okul",
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
        "topic": "Seyahat",
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
        "topic": "Seyahat",
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
        "topic": "Seyahat",
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
        "topic": "İş Hayatı",
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
        "topic": "İş Hayatı",
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
        "topic": "İş Hayatı",
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
        "topic": "Serbest",
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
        "topic": "Serbest",
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
        "topic": "Akademik",
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
        "topic": "Akademik",
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
        "Open": "Serbest",
        "Daily Life": "Günlük Hayat",
        "School": "Okul",
        "Travel": "Seyahat",
        "Work Life": "İş Hayatı",
        "Academic": "Akademik",
        "Science": "Science",
        "Health": "Health",
        "Sport": "Sport",
    }
    return topic_map.get(topic, topic)
