from __future__ import annotations

from typing import Any


COMMON_NAMES = [
    "Aylin",
    "Deniz",
    "Eren",
    "Selin",
    "Bora",
    "Mina",
    "Kerem",
    "Lina",
    "Arda",
    "Derya",
    "Kaan",
    "Elif",
    "Yusuf",
    "Asya",
    "Can",
    "Melis",
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
    "Data Science": "data work improves when method is visible enough to inspect",
    "Computer Science": "systems become easier to trust when logic is made explicit",
    "Technology": "good tools matter most when they support clear human decisions",
    "Finance": "financial clarity grows from habits that make tradeoffs visible",
    "Environment": "environmental awareness becomes practical when observation leads to action",
    "Psychology": "attention to patterns often reveals what emotion alone can hide",
    "Communication": "clear communication reduces friction before it becomes conflict",
    "Arts": "artistic practice deepens when repetition keeps making room for surprise",
    "Culture": "cultural understanding expands when ordinary rituals are examined carefully",
    "Food": "food habits become meaningful when they balance care, rhythm, and pleasure",
    "Public Services": "public systems feel stronger when reliability is built into routine",
    "Media": "media literacy improves when messages are examined rather than absorbed automatically",
}


TOPIC_BLUEPRINTS: dict[str, dict[str, Any]] = {
    "Daily Life": {
        "prefixes": ["Morning", "Evening", "Weekend", "Neighborhood"],
        "subjects": ["Routine", "Reset", "Review", "Plan"],
        "settings": [
            "the apartment before the first bus",
            "the kitchen after dinner",
            "the neighborhood market on Saturday morning",
            "the small desk near the living-room window",
        ],
        "goals": [
            "protect a calmer start to the day",
            "reduce clutter before it grows into stress",
            "keep ordinary tasks from feeling shapeless",
            "turn repeated errands into steadier habits",
        ],
        "keyword_sets": [
            ["morning", "routine", "coffee", "plan"],
            ["market", "bag", "street", "weekend"],
            ["window", "desk", "note", "evening"],
            ["kitchen", "counter", "order", "habit"],
        ],
        "action_template": "{person} checks {kw0} details, keeps {kw1} visible, and uses {kw2} as a small anchor before the next task.",
        "problem_template": "earlier attempts often felt rushed, messy, or harder to repeat than expected",
        "detail_template": "Once the rhythm improved, details around {kw3} and {kw1} became easier to notice without hurry",
        "result_template": "the day now feels steadier and less reactive from one hour to the next",
    },
    "School": {
        "prefixes": ["Classroom", "Homework", "Library", "Study"],
        "subjects": ["Routine", "Workflow", "Review", "Session"],
        "settings": [
            "the school library after lessons",
            "a desk covered with notebooks and summaries",
            "a group project table near the classroom door",
            "the quiet hallway before the teacher arrives",
        ],
        "goals": [
            "understand the material instead of memorizing it blindly",
            "make revision easier before exam week arrives",
            "turn scattered notes into something useful later",
            "reduce confusion when tasks become more complex",
        ],
        "keyword_sets": [
            ["student", "library", "notes", "review"],
            ["teacher", "question", "lesson", "summary"],
            ["assignment", "draft", "class", "outline"],
            ["exam", "subject", "calendar", "practice"],
        ],
        "action_template": "{person} organizes {kw0} work, checks {kw1}, and writes short {kw2} before leaving the study block.",
        "problem_template": "the first version of the work often became crowded and difficult to revisit later",
        "detail_template": "That change made connections around {kw3} and {kw2} easier to trace when pressure increased",
        "result_template": "studying now feels more deliberate and less dependent on last-minute effort",
    },
    "Travel": {
        "prefixes": ["Station", "City", "Route", "Arrival"],
        "subjects": ["Review", "Workflow", "Plan", "Session"],
        "settings": [
            "a crowded train station before departure",
            "the lobby of a small hotel after a late arrival",
            "a wet city center during light afternoon rain",
            "the desk beside a folded map and a travel ticket",
        ],
        "goals": [
            "begin each trip without unnecessary confusion",
            "keep movement calm even when information changes quickly",
            "see more of a place without turning the day into a race",
            "treat uncertainty as manageable rather than threatening",
        ],
        "keyword_sets": [
            ["ticket", "station", "platform", "bag"],
            ["hotel", "arrival", "city", "map"],
            ["route", "street", "rain", "detour"],
            ["travel", "choice", "time", "plan"],
        ],
        "action_template": "{person} checks {kw0}, studies {kw1}, and gives a few quiet minutes to {kw2} before moving on.",
        "problem_template": "past journeys created stress because small changes quickly felt larger than they were",
        "detail_template": "Once the routine stabilized, details around {kw3} and {kw2} felt easier to handle without panic",
        "result_template": "the journey now feels lighter, clearer, and easier to trust in real time",
    },
    "Work Life": {
        "prefixes": ["Agenda", "Client", "Team", "Deadline"],
        "subjects": ["Review", "Workflow", "Board", "Plan"],
        "settings": [
            "a small office before the first meeting of the week",
            "the project board used by a cross-functional team",
            "a desk covered with call notes and deadlines",
            "the meeting room just after everyone leaves",
        ],
        "goals": [
            "make decisions visible before confusion spreads",
            "turn meetings into clearer action",
            "protect attention from constant reactive work",
            "reduce hidden delays before they become expensive",
        ],
        "keyword_sets": [
            ["meeting", "agenda", "team", "office"],
            ["client", "call", "project", "notes"],
            ["deadline", "board", "update", "risk"],
            ["workflow", "folder", "version", "clarity"],
        ],
        "action_template": "{person} reviews {kw0}, writes down {kw1}, and checks whether the next {kw2} is clear enough for everyone involved.",
        "problem_template": "without structure, repeated work often returned in the form of preventable confusion",
        "detail_template": "As the process improved, signals around {kw3} and {kw2} became visible early enough to discuss honestly",
        "result_template": "the work now feels more coherent because the team shares the same picture of what matters",
    },
    "Science": {
        "prefixes": ["Observation", "Experiment", "Pattern", "Lab"],
        "subjects": ["Review", "Log", "Session", "Trial"],
        "settings": [
            "the science classroom during a careful experiment",
            "a garden bed used for repeated observation",
            "the lab table covered with simple measuring tools",
            "a notebook filled with dated comparisons",
        ],
        "goals": [
            "turn curiosity into something observable and testable",
            "notice how one variable changes the larger pattern",
            "separate guesswork from evidence",
            "make repeated observation easier to compare over time",
        ],
        "keyword_sets": [
            ["observation", "method", "result", "pattern"],
            ["experiment", "variable", "measure", "record"],
            ["light", "growth", "surface", "change"],
            ["model", "test", "signal", "evidence"],
        ],
        "action_template": "{person} repeats {kw0} steps, isolates {kw1}, and records what the current {kw2} can actually support.",
        "problem_template": "early trials looked interesting but did not yet say enough to justify a conclusion",
        "detail_template": "Once the method grew steadier, links between {kw3} and {kw2} became easier to examine without distortion",
        "result_template": "the investigation now feels more disciplined and therefore more meaningful",
    },
    "Health": {
        "prefixes": ["Sleep", "Lunch", "Screen", "Balance"],
        "subjects": ["Routine", "Reset", "Review", "Plan"],
        "settings": [
            "the last hour before sleep",
            "a lunch break inside a busy workday",
            "the home desk after long screen time",
            "a quiet walk near the apartment building",
        ],
        "goals": [
            "protect energy before fatigue becomes the main decision-maker",
            "make healthy choices easier to repeat than unhealthy ones",
            "notice how small habits shape comfort and focus",
            "replace vague intention with something the body can trust",
        ],
        "keyword_sets": [
            ["sleep", "light", "habit", "energy"],
            ["lunch", "meal", "water", "afternoon"],
            ["screen", "break", "posture", "comfort"],
            ["walk", "breathing", "calm", "balance"],
        ],
        "action_template": "{person} protects {kw0}, checks {kw1}, and treats {kw2} as a daily support instead of a dramatic project.",
        "problem_template": "the first attempt failed because the change was too abstract to survive a real schedule",
        "detail_template": "After simplifying the process, details around {kw3} and {kw0} became easier to notice before discomfort grew",
        "result_template": "the routine now feels sustainable, which makes the benefit more believable",
    },
    "Sport": {
        "prefixes": ["Practice", "Recovery", "Drill", "Match"],
        "subjects": ["Review", "Plan", "Session", "Workflow"],
        "settings": [
            "the edge of the court after practice",
            "the bench during a recovery break",
            "the training field before the next drill begins",
            "the video room after a demanding match",
        ],
        "goals": [
            "connect repetition to better understanding instead of blind effort",
            "treat recovery as part of performance",
            "protect technique when pressure rises",
            "make feedback specific enough to use the next day",
        ],
        "keyword_sets": [
            ["coach", "focus", "timing", "practice"],
            ["recovery", "water", "discipline", "session"],
            ["drill", "movement", "precision", "speed"],
            ["match", "video", "decision", "review"],
        ],
        "action_template": "{person} reviews {kw0}, repeats {kw1}, and checks whether the next {kw2} still fits the goal of the session.",
        "problem_template": "progress once felt invisible because effort and reflection were not working together",
        "detail_template": "When that changed, details around {kw3} and {kw2} became easier to refine with patience",
        "result_template": "training now feels more purposeful because the same work carries clearer meaning",
    },
    "Open": {
        "prefixes": ["Quiet", "Street", "Notebook", "Memory"],
        "subjects": ["Review", "Walk", "Session", "Pause"],
        "settings": [
            "a quiet cafe before the lunch crowd arrives",
            "the street where old habits still leave traces",
            "a bench near the river at the end of the day",
            "the room where old notebooks and photos are stored",
        ],
        "goals": [
            "create space for attention inside an otherwise crowded week",
            "notice what ordinary routines usually hide",
            "understand how mood changes what can be seen clearly",
            "turn reflection into a practice rather than an accident",
        ],
        "keyword_sets": [
            ["quiet", "notebook", "focus", "reflection"],
            ["street", "change", "memory", "walk"],
            ["photo", "detail", "question", "pause"],
            ["cafe", "idea", "mood", "window"],
        ],
        "action_template": "{person} protects {kw0}, writes into a small {kw1}, and lets {kw2} stay long enough to become readable.",
        "problem_template": "without a deliberate pause, feelings and observations used to blur together too quickly",
        "detail_template": "After the habit settled, small details around {kw3} and {kw2} carried more meaning than before",
        "result_template": "the experience now feels less noisy and more interpretable from one visit to the next",
    },
    "Academic": {
        "prefixes": ["Source", "Method", "Argument", "Evidence"],
        "subjects": ["Review", "Map", "Session", "Audit"],
        "settings": [
            "a university study room during a research block",
            "the desk where several article drafts are compared",
            "a literature review folder filled with citations",
            "a late-stage revision session for a paper",
        ],
        "goals": [
            "make the argument easier to support and revise",
            "separate evidence from decoration",
            "see where the reasoning still depends on weak links",
            "turn research material into a coherent structure",
        ],
        "keyword_sets": [
            ["research", "source", "evidence", "argument"],
            ["analysis", "claim", "citation", "revision"],
            ["method", "question", "draft", "interpretation"],
            ["thesis", "logic", "section", "support"],
        ],
        "action_template": "{person} groups {kw0}, checks each {kw1}, and asks whether the current {kw2} is doing genuine argumentative work.",
        "problem_template": "earlier drafts looked confident, yet some sections moved from fact to conclusion too quickly",
        "detail_template": "Once the structure improved, links between {kw3} and {kw2} became easier to evaluate critically",
        "result_template": "the paper now feels more trustworthy because its reasoning is visible enough to inspect",
    },
    "Data Science": {
        "prefixes": ["Notebook", "Dataset", "Trend", "Model"],
        "subjects": ["Review", "Workflow", "Session", "Audit"],
        "settings": [
            "the analytics notebook before the morning stand-up",
            "a dashboard review shared by the data team",
            "the model evaluation table during a quiet work block",
            "a dataset audit before the next experiment begins",
        ],
        "goals": [
            "turn raw information into decisions that can be explained",
            "check whether patterns are real before trusting them",
            "make the modeling workflow easier to inspect later",
            "reduce hidden noise before it shapes the result",
        ],
        "keyword_sets": [
            ["dataset", "trend", "model", "notebook"],
            ["feature", "signal", "metric", "prediction"],
            ["dashboard", "query", "pattern", "summary"],
            ["sample", "outlier", "pipeline", "cluster"],
        ],
        "action_template": "{person} reviews {kw0}, checks {kw1}, and writes a short note before trusting the current {kw2}.",
        "problem_template": "early attempts depended too much on intuition and not enough on repeatable checks",
        "detail_template": "Once the workflow stabilized, details around {kw3} and {kw2} became easier to compare without confusion",
        "result_template": "the analysis now feels more transparent because each step can be explained and repeated",
    },
    "Computer Science": {
        "prefixes": ["System", "Algorithm", "Debug", "Code"],
        "subjects": ["Review", "Workflow", "Session", "Plan"],
        "settings": [
            "the repository before a major refactor",
            "a debugging session late in the afternoon",
            "the whiteboard used to sketch algorithm choices",
            "a code review before the next release build",
        ],
        "goals": [
            "make logic easier to trust and maintain",
            "reduce hidden complexity before it spreads",
            "connect implementation choices to clear reasons",
            "turn debugging into a repeatable process rather than panic",
        ],
        "keyword_sets": [
            ["algorithm", "logic", "review", "system"],
            ["bug", "trace", "function", "state"],
            ["code", "module", "refactor", "design"],
            ["runtime", "memory", "thread", "compile"],
        ],
        "action_template": "{person} inspects {kw0}, checks {kw1}, and rewrites a small part of the {kw2} before touching the larger system.",
        "problem_template": "older solutions solved the immediate issue but left the deeper structure difficult to reason about",
        "detail_template": "With a calmer process, details around {kw3} and {kw2} became visible enough to improve instead of ignore",
        "result_template": "the system now feels easier to maintain because complexity is no longer hiding in the background",
    },
    "Technology": {
        "prefixes": ["Product", "Interface", "Device", "Tool"],
        "subjects": ["Review", "Workflow", "Session", "Reset"],
        "settings": [
            "a product planning room before a feature launch",
            "the interface review shared by the design team",
            "a table covered with devices and user notes",
            "the support board after a week of feedback",
        ],
        "goals": [
            "make tools feel more helpful than distracting",
            "connect product choices to actual user needs",
            "reduce friction before it becomes abandonment",
            "turn feedback into practical improvement instead of noise",
        ],
        "keyword_sets": [
            ["device", "tool", "update", "workflow"],
            ["interface", "feature", "feedback", "user"],
            ["product", "support", "design", "clarity"],
            ["screen", "signal", "flow", "access"],
        ],
        "action_template": "{person} reviews {kw0}, tests {kw1}, and checks whether the current {kw2} supports the user instead of interrupting them.",
        "problem_template": "the first version often solved one problem while quietly creating another layer of friction",
        "detail_template": "After the review improved, details around {kw3} and {kw2} became easier to adjust with care",
        "result_template": "the technology now feels more humane because it serves attention instead of stealing it",
    },
    "Finance": {
        "prefixes": ["Budget", "Savings", "Payment", "Expense"],
        "subjects": ["Review", "Plan", "Session", "Audit"],
        "settings": [
            "the kitchen table during a weekly budget check",
            "a banking app review at the end of the month",
            "a spreadsheet used to compare recurring expenses",
            "the notebook where long-term savings are tracked",
        ],
        "goals": [
            "make tradeoffs visible before money feels stressful",
            "reduce avoidable spending without turning life rigid",
            "understand where recurring costs quietly accumulate",
            "turn financial planning into something calm and repeatable",
        ],
        "keyword_sets": [
            ["budget", "expense", "saving", "plan"],
            ["payment", "balance", "month", "review"],
            ["income", "cost", "choice", "record"],
            ["finance", "goal", "habit", "stability"],
        ],
        "action_template": "{person} checks {kw0}, compares {kw1}, and writes down one decision before the next {kw2} begins.",
        "problem_template": "money once felt abstract until small repeated costs became impossible to ignore",
        "detail_template": "As the record improved, links between {kw3} and {kw2} became easier to discuss honestly",
        "result_template": "the plan now feels calmer because financial choices are visible before they become urgent",
    },
    "Environment": {
        "prefixes": ["Garden", "Waste", "Energy", "Climate"],
        "subjects": ["Review", "Routine", "Session", "Check"],
        "settings": [
            "the shared recycling corner in the building",
            "a small garden used for seasonal observation",
            "the home meter review at the end of the week",
            "a community clean-up planning table",
        ],
        "goals": [
            "turn environmental concern into specific action",
            "notice where daily habits shape resource use",
            "replace vague awareness with visible patterns",
            "connect small decisions to larger systems without exaggeration",
        ],
        "keyword_sets": [
            ["recycling", "waste", "sorting", "habit"],
            ["garden", "soil", "water", "season"],
            ["energy", "meter", "usage", "pattern"],
            ["climate", "community", "cleanup", "action"],
        ],
        "action_template": "{person} reviews {kw0}, checks {kw1}, and asks what the current {kw2} is really showing about daily behavior.",
        "problem_template": "the issue once felt too large to influence, which made useful action easy to postpone",
        "detail_template": "When the process became concrete, details around {kw3} and {kw2} felt easier to understand and improve",
        "result_template": "the routine now turns environmental concern into something practical instead of merely abstract",
    },
    "Psychology": {
        "prefixes": ["Attention", "Emotion", "Habit", "Stress"],
        "subjects": ["Review", "Journal", "Session", "Map"],
        "settings": [
            "a quiet journal session after a difficult day",
            "the small pause before a stressful conversation",
            "a notebook used to track repeated emotional patterns",
            "the desk where thoughts are separated from reactions",
        ],
        "goals": [
            "notice patterns before they become overwhelming",
            "understand the link between thought, emotion, and action",
            "replace vague tension with something observable",
            "give repeated feelings a structure that can be examined",
        ],
        "keyword_sets": [
            ["attention", "emotion", "pattern", "journal"],
            ["stress", "response", "pause", "reaction"],
            ["habit", "thought", "mind", "reflection"],
            ["memory", "feeling", "signal", "awareness"],
        ],
        "action_template": "{person} names {kw0}, slows down {kw1}, and writes a short note before the next {kw2} shapes the day.",
        "problem_template": "earlier responses felt automatic because discomfort arrived faster than understanding",
        "detail_template": "Once the notes became more regular, links between {kw3} and {kw2} were easier to interpret without drama",
        "result_template": "the situation now feels more readable because emotion is no longer mistaken for the whole story",
    },
    "Communication": {
        "prefixes": ["Message", "Dialogue", "Meeting", "Feedback"],
        "subjects": ["Review", "Workflow", "Session", "Reset"],
        "settings": [
            "a team conversation that needs more clarity",
            "the notes page after a difficult meeting",
            "a draft message prepared before sending",
            "a feedback exchange between two colleagues",
        ],
        "goals": [
            "say less but mean it more clearly",
            "reduce misunderstanding before it hardens into conflict",
            "give feedback that can actually be used",
            "separate tone problems from idea problems",
        ],
        "keyword_sets": [
            ["message", "tone", "clarity", "feedback"],
            ["dialogue", "question", "response", "timing"],
            ["meeting", "summary", "point", "follow-up"],
            ["communication", "signal", "listener", "intent"],
        ],
        "action_template": "{person} drafts {kw0}, checks {kw1}, and asks whether the next {kw2} will sound as clear as it looks on the page.",
        "problem_template": "the first version often created ambiguity because speed mattered more than precision",
        "detail_template": "As the exchange improved, details around {kw3} and {kw2} were easier to adjust before they caused friction",
        "result_template": "the conversation now feels cleaner because the real point is easier for everyone to see",
    },
    "Arts": {
        "prefixes": ["Studio", "Sketch", "Rehearsal", "Canvas"],
        "subjects": ["Review", "Session", "Routine", "Study"],
        "settings": [
            "a quiet studio before the first sketch of the day",
            "the rehearsal room during a repeated passage",
            "a table covered with brushes, paper, and notes",
            "the gallery bench where one work is revisited slowly",
        ],
        "goals": [
            "let repetition refine perception instead of killing interest",
            "notice what a work is doing before judging it too quickly",
            "balance technique with curiosity",
            "protect a creative rhythm that can survive ordinary life",
        ],
        "keyword_sets": [
            ["sketch", "line", "studio", "rhythm"],
            ["canvas", "color", "detail", "composition"],
            ["rehearsal", "passage", "timing", "voice"],
            ["gallery", "work", "attention", "response"],
        ],
        "action_template": "{person} repeats {kw0}, studies {kw1}, and lets the next {kw2} settle before calling the work finished.",
        "problem_template": "creative effort once felt inconsistent because pressure arrived before observation had time to mature",
        "detail_template": "After the routine stabilized, details around {kw3} and {kw2} carried more meaning instead of more noise",
        "result_template": "the practice now feels more generous because patience has become part of the method",
    },
    "Culture": {
        "prefixes": ["Festival", "Archive", "Tradition", "Community"],
        "subjects": ["Review", "Walk", "Session", "Note"],
        "settings": [
            "a neighborhood event built around shared ritual",
            "the local archive where old programs are stored",
            "a cultural center before the evening gathering starts",
            "a street where familiar traditions still shape the mood",
        ],
        "goals": [
            "see culture as something lived rather than merely described",
            "understand how rituals hold memory in public space",
            "notice how repeated forms carry meaning across time",
            "connect personal experience to wider community patterns",
        ],
        "keyword_sets": [
            ["festival", "ritual", "community", "memory"],
            ["archive", "program", "history", "tradition"],
            ["street", "gathering", "music", "mood"],
            ["culture", "practice", "place", "identity"],
        ],
        "action_template": "{person} watches {kw0}, records {kw1}, and asks what the current {kw2} is preserving beneath the visible event.",
        "problem_template": "at first the scene felt familiar but too broad to interpret clearly",
        "detail_template": "With slower attention, details around {kw3} and {kw2} became easier to connect across time",
        "result_template": "the experience now feels richer because it reveals how public habits carry private meanings",
    },
    "Food": {
        "prefixes": ["Kitchen", "Recipe", "Market", "Meal"],
        "subjects": ["Review", "Routine", "Session", "Plan"],
        "settings": [
            "the kitchen counter before dinner begins",
            "the market aisle during a weekly food run",
            "a notebook filled with recipe notes and substitutions",
            "the table where a simple meal becomes a shared habit",
        ],
        "goals": [
            "make food choices more thoughtful without making them rigid",
            "turn preparation into a calmer part of the week",
            "notice how taste, timing, and care shape a meal together",
            "balance pleasure with practicality in everyday cooking",
        ],
        "keyword_sets": [
            ["recipe", "ingredient", "kitchen", "timing"],
            ["market", "meal", "choice", "basket"],
            ["flavor", "portion", "table", "habit"],
            ["food", "prep", "note", "routine"],
        ],
        "action_template": "{person} checks {kw0}, prepares {kw1}, and makes one small choice before the next {kw2} begins to feel rushed.",
        "problem_template": "the meal once felt like another task to survive instead of something that could support the day",
        "detail_template": "As the rhythm improved, details around {kw3} and {kw2} became easier to enjoy and repeat",
        "result_template": "the meal now feels both more practical and more satisfying than before",
    },
    "Public Services": {
        "prefixes": ["Clinic", "Transit", "Library", "Service"],
        "subjects": ["Review", "Workflow", "Session", "Plan"],
        "settings": [
            "the public clinic waiting area before appointments begin",
            "a transport office helping residents with daily travel",
            "the local library desk during a busy afternoon",
            "a municipal service counter handling repeated requests",
        ],
        "goals": [
            "make public systems easier to navigate without confusion",
            "reduce friction in services people rely on every week",
            "see how small process changes affect trust",
            "protect clarity when many people need help at once",
        ],
        "keyword_sets": [
            ["service", "queue", "request", "clarity"],
            ["clinic", "appointment", "record", "support"],
            ["transit", "schedule", "desk", "route"],
            ["library", "access", "community", "help"],
        ],
        "action_template": "{person} checks {kw0}, organizes {kw1}, and watches whether the next {kw2} will remain clear for the people waiting.",
        "problem_template": "the system once seemed more complicated than it needed to be because useful steps were not visible enough",
        "detail_template": "When the workflow improved, details around {kw3} and {kw2} became easier to follow without repeated explanation",
        "result_template": "the service now feels more reliable because its logic is easier for people to understand",
    },
    "Media": {
        "prefixes": ["Headline", "Podcast", "Article", "Media"],
        "subjects": ["Review", "Session", "Audit", "Plan"],
        "settings": [
            "a desk covered with articles, notes, and screenshots",
            "the first listening pass of a current-affairs podcast",
            "a comparison between several headlines about the same event",
            "a media notebook used to separate fact from framing",
        ],
        "goals": [
            "read media with more distance and less automatic agreement",
            "notice how framing shapes interpretation",
            "separate speed from reliability when information arrives quickly",
            "turn consumption into analysis instead of passive reaction",
        ],
        "keyword_sets": [
            ["headline", "source", "framing", "evidence"],
            ["article", "claim", "quote", "context"],
            ["podcast", "listener", "tone", "signal"],
            ["media", "summary", "bias", "question"],
        ],
        "action_template": "{person} compares {kw0}, checks the {kw1}, and asks what the current {kw2} is encouraging the audience to assume.",
        "problem_template": "the first reading often felt convincing simply because it was fast, polished, and emotionally easy to accept",
        "detail_template": "Once the review slowed down, details around {kw3} and {kw2} became easier to challenge intelligently",
        "result_template": "the material now feels more legible because message and method are examined together",
    },
}


def _make_blueprint_scenario(
    topic: str,
    *,
    title: str,
    person: str,
    setting: str,
    keywords: list[str],
    action_template: str,
    goal: str,
    problem: str,
    detail_template: str,
    result: str,
) -> dict[str, Any]:
    kw0, kw1, kw2, kw3 = keywords
    routine = action_template.format(person=person, kw0=kw0, kw1=kw1, kw2=kw2, kw3=kw3)
    change = (
        f"{person} adjusted the timing, simplified the order of the steps, and treated {kw0} and {kw1} as fixed anchors"
    )
    detail = detail_template.format(person=person, kw0=kw0, kw1=kw1, kw2=kw2, kw3=kw3)
    return {
        "title": title,
        "topic": topic,
        "keywords": keywords,
        "person": person,
        "setting": setting,
        "routine": routine,
        "goal": goal,
        "problem": problem,
        "change": change,
        "detail": detail,
        "result": result,
        "reflection": TOPIC_REFLECTIONS[topic],
    }


def _expand_topic(topic: str, blueprint: dict[str, Any], count: int = 16) -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    prefixes = blueprint["prefixes"]
    subjects = blueprint["subjects"]
    settings = blueprint["settings"]
    goals = blueprint["goals"]
    keyword_sets = blueprint["keyword_sets"]
    people = blueprint.get("people", COMMON_NAMES)
    action_template = blueprint["action_template"]
    problem_template = blueprint["problem_template"]
    detail_template = blueprint["detail_template"]
    result_template = blueprint["result_template"]

    for idx in range(count):
        prefix = prefixes[(idx // len(subjects)) % len(prefixes)]
        subject = subjects[idx % len(subjects)]
        title = f"{prefix} {subject}"
        person = people[idx % len(people)]
        setting = settings[(idx + (idx // len(subjects))) % len(settings)]
        goal = goals[(idx // len(subjects)) % len(goals)]
        keywords = keyword_sets[idx % len(keyword_sets)]
        scenarios.append(
            _make_blueprint_scenario(
                topic,
                title=title,
                person=person,
                setting=setting,
                keywords=keywords,
                action_template=action_template,
                goal=goal,
                problem=problem_template,
                detail_template=detail_template,
                result=result_template,
            )
        )
    return scenarios


SCENARIOS: list[dict[str, Any]] = []
for topic_name, blueprint in TOPIC_BLUEPRINTS.items():
    SCENARIOS.extend(_expand_topic(topic_name, blueprint, count=16))


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
        "Günlük Hayat": "Daily Life",
        "School": "School",
        "Okul": "School",
        "Travel": "Travel",
        "Seyahat": "Travel",
        "Work Life": "Work Life",
        "İş Hayatı": "Work Life",
        "Academic": "Academic",
        "Akademik": "Academic",
        "Science": "Science",
        "Bilim": "Science",
        "Health": "Health",
        "Sağlık": "Health",
        "Sport": "Sport",
        "Spor": "Sport",
        "Data Science": "Data Science",
        "Veri Bilimi": "Data Science",
        "Computer Science": "Computer Science",
        "Bilgisayar Bilimi": "Computer Science",
        "Technology": "Technology",
        "Teknoloji": "Technology",
        "Finance": "Finance",
        "Finans": "Finance",
        "Environment": "Environment",
        "Çevre": "Environment",
        "Psychology": "Psychology",
        "Psikoloji": "Psychology",
        "Communication": "Communication",
        "İletişim": "Communication",
        "Arts": "Arts",
        "Sanat": "Arts",
        "Culture": "Culture",
        "Kültür": "Culture",
        "Food": "Food",
        "Yemek": "Food",
        "Public Services": "Public Services",
        "Kamu Hizmetleri": "Public Services",
        "Media": "Media",
        "Medya": "Media",
    }
    return topic_map.get(topic, topic)
