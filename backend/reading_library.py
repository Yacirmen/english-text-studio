from __future__ import annotations

from typing import Any


READING_SEEDS: list[dict[str, Any]] = [
    {
        "title": "A Simple Morning Routine",
        "level": "A1",
        "topic": "Günlük Hayat",
        "keywords": ["morning", "coffee", "bus", "friend"],
        "text": (
            "Every morning, Lina wakes up at seven. She drinks coffee in the kitchen and checks the time. "
            "Then she walks to the bus stop near her home. On the bus, she often sees her friend Ece. "
            "They talk about school, music, and their plans for the day. The ride is short, but it helps Lina feel ready. "
            "When she arrives, she is calm, awake, and happy to begin."
        ),
    },
    {
        "title": "After-School Library Time",
        "level": "A1",
        "topic": "Okul",
        "keywords": ["student", "library", "teacher", "study"],
        "text": (
            "Mert is a student at a small school. After class, he goes to the library with his teacher. "
            "He wants to study for a science test. The library is quiet and bright, so it is easy to focus. "
            "His teacher shows him a short text and asks simple questions. Mert writes the answers in his notebook. "
            "He feels more confident before he goes home."
        ),
    },
    {
        "title": "Getting Ready for a Trip",
        "level": "A2",
        "topic": "Seyahat",
        "keywords": ["airport", "ticket", "hotel", "travel"],
        "text": (
            "Selin is getting ready for a short trip to Izmir. She checks her ticket twice before leaving home because she does not want any problem at the airport. "
            "Her bag is small, but she packs carefully so she can travel comfortably. After she lands, she plans to take a taxi to her hotel and rest for a while. "
            "Although the trip is short, she feels excited because a new city always gives her fresh energy and ideas."
        ),
    },
    {
        "title": "An Easy Workday Plan",
        "level": "A2",
        "topic": "İş Hayatı",
        "keywords": ["meeting", "office", "email", "plan"],
        "text": (
            "On Monday morning, Arda arrives at the office before his first meeting. He opens his laptop, reads an important email from his manager, and updates his plan for the day. "
            "The team has a short meeting at ten, so he uses the early hours to organize his notes. Because he prepares in advance, the rest of the day feels smoother and less stressful. "
            "A clear plan helps him finish his work without rushing."
        ),
    },
    {
        "title": "A Balanced School Week",
        "level": "B1",
        "topic": "Okul",
        "keywords": ["student", "exam", "teacher", "goal"],
        "text": (
            "Zeynep is a student who tries to keep her school week balanced. She has an exam on Friday, but she does not want to leave all her work until the last night. "
            "Instead, she studies a little each day and asks her teacher questions when something is unclear. This habit makes her feel more relaxed and gives her a clear goal for each evening. "
            "By the time the exam arrives, she is tired but prepared, and that confidence changes the way she performs."
        ),
    },
    {
        "title": "Working Through a Busy Day",
        "level": "B1",
        "topic": "İş Hayatı",
        "keywords": ["project", "team", "office", "task"],
        "text": (
            "At the office, Deniz is helping her team finish an important project before the weekend. Every task looks small at first, but together they create a long list of work that needs real attention. "
            "She starts by choosing the most urgent part and then speaks with her team about what can wait. This simple method keeps everyone calmer and makes the project easier to manage. "
            "By the afternoon, the office still feels busy, but it no longer feels confusing."
        ),
    },
    {
        "title": "Finding Meaning in Routine",
        "level": "B2",
        "topic": "Günlük Hayat",
        "keywords": ["balance", "goal", "meaningful", "life"],
        "text": (
            "For a long time, Ekin believed that an interesting life required dramatic change, but she has slowly started to see value in smaller patterns. "
            "The balance she keeps between work, family, and personal goals does not look impressive from the outside, yet it makes her days feel meaningful. "
            "Instead of waiting for a perfect opportunity, she now pays attention to the quiet decisions that shape ordinary hours. "
            "That shift in perspective has not transformed her life overnight, but it has made her routine feel more deliberate, steady, and satisfying."
        ),
    },
    {
        "title": "A Team Under Pressure",
        "level": "B2",
        "topic": "İş Hayatı",
        "keywords": ["deadline", "team", "project", "communication"],
        "text": (
            "When the project deadline moved forward by three days, the whole team had to adjust quickly. At first, people reacted with visible stress, because each delay in communication created another layer of confusion. "
            "Their manager decided to shorten meetings, clarify responsibilities, and keep the team focused on the most valuable tasks. "
            "That change did not remove the pressure, but it stopped the atmosphere from becoming chaotic. By the end of the week, the project was still demanding, yet the team felt far more capable because their communication had become sharper and more purposeful."
        ),
    },
    {
        "title": "Arriving in a New City",
        "level": "B2",
        "topic": "Seyahat",
        "keywords": ["travel", "city", "different", "quiet"],
        "text": (
            "Travel often changes your attention before it changes your location. When Asya arrived in a new city, the first thing she noticed was not the famous buildings but the different rhythm of ordinary life. "
            "The streets were quieter than she expected, and even simple activities seemed to happen with more patience. Instead of rushing through her plan, she decided to slow down and observe. "
            "That choice made the trip more rewarding, because the city gradually revealed its character through small details rather than obvious attractions."
        ),
    },
    {
        "title": "A More Demanding Perspective",
        "level": "C1",
        "topic": "Serbest",
        "keywords": ["challenge", "purpose", "result", "different"],
        "text": (
            "One of the most difficult parts of personal growth is recognizing that progress rarely feels dramatic while it is happening. A challenge often looks ordinary in the moment, which is why people overlook how deeply it can reshape their sense of purpose. "
            "Only later, when they compare an old version of themselves with a newer one, do they notice a different pattern of thinking, deciding, and responding. "
            "The result is not always visible to other people, but it changes the internal logic of daily life in ways that are both subtle and lasting."
        ),
    },
    {
        "title": "Research as a Structured Conversation",
        "level": "Academic",
        "topic": "Akademik",
        "keywords": ["research", "analysis", "evidence", "method"],
        "text": (
            "Effective research is rarely a matter of collecting information without structure. Instead, it depends on a method that connects analysis to evidence in a transparent way. "
            "A strong academic text makes its reasoning visible: it shows why certain sources were selected, how claims are supported, and where the limits of the argument remain. "
            "When students understand research as a structured conversation rather than a performance of complexity, they become more capable of producing writing that is both precise and intellectually honest."
        ),
    },
    {
        "title": "Interpreting Data Carefully",
        "level": "Academic",
        "topic": "Akademik",
        "keywords": ["data", "result", "theory", "analysis"],
        "text": (
            "Data does not automatically produce understanding. Before any result can be treated as meaningful, it must be interpreted through a careful process of analysis and comparison. "
            "This is where theory becomes useful: it gives researchers a framework for deciding what matters, what counts as a pattern, and what may simply be noise. "
            "Without that framework, even accurate data can lead to weak conclusions. Good academic work, therefore, depends not only on gathering information but also on explaining how interpretation was shaped."
        ),
    },
    {
        "title": "A Small Science Fair Project",
        "level": "B1",
        "topic": "Science",
        "keywords": ["experiment", "result", "method", "student"],
        "text": (
            "During the school science fair, a student named Eren presented a simple experiment about plant growth and light. "
            "He explained his method carefully so visitors could understand how the project worked from start to finish. "
            "Although the result was not surprising, the way he compared each stage made the presentation stronger. "
            "His teacher said that good science is not only about discovering something new, but also about showing clear thinking and honest observation."
        ),
    },
    {
        "title": "Building Better Health Habits",
        "level": "B1",
        "topic": "Health",
        "keywords": ["health", "routine", "balance", "goal"],
        "text": (
            "Many people try to improve their health by making dramatic changes, but small habits often last longer. "
            "Melis began with a simple routine: better sleep, short walks, and more regular meals. "
            "Instead of chasing a perfect result, she focused on balance and chose one realistic goal each week. "
            "That slower method helped her feel more energetic without turning the process into a stressful challenge."
        ),
    },
    {
        "title": "Learning Through Sport",
        "level": "A2",
        "topic": "Sport",
        "keywords": ["team", "goal", "practice", "energy"],
        "text": (
            "Kerem joins his school basketball team twice a week. At first, he only wanted exercise, but regular practice taught him more than that. "
            "He learned how a team works, how to stay calm after mistakes, and how to keep his energy for the right moment. "
            "When the coach gives the team a goal, everyone has to support each other. This makes sport feel useful both on and off the court."
        ),
    },
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
