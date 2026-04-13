from __future__ import annotations

from typing import Any


def entry(
    title: str,
    level: str,
    topic: str,
    keywords: list[str],
    text: str,
) -> dict[str, Any]:
    return {
        "title": title,
        "level": level,
        "topic": topic,
        "keywords": keywords,
        "text": text,
    }


READING_SEEDS: list[dict[str, Any]] = [
    entry(
        "Morning Bus Talk",
        "A1",
        "Günlük Hayat",
        ["morning", "bus", "friend", "coffee"],
        "Every morning, Lina wakes up early and drinks a small cup of coffee. "
        "She walks to the bus stop near her home and waits with her friend Duru. "
        "On the bus, they talk about music, school, and the weather. "
        "The ride is short, but it helps Lina feel calm and ready for the day.",
    ),
    entry(
        "A Quiet Evening at Home",
        "A1",
        "Günlük Hayat",
        ["home", "dinner", "family", "evening"],
        "In the evening, Can comes home from school and helps his family. "
        "He sets the table, talks with his sister, and eats dinner with everyone. "
        "After dinner, they sit together for a short time and share stories from the day. "
        "The house feels warm, simple, and peaceful.",
    ),
    entry(
        "First Day in the Library",
        "A1",
        "Okul",
        ["student", "library", "book", "teacher"],
        "Mert is a new student at his school. One afternoon, his teacher takes the class to the library. "
        "Mert chooses a short book about animals and sits near the window. "
        "The room is quiet, so he can read slowly and understand each page. "
        "Before he leaves, he smiles because the library already feels friendly.",
    ),
    entry(
        "Simple Science Notes",
        "A1",
        "Science",
        ["science", "plant", "water", "light"],
        "At school, Elif learns about how a plant grows. "
        "Her teacher says a plant needs water, light, and time. "
        "Elif writes these ideas in her notebook and draws a small green leaf. "
        "The lesson is easy to follow, and it makes science feel interesting.",
    ),
    entry(
        "Practice Before the Match",
        "A1",
        "Sport",
        ["team", "ball", "coach", "practice"],
        "Before the match, the team meets on the school field. "
        "The coach gives each player a ball and starts a short practice. "
        "Efe runs, passes, and listens carefully. "
        "He feels a little nervous, but the team works together and gives him confidence.",
    ),
    entry(
        "A Healthy Lunch Break",
        "A1",
        "Health",
        ["lunch", "fruit", "water", "healthy"],
        "During lunch break, Zeynep opens a small box with fruit and a sandwich. "
        "She drinks water and sits outside with her cousin. "
        "They talk about school while the sun warms the garden. "
        "A simple healthy meal gives her energy for the afternoon.",
    ),
    entry(
        "Packing for a Weekend Trip",
        "A2",
        "Seyahat",
        ["travel", "ticket", "hotel", "bag"],
        "Selin is packing for a weekend trip to Izmir. "
        "She checks her ticket twice and places it in the front pocket of her bag. "
        "Because she does not want to carry too much, she chooses comfortable clothes and one light jacket. "
        "When she arrives at the hotel, she plans to rest for an hour before exploring the city.",
    ),
    entry(
        "A Busy School Afternoon",
        "A2",
        "Okul",
        ["student", "exam", "class", "study"],
        "After lunch, Bora stays at school to study for an exam. "
        "His class was difficult in the morning, so he wants to review his notes while the ideas are still fresh. "
        "He meets two other students in a quiet room and they solve simple questions together. "
        "By the time he goes home, he feels tired but more prepared.",
    ),
    entry(
        "Office Notes Before Noon",
        "A2",
        "İş Hayatı",
        ["office", "meeting", "email", "plan"],
        "On Monday morning, Arda arrives at the office before his first meeting. "
        "He reads an important email from his manager and updates his plan for the day. "
        "Because he organizes his notes early, the meeting feels easier and less stressful. "
        "A clear plan helps him move through the rest of the day with more confidence.",
    ),
    entry(
        "A Better Sleep Routine",
        "A2",
        "Health",
        ["sleep", "routine", "energy", "habit"],
        "Leyla wants more energy during the week, so she starts a better sleep routine. "
        "She turns off her phone earlier, drinks tea instead of coffee at night, and reads for twenty minutes before bed. "
        "The change feels small at first, but after a few days she wakes up more easily. "
        "A simple habit gives her mornings a calmer start.",
    ),
    entry(
        "Why the Sky Changes",
        "A2",
        "Science",
        ["sky", "light", "science", "color"],
        "In science class, the students learn why the sky does not always look the same. "
        "Their teacher explains that light moves in different ways and changes the color we see. "
        "At sunset, the class looks outside and notices warm orange tones over the buildings. "
        "The lesson feels more memorable because the idea is connected to real life.",
    ),
    entry(
        "Training Twice a Week",
        "A2",
        "Sport",
        ["sport", "team", "goal", "energy"],
        "Kerem joins basketball practice twice a week after school. "
        "At first he only wanted exercise, but he soon noticed that sport also taught him patience and focus. "
        "When the coach gives the team a goal, everyone has to support each other and stay alert. "
        "That makes practice useful both on and off the court.",
    ),
    entry(
        "Finding a Calm Daily Rhythm",
        "B1",
        "Günlük Hayat",
        ["routine", "balance", "quiet", "focus"],
        "For a long time, Aslı thought productive people always lived at a high speed. "
        "Later, she realized that a calmer routine gave her better focus and a stronger sense of balance. "
        "She now begins the day without looking at her phone, takes short breaks between tasks, and protects one quiet hour in the evening. "
        "Nothing about her schedule looks dramatic, yet it has made ordinary days feel more manageable and satisfying.",
    ),
    entry(
        "Preparing for a Group Presentation",
        "B1",
        "Okul",
        ["presentation", "student", "research", "teacher"],
        "Three students in the same class are preparing a group presentation about city life. "
        "At first, they all collect information separately, but their teacher reminds them that a good presentation needs one clear structure. "
        "After that, they divide the work more carefully and compare their research before making slides. "
        "The process takes longer than they expected, yet it helps them speak with more confidence on presentation day.",
    ),
    entry(
        "The Value of a Clear Agenda",
        "B1",
        "İş Hayatı",
        ["agenda", "meeting", "project", "team"],
        "Deniz works with a small team that handles several projects at the same time. "
        "When meetings do not have a clear agenda, people leave with different ideas about what to do next. "
        "She started writing a short agenda before each meeting and sending it to the team in advance. "
        "That simple change reduced confusion and helped everyone move from discussion to action much faster.",
    ),
    entry(
        "Choosing the Right Place to Stay",
        "B1",
        "Seyahat",
        ["travel", "hotel", "street", "choice"],
        "While planning a short trip, Emre noticed that choosing the right hotel was harder than buying the ticket. "
        "A beautiful room meant little if the street was noisy or the location made daily travel difficult. "
        "Instead of looking only at photos, he read detailed reviews and compared what other visitors said about comfort, transport, and safety. "
        "That careful approach helped him make a better decision and enjoy the city with less stress.",
    ),
    entry(
        "A Science Fair Revision",
        "B1",
        "Science",
        ["experiment", "result", "method", "fair"],
        "During the school science fair, Eren presented an experiment about plant growth and light. "
        "His first explanation focused only on the result, but his teacher encouraged him to explain the method more clearly. "
        "After he revised the poster, visitors understood why the comparison mattered and how the test had been designed. "
        "The project did not become more complex, but it became much easier to trust.",
    ),
    entry(
        "Health Habits That Last",
        "B1",
        "Health",
        ["health", "routine", "goal", "balance"],
        "Many people try to improve their health by making dramatic changes, but small habits often last longer. "
        "Melis began with better sleep, short walks, and more regular meals instead of following a strict plan. "
        "By focusing on one realistic goal each week, she avoided the pressure that usually made her quit too early. "
        "Her progress was not sudden, but it was steady enough to become part of daily life.",
    ),
    entry(
        "Learning Patience Through Sport",
        "B1",
        "Sport",
        ["practice", "team", "mistake", "coach"],
        "When Yusuf joined the volleyball team, he expected every practice to feel exciting from the first minute. "
        "Instead, he learned that improvement often comes from repeating small movements and correcting simple mistakes. "
        "His coach paid close attention to timing and discipline, which sometimes felt frustrating at first. "
        "Over time, Yusuf understood that patience was not separate from sport but one of its most useful lessons.",
    ),
    entry(
        "Meaning Inside Ordinary Hours",
        "B2",
        "Günlük Hayat",
        ["meaningful", "balance", "goal", "life"],
        "For a long time, Ekin believed that an interesting life required dramatic change, but she has slowly started to see value in smaller patterns. "
        "The balance she keeps between work, family, and personal goals does not look impressive from the outside, yet it makes her days feel meaningful. "
        "Instead of waiting for a perfect opportunity, she now pays attention to the quiet decisions that shape ordinary hours. "
        "That shift in perspective has not transformed her life overnight, but it has made her routine feel more deliberate, steady, and satisfying.",
    ),
    entry(
        "A Team Under Pressure",
        "B2",
        "İş Hayatı",
        ["deadline", "team", "project", "communication"],
        "When the project deadline moved forward by three days, the whole team had to adjust quickly. "
        "At first, people reacted with visible stress because every delay in communication created another layer of confusion. "
        "Their manager shortened meetings, clarified responsibilities, and pushed the group to focus on the most valuable tasks. "
        "The pressure did not disappear, but the team became more capable once communication turned sharper and more purposeful.",
    ),
    entry(
        "Arriving in a New City",
        "B2",
        "Seyahat",
        ["travel", "city", "different", "quiet"],
        "Travel often changes your attention before it changes your location. "
        "When Asya arrived in a new city, the first thing she noticed was not the famous buildings but the different rhythm of ordinary life. "
        "The streets were quieter than she expected, and even simple activities seemed to happen with more patience. "
        "By slowing down and observing instead of rushing through her plan, she discovered the character of the city through small details.",
    ),
    entry(
        "When Study Becomes Independent",
        "B2",
        "Okul",
        ["study", "independent", "teacher", "discipline"],
        "At the beginning of the year, Elif depended heavily on her teachers to tell her exactly what to read and when to review it. "
        "As the courses became more demanding, she learned that independent study required both discipline and judgment. "
        "She started planning her own revision sessions, identifying weak areas, and choosing which material deserved more time. "
        "That change did not make school easier, but it made her learning more intentional and much more mature.",
    ),
    entry(
        "A More Careful Health Decision",
        "B2",
        "Health",
        ["health", "choice", "habit", "evidence"],
        "People often make health decisions for emotional reasons and only later search for evidence that supports them. "
        "Mina noticed this in herself when she wanted to follow an extreme diet after reading a few persuasive posts online. "
        "Instead of acting immediately, she compared expert advice, looked for consistent evidence, and asked what kind of habit she could maintain for months rather than days. "
        "That more careful approach protected her from a dramatic choice that would probably not have lasted.",
    ),
    entry(
        "The Hidden Discipline of Science",
        "B2",
        "Science",
        ["science", "evidence", "observation", "pattern"],
        "Many people admire scientific discoveries without noticing how much discipline ordinary observation requires. "
        "A useful scientific pattern does not appear simply because someone hopes to find one; it emerges through patient comparison, revision, and doubt. "
        "Researchers must separate what looks interesting from what can actually be supported by evidence. "
        "That is why science depends as much on restraint and clarity as it does on imagination.",
    ),
    entry(
        "Sport Beyond the Scoreboard",
        "B2",
        "Sport",
        ["sport", "pressure", "performance", "focus"],
        "From the outside, sport often looks like a simple contest of strength, speed, or talent. "
        "From the inside, however, performance is shaped by pressure, rhythm, concentration, and the ability to recover from error. "
        "A player who loses focus for a few seconds can change the whole tone of a match, even if their skill remains the same. "
        "That is why serious training develops mental habits as carefully as physical ones.",
    ),
    entry(
        "A Demanding Perspective",
        "C1",
        "Serbest",
        ["challenge", "purpose", "result", "different"],
        "One of the most difficult parts of personal growth is recognizing that progress rarely feels dramatic while it is happening. "
        "A challenge often looks ordinary in the moment, which is why people overlook how deeply it can reshape their sense of purpose. "
        "Only later, when they compare an older version of themselves with a newer one, do they notice a different pattern of thinking, deciding, and responding. "
        "The result is not always visible to others, but it changes the internal logic of daily life in ways that are subtle and lasting.",
    ),
    entry(
        "The Social Texture of Travel",
        "C1",
        "Seyahat",
        ["travel", "culture", "attention", "experience"],
        "Travel is often described as movement across geography, yet its deeper impact usually comes from a shift in attention. "
        "A new place forces the traveler to interpret ordinary signals again, from tone of voice to the pace of public life. "
        "What seems efficient or polite in one setting may carry a different meaning in another, and this tension can either frustrate or educate the visitor. "
        "The most rewarding travel experiences therefore depend less on collecting attractions than on learning how to observe with patience.",
    ),
    entry(
        "High Standards at Work",
        "C1",
        "İş Hayatı",
        ["leadership", "responsibility", "pressure", "decision"],
        "In demanding workplaces, leadership is tested less by routine success than by the quality of decisions made under pressure. "
        "A manager who communicates well in calm conditions may still struggle when expectations rise, timelines contract, and responsibility becomes personal. "
        "What distinguishes stronger leaders is not confidence alone, but the ability to remain precise, distribute responsibility intelligently, and protect the team's focus. "
        "Under pressure, clarity becomes a form of stability rather than a stylistic preference.",
    ),
    entry(
        "Why School Still Matters",
        "C1",
        "Okul",
        ["education", "discipline", "curiosity", "judgment"],
        "School is sometimes reduced to a system for delivering information, but its deeper value lies in how it trains judgment. "
        "Students are not simply asked to remember facts; they are pushed to organize knowledge, compare perspectives, and defend their reasoning under scrutiny. "
        "When education works well, curiosity is not treated as decoration but as the engine that keeps discipline intellectually alive. "
        "That is why a good school experience can shape habits of thought long after specific lessons are forgotten.",
    ),
    entry(
        "The Ethics of Public Health",
        "C1",
        "Health",
        ["health", "policy", "evidence", "public"],
        "Public health decisions are rarely technical in a narrow sense, because evidence must always be interpreted within social reality. "
        "A policy that looks efficient on paper may fail if it ignores trust, access, or the everyday constraints that shape human behavior. "
        "This makes health planning both scientific and ethical: it must weigh measurable outcomes against unequal conditions and competing responsibilities. "
        "The challenge is not only to know what works, but to understand for whom it works and under what conditions it remains fair.",
    ),
    entry(
        "Science and Intellectual Restraint",
        "C1",
        "Science",
        ["theory", "science", "evidence", "restraint"],
        "Scientific thought is often associated with innovation, but its intellectual strength depends equally on restraint. "
        "A persuasive theory must not only explain a pattern elegantly; it must survive contact with evidence that could weaken or even overturn it. "
        "This requirement creates a culture of disciplined doubt in which claims are valued not for sounding impressive, but for remaining accountable to observation. "
        "In that sense, science advances through controlled humility as much as through brilliance.",
    ),
    entry(
        "Performance Under Watch",
        "C1",
        "Sport",
        ["performance", "focus", "pressure", "discipline"],
        "Elite sport exposes a paradox at the center of performance: the body must act freely while the mind remains under extraordinary control. "
        "Athletes train not only to improve movement, but to preserve judgment when emotion, fatigue, and public attention converge. "
        "A moment of hesitation can distort timing, while excessive self-consciousness can interrupt skill that is normally automatic. "
        "For this reason, discipline in sport is psychological as much as physical.",
    ),
    entry(
        "Research as a Structured Conversation",
        "Academic",
        "Akademik",
        ["research", "analysis", "evidence", "method"],
        "Effective research is rarely a matter of collecting information without structure. "
        "Instead, it depends on a method that connects analysis to evidence in a transparent way. "
        "A strong academic text makes its reasoning visible: it shows why certain sources were selected, how claims are supported, and where the limits of the argument remain. "
        "When students understand research as a structured conversation rather than a performance of complexity, they produce writing that is both more precise and more intellectually honest.",
    ),
    entry(
        "Interpreting Data Carefully",
        "Academic",
        "Akademik",
        ["data", "result", "theory", "analysis"],
        "Data does not automatically produce understanding. "
        "Before any result can be treated as meaningful, it must be interpreted through a careful process of analysis and comparison. "
        "Theory becomes useful here because it provides a framework for deciding what matters, what counts as a pattern, and what may simply be noise. "
        "Without that framework, even accurate data can lead to weak conclusions and overstated claims.",
    ),
    entry(
        "Academic Writing and Precision",
        "Academic",
        "Akademik",
        ["argument", "source", "claim", "precision"],
        "Academic writing gains authority not from complexity alone, but from disciplined precision. "
        "A well-developed argument defines its central claim, distinguishes evidence from interpretation, and signals where uncertainty remains. "
        "This precision matters because readers must be able to follow not only what the writer believes, but how that position was constructed. "
        "Clarity, in this sense, is not the opposite of sophistication; it is one of its strongest forms.",
    ),
    entry(
        "From Evidence to Interpretation",
        "Academic",
        "Science",
        ["evidence", "interpretation", "model", "finding"],
        "Scientific findings become academically useful only when the movement from evidence to interpretation is carefully explained. "
        "A dataset may reveal regularities, but those regularities still require a conceptual model that identifies what they mean and why they matter. "
        "This is why strong academic science writing does more than report results: it positions those results within a wider argument about method, limitation, and significance. "
        "Interpretation is therefore not an optional extra but the bridge between raw observation and knowledge.",
    ),
    entry(
        "Health Research and Public Claims",
        "Academic",
        "Health",
        ["health", "study", "evidence", "claim"],
        "Public discussion of health research often moves faster than the evidence can responsibly support. "
        "A single study may attract attention because its claim is easy to repeat, yet its scope, sample, and limitations are often ignored in wider circulation. "
        "Academic analysis slows this process down by asking how conclusions were drawn, what kind of evidence was used, and whether the result can reasonably be generalized. "
        "That slower reading protects inquiry from becoming speculation dressed as certainty.",
    ),
]


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
