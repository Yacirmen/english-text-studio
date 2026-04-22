import hashlib
import json
import os
import random
import re
import secrets
import smtplib
import sqlite3
from collections import Counter
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx
import bcrypt
from fastapi import Cookie, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field
from backend.lexical_engine import covered_token_indexes, match_phrases, resolve_phrase, token_records
from backend.reading_library import READING_SEEDS, normalize_topic

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:  # pragma: no cover
    psycopg = None
    dict_row = None


ROOT_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT_DIR / "frontend"
ENV_PATH = ROOT_DIR / ".env"
DB_PATH = Path(os.getenv("READLEX_DB_PATH", str(ROOT_DIR / "backend" / "app.db"))).resolve()
CURATED_LIBRARY_SOURCE = "desktop_curated"
CURATED_READINGS_PATH = ROOT_DIR / "backend" / "curated_readings.txt"
EXTRA_WORD_MAP_PATH = ROOT_DIR / "backend" / "extra_word_map.json"
LIBRARY_WORD_MAP_PATH = ROOT_DIR / "backend" / "library_word_map.json"
CEFR_VOCAB_INDEX_PATH = ROOT_DIR / "backend" / "cefr_vocab_index.json"
SESSION_COOKIE = "readlex_session"
WORD_DETAIL_CACHE: dict[str, dict[str, str]] = {}
GENERATE_CACHE: dict[str, str] = {}
EXTRA_WORD_MAP: dict[str, str] = {}
LIBRARY_WORD_MAP: dict[str, str] = {}
APPROVED_LEXICAL_MAP: dict[str, str] = {}
APPROVED_LEXICAL_MAP_READY = False
CEFR_VOCAB_INDEX: dict[str, dict[str, Any]] = {}
QUIZ_DISTRACTOR_BANK = {
    "verb": ["kaydetmek", "yorumlamak", "ta??mak", "dengelemek", "kar??la?t?rmak", "geli?tirmek"],
    "adjective": ["d?zenli", "kar???k", "dar", "geni?", "yo?un", "sakin", "net", "karma??k", "yava?", "h?zl?", "g??l?", "zay?f"],
    "noun": ["ama?", "denge", "al??kanl?k", "kan?t", "yolculuk", "odak", "fikir", "yorum", "kavram", "??z?m"],
}
LEVEL_CONFIG = {
    "A1": {"min_words": 60, "max_words": 100, "label": "Ã‡ok temel ve gÃ¼nlÃ¼k"},
    "A2": {"min_words": 90, "max_words": 130, "label": "Basit ve gÃ¼nlÃ¼k"},
    "B1": {"min_words": 120, "max_words": 170, "label": "DoÄŸal ve akÄ±cÄ±"},
    "B2": {"min_words": 150, "max_words": 220, "label": "Daha zengin ama rahat okunur"},
    "C1": {"min_words": 180, "max_words": 260, "label": "Ä°leri, doÄŸal ve detaylÄ±"},
    "C2": {"min_words": 190, "max_words": 280, "label": "Ã‡ok ileri ve incelikli"},
    "Academic": {"min_words": 190, "max_words": 280, "label": "Akademik ve daha analitik"},
}
CEFR_LEVEL_ORDER = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6, "Academic": 6}
READING_LEVEL_TARGETS = {
    "A1": {"target": "A1", "ideal_avg": 7, "max_avg": 9, "advanced_min": 0, "needs_contrast": False, "needs_cause": False},
    "A2": {"target": "A2", "ideal_avg": 9, "max_avg": 12, "advanced_min": 0, "needs_contrast": False, "needs_cause": True},
    "B1": {"target": "B1", "ideal_avg": 13, "max_avg": 17, "advanced_min": 0, "needs_contrast": True, "needs_cause": True},
    "B2": {"target": "B2", "ideal_avg": 17, "max_avg": 22, "advanced_min": 2, "needs_contrast": True, "needs_cause": True},
    "C1": {"target": "C1", "ideal_avg": 20, "max_avg": 26, "advanced_min": 4, "needs_contrast": True, "needs_cause": True},
    "C2": {"target": "C2", "ideal_avg": 23, "max_avg": 30, "advanced_min": 5, "needs_contrast": True, "needs_cause": True},
    "Academic": {"target": "C2", "ideal_avg": 23, "max_avg": 30, "advanced_min": 5, "needs_contrast": True, "needs_cause": True},
}
GENERIC_OPENING_PATTERNS = (
    "most people",
    "many people",
    "the goal is",
    "in today's world",
    "at first",
    "seen analytically",
)
CONTRAST_MARKERS = ("although", "however", "while", "yet", "whereas", "even though")
CAUSE_MARKERS = ("because", "therefore", "so that", "as a result", "since", "consequently")
LOCAL_WORD_MAP = {
    "academic": "akademik",
    "airport": "havaalanÄ±",
    "analysis": "analiz",
    "balance": "denge",
    "busy": "yoÄŸun",
    "bus": "otobÃ¼s",
    "calm": "sakin",
    "challenge": "zorluk",
    "city": "ÅŸehir",
    "coffee": "kahve",
    "collaboration": "iÅŸ birliÄŸi",
    "concept": "kavram",
    "data": "veri",
    "different": "farklÄ±",
    "difficult": "zor",
    "early": "erken",
    "education": "eÄŸitim",
    "email": "e-posta",
    "exam": "sÄ±nav",
    "evidence": "kanÄ±t",
    "flexible": "esnek",
    "friend": "arkadaÅŸ",
    "goal": "hedef",
    "happy": "mutlu",
    "hotel": "otel",
    "important": "Ã¶nemli",
    "late": "geÃ§",
    "library": "kÃ¼tÃ¼phane",
    "life": "hayat",
    "meaningful": "anlamlÄ±",
    "meeting": "toplantÄ±",
    "method": "yÃ¶ntem",
    "morning": "sabah",
    "office": "ofis",
    "plan": "plan",
    "project": "proje",
    "purpose": "amaÃ§",
    "quiet": "sessiz",
    "research": "araÅŸtÄ±rma",
    "result": "sonuÃ§",
    "rewarding": "tatmin edici",
    "school": "okul",
    "simple": "basit",
    "student": "Ã¶ÄŸrenci",
    "study": "Ã§alÄ±ÅŸma",
    "task": "gÃ¶rev",
    "teacher": "Ã¶ÄŸretmen",
    "team": "ekip",
    "ticket": "bilet",
    "travel": "seyahat etmek",
    "work": "iÅŸ",
    "workday": "iÅŸ gÃ¼nÃ¼",
}
LOCAL_WORD_MAP.update(
    {
        "achieve": "baÅŸarmak",
        "achievement": "baÅŸarÄ±",
        "active": "aktif",
        "activity": "etkinlik",
        "adapt": "uyum saÄŸlamak",
        "adjust": "ayarlamak",
        "advice": "tavsiye",
        "affect": "etkilemek",
        "afternoon": "Ã¶ÄŸleden sonra",
        "agree": "kabul etmek",
        "allow": "izin vermek",
        "already": "zaten",
        "amazing": "harika",
        "answer": "cevap",
        "approach": "yaklaÅŸÄ±m",
        "article": "makale",
        "artist": "sanatÃ§Ä±",
        "attention": "dikkat",
        "available": "mevcut",
        "begin": "baÅŸlamak",
        "benefit": "fayda",
        "better": "daha iyi",
        "book": "kitap",
        "break": "mola",
        "careful": "dikkatli",
        "career": "kariyer",
        "change": "deÄŸiÅŸim",
        "choice": "seÃ§im",
        "college": "Ã¼niversite",
        "comfortable": "rahat",
        "communication": "iletiÅŸim",
        "community": "topluluk",
        "conference": "konferans",
        "confident": "Ã¶zgÃ¼venli",
        "continue": "devam etmek",
        "conversation": "sohbet",
        "create": "oluÅŸturmak",
        "crowded": "kalabalÄ±k",
        "deadline": "son tarih",
        "decision": "karar",
        "deliver": "teslim etmek",
        "design": "tasarÄ±m",
        "detail": "ayrÄ±ntÄ±",
        "discussion": "tartÄ±ÅŸma",
        "discover": "keÅŸfetmek",
        "easy": "kolay",
        "effective": "etkili",
        "effort": "Ã§aba",
        "energy": "enerji",
        "environment": "Ã§evre",
        "example": "Ã¶rnek",
        "experience": "deneyim",
        "explain": "aÃ§Ä±klamak",
        "explore": "keÅŸfetmek",
        "family": "aile",
        "feature": "Ã¶zellik",
        "feedback": "geri bildirim",
        "feeling": "duygu",
        "final": "son",
        "focus": "odak",
        "future": "gelecek",
        "gain": "kazanmak",
        "grade": "not",
        "growth": "geliÅŸim",
        "habit": "alÄ±ÅŸkanlÄ±k",
        "health": "saÄŸlÄ±k",
        "helpful": "yararlÄ±",
        "highlight": "vurgulamak",
        "history": "geÃ§miÅŸ",
        "idea": "fikir",
        "improve": "geliÅŸtirmek",
        "include": "iÃ§ermek",
        "independent": "baÄŸÄ±msÄ±z",
        "information": "bilgi",
        "insight": "iÃ§gÃ¶rÃ¼",
        "interview": "gÃ¶rÃ¼ÅŸme",
        "journey": "yolculuk",
        "knowledge": "bilgi birikimi",
        "listen": "dinlemek",
        "manage": "yÃ¶netmek",
        "manager": "yÃ¶netici",
        "market": "pazar",
        "material": "materyal",
        "measure": "Ã¶lÃ§mek",
        "modern": "modern",
        "motivate": "motive etmek",
        "natural": "doÄŸal",
        "network": "aÄŸ",
        "notice": "fark etmek",
        "opportunity": "fÄ±rsat",
        "organize": "dÃ¼zenlemek",
        "outcome": "sonuÃ§",
        "patient": "sabÄ±rlÄ±",
        "pattern": "Ã¶rÃ¼ntÃ¼",
        "people": "insanlar",
        "performance": "performans",
        "personal": "kiÅŸisel",
        "place": "yer",
        "positive": "olumlu",
        "practice": "pratik",
        "prepare": "hazÄ±rlamak",
        "present": "sunmak",
        "pressure": "baskÄ±",
        "priority": "Ã¶ncelik",
        "problem": "sorun",
        "process": "sÃ¼reÃ§",
        "promote": "teÅŸvik etmek",
        "question": "soru",
        "quick": "hÄ±zlÄ±",
        "realistic": "gerÃ§ekÃ§i",
        "reason": "neden",
        "record": "kayÄ±t",
        "reflect": "yansÄ±tmak",
        "regular": "dÃ¼zenli",
        "relationship": "iliÅŸki",
        "month": "ay",
        "routine": "rutin",
        "realistic": "gerçekçi",
        "evening": "akşam",
        "story": "hikâye",
        "phrase": "ifade / kalıp",
        "context": "bağlam",
        "notice": "fark etmek",
        "carefully": "dikkatlice",
        "together": "birlikte",
        "stressed": "stresli",
        "rush": "acele etmek",
        "rushing": "acele etme",
        "weekend": "hafta sonu",
        "video": "video",
        "plane": "uçak",
        "planes": "uçaklar",
        "expect": "beklemek",
        "expected": "beklenen",
        "recognize": "tanımak / fark etmek",
        "common": "yaygın",
        "pattern": "örüntü",
        "patterns": "örüntüler",
        "faster": "daha hızlı",
    }
)

LOCAL_PHRASE_MAP = {
    "work life": "iş hayatı",
    "daily life": "günlük hayat",
    "saved words": "kaydedilmiş kelimeler",
    "quick review": "hızlı tekrar",
    "word history": "kelime geçmişi",
    "reading stage": "okuma alanı",
    "reading setup": "okuma ayarları",
    "break up": "ayrılmak",
    "give up": "vazgeçmek",
    "look after": "ilgilenmek / bakmak",
    "set up": "kurmak",
    "run into": "karşılaşmak",
    "figure out": "çözmek / anlamak",
    "take off": "havalanmak",
    "turn out": "sonuçlanmak / ortaya çıkmak",
    "calm down": "sakinleşmek",
    "get along": "iyi geçinmek",
    "classroom-based": "sınıf temelli",
    "decision-making": "karar verme",
    "e-posta": "e-posta",
    "evidence-based": "kanıta dayalı",
    "face-to-face": "yüz yüze",
    "fast-paced": "hızlı tempolu",
    "high-quality": "yüksek kaliteli",
    "home-cooked": "ev yapımı",
    "mini-computers": "mini bilgisayarlar",
    "non-verbal": "sözsüz",
    "old-fashioned": "eski moda",
    "one-time": "tek seferlik",
    "open-minded": "açık fikirli",
    "real-life": "gerçek hayat",
    "real-world": "gerçek dünya",
    "self-awareness": "öz farkındalık",
    "self-discipline": "öz disiplin",
    "short-term": "kısa vadeli",
    "thirty-minute": "otuz dakikalık",
    "two-hour": "iki saatlik",
    "well-being": "iyi oluş",
    "always-connected": "sürekli bağlantıda",
    "work-life": "iş-yaşam",
    "work-life balance": "iş-yaşam dengesi",
    "work life balance": "iş-yaşam dengesi",
    "post-truth": "hakikat sonrası",
    "fight-or-flight": "savaş ya da kaç",
    "black box": "kara kutu",
    "black boxes": "kara kutular",
    "decision making": "karar verme",
    "social media": "sosyal medya",
    "mental health": "ruh sağlığı",
    "climate change": "iklim değişikliği",
    "climate crisis": "iklim krizi",
    "space exploration": "uzay araştırmaları",
    "space tourism": "uzay turizmi",
    "outer space": "dış uzay",
    "outer space treaty": "Dış Uzay Antlaşması",
    "basic income": "temel gelir",
    "universal basic income": "evrensel temel gelir",
    "blue-collar": "mavi yakalı",
    "white-collar": "beyaz yakalı",
    "low-earth orbit": "alçak dünya yörüngesi",
    "low earth orbit": "alçak dünya yörüngesi",
    "earth observation": "yer gözlemi",
    "closed-loop": "kapalı döngü",
    "open-plan": "açık plan",
    "mixed-use": "karma kullanımlı",
    "face to face": "yüz yüze",
    "in conclusion": "sonuç olarak",
    "to summarize": "özetle",
    "for instance": "örneğin",
    "in contrast": "buna karşılık",
    "in reality": "gerçekte",
    "in summary": "özet olarak",
    "in light of": "... ışığında",
    "in the long term": "uzun vadede",
    "in the short term": "kısa vadede",
    "due to": "nedeniyle",
    "rather than": "yerine",
    "in favor of": "lehine",
    "means-tested": "gelir testine dayalı",
    "zero-carbon": "sıfır karbon",
    "zero carbon": "sıfır karbon",
    "de-extinction": "yeniden tür canlandırma",
    "multi-planetary": "çok gezegenli",
    "long-term": "uzun vadeli",
    "short-term contracts": "kısa süreli sözleşmeler",
    "genetic modification": "genetik değişim",
    "human embryos": "insan embriyoları",
    "science fiction": "bilim kurgu",
    "gene editing": "gen düzenleme",
    "hereditary diseases": "kalıtsal hastalıklar",
    "designer babies": "tasarım bebekler",
    "cognitive abilities": "bilişsel yetenekler",
    "socioeconomic inequalities": "sosyoekonomik eşitsizlikler",
    "human genome": "insan genomu",
    "digital detox": "dijital detoks",
    "solitary introspection": "yalnız iç gözlem",
    "cognitive downtime": "zihinsel dinlenme süresi",
    "open-plan offices": "açık ofis düzenleri",
    "biophilic design": "biyofilik tasarım",
    "natural light": "doğal ışık",
    "public safety": "kamu güvenliği",
    "social cohesion": "toplumsal uyum",
    "solar radiation management": "güneş ışınımı yönetimi",
    "carbon fertilization": "karbon gübreleme",
    "stratospheric aerosol injection": "stratosfere aerosol enjeksiyonu",
    "greenhouse gas": "sera gazı",
    "sea levels": "deniz seviyeleri",
    "weather patterns": "hava düzenleri",
    "analysis paralysis": "karar felci",
    "buyer's remorse": "satın alma pişmanlığı",
    "mother tongue": "ana dil",
    "gig economy": "gig ekonomisi",
    "independent contractors": "bağımsız çalışanlar",
    "collective bargaining": "toplu pazarlık",
    "artificial general intelligence": "yapay genel zeka",
    "structural unemployment": "yapısal işsizlik",
    "machine learning": "makine öğrenmesi",
    "mri scans": "MR taramaları",
    "ct scans": "BT taramaları",
    "life support systems": "yaşam destek sistemleri",
    "earth-observation satellites": "yer gözlem uyduları",
    "orbital debris": "yörünge enkazı",
    "kessler syndrome": "Kessler sendromu",
    "space commercialization": "uzayın ticarileşmesi",
    "post-truth era": "hakikat sonrası çağ",
    "false equivalence": "sahte eşdeğerlik",
    "restorative justice": "onarıcı adalet",
    "cognitive enhancers": "bilişsel güçlendiriciler",
    "smart drugs": "zeka artırıcı ilaçlar",
    "surveillance capitalism": "gözetim kapitalizmi",
    "personal data": "kişisel veri",
    "hate speech": "nefret söylemi",
    "militant democracy": "militan demokrasi",
    "de-extinction technology": "tür diriltme teknolojisi",
}

FEATURED_PHRASAL_READING: dict[str, Any] = {
    "title": "Phrasal Verbs Demo (B1)",
    "level": "B1",
    "topic": "Random",
    "keywords": [
        "break up",
        "give up",
        "look after",
        "set up",
        "run into",
        "figure out",
        "take off",
        "turn out",
        "calm down",
        "get along",
    ],
    "text": (
        "Last month, my friend Ece decided to start a simple routine for learning English. "
        "She kept it realistic: fifteen minutes each evening, no pressure, but no excuses. "
        "In the first week, she almost wanted to give up, because some verbs behaved differently when they worked with a small word. "
        "For example, she saw 'break up' in a sentence and realized it is a phrase with its own meaning. "
        "The next day, she ran into 'give up' again and noticed the pattern: one extra word can change the whole idea. "
        "So she began to look after these phrases like real vocabulary: she wrote them down and practiced them in short sentences. "
        "When she felt stressed, she would calm down, read the sentence again, and try to figure out the meaning from context. "
        "At the weekend, she watched a short video and heard a pilot say 'take off', which helped her remember the phrase. "
        "After two weeks, the routine turned out to work well, and she could get along with B1 texts more easily."
    ),
}

if not any(str(item.get("title") or "") == FEATURED_PHRASAL_READING["title"] for item in READING_SEEDS):
    READING_SEEDS.insert(0, FEATURED_PHRASAL_READING)

IRREGULAR_WORD_MAP = {
    "cluttered": "karışık",
    "interpreted": "yorumlanmı",
    "narrow": "dar",
}

WORD_MEANING_OVERRIDES = {
    "the": "belirli tanımlık",
    "in": "içinde",
    "for": "için",
    "than": "-den / kıyasla",
    "when": "-dığı zaman",
    "on": "üzerinde",
    "not": "değil",
    "start": "başlamak",
    "started": "başlamak",
    "decide": "karar vermek",
    "decided": "karar vermek",
    "almost": "neredeyse",
    "excuse": "bahane",
    "excuses": "bahaneler",
    "sentence": "cümle",
    "sentences": "cümleler",
    "pilot": "pilot",
    "often": "sık sık",
    "how": "nasıl",
    "no": "hayır / yok",
    "by": "tarafından / ile",
    "down": "aşağı",
    "during": "sırasında",
    "about": "hakkında",
    "because": "çünkü",
    "however": "ancak",
    "although": "her ne kadar",
    "while": "iken",
    "since": "çünkü",
    "therefore": "bu nedenle",
    "consequently": "sonuç olarak",
    "illustrate": "örneklemek",
    "model": "model",
    "simplified": "sadeleştirmiş",
    "illustrates": "örneklemek",
    "illustrated": "örneklemek",
    "illustrating": "örneklemek",
    "fragment": "parça",
    "fragmented": "parçalanmış",
    "may": "-ebilir / olabilir",
    "did": "yaptı",
    "do": "yapmak",
    "there": "orada",
    "up": "yukarı / kadar",
    "go": "gitmek",
    "keep": "sürdürmek",
    "risk": "risk",
    "platform": "platform",
    "video": "video",
    "stress": "stres",
    "festival": "festival",
    "program": "program",
    "many": "birçok",
    "need": "ihtiyaç duymak",
    "park": "park",
    "well": "iyi",
    "take": "almak",
    "know": "bilmek",
    "other": "diğer",
    "such": "böyle / gibi",
    "internet": "internet",
    "should": "-meli / -malı",
    "off": "kapalı / kapatmak",
    "all": "hepsi / tüm",
    "second": "ikinci",
    "modern": "modern",
    "might": "olabilir",
    "must": "zorunda / mutlaka",
    "bad": "kötü",
    "quite": "oldukça",
    "tv": "televizyon",
    "deeply": "derinden / son derece",
    "flexibility": "esneklik",
    "mini-computers": "mini bilgisayarlar",
    "responsibly": "sorumlu bir şekilde",
    "globalized": "küreselleşmiş",
    "loneliness": "yalnızlık",
    "thirty-minute": "otuz dakikalık",
    "sports": "sporlar",
    "sport": "spor",
    "careless": "dikkatsiz",
    "litter": "çöp atmak / çöp",
    "overcrowding": "aşırı kalabalık",
    "toefl": "TOEFL sınavı",
    "ielts": "IELTS sınavı",
    "old-fashioned": "eski moda",
    "self-discipline": "öz disiplin",
    "high": "yüksek",
    "multitasking": "çoklu görev yapma",
    "prioritize": "önceliklendirmek",
    "face-to-face": "yüz yüze",
    "weaken": "zayıflatmak",
    "well-being": "iyi oluş hali",
    "unused": "kullanılmayan",
    "persistence": "sebat",
    "real-life": "gerçek hayat",
    "open-minded": "açık fikirli",
    "teamwork": "takım çalışması",
    "misunderstand": "yanlış anlamak",
    "non-verbal": "sözsüz",
    "high-quality": "yüksek kaliteli",
    "undergone": "geçirmiş",
    "unreliable": "güvenilmez",
    "mindful": "bilinçli / farkında",
    "overwhelm": "bunaltmak",
    "reconsider": "yeniden değerlendirmek",
    "industrialization": "sanayileşme",
    "short-term": "kısa vadeli",
    "overriding": "baskın / belirleyici",
    "maximize": "en üst düzeye çıkarmak",
    "inaccurate": "hatalı / doğru olmayan",
    "one-time": "tek seferlik",
    "self-awareness": "öz farkındalık",
    "unknowingly": "farkında olmadan",
    "misjudgments": "yanlış yargılar",
    "subtly": "ince bir şekilde",
    "real-world": "gerçek dünya",
    "reshape": "yeniden şekillendirmek",
    "stimuli": "uyaranlar",
    "far": "uzak / çok",
    "restructuring": "yeniden yapılandırma",
    "hinder": "engellemek",
    "prioritizing": "önceliklendirme",
    "quantitative": "nicel",
    "within": "içinde",
    "perceive": "algılamak",
    "low": "düşük",
    "misinterpreted": "yanlış yorumlanmış",
    "underestimate": "hafife almak",
    "overestimate": "fazla tahmin etmek",
    "misunderstood": "yanlış anlaşılmış",
    "instability": "istikrarsızlık",
    "inefficiency": "verimsizlik",
    "superficial": "yüzeysel",
    "adjectives": "sıfatlar",
    "adverbs": "zarflar",
    "also": "ayrıca",
    "analytical": "analitik",
    "always": "her zaman",
    "another": "başka bir",
    "best": "en iyi",
    "classroom-based": "sınıf temelli",
    "collocations": "kelime eşleşmeleri",
    "inspectable": "incelenebilir",
    "recognizable": "tanınabilir",
    "measurable": "ölçülebilir",
    "interpretive": "yoruma dayalı",
    "reflective": "düşünsel",
    "accessibility": "erişilebilirlik",
    "accomplishment": "başarı",
    "align": "uyum sağlamak",
    "allocate": "tahsis etmek",
    "alteration": "değişiklik",
    "amplify": "güçlendirmek",
    "broaden": "genişletmek",
    "cognition": "biliş",
    "cohesive": "bütünlüklü",
    "collaborate": "iş birliği yapmak",
    "communicative": "iletişimsel",
    "comprehension": "kavrayış",
    "conformity": "uyum gösterme",
    "connectivity": "bağlantısallık",
    "cross-functional": "fonksiyonlar arası",
    "contextual": "bağlamsal",
    "contradict": "çelişmek",
    "conversely": "tersine",
    "curate": "seçip düzenlemek",
    "current-affairs": "güncel olaylar",
    "decision-making": "karar verme",
    "depletion": "tükenme",
    "disconnect": "kopukluk",
    "disadvantages": "dezavantajlar",
    "discourage": "cesaret kırmak",
    "disproportionate": "orantısız",
    "durable": "kalıcı",
    "evidence-based": "kanıta dayalı",
    "either": "ya da / herhangi biri",
    "emphasizes": "vurgular",
    "encompasses": "kapsar",
    "energetic": "enerjik",
    "errands": "ufak işler",
    "estimations": "tahminler",
    "factual": "olgusal",
    "familiarity": "aşinalık",
    "fast-paced": "hızlı tempolu",
    "favorite": "favori",
    "find": "bulmak",
    "flawed": "kusurlu",
    "going": "gitmek / ilerlemek",
    "grandparent": "büyükanne veya büyükbaba",
    "have": "sahip olmak",
    "informational": "bilgilendirici",
    "integrate": "bütünleştirmek",
    "interpersonal": "kişilerarası",
    "intrinsic": "içsel",
    "intuitive": "sezgisel",
    "misconception": "yanlış kanı",
    "misinformation": "yanlış bilgi",
    "overload": "aşırı yüklenme",
    "polarized": "kutuplaşmış",
    "resilience": "dayanıklılık",
    "reinforce": "pekiştirmek",
    "verification": "doğrulama",
    "shortcuts": "kısayollar",
    "irritated": "sinirli",
    "misguided": "yanlış yönlendirilmiş",
    "disciplined": "disiplinli",
    "blurred": "bulanık",
    "unsupported": "desteklenmeyen",
    "wanted": "istenen",
    "needed": "gerekli",
    "looked": "göründü",
    "unfocused": "odaksız",
    "unresolved": "çözülmemiş",
    "before": "önce",
    "inside": "içinde",
    "over": "üzerinde / boyunca",
    "near": "yakınında",
    "much": "çok",
    "most": "çoğu / en çok",
    "get": "almak / elde etmek",
    "plan": "plan",
    "project": "proje",
    "risk": "risk",
    "platform": "platform",
    "stress": "stres",
    "drama": "drama",
    "festival": "festival",
    "program": "program",
    "pilot": "pilot",
    "video": "video",
    "living-room": "oturma odası",
    "late-stage": "geç evre",
    "distort": "çarpıtmak",
    "home-cooked": "ev yapımı",
    "well-being": "iyi oluş",
    "work-life": "iş-yaşam",
    "always-connected": "sürekli bağlantıda",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_env_file() -> None:
    if not ENV_PATH.exists():
        return
    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        cleaned = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), cleaned)


load_env_file()

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "hf").strip().lower()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct").strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_BASE_URL = os.getenv("HF_BASE_URL", "https://router.huggingface.co/v1").strip()
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY", "").strip()
GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
USE_POSTGRES = DATABASE_URL.startswith("postgres")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:8041").strip().rstrip("/")
CORS_ALLOWED_ORIGINS_RAW = os.getenv("CORS_ALLOWED_ORIGINS", "").strip()
COOKIE_SECURE_RAW = os.getenv("COOKIE_SECURE", "auto").strip().lower()
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "").strip()
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "").strip()
SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "587").strip() or "587")
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "").strip()
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME).strip()
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").strip().lower() != "false"


def normalized_origin(url: str) -> str:
    raw = str(url or "").strip().rstrip("/")
    if not raw:
        return ""
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    if not parsed.scheme or not parsed.netloc:
        return ""
    return f"{parsed.scheme}://{parsed.netloc}"


def build_allowed_origins() -> list[str]:
    configured = [
        normalized_origin(item)
        for item in CORS_ALLOWED_ORIGINS_RAW.split(",")
        if item.strip()
    ]
    if configured:
        return sorted({item for item in configured if item})
    defaults = {
        normalized_origin(APP_BASE_URL),
        "http://127.0.0.1:8041",
        "http://localhost:8041",
        "http://127.0.0.1:8046",
        "http://localhost:8046",
    }
    return sorted({item for item in defaults if item})


ALLOWED_ORIGINS = build_allowed_origins()
COOKIE_SECURE = (
    COOKIE_SECURE_RAW == "true"
    if COOKIE_SECURE_RAW in {"true", "false"}
    else normalized_origin(APP_BASE_URL).startswith("https://")
)


class GenerateRequest(BaseModel):
    level: str
    topic: str
    length_target: int = Field(ge=60, le=320)
    keywords: list[str] = Field(default_factory=list)
    source: str = "library"
    exclude_title: str | None = None


class ExplainRequest(BaseModel):
    text: str
    word: str
    content_source: str | None = None


class FillMissingRequest(BaseModel):
    text: str
    max_words: int = Field(default=180, ge=10, le=400)


class AuthRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=72)


class ResendVerificationRequest(BaseModel):
    email: str = Field(min_length=5, max_length=120)


class QuizAnswerRequest(BaseModel):
    word_id: int
    answer: str
    question_type: str = "meaning"


class FriendRequestPayload(BaseModel):
    username: str = Field(min_length=3, max_length=32)


class FriendRespondPayload(BaseModel):
    action: str = Field(pattern="^(accept|decline)$")


def today_iso_date() -> str:
    return datetime.now().astimezone().date().isoformat()


def build_http_client() -> httpx.Client:
    return httpx.Client(timeout=90.0, trust_env=False)


def build_openai_compatible_client(base_url: str, api_key: str) -> OpenAI:
    return OpenAI(base_url=base_url, api_key=api_key, http_client=build_http_client())


def _pg_query(query: str) -> str:
    return query.replace("?", "%s")


def load_json_map(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace") or "{}")
    except Exception:
        return {}
    if isinstance(data, dict):
        return {str(k).strip().lower(): str(v).strip() for k, v in data.items() if str(k).strip() and str(v).strip()}
    return {}


def save_json_map(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned = {str(k).strip().lower(): str(v).strip() for k, v in data.items() if str(k).strip() and str(v).strip()}
    path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")


EXTRA_WORD_MAP.update(load_json_map(EXTRA_WORD_MAP_PATH))
LIBRARY_WORD_MAP.update(load_json_map(LIBRARY_WORD_MAP_PATH))


def _row_to_dict(row: Any) -> dict[str, Any] | None:
    if row is None:
        return None
    if isinstance(row, sqlite3.Row):
        return dict(row)
    if isinstance(row, dict):
        return row
    return dict(row)


def _rows_to_dicts(rows: list[Any]) -> list[dict[str, Any]]:
    return [_row_to_dict(row) or {} for row in rows]


def db_fetchone(query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(_pg_query(query), params)
                return _row_to_dict(cur.fetchone())
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        return _row_to_dict(connection.execute(query, params).fetchone())
    finally:
        connection.close()


def db_fetchall(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(_pg_query(query), params)
                return _rows_to_dicts(cur.fetchall())
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        return _rows_to_dicts(connection.execute(query, params).fetchall())
    finally:
        connection.close()


def db_execute(query: str, params: tuple[Any, ...] = ()) -> None:
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(_pg_query(query), params)
            conn.commit()
        return
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute(query, params)
        connection.commit()
    finally:
        connection.close()


def db_insert(query: str, params: tuple[Any, ...] = ()) -> int:
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(_pg_query(query), params)
                row = cur.fetchone()
            conn.commit()
        if not row:
            raise RuntimeError("PostgreSQL insert did not return an id.")
        if "id" in row:
            return int(row["id"])
        return int(next(iter(row.values())))
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.execute(query, params)
        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()


def seed_readings() -> None:
    # Keep the shipped library deterministic: clear previous generated/manual
    # readings and rebuild the catalog from the current seed list.
    db_execute("DELETE FROM readings WHERE source = ?", ("manual",))
    for item in READING_SEEDS:
        payload = (
            item["title"],
            item["text"],
            item["level"],
            item["topic"],
            json.dumps(item["keywords"], ensure_ascii=False),
            len(item["text"].split()),
            "manual",
            1,
        )
        insert_query = (
            "INSERT INTO readings (title, text, level, topic, keywords, word_count, source, is_published) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        if USE_POSTGRES:
            insert_query += " RETURNING id"
        db_insert(insert_query, payload)


CURATED_HEADER_PATTERN = re.compile(
    r"^\[(A1|A2|B1|B2|C1|C2)-(\d+)(?: \| Topic: ([^|\]]+) \| Words: (\d+))?\]$",
    re.MULTILINE,
)
CURATED_TITLE_OVERRIDES: dict[str, dict[int, str]] = {
    "A1": {
        1: "Emma's Daily Routine",
        2: "Tom at the Park",
        3: "Anna and Lucy",
        4: "A Day at the Office",
        5: "Sarah's Love of Music",
        6: "Summer by the Sea",
        7: "My Brother the Student",
        8: "A Trip to the Supermarket",
        9: "A Beautiful Day in the Park",
        10: "Dinner with My Family",
    },
    "A2": {
        1: "A Peaceful Summer Holiday",
        2: "A Busy Day at Work",
        3: "A Weekend with My Grandparents",
        4: "Starting to Learn English",
        5: "My New Phone",
        6: "A Birthday Party to Remember",
        7: "A Helpful Sunday at Home",
        8: "Visiting a New City",
        9: "Working in a Local Shop",
        10: "A Movie Night with Family",
    },
    "B1": {
        1: "Learning English Step by Step",
        2: "Traveling Alone for the First Time",
        3: "Managing Stress at Work",
        4: "Using Technology with Balance",
        5: "Simple Habits for Better Health",
        6: "The Power of Everyday Routines",
        7: "Small Actions for the Environment",
        8: "What Keeps Friendship Strong",
        9: "Why Learning Never Stops",
        10: "The Value of Good Communication",
        11: "How Smartphones Changed Daily Life",
        12: "Why a Second Language Matters",
        13: "The Rise of Working from Home",
        14: "Why Exercise Still Matters",
        15: "Protecting Nature in Daily Life",
        16: "The Real Impact of Tourism",
        17: "The New Habit of Online Shopping",
        18: "Finding the Best Way Around the City",
        19: "The Fast Food Debate",
        20: "Why Reading Still Matters",
    },
    "B2": {
        1: "The Promise and Limits of Online Education",
        2: "Why Multitasking Reduces Quality",
        3: "Staying Human in a Digital World",
        4: "Building a Sustainable Healthy Lifestyle",
        5: "Collective Responsibility for the Environment",
        6: "Maintaining Strong Relationships",
        7: "Learning Through Consistent Practice",
        8: "Travel as a Form of Growth",
        9: "Staying Productive in a Distracting World",
        10: "Communication Beyond Words",
    },
    "C1": {
        1: "Education in the Digital Age",
        2: "Technology and the Attention Economy",
        3: "Rethinking Productivity at Work",
        4: "The Urgency of Environmental Sustainability",
        5: "How Social Environments Shape Behavior",
        6: "Communication as a Professional Advantage",
        7: "The Hidden Strategy Behind Learning",
        8: "Media, Influence, and Public Perception",
        9: "What Makes Decisions So Complex",
        10: "Personal Development as a Long Process",
        11: "Editing Humanity's Future",
        12: "The Mental Cost of Constant Connection",
        13: "Architecture and Human Behavior",
        14: "The Ethical Gamble of Geoengineering",
        15: "When Too Much Choice Becomes a Burden",
        16: "Why Linguistic Diversity Must Survive",
        17: "The Gig Economy and Eroding Labor Rights",
        18: "Can Universal Basic Income Really Work",
        19: "AI in Healthcare: Promise and Risk",
        20: "Why Space Exploration Still Matters",
    },
    "C2": {
        1: "How Information Reshaped Knowledge",
        2: "Perception and the Shape of Society",
        3: "Decision Making Inside Complexity",
        4: "Technology as a Behavioral Force",
        5: "The Nonlinear Nature of Learning",
        6: "Productivity Without Real Focus",
        7: "Language as a Way of Seeing",
        8: "How Humans Misread Risk",
        9: "Innovation Beyond Easy Narratives",
        10: "The Limits of Rational Behavior",
        11: "Private Power in the New Space Race",
        12: "Journalism After Objectivity",
        13: "Why Traditional Prisons Fail",
        14: "The Radical Logic of Degrowth",
        15: "The Ethics of Academic Enhancement",
        16: "Inside Surveillance Capitalism",
        17: "In Defense of Brutalism",
        18: "The Paradox of Tolerance",
        19: "The Myth of Meritocracy",
        20: "The Ethical Risk of De-Extinction",
    },
}
LIBRARY_TOPIC_ALIASES = {
    "Academic": "Education",
    "Arts": "Arts",
    "Communication": "Communication",
    "Communication & Language": "Communication",
    "Complexity & Decision Making": "Psychology",
    "Culture": "Culture",
    "Daily Life": "Daily Life",
    "Decision Making": "Psychology",
    "Education": "Education",
    "Environment": "Environment",
    "Finance": "Finance",
    "Food": "Food",
    "General": "Daily Life",
    "Health": "Health",
    "Human Behavior": "Psychology",
    "Innovation & Change": "Technology",
    "Knowledge & Information": "Media",
    "Learning": "Education",
    "Learning & Cognition": "Education",
    "Learning Strategies": "Education",
    "Media": "Media",
    "Media & Information": "Media",
    "Personal Development": "Psychology",
    "Productivity": "Work Life",
    "Productivity & Focus": "Work Life",
    "Psychology": "Psychology",
    "Public Services": "Public Services",
    "Risk & Uncertainty": "Psychology",
    "Science": "Science",
    "School": "Education",
    "Social Life": "Communication",
    "Social Psychology": "Psychology",
    "Society & Perception": "Culture",
    "Technology": "Technology",
    "Technology & Human Behavior": "Technology",
    "Travel": "Travel",
    "Work & Career": "Work Life",
    "Work & Productivity": "Work Life",
    "Work Life": "Work Life",
}
CURATED_KEYWORD_STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "if",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "from",
    "by",
    "as",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "it",
    "this",
    "that",
    "these",
    "those",
    "he",
    "she",
    "they",
    "we",
    "you",
    "i",
    "his",
    "her",
    "their",
    "our",
    "my",
    "your",
    "me",
    "him",
    "them",
    "us",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "can",
    "could",
    "will",
    "would",
    "should",
    "may",
    "might",
    "must",
    "not",
    "no",
    "yes",
    "very",
    "more",
    "most",
    "many",
    "much",
    "one",
    "two",
    "also",
    "than",
    "then",
    "there",
    "here",
    "about",
    "into",
    "over",
    "under",
    "after",
    "before",
    "during",
    "while",
    "when",
    "where",
    "which",
    "who",
    "whom",
    "whose",
    "because",
    "however",
    "although",
    "instead",
    "each",
    "every",
    "some",
    "any",
    "all",
    "other",
    "another",
    "today",
    "yesterday",
    "last",
    "next",
    "now",
    "really",
    "often",
    "sometimes",
    "usually",
}


def derive_curated_topic(level: str, body: str) -> str:
    lowered = body.lower()
    rules = [
        ("Education", ["school", "student", "study", "teacher", "homework", "english", "learn", "learning"]),
        ("Work & Career", ["office", "work", "meeting", "project", "colleague", "employees", "job", "tasks"]),
        ("Technology", ["phone", "smartphone", "internet", "social media", "technology", "computer", "devices", "screens"]),
        ("Travel", ["travel", "trip", "holiday", "hotel", "beach", "city", "village", "countries", "airport"]),
        ("Health", ["healthy", "exercise", "sleep", "diet", "food", "mental health", "rest"]),
        ("Environment", ["environment", "pollution", "climate", "waste", "recycle", "energy", "plastic"]),
        ("Communication", ["communicat", "listen", "listening", "message", "conversation", "body language", "tone of voice"]),
        ("Social Life", ["friends", "friendship", "party", "family", "together", "relationships"]),
        ("Daily Life", ["morning", "breakfast", "dinner", "house", "park", "supermarket", "routine", "day"]),
    ]
    for topic_name, needles in rules:
        if any(needle in lowered for needle in needles):
            return topic_name
    return "General"


def normalize_library_topic(topic: str) -> str:
    normalized = normalize_topic((topic or "").strip())
    if normalized in {"", "Random", "Open", "Serbest"}:
        return "Random"
    return LIBRARY_TOPIC_ALIASES.get(normalized, normalized)


def derive_curated_keywords(body: str, topic: str) -> list[str]:
    words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", body.lower())
    counts = Counter(word for word in words if len(word) > 2 and word not in CURATED_KEYWORD_STOPWORDS)
    keywords: list[str] = []
    for piece in re.split(r"[^A-Za-z]+", topic.lower()):
        cleaned = piece.strip()
        if cleaned and cleaned not in CURATED_KEYWORD_STOPWORDS and cleaned not in keywords:
            keywords.append(cleaned)
    for word, _count in counts.most_common(6):
        if word not in keywords:
            keywords.append(word)
        if len(keywords) >= 6:
            break
    return keywords[:6] or ["reading"]


def parse_curated_readings_file() -> list[dict[str, Any]]:
    if not CURATED_READINGS_PATH.exists():
        return []
    text = CURATED_READINGS_PATH.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    headers = list(CURATED_HEADER_PATTERN.finditer(text))
    items: list[dict[str, Any]] = []
    for index, match in enumerate(headers):
        level = match.group(1)
        entry_number = int(match.group(2))
        topic = (match.group(3) or "").strip()
        start = match.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        body = text[start:end].strip()
        if not body:
            continue
        body = re.sub(r"\n{2,}", "\n\n", body)
        if not topic:
            topic = derive_curated_topic(level, body)
        topic = normalize_library_topic(topic)
        title = CURATED_TITLE_OVERRIDES.get(level, {}).get(entry_number, f"{topic} Reading {entry_number}")
        keywords = derive_curated_keywords(body, topic)
        word_count = len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", body))
        items.append(
            {
                "title": title,
                "text": body,
                "level": level,
                "topic": topic,
                "keywords": keywords,
                "word_count": word_count,
            }
        )
    return items


def import_curated_readings() -> None:
    items = parse_curated_readings_file()
    if not items:
        return
    db_execute("DELETE FROM readings WHERE source = ?", (CURATED_LIBRARY_SOURCE,))
    insert_query = (
        "INSERT INTO readings (title, text, level, topic, keywords, word_count, source, is_published) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )
    if USE_POSTGRES:
        insert_query += " RETURNING id"
    for item in items:
        payload = (
            item["title"],
            item["text"],
            item["level"],
            item["topic"],
            json.dumps(item["keywords"], ensure_ascii=False),
            int(item["word_count"]),
            CURATED_LIBRARY_SOURCE,
            1,
        )
        db_insert(insert_query, payload)


def ensure_learning_tables() -> None:
    table_statements = [
        """
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id INTEGER PRIMARY KEY,
            daily_goal INTEGER NOT NULL DEFAULT 5,
            streak_count INTEGER NOT NULL DEFAULT 0,
            last_streak_date TEXT,
            updated_at TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reading_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            level TEXT NOT NULL,
            topic TEXT NOT NULL,
            content_source TEXT NOT NULL,
            viewed_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS friendships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requester_id INTEGER NOT NULL,
            addressee_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(requester_id, addressee_id),
            FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (addressee_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS social_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS lexical_review_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL,
            canonical TEXT NOT NULL,
            meaning TEXT NOT NULL,
            kind TEXT NOT NULL DEFAULT 'word',
            source TEXT NOT NULL DEFAULT 'fallback',
            status TEXT NOT NULL DEFAULT 'pending',
            confidence REAL NOT NULL DEFAULT 0.5,
            sample_context TEXT,
            occurrence_count INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(term, meaning)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS lexical_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL UNIQUE,
            meaning TEXT NOT NULL,
            kind TEXT NOT NULL DEFAULT 'word',
            source TEXT NOT NULL DEFAULT 'curated',
            confidence REAL NOT NULL DEFAULT 1.0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
    ]
    if USE_POSTGRES:
        table_statements = [
            """
            CREATE TABLE IF NOT EXISTS user_progress (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                daily_goal INTEGER NOT NULL DEFAULT 5,
                streak_count INTEGER NOT NULL DEFAULT 0,
                last_streak_date TEXT,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS reading_history (
                id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                level TEXT NOT NULL,
                topic TEXT NOT NULL,
                content_source TEXT NOT NULL,
                viewed_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS friendships (
                id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                requester_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                addressee_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(requester_id, addressee_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS social_events (
                id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                receiver_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                event_type TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS lexical_review_queue (
                id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                term TEXT NOT NULL,
                canonical TEXT NOT NULL,
                meaning TEXT NOT NULL,
                kind TEXT NOT NULL DEFAULT 'word',
                source TEXT NOT NULL DEFAULT 'fallback',
                status TEXT NOT NULL DEFAULT 'pending',
                confidence DOUBLE PRECISION NOT NULL DEFAULT 0.5,
                sample_context TEXT,
                occurrence_count INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(term, meaning)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS lexical_entries (
                id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                term TEXT NOT NULL UNIQUE,
                meaning TEXT NOT NULL,
                kind TEXT NOT NULL DEFAULT 'word',
                source TEXT NOT NULL DEFAULT 'curated',
                confidence DOUBLE PRECISION NOT NULL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
        ]
    for statement in table_statements:
        db_execute(statement.strip())


def init_db() -> None:
    schema_sqlite = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            verified_at TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS saved_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            word TEXT NOT NULL,
            source_text TEXT NOT NULL,
            turkish TEXT NOT NULL,
            context TEXT NOT NULL,
            example TEXT NOT NULL,
            click_count INTEGER NOT NULL DEFAULT 1,
            last_result TEXT NOT NULL DEFAULT 'new',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(user_id, word),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            level TEXT NOT NULL,
            topic TEXT NOT NULL,
            keywords TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            source TEXT NOT NULL DEFAULT 'manual',
            is_published INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS email_verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            token TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            used_at TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """
    schema_postgres = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            verified_at TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS saved_words (
            id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            word TEXT NOT NULL,
            source_text TEXT NOT NULL,
            turkish TEXT NOT NULL,
            context TEXT NOT NULL,
            example TEXT NOT NULL,
            click_count INTEGER NOT NULL DEFAULT 1,
            last_result TEXT NOT NULL DEFAULT 'new',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(user_id, word)
        );
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            level TEXT NOT NULL,
            topic TEXT NOT NULL,
            keywords TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            source TEXT NOT NULL DEFAULT 'manual',
            is_published INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS email_verifications (
            id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            email TEXT NOT NULL,
            token TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            used_at TEXT,
            created_at TEXT NOT NULL
        );
    """
    if USE_POSTGRES:
        if psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(schema_postgres)
            conn.commit()
        return
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.executescript(schema_sqlite)
        connection.commit()
    finally:
        connection.close()


def ensure_auth_columns() -> None:
    statements = [
        "ALTER TABLE users ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1",
        "ALTER TABLE users ADD COLUMN verified_at TEXT",
    ]
    for statement in statements:
        try:
            db_execute(statement)
        except Exception as exc:  # pragma: no cover - migration safety
            message = str(exc).lower()
            if "duplicate" in message or "already exists" in message:
                continue
            if "sqlite" in message and "duplicate column name" in message:
                continue
            raise


init_db()
ensure_auth_columns()
ensure_learning_tables()
seed_readings()
import_curated_readings()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def hash_password_legacy(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def is_legacy_password_hash(password_hash: str) -> bool:
    return bool(re.fullmatch(r"[a-f0-9]{64}", str(password_hash or "").strip()))


def verify_password(password: str, password_hash: str) -> bool:
    stored_hash = str(password_hash or "").strip()
    if not stored_hash:
        return False
    if is_legacy_password_hash(stored_hash):
        return secrets.compare_digest(hash_password_legacy(password), stored_hash)
    try:
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
    except Exception:
        return False


def password_hash_needs_upgrade(password_hash: str) -> bool:
    stored_hash = str(password_hash or "").strip()
    if not stored_hash:
        return True
    if is_legacy_password_hash(stored_hash):
        return True
    return not stored_hash.startswith("$2")


def clean_username(username: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "", username).strip().lower()
    if len(cleaned) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters.")
    return cleaned


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def verification_email_configured() -> bool:
    return bool((RESEND_API_KEY and RESEND_FROM_EMAIL) or (SMTP_HOST and SMTP_FROM_EMAIL))


def send_email_message(to_email: str, subject: str, html_body: str, text_body: str) -> None:
    if not verification_email_configured():
        raise HTTPException(status_code=503, detail="Email verification is not configured yet.")
    if RESEND_API_KEY and RESEND_FROM_EMAIL:
        try:
            with build_http_client() as client:
                response = client.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {RESEND_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "from": RESEND_FROM_EMAIL,
                        "to": [to_email],
                        "subject": subject,
                        "html": html_body,
                        "text": text_body,
                    },
                )
                response.raise_for_status()
            return
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=503, detail="Verification email could not be sent through Resend.") from exc
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = SMTP_FROM_EMAIL
    message["To"] = to_email
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            if SMTP_USE_TLS:
                server.starttls()
            if SMTP_USERNAME:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
    except smtplib.SMTPException as exc:
        raise HTTPException(status_code=503, detail=f"Verification email could not be sent: {exc}") from exc
    except OSError as exc:
        raise HTTPException(status_code=503, detail="Verification email service is unreachable right now.") from exc


def create_verification_token(user_id: int, email: str) -> str:
    token = secrets.token_urlsafe(32)
    created_at = now_iso()
    expires_at = (now_utc() + timedelta(hours=24)).isoformat()
    db_execute("DELETE FROM email_verifications WHERE user_id = ? AND used_at IS NULL", (user_id,))
    db_execute(
        """
        INSERT INTO email_verifications (user_id, email, token, expires_at, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, email, token, expires_at, created_at),
    )
    return token


def send_verification_email(email: str, token: str) -> None:
    verify_url = f"{APP_BASE_URL}/api/auth/verify-email?token={token}"
    subject = "Verify your ReadLex account"
    text_body = (
        "Welcome to ReadLex.\n\n"
        f"Verify your email by opening this link:\n{verify_url}\n\n"
        "This link expires in 24 hours."
    )
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #183153;">
        <h2>Verify your ReadLex account</h2>
        <p>Thanks for signing up. Click the button below to activate your account.</p>
        <p><a href="{verify_url}" style="display:inline-block;padding:12px 18px;border-radius:999px;background:#58cc02;color:#0f2c49;text-decoration:none;font-weight:700;">Verify Email</a></p>
        <p style="color:#6f8098;">If the button does not work, use this link:</p>
        <p><a href="{verify_url}">{verify_url}</a></p>
        <p style="color:#6f8098;">This link expires in 24 hours.</p>
      </body>
    </html>
    """.strip()
    send_email_message(email, subject, html_body, text_body)


def user_payload(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if not row:
        return None
    return {
        "id": row["id"],
        "username": row["username"],
        "created_at": row["created_at"],
        "email_verified": bool(row.get("is_active", 1)),
    }


def require_user(session_token: str | None) -> dict[str, Any]:
    if not session_token:
        raise HTTPException(status_code=401, detail="Önce giriş yapmalısın.")
    row = db_fetchone(
        """
        SELECT users.id, users.username, users.created_at, users.is_active
        FROM sessions
        JOIN users ON users.id = sessions.user_id
        WHERE sessions.token = ?
        """,
        (session_token,),
    )
    if not row:
        raise HTTPException(status_code=401, detail="Session not found. Please log in again.")
    return user_payload(row) or {}


def optional_user(session_token: str | None) -> dict[str, Any] | None:
    if not session_token:
        return None
    try:
        return require_user(session_token)
    except HTTPException:
        return None


def create_session(response: Response, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    db_execute(
        "INSERT INTO sessions (token, user_id, created_at) VALUES (?, ?, ?)",
        (token, user_id, now_iso()),
    )
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
        path="/",
        max_age=60 * 60 * 24 * 30,
    )
    return token


def clear_session(response: Response, session_token: str | None) -> None:
    if session_token:
        db_execute("DELETE FROM sessions WHERE token = ?", (session_token,))
    response.delete_cookie(SESSION_COOKIE, path="/", samesite="lax", secure=COOKIE_SECURE)


def ensure_user_progress(user_id: int) -> dict[str, Any]:
    row = db_fetchone(
        "SELECT user_id, daily_goal, streak_count, last_streak_date, updated_at FROM user_progress WHERE user_id = ?",
        (user_id,),
    )
    if row:
        return row
    timestamp = now_iso()
    insert_query = (
        "INSERT INTO user_progress (user_id, daily_goal, streak_count, last_streak_date, updated_at) "
        "VALUES (?, 5, 0, NULL, ?)"
    )
    if USE_POSTGRES:
        insert_query += " RETURNING user_id"
        db_insert(insert_query, (user_id, timestamp))
    else:
        db_execute(insert_query, (user_id, timestamp))
    return {
        "user_id": user_id,
        "daily_goal": 5,
        "streak_count": 0,
        "last_streak_date": None,
        "updated_at": timestamp,
    }


def count_words_saved_today(user_id: int) -> int:
    today = today_iso_date()
    row = db_fetchone(
        """
        SELECT COUNT(*) AS total
        FROM saved_words
        WHERE user_id = ? AND substr(updated_at, 1, 10) = ?
        """,
        (user_id, today),
    ) or {"total": 0}
    return int(row["total"] or 0)


def build_progress_stats(user_id: int) -> dict[str, int]:
    progress = ensure_user_progress(user_id)
    saved_today = count_words_saved_today(user_id)
    readings_today_row = db_fetchone(
        """
        SELECT COUNT(*) AS total
        FROM reading_history
        WHERE user_id = ? AND substr(viewed_at, 1, 10) = ?
        """,
        (user_id, today_iso_date()),
    ) or {"total": 0}
    total_readings_row = db_fetchone(
        """
        SELECT COUNT(*) AS total
        FROM reading_history
        WHERE user_id = ?
        """,
        (user_id,),
    ) or {"total": 0}
    streak = int(progress.get("streak_count") or 0)
    last_streak_date = str(progress.get("last_streak_date") or "")
    today = today_iso_date()
    if saved_today >= int(progress.get("daily_goal") or 5) and last_streak_date != today:
        yesterday = (datetime.now().astimezone().date() - timedelta(days=1)).isoformat()
        streak = streak + 1 if last_streak_date == yesterday else 1
        db_execute(
            "UPDATE user_progress SET streak_count = ?, last_streak_date = ?, updated_at = ? WHERE user_id = ?",
            (streak, today, now_iso(), user_id),
        )
        progress["streak_count"] = streak
        progress["last_streak_date"] = today
    hard_row = db_fetchone(
        """
        SELECT COUNT(*) AS total
        FROM saved_words
        WHERE user_id = ? AND (last_result = 'wrong' OR click_count >= 3)
        """,
        (user_id,),
    ) or {"total": 0}
    return {
        "daily_goal": int(progress.get("daily_goal") or 5),
        "saved_today": saved_today,
        "readings_today": int(readings_today_row["total"] or 0),
        "total_readings": int(total_readings_row["total"] or 0),
        "streak": int(progress.get("streak_count") or 0),
        "hard_words": int(hard_row["total"] or 0),
    }


def get_progress_history(user_id: int, limit: int = 14) -> list[dict[str, Any]]:
    reading_rows = db_fetchall(
        """
        SELECT substr(viewed_at, 1, 10) AS day, COUNT(*) AS texts
        FROM reading_history
        WHERE user_id = ?
        GROUP BY substr(viewed_at, 1, 10)
        ORDER BY day DESC
        LIMIT ?
        """,
        (user_id, limit),
    )
    word_rows = db_fetchall(
        """
        SELECT substr(updated_at, 1, 10) AS day, COUNT(*) AS words
        FROM saved_words
        WHERE user_id = ?
        GROUP BY substr(updated_at, 1, 10)
        ORDER BY day DESC
        LIMIT ?
        """,
        (user_id, limit),
    )
    by_day: dict[str, dict[str, Any]] = {}
    for row in reading_rows:
        day = str(row.get("day") or "").strip()
        if not day:
            continue
        by_day.setdefault(day, {"date": day, "texts": 0, "words": 0})
        by_day[day]["texts"] = int(row.get("texts") or 0)
    for row in word_rows:
        day = str(row.get("day") or "").strip()
        if not day:
            continue
        by_day.setdefault(day, {"date": day, "texts": 0, "words": 0})
        by_day[day]["words"] = int(row.get("words") or 0)
    return [by_day[day] for day in sorted(by_day.keys(), reverse=True)[:limit]]


def get_reading_history(user_id: int, limit: int = 4) -> list[dict[str, Any]]:
    return db_fetchall(
        """
        SELECT id, title, level, topic, content_source, viewed_at
        FROM reading_history
        WHERE user_id = ?
          AND id IN (
              SELECT MAX(id)
              FROM reading_history
              WHERE user_id = ?
              GROUP BY title, text, level, topic, content_source
          )
        ORDER BY viewed_at DESC, id DESC
        LIMIT ?
        """,
        (user_id, user_id, limit),
    )


def record_reading_history(
    user_id: int,
    *,
    title: str,
    text: str,
    level: str,
    topic: str,
    content_source: str,
) -> None:
    timestamp = now_iso()
    insert_query = (
        "INSERT INTO reading_history (user_id, title, text, level, topic, content_source, viewed_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )
    if USE_POSTGRES:
        insert_query += " RETURNING id"
        db_insert(insert_query, (user_id, title, text, level, topic, content_source, timestamp))
    else:
        db_execute(insert_query, (user_id, title, text, level, topic, content_source, timestamp))
    overflow = db_fetchall(
        """
        SELECT id
        FROM reading_history
        WHERE user_id = ?
        ORDER BY viewed_at DESC, id DESC
        LIMIT 100 OFFSET 12
        """,
        (user_id,),
    )
    for row in overflow:
        db_execute("DELETE FROM reading_history WHERE id = ? AND user_id = ?", (int(row["id"]), user_id))


def build_user_stats(user_id: int) -> dict[str, int]:
    row = db_fetchone(
        """
        SELECT COUNT(*) AS saved_words,
               SUM(CASE WHEN last_result = 'correct' THEN 1 ELSE 0 END) AS mastered_words
        FROM saved_words
        WHERE user_id = ?
        """,
        (user_id,),
    ) or {"saved_words": 0, "mastered_words": 0}
    stats = {
        "saved_words": int(row["saved_words"] or 0),
        "mastered_words": int(row["mastered_words"] or 0),
    }
    stats.update(build_progress_stats(user_id))
    return stats


def social_user_payload(row: dict[str, Any], friendship_id: int | None = None) -> dict[str, Any]:
    stats = build_user_stats(int(row["id"]))
    return {
        "id": int(row["id"]),
        "username": str(row["username"]),
        "friendship_id": friendship_id,
        "streak": int(stats.get("streak") or 0),
        "total_readings": int(stats.get("total_readings") or 0),
        "saved_words": int(stats.get("saved_words") or 0),
        "words_today": int(stats.get("saved_today") or 0),
    }


def get_friendship_between(user_id: int, other_user_id: int) -> dict[str, Any] | None:
    return db_fetchone(
        """
        SELECT id, requester_id, addressee_id, status, created_at, updated_at
        FROM friendships
        WHERE (requester_id = ? AND addressee_id = ?)
           OR (requester_id = ? AND addressee_id = ?)
        """,
        (user_id, other_user_id, other_user_id, user_id),
    )


def list_social_friends(user_id: int) -> list[dict[str, Any]]:
    rows = db_fetchall(
        """
        SELECT f.id AS friendship_id, u.id, u.username
        FROM friendships f
        JOIN users u ON u.id = CASE
            WHEN f.requester_id = ? THEN f.addressee_id
            ELSE f.requester_id
        END
        WHERE (f.requester_id = ? OR f.addressee_id = ?)
          AND f.status = 'accepted'
        ORDER BY f.updated_at DESC
        """,
        (user_id, user_id, user_id),
    )
    return [social_user_payload(row, int(row["friendship_id"])) for row in rows]


def list_social_requests(user_id: int, direction: str) -> list[dict[str, Any]]:
    if direction == "incoming":
        rows = db_fetchall(
            """
            SELECT f.id AS request_id, f.created_at, u.id, u.username
            FROM friendships f
            JOIN users u ON u.id = f.requester_id
            WHERE f.addressee_id = ? AND f.status = 'pending'
            ORDER BY f.created_at DESC
            """,
            (user_id,),
        )
    else:
        rows = db_fetchall(
            """
            SELECT f.id AS request_id, f.created_at, u.id, u.username
            FROM friendships f
            JOIN users u ON u.id = f.addressee_id
            WHERE f.requester_id = ? AND f.status = 'pending'
            ORDER BY f.created_at DESC
            """,
            (user_id,),
        )
    return [
        {
            "request_id": int(row["request_id"]),
            "created_at": row["created_at"],
            "user": social_user_payload(row),
        }
        for row in rows
    ]


def list_social_suggestions(user_id: int, limit: int = 6) -> list[dict[str, Any]]:
    rows = db_fetchall(
        """
        SELECT id, username
        FROM users
        WHERE id != ?
          AND id NOT IN (
              SELECT CASE
                  WHEN requester_id = ? THEN addressee_id
                  ELSE requester_id
              END
              FROM friendships
              WHERE requester_id = ? OR addressee_id = ?
          )
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, user_id, user_id, user_id, limit),
    )
    return [social_user_payload(row) for row in rows]


def save_word_for_user(user_id: int, word: str, text: str, detail: dict[str, str]) -> None:
    timestamp = now_iso()
    existing = db_fetchone(
        "SELECT id, click_count FROM saved_words WHERE user_id = ? AND word = ?",
        (user_id, word.lower()),
    )
    if existing:
        db_execute(
            """
            UPDATE saved_words
            SET source_text = ?, turkish = ?, context = ?, example = ?,
                click_count = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                text,
                detail["turkish"],
                detail["context"],
                detail["example"],
                int(existing["click_count"]) + 1,
                timestamp,
                existing["id"],
            ),
        )
    else:
        db_execute(
            """
            INSERT INTO saved_words (
                user_id, word, source_text, turkish, context, example,
                click_count, last_result, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, 1, 'new', ?, ?)
            """,
            (
                user_id,
                word.lower(),
                text,
                detail["turkish"],
                detail["context"],
                detail["example"],
                timestamp,
                timestamp,
            ),
          )


def detail_is_saveable(word: str, detail: dict[str, str]) -> bool:
    turkish = (detail.get("turkish") or "").strip()
    if not turkish:
        return False
    lowered = turkish.lower()
    if "alınamadı" in lowered or "bulunamadı" in lowered:
        return False
    if lowered == word.strip().lower():
        return False
    return True


def classify_turkish_meaning(value: str) -> str:
    lowered = value.strip().lower()
    if lowered.endswith(("mek", "mak")):
        return "verb"
    if lowered.endswith(("yor", "ıyor", "iyor", "uyor", "ilir", "ılır", "ulur", "lanır", "lenir")):
        return "verb"
    if lowered.endswith(("li", "lı", "lu", "lü", "siz", "sız", "suz", "süz", "sel", "sal")):
        return "adjective"
    if lowered.endswith(("ik", "ık", "uk", "ük")):
        return "adjective"
    return "noun"


def quiz_candidate_meanings(words: list[dict[str, Any]], target_id: int, target_turkish: str) -> list[str]:
    values: list[str] = []
    target_kind = classify_turkish_meaning(target_turkish)
    for row in words:
        if int(row["id"]) == int(target_id):
            continue
        candidate = str(row.get("turkish") or "").strip().lower()
        if not candidate:
            continue
        if any(mark in candidate for mark in ["alınamadı", "bulunamadı", "not available"]):
            continue
        if len(candidate) < 2:
            continue
        if classify_turkish_meaning(candidate) != target_kind:
            continue
        if candidate not in values:
            values.append(candidate)
    for fallback in QUIZ_DISTRACTOR_BANK[target_kind]:
        if fallback != target_turkish.strip().lower() and fallback not in values:
            values.append(fallback)
    return values


def get_recent_words(
    user_id: int,
    limit: int = 20,
    *,
    randomize: bool = False,
    exclude_ids: list[int] | None = None,
) -> list[dict[str, Any]]:
    order_clause = "RANDOM()" if not USE_POSTGRES else "RANDOM()"
    if not randomize:
        order_clause = "updated_at DESC"
    filtered_exclude = [int(item) for item in (exclude_ids or []) if str(item).strip()]
    params: list[Any] = [user_id]
    where_parts = ["user_id = ?"]
    if randomize and filtered_exclude:
        placeholders = ", ".join(["?"] * len(filtered_exclude))
        where_parts.append(f"id NOT IN ({placeholders})")
        params.extend(filtered_exclude)
    params.append(limit)
    rows = db_fetchall(
        f"""
        SELECT id, word, turkish, click_count, last_result, updated_at
        FROM saved_words
        WHERE {' AND '.join(where_parts)}
        ORDER BY {order_clause}
        LIMIT ?
        """,
        tuple(params),
    )
    if randomize and filtered_exclude and len(rows) < limit:
        rows = db_fetchall(
            f"""
            SELECT id, word, turkish, click_count, last_result, updated_at
            FROM saved_words
            WHERE user_id = ?
            ORDER BY {order_clause}
            LIMIT ?
            """,
            (user_id, limit),
        )
    return rows


def build_quiz_question(
    user_id: int,
    exclude_word_id: int | None = None,
    *,
    mode: str = "saved",
) -> dict[str, Any] | None:
    words = db_fetchall(
        """
        SELECT id, word, turkish, context, example, click_count, last_result
        FROM saved_words
        WHERE user_id = ?
        ORDER BY updated_at DESC
        """,
        (user_id,),
    )
    if len(words) < 4:
        return None
    if exclude_word_id is not None:
        alternate_words = [row for row in words if int(row["id"]) != int(exclude_word_id)]
        if len(alternate_words) >= 4:
            words = alternate_words
    if mode == "hard":
        ranked = sorted(
            words,
            key=lambda row: (
                row["last_result"] != "wrong",
                row["click_count"] < 3,
                row["last_result"] == "correct",
                row["id"],
            ),
        )
    else:
        ranked = sorted(
            words,
            key=lambda row: (row["last_result"] == "correct", row["click_count"], row["id"]),
        )
    target = ranked[0]
    translation_distractors = quiz_candidate_meanings(words, int(target["id"]), str(target["turkish"]))[:3]
    translation_options = list(dict.fromkeys(translation_distractors + [str(target["turkish"]).strip().lower()]))
    while len(translation_options) < 4:
        for fallback in quiz_candidate_meanings(words, int(target["id"]), str(target["turkish"])):
            if fallback not in translation_options:
                translation_options.append(fallback)
            if len(translation_options) == 4:
                break

    example_text = str(target["example"] or "").strip()
    can_make_blank = bool(example_text) and re.search(rf"\b{re.escape(str(target['word']))}\b", example_text, flags=re.IGNORECASE)
    if can_make_blank and random.random() < 0.5:
        blank_sentence = re.sub(
            rf"\b{re.escape(str(target['word']))}\b",
            "_____",
            example_text,
            count=1,
            flags=re.IGNORECASE,
        )
        word_distractors = [row["word"] for row in words if row["id"] != target["id"]][:3]
        word_options = list(dict.fromkeys(word_distractors + [target["word"]]))
        while len(word_options) < 4:
            for fallback in ["result", "habit", "travel", "focus"]:
                if fallback not in word_options:
                    word_options.append(fallback)
                if len(word_options) == 4:
                    break
        random.shuffle(word_options)
        return {
            "word_id": target["id"],
            "question_type": "blank",
            "question": "Which word best completes the sentence?",
            "sentence": blank_sentence,
            "word": target["word"],
            "options": word_options[:4],
            "answer": target["word"],
            "context": target["context"],
            "example": target["example"],
        }

    random.shuffle(translation_options)
    return {
        "word_id": target["id"],
        "question_type": "meaning",
        "question": f'What is the best Turkish meaning of "{target["word"]}"?',
        "word": target["word"],
        "options": translation_options[:4],
        "answer": target["turkish"],
        "context": target["context"],
        "example": target["example"],
        "mode": mode,
    }


def sanitize_keywords(raw_keywords: list[str]) -> list[str]:
    seen, result = set(), []
    for item in raw_keywords:
        cleaned = item.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered not in seen:
            seen.add(lowered)
            result.append(cleaned)
    return result


def normalize_phrase_key(value: str) -> str:
    lowered = repair_mojibake(str(value or "")).strip().lower()
    lowered = (
        lowered.replace("’", "'")
        .replace("`", "'")
        .replace("–", "-")
        .replace("—", "-")
    )
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


def phrase_lookup_candidates(value: str) -> list[str]:
    base = normalize_phrase_key(value)
    if not base:
        return []
    candidates: list[str] = []

    def add(item: str) -> None:
        cleaned = normalize_phrase_key(item)
        if cleaned and cleaned not in candidates:
            candidates.append(cleaned)

    add(base)
    add(base.replace("-", " "))
    add(base.replace(" ", "-"))
    add(base.replace("'", ""))
    add(base.replace("'", " ").replace("  ", " "))
    return candidates


def sanitize_word(word: str) -> str:
    cleaned = normalize_phrase_key(word)
    cleaned = re.sub(r"[^A-Za-z' -]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -'")
    return cleaned


def parse_keywords_field(value: str) -> list[str]:
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in value.split(",") if item.strip()]


def library_source_filter() -> tuple[str, tuple[Any, ...]]:
    return " AND source = ?", (CURATED_LIBRARY_SOURCE,)


def pick_library_reading(
    level: str,
    topic: str,
    keywords: list[str],
    length_target: int,
    exclude_title: str | None = None,
) -> dict[str, Any] | None:
    normalized_topic = normalize_library_topic(topic)

    if (
        level == "B1"
        and normalized_topic in {"Open", "Serbest", "Random"}
        and not keywords
        and not exclude_title
        and isinstance(FEATURED_PHRASAL_READING, dict)
        and str(FEATURED_PHRASAL_READING.get("title") or "")
    ):
        return {
            "id": 0,
            "title": str(FEATURED_PHRASAL_READING["title"]),
            "text": str(FEATURED_PHRASAL_READING["text"]),
            "level": "B1",
            "topic": str(FEATURED_PHRASAL_READING.get("topic") or "Random"),
            "keywords": list(FEATURED_PHRASAL_READING.get("keywords") or []),
            "word_count": len(str(FEATURED_PHRASAL_READING["text"]).split()),
            "source": "featured",
        }
    source_clause, source_params = library_source_filter()
    rows = db_fetchall(
        f"""
        SELECT id, title, text, level, topic, keywords, word_count, source
        FROM readings
        WHERE is_published = 1 AND level = ?{source_clause}
        ORDER BY id
        """,
        (level, *source_params),
    )
    if not rows:
        return None

    if (
        level == "B1"
        and normalized_topic in {"Open", "Serbest", "Random"}
        and not keywords
        and not exclude_title
    ):
        featured_title = str(FEATURED_PHRASAL_READING.get("title") or "")
        if featured_title:
            featured_row = next((row for row in rows if str(row.get("title") or "") == featured_title), None)
            if featured_row:
                return {
                    "id": featured_row["id"],
                    "title": featured_row["title"],
                    "text": featured_row["text"],
                    "level": featured_row["level"],
                    "topic": featured_row["topic"],
                    "keywords": parse_keywords_field(featured_row["keywords"]),
                    "word_count": featured_row["word_count"],
                    "source": featured_row["source"],
                }
    filtered_rows = rows
    if normalized_topic not in {"Open", "Serbest", "Random"}:
        exact_topic_rows = [
            row for row in filtered_rows
            if normalize_library_topic(str(row["topic"])) == normalized_topic
        ]
        if exact_topic_rows:
            filtered_rows = exact_topic_rows
    if exclude_title:
        alternate_rows = [row for row in filtered_rows if str(row["title"]) != exclude_title]
        if alternate_rows:
            filtered_rows = alternate_rows
    if not filtered_rows:
        filtered_rows = rows
    scored: list[tuple[float, dict[str, Any]]] = []
    for row in filtered_rows:
        quality = LIBRARY_READING_QUALITY_INDEX.get(str(row["title"]), {})
        length_penalty = abs(int(row["word_count"]) - int(length_target)) * 0.65
        keyword_bonus = float(quality.get("keyword_hits", 0)) * 8
        quality_bonus = float(quality.get("score", 0)) * 0.45
        lexical_bonus = float(quality.get("advanced_hits", 0)) * (3 if level in {"B2", "C1", "C2", "Academic"} else 1)
        repetition_penalty = float(quality.get("repeated_openings", 0)) * 9 + float(quality.get("repeated_shapes", 0)) * 4
        score = length_penalty + repetition_penalty - keyword_bonus - quality_bonus - lexical_bonus
        scored.append((score, row))
    scored.sort(key=lambda item: (item[0], item[1]["id"]))
    candidate_pool = [row for _score, row in scored[: min(18, len(scored))]]
    best = random.choice(candidate_pool or filtered_rows)
    return {
        "id": best["id"],
        "title": best["title"],
        "text": best["text"],
        "level": best["level"],
        "topic": best["topic"],
        "keywords": parse_keywords_field(best["keywords"]),
        "word_count": best["word_count"],
        "source": best["source"],
    }


def build_text_prompt(level: str, topic: str, keywords: list[str], length_target: int) -> str:
    cfg = LEVEL_CONFIG[level]
    return f"""
Write a natural English reading text for a {level} learner.

Topic:
{topic}

Use these keywords naturally:
{", ".join(keywords)}

Rules:
- Write only one paragraph
- Keep the text clear, natural, and realistic
- Do not force the keywords
- Target length: around {length_target} words
- Stay between {cfg["min_words"]} and {cfg["max_words"]} words
- Aim for at least {cfg["min_words"]} words before stopping
- Do not use markdown, bullet points, bold markers, or headings
- Do not wrap any word with symbols such as ** or quotes for emphasis
- Give only the reading text
""".strip()


def build_plan_prompt(level: str, topic: str, keywords: list[str], length_target: int) -> str:
    cfg = LEVEL_CONFIG[level]
    return f"""
Create a short writing plan for an English reading text.

Topic: {topic}
Level: {level}
Keywords: {", ".join(keywords)}
Target length: {length_target} words

Return valid JSON only:
{{
  "scenario": "one short realistic scenario",
  "voice": "short style note",
  "beats": ["beat 1", "beat 2", "beat 3", "beat 4"]
}}

Rules:
- Scenario must be realistic and simple
- Beats should describe the paragraph flow
- Keep everything short
- No markdown
- No extra text
- The final writing should fit between {cfg["min_words"]} and {cfg["max_words"]} words
""".strip()


def build_text_from_plan_prompt(level: str, topic: str, keywords: list[str], length_target: int, plan: dict[str, Any]) -> str:
    cfg = LEVEL_CONFIG[level]
    beats = "\n".join(f"- {beat}" for beat in plan.get("beats", [])[:4])
    return f"""
Write a natural English reading text for a {level} learner.

Topic:
{topic}

Scenario:
{plan.get("scenario", topic)}

Voice:
{plan.get("voice", "clear and natural")}

Flow:
{beats}

Use these keywords naturally:
{", ".join(keywords)}

Rules:
- Write only one paragraph
- Keep the text clear, natural, and realistic
- Do not force the keywords
- Target length: around {length_target} words
- Stay between {cfg["min_words"]} and {cfg["max_words"]} words
- Do not use markdown, bullet points, bold markers, or headings
- Give only the reading text
""".strip()


def build_word_prompt(text: str, word: str) -> str:
    return f"""
The learner is reading this English text:

\"\"\"{text}\"\"\"

Explain this word in Turkish: "{word}"

Rules:
- First line: Turkish meaning
- Second line: meaning in the context of the text
- Third line: one short and simple English example sentence
- Keep it short and clear
""".strip()


def build_word_strict_prompt(text: str, word: str) -> str:
    return f"""
The learner is reading this English text:

\"\"\"{text}\"\"\"

Target word: "{word}"

Return valid JSON only:
{{
  "turkish": "...",
  "context": "...",
  "example": "..."
}}

Rules:
- The "turkish" value must be a natural Turkish meaning for this English word
- The "context" value must explain the meaning inside this text in Turkish
- The "example" value must be one short English sentence using the same word naturally
- Never leave any field empty
- No markdown
- No extra text
""".strip()


def extract_text(data: dict[str, Any]) -> str:
    candidates = data.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        texts = [part.get("text", "") for part in parts if part.get("text")]
        if texts:
            return "\n".join(texts).strip()
    return ""


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", text))


def clean_generated_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"[*_#`]+", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def parse_json_response(raw_text: str) -> dict[str, Any]:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        data = json.loads(cleaned)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = cleaned[start : end + 1]
            candidate = re.sub(r",(\s*[}\]])", r"\1", candidate)
            try:
                data = json.loads(candidate)
                return data if isinstance(data, dict) else {}
            except json.JSONDecodeError:
                return {}
        return {}


def repair_mojibake(value: str) -> str:
    if not value:
        return value
    suspicious = ("Ã", "Å", "Ä", "Ä±", "ÄŸ", "ÅŸ", "Ã¼", "Ã¶", "Ã§", "â")
    targeted_replacements = {
        "ta??mak": "taşımak",
        "kar??la?t?rmak": "karşılaştırmak",
        "d?zenli": "düzenli",
        "kar???k": "karışık",
        "geni?": "geniş",
        "yo?un": "yoğun",
        "karma??k": "karmaşık",
        "yava?": "yavaş",
        "h?zl?": "hızlı",
        "g??l?": "güçlü",
        "zay?f": "zayıf",
        "ama?": "amaç",
        "al??kanl?k": "alışkanlık",
        "kan?t": "kanıt",
        "??z?m": "çözüm",
        "al?namad?": "alınamadı",
        "bulunamad?": "bulunamadı",
        "?yor": "ıyor",
        "?l?r": "ılır",
        "l?": "lı",
        "s?z": "sız",
        "?k": "ık",
    }
    needs_decode = any(token in value for token in suspicious)
    needs_replacements = any(token in value for token in targeted_replacements)
    if not needs_decode and not needs_replacements:
        return value
    repaired_value = value
    if needs_decode:
        for source_encoding in ("latin1", "cp1252"):
            try:
                repaired = value.encode(source_encoding).decode("utf-8")
                if repaired:
                    repaired_value = repaired
                    break
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
    for source, target in targeted_replacements.items():
        repaired_value = repaired_value.replace(source, target)
    return repaired_value


def sanitize_text_tree(value: Any) -> Any:
    if isinstance(value, str):
        return repair_mojibake(value)
    if isinstance(value, dict):
        return {sanitize_text_tree(key): sanitize_text_tree(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_text_tree(item) for item in value]
    if isinstance(value, tuple):
        return tuple(sanitize_text_tree(item) for item in value)
    return value


def sanitize_runtime_text_catalogs() -> None:
    global QUIZ_DISTRACTOR_BANK, LEVEL_CONFIG, LOCAL_WORD_MAP, LOCAL_PHRASE_MAP
    global IRREGULAR_WORD_MAP, WORD_MEANING_OVERRIDES, EXTRA_WORD_MAP, LIBRARY_WORD_MAP
    global FEATURED_PHRASAL_READING
    QUIZ_DISTRACTOR_BANK = sanitize_text_tree(QUIZ_DISTRACTOR_BANK)
    LEVEL_CONFIG = sanitize_text_tree(LEVEL_CONFIG)
    LOCAL_WORD_MAP = sanitize_text_tree(LOCAL_WORD_MAP)
    LOCAL_PHRASE_MAP = sanitize_text_tree(LOCAL_PHRASE_MAP)
    IRREGULAR_WORD_MAP = sanitize_text_tree(IRREGULAR_WORD_MAP)
    WORD_MEANING_OVERRIDES = sanitize_text_tree(WORD_MEANING_OVERRIDES)
    EXTRA_WORD_MAP = sanitize_text_tree(EXTRA_WORD_MAP)
    LIBRARY_WORD_MAP = sanitize_text_tree(LIBRARY_WORD_MAP)
    FEATURED_PHRASAL_READING = sanitize_text_tree(FEATURED_PHRASAL_READING)


sanitize_runtime_text_catalogs()


def is_suspicious_meaning(source_word: str, candidate: str) -> bool:
    cleaned = repair_mojibake(candidate).strip().lower()
    source = source_word.strip().lower()
    if not cleaned:
        return True
    if "?" in cleaned:
        return True
    if cleaned == source or cleaned.startswith(source + " "):
        return True
    if re.search(r"\b(the|and|but|than|because|however|while|since|although)\b", cleaned):
        return True
    compact = re.sub(r"[^a-z]", "", cleaned)
    if compact and compact in {
        "simplifi",
        "irritat",
        "misguid",
        "disciplin",
        "blurr",
        "unsupport",
        "want",
        "need",
        "look",
        "unfocus",
        "unresolv",
    }:
        return True
    if compact and source.startswith(compact) and len(source) - len(compact) <= 3:
        return True
    return False


def lookup_word_map_value(key: str) -> str | None:
    lowered = key.lower()
    approved_map = get_approved_lexical_map()
    if lowered in approved_map:
        return repair_mojibake(approved_map[lowered])
    if lowered in WORD_MEANING_OVERRIDES:
        return repair_mojibake(WORD_MEANING_OVERRIDES[lowered])
    if lowered in LOCAL_WORD_MAP:
        return repair_mojibake(LOCAL_WORD_MAP[lowered])
    if lowered in IRREGULAR_WORD_MAP:
        return repair_mojibake(IRREGULAR_WORD_MAP[lowered])
    if lowered in LIBRARY_WORD_MAP:
        return repair_mojibake(LIBRARY_WORD_MAP[lowered])
    if lowered in EXTRA_WORD_MAP:
        return repair_mojibake(EXTRA_WORD_MAP[lowered])
    return None


def get_approved_lexical_map(force: bool = False) -> dict[str, str]:
    global APPROVED_LEXICAL_MAP, APPROVED_LEXICAL_MAP_READY
    if APPROVED_LEXICAL_MAP_READY and not force:
        return APPROVED_LEXICAL_MAP
    try:
        rows = db_fetchall("SELECT term, meaning FROM lexical_entries")
    except Exception:
        rows = []
    APPROVED_LEXICAL_MAP = {
        normalize_phrase_key(str(row.get("term") or "")): repair_mojibake(str(row.get("meaning") or ""))
        for row in rows
        if str(row.get("term") or "").strip() and str(row.get("meaning") or "").strip()
    }
    APPROVED_LEXICAL_MAP_READY = True
    return APPROVED_LEXICAL_MAP


def runtime_lexical_maps() -> tuple[dict[str, str], ...]:
    return (
        LOCAL_PHRASE_MAP,
        get_approved_lexical_map(),
        LIBRARY_WORD_MAP,
        EXTRA_WORD_MAP,
        WORD_MEANING_OVERRIDES,
    )


def queue_lexical_candidate(
    term: str,
    canonical: str,
    meaning: str,
    *,
    kind: str = "word",
    source: str = "fallback",
    sample_context: str = "",
    confidence: float = 0.55,
) -> None:
    cleaned_term = sanitize_word(term)
    cleaned_canonical = sanitize_word(canonical) or cleaned_term
    cleaned_meaning = repair_mojibake(str(meaning or "")).strip()
    if not cleaned_term or not cleaned_meaning:
        return
    if cleaned_term in get_approved_lexical_map() or cleaned_canonical in get_approved_lexical_map():
        return
    timestamp = now_iso()
    existing = db_fetchone(
        "SELECT id, occurrence_count FROM lexical_review_queue WHERE term = ? AND meaning = ?",
        (cleaned_term, cleaned_meaning),
    )
    if existing:
        db_execute(
            """
            UPDATE lexical_review_queue
            SET occurrence_count = ?, sample_context = COALESCE(NULLIF(?, ''), sample_context), updated_at = ?
            WHERE id = ?
            """,
            (int(existing["occurrence_count"] or 0) + 1, sample_context[:500], timestamp, int(existing["id"])),
        )
        return
    db_execute(
        """
        INSERT INTO lexical_review_queue (
            term, canonical, meaning, kind, source, status, confidence,
            sample_context, occurrence_count, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, 'pending', ?, ?, 1, ?, ?)
        """,
        (
            cleaned_term,
            cleaned_canonical,
            cleaned_meaning,
            kind,
            source,
            float(confidence),
            sample_context[:500],
            timestamp,
            timestamp,
        ),
    )


def infer_turkish_meaning(word: str) -> str:
    lowered = normalize_phrase_key(word)
    phrase_hit = resolve_phrase(lowered, *runtime_lexical_maps())
    if phrase_hit:
        return repair_mojibake(phrase_hit["meaning"])
    for phrase_candidate in phrase_lookup_candidates(lowered):
        if phrase_candidate in LOCAL_PHRASE_MAP:
            return repair_mojibake(LOCAL_PHRASE_MAP[phrase_candidate])
    for candidate in word_root_candidates(lowered):
        for phrase_candidate in phrase_lookup_candidates(candidate):
            if phrase_candidate in LOCAL_PHRASE_MAP:
                return repair_mojibake(LOCAL_PHRASE_MAP[phrase_candidate])
        resolved = lookup_word_map_value(candidate)
        if resolved and not is_suspicious_meaning(lowered, resolved):
            if lowered.endswith("ly") and candidate != lowered:
                return repair_mojibake(f"{resolved} bir şekilde")
            return resolved
    return lowered


def is_compound_expression(word: str) -> bool:
    lowered = word.lower().strip()
    return " " in lowered or "-" in lowered


def infer_contextual_library_meaning(word: str, sentence: str) -> str:
    lowered_word = word.lower().strip()
    profile = resolve_cefr_entry(lowered_word)
    lemma = str(profile.get("lemma") or lowered_word) if profile else lowered_word
    compact_sentence = re.sub(r"\s+", " ", sentence).strip().lower()
    tokens = re.findall(r"[a-z]+(?:['-][a-z]+)*", compact_sentence)
    sentence_has_number = bool(re.search(r"\b\d+\b", compact_sentence))
    if lemma.startswith("treat") and " as " in compact_sentence:
        return "ele almak"
    if lemma == "since":
        if compact_sentence.startswith("since ") and any(marker in compact_sentence for marker in ("because", "as", "so", "it was", "it is")):
            return "çünkü"
        if " since then" in compact_sentence or " since " in compact_sentence:
            return "beri"
        return "beri"
    if lemma == "right":
        if "right now" in compact_sentence:
            return "hemen şimdi"
        if "right away" in compact_sentence:
            return "hemen"
        if "right to" in compact_sentence:
            return "hak"
        if "turn right" in compact_sentence or "on the right" in compact_sentence:
            return "sağ"
        return "doğru"
    if lemma == "still":
        if "still" in tokens and "yet" in tokens:
            return "henüz"
        return "hala"
    if lemma == "even":
        return "hatta"
    if lemma == "over":
        if "over there" in compact_sentence:
            return "şurada"
        if "all over" in compact_sentence:
            return "her yerde"
        if "over the" in compact_sentence and any(unit in compact_sentence for unit in ("day", "week", "month", "year", "years", "hours", "minutes")):
            return "boyunca"
        if sentence_has_number and "over" in tokens:
            return "üzerinde"
        if "over" in tokens and any(prep in tokens for prep in ("the", "a", "an")):
            return "üstünde"
        return "üzerinden"
    if lemma == "like":
        if "would like" in compact_sentence or "i'd like" in compact_sentence or "we'd like" in compact_sentence:
            return "istemek"
        return "gibi"
    if lemma == "as":
        if " as well" in compact_sentence:
            return "de"
        if "as soon as" in compact_sentence:
            return "... olur olmaz"
        if "as if" in compact_sentence:
            return "sanki"
        if " as " in compact_sentence:
            return "olarak"
        return "olarak"
    if lemma == "case":
        if "in case" in compact_sentence:
            return "olur da"
        if "case of" in compact_sentence:
            return "vakası"
        return "durum"
    if lemma == "issue":
        if any(token in tokens for token in ("problem", "problems", "challenge", "challenges")):
            return "sorun"
        if any(token in tokens for token in ("magazine", "journal", "edition")):
            return "sayı"
        return "konu"
    if lemma == "mean":
        if "mean to" in compact_sentence or "meant to" in compact_sentence:
            return "niyet etmek"
        return "anlamına gelmek"
    if lemma == "run":
        if "run into" in compact_sentence:
            return "karşılaşmak"
        if "run out" in compact_sentence:
            return "tükenmek"
        if "run a" in compact_sentence or "run an" in compact_sentence or "run the" in compact_sentence:
            return "işletmek"
        return "koşmak"
    if lemma == "set":
        if "set up" in compact_sentence:
            return "kurmak"
        if "set off" in compact_sentence:
            return "yola çıkmak"
        if "set out" in compact_sentence:
            return "yola koyulmak"
        if "set" in tokens and "goal" in tokens:
            return "belirlemek"
        return "ayarlamak"
    if lemma == "illustrate":
        return "örnekleyerek göstermek"
    if lemma == "simplify":
        return "sadeleştirmek"
    if lemma == "bias":
        return "önyargı"
    if lemma == "model":
        return "model"
    if lemma == "trust":
        return "güven"
    if lemma == "speed":
        return "hız"
    if lemma == "exterior":
        return "dış yüzey"
    resolved = infer_turkish_meaning(lemma)
    if resolved != lemma:
        return resolved
    return infer_turkish_meaning(word)


def is_library_name(word: str) -> bool:
    cleaned = re.sub(r"[^A-Za-z]", "", word).strip().lower()
    return cleaned in {
        "aylin", "deniz", "eren", "selin", "bora", "mina", "kerem", "lina",
        "arda", "derya", "kaan", "elif", "yusuf", "asya", "can", "melis",
        "emma", "tom", "lucy", "anna", "david", "sarah", "ali",
    }


def translate_library_word_with_fallback(word: str, lemma: str) -> str:
    candidates = [word.strip(), lemma.strip()]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            if GOOGLE_TRANSLATE_API_KEY:
                translated = repair_mojibake(translate_text_google(candidate, target_language="tr", source_language="en"))
            else:
                translated = repair_mojibake(
                    request_model(
                        f'Translate this English word or short phrase into Turkish: "{candidate}"\nReturn only the Turkish translation.',
                        "You are a translation engine. Return only the Turkish translation. No punctuation, no extra text.",
                        temperature=0.0,
                        max_output_tokens=24,
                    )
                )
        except Exception:
            continue
        translated = translated.strip().strip("\"").strip("'")
        if translated and not should_use_local_meaning(candidate, translated) and translation_looks_usable(translated):
            queue_lexical_candidate(
                candidate,
                lemma,
                translated,
                kind="phrase" if is_compound_expression(candidate) else "word",
                source="ai_fallback",
            )
            return translated
    return ""


def force_library_meaning(word: str, lemma: str, current: str) -> str:
    cleaned_current = repair_mojibake(current).strip()
    if cleaned_current and not should_use_local_meaning(word, cleaned_current):
        return cleaned_current

    translated = translate_library_word_with_fallback(word, lemma)
    if translated:
        return translated

    inferred = infer_turkish_meaning(word)
    if word.lower().strip() in LOCAL_PHRASE_MAP and inferred:
        return inferred
    if inferred and inferred != word.lower().strip() and not should_use_local_meaning(word, inferred):
        return inferred

    if is_library_name(word):
        return "özel isim"

    if word.isupper() and len(word) >= 2:
        return "kısaltma / özel ad"

    if len(word) <= 2:
        return "bağlama göre işlevsel kelime"

    return "bağlama göre kullanılan ifade"


TOPIC_SCENARIOS: dict[str, list[str]] = {
    "Serbest": [
        "a learner notices a small problem and fixes it through a better habit",
        "a short everyday decision becomes easier after clear communication",
        "a practical routine helps someone stay focused and organized",
    ],
    "Random": [
        "a learner notices a small problem and fixes it through a better habit",
        "a short everyday decision becomes easier after clear communication",
        "a practical routine helps someone stay focused and organized",
    ],
    "Education": [
        "a student improves a study plan before an important exam",
        "a teacher helps a class understand a difficult idea through examples",
    ],
    "Travel": [
        "a traveler solves a small problem in an unfamiliar city",
        "a short trip becomes smoother because someone prepares carefully",
    ],
    "Work Life": [
        "a team handles a deadline by clarifying responsibilities",
        "a meeting becomes useful when people focus on the real problem",
    ],
    "Technology": [
        "a person uses a digital tool more intentionally instead of getting distracted",
        "a small technical change improves how a team works",
    ],
    "Health": [
        "a person builds a healthier routine through realistic daily choices",
        "a simple habit improves energy, sleep, and attention",
    ],
    "Daily Life": [
        "a busy day becomes manageable through planning and calm decisions",
        "a household routine improves after one practical change",
    ],
    "Environment": [
        "a community reduces waste through a small shared decision",
        "a local project makes people think differently about resources",
    ],
    "Communication": [
        "a misunderstanding is solved through clearer language",
        "feedback becomes useful when it is specific and respectful",
    ],
    "Food": [
        "a meal choice becomes part of a healthier routine",
        "someone learns why preparation changes the quality of a meal",
    ],
    "Public Services": [
        "a public service works better when people understand how to use it",
        "a local transport issue improves through better coordination",
    ],
    "Media": [
        "a reader learns to check information before sharing it",
        "a platform changes how people notice and react to news",
    ],
    "Science": [
        "a simple observation leads to a clearer scientific explanation",
        "evidence changes how people understand a common problem",
    ],
    "Psychology": [
        "a person recognizes a pattern in attention, stress, or motivation",
        "a small mental habit changes how someone reacts to pressure",
    ],
    "Finance": [
        "a simple budget helps someone make a calmer decision",
        "a financial choice becomes clearer after comparing priorities",
    ],
    "Arts": [
        "an artist improves a project through practice and revision",
        "a creative choice changes how people experience a piece of work",
    ],
    "Culture": [
        "a community tradition helps people understand shared identity",
        "a cultural habit reveals how memory and belonging work",
    ],
}


TOPIC_SENTENCE_BANK: dict[str, list[str]] = {
    "Serbest": [
        "Mina wanted to make her day feel less rushed, so she wrote down the three tasks that mattered most.",
        "At first the plan looked too simple, but it helped her notice what was useful and what was only noise.",
        "By the evening, she understood that a small routine can make a normal day feel more controlled.",
    ],
    "Random": [
        "Mina wanted to make her day feel less rushed, so she wrote down the three tasks that mattered most.",
        "At first the plan looked too simple, but it helped her notice what was useful and what was only noise.",
        "By the evening, she understood that a small routine can make a normal day feel more controlled.",
    ],
    "Education": [
        "A student changed the way she studied after realizing that long notes did not always help her remember.",
        "She began to review short examples, explain ideas aloud, and connect new information to earlier lessons.",
    ],
    "Travel": [
        "During a short trip, Arda learned that good preparation can prevent many small problems.",
        "He checked the route, kept important details on his phone, and asked for help when the signs were unclear.",
    ],
    "Work Life": [
        "The team was close to a deadline, but the real problem was not the amount of work.",
        "Once each person explained their responsibility clearly, the project became easier to manage.",
    ],
    "Technology": [
        "Deniz used to open every notification immediately, even when he needed to concentrate.",
        "After changing a few settings, his phone became a tool again instead of a constant interruption.",
    ],
    "Health": [
        "Selin wanted to feel healthier, but she knew that extreme plans would not last very long.",
        "She started with short walks, better sleep, and meals that were easy to prepare at home.",
    ],
    "Daily Life": [
        "A normal morning became stressful because too many small decisions were left until the last minute.",
        "Preparing a few things the night before made the next day calmer and more predictable.",
    ],
    "Environment": [
        "A neighborhood group decided to reduce waste by making recycling easier for everyone.",
        "The change was small, but it helped people see how daily habits affect shared spaces.",
    ],
    "Communication": [
        "Two friends disagreed because each person thought the other one understood the plan.",
        "When they slowed down and explained the details, the problem became much easier to solve.",
    ],
    "Food": [
        "Instead of eating quickly outside, Ece prepared a simple meal before a busy afternoon.",
        "The food was not complicated, but it helped her feel more energetic and focused.",
    ],
    "Public Services": [
        "A new bus route confused many people during its first week.",
        "Clear signs and patient explanations helped passengers use the service with more confidence.",
    ],
    "Media": [
        "Before sharing an article, Lina checked where it came from and whether other sources confirmed it.",
        "That small pause helped her avoid spreading a dramatic but misleading story.",
    ],
    "Science": [
        "A simple classroom experiment helped students understand why evidence matters.",
        "They compared results, noticed patterns, and changed their first explanation.",
    ],
    "Psychology": [
        "Kerem noticed that he made worse decisions when he was tired and distracted.",
        "By taking short breaks, he became more aware of his attention and emotions.",
    ],
    "Finance": [
        "A basic budget helped Asya see which expenses were necessary and which were only habits.",
        "After one week, she felt more confident because her choices matched her priorities.",
    ],
    "Arts": [
        "An artist revised the same sketch several times before the final version felt balanced.",
        "Each small change made the image clearer and more expressive.",
    ],
    "Culture": [
        "A local festival reminded people why shared traditions can feel meaningful.",
        "The event connected food, music, memory, and the stories of older family members.",
    ],
}


def choose_local_scenario(topic: str, keywords: list[str]) -> dict[str, Any]:
    topic_key = topic if topic in TOPIC_SCENARIOS else "Serbest"
    scenario_seed = TOPIC_SCENARIOS[topic_key][len(keywords) % len(TOPIC_SCENARIOS[topic_key])]
    return {
        "scenario": scenario_seed,
        "voice": "clear, natural, and realistic",
        "beats": [
            "open with a clear everyday situation",
            "introduce a practical action or responsibility",
            "connect the keywords through a natural flow",
            "end with a small reflection or outcome",
        ],
    }


def has_library_mapping(word: str) -> bool:
    return any(candidate in LIBRARY_WORD_MAP for candidate in word_root_candidates(word))


def build_local_word_detail(text: str, word: str) -> dict[str, str]:
    if has_library_mapping(word):
        return build_library_word_detail(text, word)
    meaning = infer_turkish_meaning(word)
    sentence = find_sentence_for_word(text, word)
    context = repair_mojibake(f'"{word}" burada büyük olasılıkla "{meaning}" anlamında kullanılıyor.')
    example = f"The word {word} appears in this reading text."
    if sentence:
        compact_sentence = re.sub(r"\s+", " ", sentence).strip()
        context = repair_mojibake(
            f'Bu metinde "{word}" kelimesi "{meaning}" fikrini veriyor. Geçtiği bölüm: {compact_sentence}'
        )
        example = compact_sentence
    return {
        "turkish": meaning,
        "context": context,
        "example": example,
        "collocations": extract_collocations(text, word),
    }


def should_use_local_meaning(word: str, candidate: str) -> bool:
    cleaned = candidate.strip().lower()
    lowered_word = word.strip().lower()
    return not cleaned or cleaned == lowered_word or cleaned.startswith(lowered_word + " ") or is_suspicious_meaning(lowered_word, cleaned)


def html_unescape(value: str) -> str:
    return (
        value.replace("&#39;", "'")
        .replace("&quot;", '"')
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
    )


def translate_text_google(text: str, *, target_language: str = "tr", source_language: str | None = None) -> str:
    if not GOOGLE_TRANSLATE_API_KEY:
        raise HTTPException(status_code=500, detail="GOOGLE_TRANSLATE_API_KEY bulunamadı.")
    payload: dict[str, Any] = {
        "q": text,
        "target": target_language,
        "format": "text",
        "key": GOOGLE_TRANSLATE_API_KEY,
    }
    if source_language:
        payload["source"] = source_language
    with build_http_client() as client:
        response = client.post(GOOGLE_TRANSLATE_API_URL, data=payload)
        response.raise_for_status()
        data = response.json()
    translated = (
        data.get("data", {})
        .get("translations", [{}])[0]
        .get("translatedText", "")
    )
    return html_unescape(str(translated).strip())


def find_sentence_for_word(text: str, word: str) -> str:
    candidates = re.split(r"(?<=[.!?])\s+", text.strip())
    needle = re.sub(r"\s+", " ", word.strip())
    if " " in needle:
        lowered = needle.lower()
        for sentence in candidates:
            if lowered in sentence.lower():
                return sentence.strip()
        phrase_hit = resolve_phrase(needle, *runtime_lexical_maps())
        if phrase_hit:
            canonical = str(phrase_hit.get("canonical") or "")
            for sentence in candidates:
                if any(match.canonical == canonical for match in match_phrases(sentence, *runtime_lexical_maps())):
                    return sentence.strip()
        return ""
    for sentence in candidates:
        if re.search(rf"\b{re.escape(word)}\b", sentence, flags=re.IGNORECASE):
            return sentence.strip()
    return ""


def extract_unique_words(text: str) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for match in re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", text):
        lowered = match.lower()
        if lowered not in seen:
            seen.add(lowered)
            ordered.append(lowered)
    return ordered


def describe_word_form(word: str) -> dict[str, str]:
    lowered = word.lower().strip()
    profile = resolve_cefr_entry(lowered)
    root = str(profile.get("lemma") or lowered) if profile else lowered
    note = "yalın biçim"
    if lowered.endswith("ies") and len(lowered) > 4:
        root = lowered[:-3] + "y"
        note = "köküne -ies eklenmiş; çoğul ya da 3. tekil çekim olabilir"
    elif lowered.endswith("es") and len(lowered) > 3:
        root = lowered[:-2]
        note = "köküne -es eklenmiş; çoğul ya da 3. tekil çekim olabilir"
    elif lowered.endswith("s") and len(lowered) > 3:
        root = lowered[:-1]
        note = "köküne -s eklenmiş; bu cümlede çoğunlukla 3. tekil ya da çoğul kullanım verir"
    elif lowered.endswith("ing") and len(lowered) > 4:
        root = lowered[:-3]
        if len(root) > 2 and root[-1] == root[-2]:
            root = root[:-1]
        note = "-ing eki almış; süreç, isimleşme ya da sıfat görevi taşıyabilir"
    elif lowered.endswith("ed") and len(lowered) > 3:
        root = lowered[:-2]
        if root.endswith("i"):
            root = root[:-1] + "y"
        elif len(root) > 2 and root[-1] == root[-2]:
            root = root[:-1]
        note = "-ed eki almış; geçmiş zaman, edilgen ya da sıfatlaşmış kullanım olabilir"
    elif lowered.endswith("ly") and len(lowered) > 4:
        root = lowered[:-2]
        note = "-ly eki almış; zarf biçiminde kullanılıyor"
    if profile and profile.get("level"):
        note = f"{note}; tahmini CEFR seviyesi: {profile['level']}"
    return {"root": root or lowered, "note": note}


def translate_sentence_locally(text: str) -> str:
    parts = re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*|\s+|[^A-Za-z\s]", text)
    translated_parts: list[str] = []
    for part in parts:
        if re.fullmatch(r"[A-Za-z]+(?:['-][A-Za-z]+)*", part):
            translated_parts.append(infer_turkish_meaning(part))
        else:
            translated_parts.append(part)
    translated = "".join(translated_parts)
    translated = re.sub(r"\s+([,.!?;:])", r"\1", translated)
    translated = re.sub(r"\s+", " ", translated).strip()
    return repair_mojibake(translated)


def translation_looks_usable(value: str) -> bool:
    if not value:
        return False
    cleaned = repair_mojibake(value).strip()
    lowered = cleaned.lower()
    english_tokens = re.findall(r"\b[a-z]{2,}\b", lowered)
    blocked = {
        "the", "and", "but", "than", "of", "to", "in", "with", "a", "an", "as", "at",
        "on", "for", "from", "by", "is", "are", "has", "have", "had", "that", "this",
        "these", "those", "can", "will", "would", "should", "could", "looks", "become",
        "becomes", "became", "feel", "feels", "felt", "used", "like",
    }
    english_hits = [token for token in english_tokens if token in blocked]
    return len(english_hits) <= 1


def normalize_target_level(level: str) -> str:
    return READING_LEVEL_TARGETS.get(level, {}).get("target", level)


def cefr_rank(level: str) -> int:
    return CEFR_LEVEL_ORDER.get(level, 99)


def word_root_candidates(word: str) -> list[str]:
    lowered = word.lower().strip()

    def add(candidate: str) -> None:
        cleaned = candidate.strip().lower()
        if cleaned and cleaned not in candidates:
            candidates.append(cleaned)

    candidates: list[str] = []

    add(lowered)
    if lowered.endswith("ies") and len(lowered) > 4:
        add(lowered[:-3] + "y")
    if lowered.endswith("es") and len(lowered) > 3:
        add(lowered[:-2])
    if lowered.endswith("s") and len(lowered) > 3:
        add(lowered[:-1])
    if lowered.endswith("ing") and len(lowered) > 4:
        stem = lowered[:-3]
        add(stem)
        add(stem + "e")
        if len(stem) > 2 and stem[-1] == stem[-2]:
            add(stem[:-1])
    if lowered.endswith("ed") and len(lowered) > 3:
        stem = lowered[:-2]
        add(stem)
        add(stem + "e")
        if stem.endswith("i"):
            add(stem[:-1] + "y")
        if len(stem) > 2 and stem[-1] == stem[-2]:
            add(stem[:-1])
    if lowered.endswith("ly") and len(lowered) > 4:
        add(lowered[:-2])
    return candidates


def resolve_cefr_entry(word: str) -> dict[str, Any] | None:
    for candidate in word_root_candidates(word):
        entry = CEFR_VOCAB_INDEX.get(candidate)
        if entry:
            return {"lemma": candidate, **entry}
    return None


def sentence_opening_signature(sentence: str) -> str:
    tokens = re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", sentence.lower())
    return " ".join(tokens[:3]).strip()


def detect_sentence_shape(sentence: str) -> str:
    lowered = sentence.lower()
    has_contrast = any(marker in lowered for marker in CONTRAST_MARKERS)
    has_cause = any(marker in lowered for marker in CAUSE_MARKERS)
    word_count = len(re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", sentence))
    if has_contrast and has_cause:
        return "contrast+cause"
    if has_contrast:
        return "contrast"
    if has_cause:
        return "cause"
    if word_count <= 8:
        return "short"
    if word_count >= 24:
        return "long"
    return "plain"


def assess_library_reading_quality(text: str, level: str, keywords: list[str]) -> dict[str, Any]:
    sentences = [item.strip() for item in re.split(r"(?<=[.!?])\s+", text.strip()) if item.strip()]
    tokens = extract_unique_words(text)
    sentence_lengths = [len(re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", sentence)) for sentence in sentences]
    avg_sentence_length = sum(sentence_lengths) / max(len(sentence_lengths), 1)
    target_rule = READING_LEVEL_TARGETS.get(level, READING_LEVEL_TARGETS["B1"])
    target_rank = cefr_rank(normalize_target_level(level))

    advanced_hits = 0
    known_levels = 0
    for token in tokens:
        entry = resolve_cefr_entry(token)
        if not entry:
            continue
        known_levels += 1
        if cefr_rank(str(entry["level"])) >= target_rank:
            advanced_hits += 1

    openings = [sentence_opening_signature(sentence) for sentence in sentences if sentence_opening_signature(sentence)]
    repeated_openings = len(openings) - len(set(openings))
    shape_types = [detect_sentence_shape(sentence) for sentence in sentences]
    repeated_shapes = max((shape_types.count(shape) for shape in set(shape_types)), default=0)
    lowered_text = text.lower()
    keyword_hits = sum(1 for keyword in keywords if keyword and keyword.lower() in lowered_text)
    banned_opening_hit = 1 if openings and openings[0].startswith(GENERIC_OPENING_PATTERNS) else 0
    contrast_hit = any(shape in {"contrast", "contrast+cause"} for shape in shape_types)
    cause_hit = any(shape in {"cause", "contrast+cause"} for shape in shape_types)
    long_hit = any(length >= 18 for length in sentence_lengths)
    short_hit = any(length <= 8 for length in sentence_lengths)
    generic_phrase_hits = sum(lowered_text.count(pattern) for pattern in GENERIC_OPENING_PATTERNS)

    score = 100
    score -= abs(avg_sentence_length - target_rule["ideal_avg"]) * 1.8
    if avg_sentence_length > target_rule["max_avg"]:
        score -= (avg_sentence_length - target_rule["max_avg"]) * 3
    score -= repeated_openings * 8
    score -= max(0, repeated_shapes - 2) * 7
    score -= generic_phrase_hits * 12
    score -= banned_opening_hit * 18
    score += keyword_hits * 6
    score += 6 if short_hit else -6
    score += 6 if long_hit or level in {"A1", "A2"} else -6
    score += 7 if contrast_hit or not target_rule["needs_contrast"] else -8
    score += 7 if cause_hit or not target_rule["needs_cause"] else -8
    if known_levels:
        score += min(12, advanced_hits * 2)
    if level in {"B2", "C1", "C2", "Academic"} and advanced_hits < target_rule["advanced_min"]:
        score -= (target_rule["advanced_min"] - advanced_hits) * 8

    return {
        "score": round(score, 2),
        "avg_sentence_length": round(avg_sentence_length, 2),
        "advanced_hits": advanced_hits,
        "keyword_hits": keyword_hits,
        "repeated_openings": repeated_openings,
        "repeated_shapes": repeated_shapes,
        "contrast_hit": contrast_hit,
        "cause_hit": cause_hit,
    }


def build_library_sentence_index(readings: list[dict[str, Any]]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for item in readings:
        for sentence in re.split(r"(?<=[.!?])\s+", str(item.get("text", "")).strip()):
            compact_sentence = re.sub(r"\s+", " ", sentence).strip()
            if not compact_sentence:
                continue
            for word in extract_unique_words(compact_sentence):
                bucket = index.setdefault(word, [])
                if compact_sentence not in bucket:
                    bucket.append(compact_sentence)
    return index


LIBRARY_SENTENCE_INDEX = build_library_sentence_index(READING_SEEDS)
LIBRARY_READING_QUALITY_INDEX = {
    item["title"]: assess_library_reading_quality(
        str(item.get("text", "")),
        str(item.get("level", "B1")),
        list(item.get("keywords", [])),
    )
    for item in READING_SEEDS
}


def gather_library_examples(word: str, current_sentence: str = "") -> list[str]:
    candidates = LIBRARY_SENTENCE_INDEX.get(word.lower(), [])
    picked: list[str] = []
    normalized_current = re.sub(r"\s+", " ", current_sentence).strip()
    for sentence in candidates:
        if normalized_current and sentence == normalized_current:
            continue
        if sentence not in picked:
            picked.append(sentence)
        if len(picked) >= 3:
            break
    if not picked and normalized_current:
        picked.append(normalized_current)
    return picked[:3]


def extract_collocations(text: str, word: str, limit: int = 3) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    lowered = word.lower()
    collocations: list[str] = []
    seen: set[str] = set()
    for sentence in sentences:
        tokens = re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", sentence)
        lowered_tokens = [token.lower() for token in tokens]
        for index, token in enumerate(lowered_tokens):
            if token != lowered:
                continue
            windows = [
                lowered_tokens[max(0, index - 1): min(len(tokens), index + 2)],
                lowered_tokens[max(0, index - 2): min(len(tokens), index + 1)],
                lowered_tokens[max(0, index): min(len(tokens), index + 3)],
            ]
            for chunk in windows:
                phrase = " ".join(chunk).strip()
                if len(chunk) < 2 or phrase in seen:
                    continue
                seen.add(phrase)
                collocations.append(phrase)
                if len(collocations) >= limit:
                    return collocations
    if not collocations:
        collocations.append(lowered)
    return collocations[:limit]


def build_library_word_detail(text: str, word: str) -> dict[str, str]:
    lowered_word = word.lower()
    if is_compound_expression(lowered_word):
        sentence = find_sentence_for_word(text, word)
        phrase_hit = resolve_phrase(lowered_word, *runtime_lexical_maps())
        canonical_phrase = str(phrase_hit.get("canonical") or lowered_word) if phrase_hit else lowered_word
        library_meaning = repair_mojibake(str(phrase_hit.get("meaning") or "")) if phrase_hit else infer_turkish_meaning(lowered_word)
        if not phrase_hit and should_use_local_meaning(word, library_meaning):
            library_meaning = translate_library_word_with_fallback(lowered_word, canonical_phrase) or "bağlama göre kullanılan ifade"
        compact_sentence = re.sub(r"\s+", " ", sentence).strip() if sentence else ""
        context_lines = [f'Bu metindeki anlamı: "{library_meaning}"']
        if canonical_phrase != lowered_word:
            context_lines.append(f"Kalıp kökü: {canonical_phrase}")
        if compact_sentence:
            context_lines.append(f"Geçtiği cümle: {compact_sentence}")
        example_lines = [f"1. {compact_sentence}" if compact_sentence else f"1. The phrase {word} appears in this reading text."]
        return {
            "turkish": repair_mojibake(library_meaning),
            "context": repair_mojibake("\n".join(context_lines)),
            "example": repair_mojibake("\n".join(example_lines)),
            "collocations": extract_collocations(text, word),
        }
    profile = resolve_cefr_entry(lowered_word)
    lemma = str(profile.get("lemma") or lowered_word) if profile else lowered_word
    forced_override = WORD_MEANING_OVERRIDES.get(lowered_word) or WORD_MEANING_OVERRIDES.get(lemma)
    override_meaning = lookup_word_map_value(lowered_word) or lookup_word_map_value(lemma)
    raw_library_meaning = repair_mojibake(str(LIBRARY_WORD_MAP.get(lowered_word) or LIBRARY_WORD_MAP.get(lemma, "")))
    sentence = find_sentence_for_word(text, word)
    if forced_override:
        library_meaning = repair_mojibake(forced_override)
    elif override_meaning and not is_suspicious_meaning(word, override_meaning):
        library_meaning = override_meaning
    elif is_suspicious_meaning(word, raw_library_meaning):
        library_meaning = infer_contextual_library_meaning(lemma, sentence)
    else:
        library_meaning = raw_library_meaning
    if not library_meaning:
        library_meaning = infer_contextual_library_meaning(lemma, sentence)
    library_meaning = force_library_meaning(word, lemma, library_meaning)
    compact_sentence = re.sub(r"\s+", " ", sentence).strip() if sentence else ""
    translated_sentence = ""
    if compact_sentence and GOOGLE_TRANSLATE_API_KEY:
        try:
            translated_sentence = translate_text_google(compact_sentence, target_language="tr", source_language="en")
        except Exception:
            translated_sentence = ""
    form_info = describe_word_form(lowered_word)
    context_lines = [f'Bu metindeki anlamı: "{library_meaning}"']
    context_lines.append(f'Kök: {form_info["root"]} · {form_info["note"]}')
    if profile and profile.get("level"):
        context_lines.append(f'Kelime seviyesi: {profile["level"]}')
    if compact_sentence:
        context_lines.append(f"Geçtiği cümle: {compact_sentence}")
    if translated_sentence and translation_looks_usable(translated_sentence):
        context_lines.append(f"TR: {translated_sentence}")

    example_sentences = gather_library_examples(lemma, compact_sentence)[:2]
    example_lines: list[str] = []
    for index, example_sentence in enumerate(example_sentences, start=1):
        example_lines.append(f"{index}. {example_sentence}")
        if GOOGLE_TRANSLATE_API_KEY:
            try:
                example_translation = translate_text_google(example_sentence, target_language="tr", source_language="en")
            except Exception:
                example_translation = ""
            if example_translation and translation_looks_usable(example_translation):
                example_lines.append(f"TR: {example_translation}")
    if not example_lines:
        example_lines = [f"1. The word {word} appears in this reading text."]
    return {
        "turkish": repair_mojibake(library_meaning or infer_contextual_library_meaning(lemma, sentence)),
        "context": repair_mojibake("\n".join(context_lines)),
        "example": repair_mojibake("\n".join(example_lines)),
        "collocations": extract_collocations(text, word),
    }


def build_library_glossary(text: str) -> dict[str, dict[str, str]]:
    glossary: dict[str, dict[str, str]] = {}
    phrase_matches = match_phrases(text, *runtime_lexical_maps())
    covered_tokens = covered_token_indexes(phrase_matches)
    for phrase_match in phrase_matches:
        key = sanitize_word(phrase_match.key)
        canonical = sanitize_word(phrase_match.canonical)
        if key and key not in glossary:
            detail = build_library_word_detail(text, key)
            detail["canonical"] = canonical
            detail["kind"] = "phrase"
            glossary[key] = detail
        if canonical and canonical != key and canonical not in glossary:
            detail = build_library_word_detail(text, canonical)
            detail["surface"] = key
            detail["kind"] = "phrase"
            glossary[canonical] = detail
    word_seen: set[str] = set()
    for index, token in enumerate(token_records(text)):
        if index in covered_tokens:
            continue
        word = sanitize_word(str(token.get("key") or ""))
        if not word or word in word_seen:
            continue
        word_seen.add(word)
        glossary[word] = build_library_word_detail(text, word)
    lowered = text.lower()
    for phrase in LOCAL_PHRASE_MAP:
        if " " in phrase and phrase in lowered and phrase not in glossary:
            glossary[phrase] = build_library_word_detail(text, phrase)
    return glossary


def build_local_reading(level: str, topic: str, keywords: list[str], length_target: int) -> str:
    topic_key = topic if topic in TOPIC_SENTENCE_BANK else "Serbest"
    base_sentences = TOPIC_SENTENCE_BANK[topic_key][:]
    keyword_sentences = []
    for index, keyword in enumerate(keywords):
        if index == 0:
            keyword_sentences.append(f"In this text, {keyword} becomes one of the key details that shapes the situation.")
        elif index == 1:
            keyword_sentences.append(f"As the paragraph develops, {keyword} fits naturally into the flow of the day.")
        elif index == 2:
            keyword_sentences.append(f"Later, {keyword} helps the reader understand the goal or challenge more clearly.")
        else:
            keyword_sentences.append(f"In a realistic way, {keyword} supports the main idea without feeling forced.")
    level_sentences = {
        "A1": [
            "The ideas stay short, direct, and very easy to follow.",
            "Each sentence gives one clear piece of information.",
        ],
        "A2": [
            "The situation is simple, clear, and easy to follow.",
            "Each step connects to the next part of the day in a natural way.",
        ],
        "B1": [
            "The situation develops gradually, and each detail supports the main idea.",
            "As the day moves forward, the person becomes more aware of what matters most.",
        ],
        "B2": [
            "Because of this, the person has to think carefully, stay calm, and adapt to changing priorities.",
            "This creates a realistic picture of how everyday choices, communication, and timing shape the final outcome.",
        ],
        "C1": [
            "As the situation grows more complex, the text highlights subtle motivations, decisions, and consequences.",
            "This makes the reading feel more layered while still staying coherent and accessible.",
        ],
        "C2": [
            "From a highly advanced perspective, the paragraph also draws attention to nuance, interpretation, and conceptual precision.",
            "The tone remains layered and analytical, so the reader can follow both the example and the broader argument behind it.",
        ],
        "Academic": [
            "From an academic perspective, the paragraph also draws attention to evidence, structure, and interpretation.",
            "The tone remains analytical, so the reader can follow both the example and the broader idea behind it.",
        ],
    }
    sentences = base_sentences + keyword_sentences + level_sentences[level]
    paragraph = " ".join(sentences)
    filler_pool = base_sentences + level_sentences[level]
    filler_index = 0
    target_ceiling = min(length_target, LEVEL_CONFIG[level]["max_words"])
    while count_words(paragraph) < target_ceiling:
        paragraph += " " + filler_pool[filler_index % len(filler_pool)]
        filler_index += 1
        if count_words(paragraph) >= target_ceiling:
            break
    trimmed = " ".join(paragraph.split()[:target_ceiling])
    return clean_generated_text(trimmed)


def validate_text_quality(text: str, level: str, keywords: list[str]) -> tuple[bool, dict[str, Any]]:
    word_count = count_words(text)
    cfg = LEVEL_CONFIG[level]
    keyword_hits = [keyword.lower() in text.lower() for keyword in keywords]
    metrics = {
        "word_count": word_count,
        "length_ok": cfg["min_words"] <= word_count <= cfg["max_words"],
        "keyword_ok": all(keyword_hits),
        "has_markdown": bool(re.search(r"[*_#`]", text)),
    }
    is_valid = bool(metrics["length_ok"] and metrics["keyword_ok"] and not metrics["has_markdown"])
    return is_valid, metrics


def ensure_provider_ready() -> None:
    if MODEL_PROVIDER == "gemini":
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail=repair_mojibake("GEMINI_API_KEY bulunamadı."))
        return
    if MODEL_PROVIDER == "hf":
        if not HF_TOKEN:
            raise HTTPException(status_code=500, detail=repair_mojibake("HF_TOKEN bulunamadı."))
        return
    raise HTTPException(status_code=500, detail=f"Desteklenmeyen provider: {MODEL_PROVIDER}")


def request_gemini(prompt: str, system_instruction: str, *, temperature: float, max_output_tokens: int, json_mode: bool = False) -> str:
    payload: dict[str, Any] = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }
    if json_mode:
        payload["generationConfig"]["responseMimeType"] = "application/json"
    with build_http_client() as client:
        response = client.post(
            GEMINI_API_URL,
            headers={"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
    text = extract_text(data)
    if not text:
        raise RuntimeError(repair_mojibake("Gemini boş yanıt döndü."))
    return text


def request_hf(prompt: str, system_instruction: str, *, temperature: float, max_output_tokens: int) -> str:
    client = build_openai_compatible_client(HF_BASE_URL, HF_TOKEN)
    response = client.chat.completions.create(
        model=HF_MODEL,
        messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_output_tokens,
    )
    text = response.choices[0].message.content or ""
    cleaned = text.strip()
    if not cleaned:
        raise RuntimeError(repair_mojibake("HF Router boş yanıt döndü."))
    return cleaned


def request_model(prompt: str, system_instruction: str, *, temperature: float, max_output_tokens: int, json_mode: bool = False) -> str:
    ensure_provider_ready()
    if MODEL_PROVIDER == "hf":
        return request_hf(prompt, system_instruction, temperature=temperature, max_output_tokens=max_output_tokens)
    return request_gemini(
        prompt,
        system_instruction,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        json_mode=json_mode,
    )


def request_text(prompt: str, level: str, topic: str, keywords: list[str]) -> str:
    cache_key = hashlib.sha1(
        json.dumps(
            {"level": level, "topic": topic, "keywords": keywords, "prompt": prompt, "provider": MODEL_PROVIDER},
            ensure_ascii=True,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    cached = GENERATE_CACHE.get(cache_key)
    if cached:
        return cached
    system_instruction = (
        "You are a premium English learning assistant. "
        "Write concise, natural reading passages and follow the requested format exactly."
    )
    min_words = LEVEL_CONFIG[level]["min_words"]
    plan = choose_local_scenario(topic, keywords)
    try:
        raw_plan = request_model(
            build_plan_prompt(level, topic, keywords, LEVEL_CONFIG[level]["max_words"]),
            "You are an expert educational content planner. Return compact JSON only.",
            temperature=0.25,
            max_output_tokens=220,
            json_mode=True,
        )
        parsed_plan = parse_json_response(raw_plan)
        if parsed_plan:
            plan = {
                "scenario": parsed_plan.get("scenario") or plan["scenario"],
                "voice": parsed_plan.get("voice") or plan["voice"],
                "beats": parsed_plan.get("beats") or plan["beats"],
            }
    except Exception:
        pass
    try:
        text = request_model(
            build_text_from_plan_prompt(level, topic, keywords, LEVEL_CONFIG[level]["max_words"], plan),
            system_instruction,
            temperature=0.6,
            max_output_tokens=min(620, LEVEL_CONFIG[level]["max_words"] * 3),
        )
        text = clean_generated_text(text)
    except Exception:
        text = ""
    is_valid, _ = validate_text_quality(text, level, keywords) if text else (False, {})
    if not is_valid and text:
        repaired = clean_generated_text(f"{text} {' '.join(keywords)}")
        repaired_ok, _ = validate_text_quality(repaired, level, keywords)
        text = repaired if repaired_ok else text
    if count_words(text) < max(60, min_words // 2):
        text = build_local_reading(level, topic, keywords, LEVEL_CONFIG[level]["max_words"])
    GENERATE_CACHE[cache_key] = text
    return text


def request_manual_explanation(text: str, word: str) -> str:
    detail = request_word_detail(text, word)
    return (
        f"Turkish meaning: {detail['turkish']}\n"
        f"Context in Turkish: {detail['context']}\n"
        f"Simple example: {detail['example']}"
    )


def request_word_detail(text: str, word: str) -> dict[str, str]:
    cache_key = f"{hashlib.sha1(text.encode('utf-8')).hexdigest()}::{word.lower()}::google-translate"
    cached = WORD_DETAIL_CACHE.get(cache_key)
    if cached:
        return cached
    local_fallback = build_local_word_detail(text, word)
    sentence = find_sentence_for_word(text, word)
    translated_meaning = ""
    translated_context = ""
    try:
        translated_meaning = translate_text_google(word, target_language="tr", source_language="en")
    except Exception:
        translated_meaning = ""
    if sentence:
        try:
            translated_context = translate_text_google(sentence, target_language="tr", source_language="en")
        except Exception:
            translated_context = ""
    result = {
        "turkish": local_fallback["turkish"] if should_use_local_meaning(word, translated_meaning) else translated_meaning,
        "context": translated_context or local_fallback["context"],
        "example": sentence or local_fallback["example"],
    }
    result = {key: repair_mojibake(str(value)) for key, value in result.items()}
    WORD_DETAIL_CACHE[cache_key] = result
    return result


def normalize_api_error(exc: Exception) -> HTTPException:
    if isinstance(exc, HTTPException):
        return exc
    raw = str(exc).strip() or "Unknown API error"
    lowered = raw.lower()
    if "api key" in lowered or "permission" in lowered or "unauthorized" in lowered:
        if MODEL_PROVIDER == "hf":
            return HTTPException(status_code=401, detail=repair_mojibake("HF token geçersiz veya yetkisiz."))
        return HTTPException(status_code=401, detail=repair_mojibake("Gemini API key geçersiz veya yetkisiz."))
    if "429" in lowered or "quota" in lowered or "rate limit" in lowered:
        if MODEL_PROVIDER == "hf":
            return HTTPException(status_code=429, detail=repair_mojibake("HF ücretsiz limitine ulaşıldı."))
        return HTTPException(status_code=429, detail=repair_mojibake("Gemini free tier limiti aşıldı."))
    if "403" in lowered:
        return HTTPException(status_code=403, detail=repair_mojibake("Seçili sağlayıcı bu isteğe izin vermedi."))
    if "404" in lowered:
        return HTTPException(status_code=404, detail=repair_mojibake("Seçili model bulunamadı."))
    if "503" in lowered or "connection" in lowered or "timed out" in lowered:
        if MODEL_PROVIDER == "hf":
            return HTTPException(status_code=503, detail=repair_mojibake("HF Router servisine şu anda ulaşılamıyor."))
        return HTTPException(status_code=503, detail=repair_mojibake("Gemini servisine şu anda ulaşılamıyor."))
    return HTTPException(status_code=500, detail=raw)


app = FastAPI(title="ReadLex")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health(session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    active_model = HF_MODEL if MODEL_PROVIDER == "hf" else GEMINI_MODEL
    configured = bool(HF_TOKEN) if MODEL_PROVIDER == "hf" else bool(GEMINI_API_KEY)
    user = optional_user(session_token)
    return {
        "status": "ok",
        "provider": MODEL_PROVIDER,
        "model": active_model,
        "configured": configured,
        "levels": list(LEVEL_CONFIG.keys()),
        "user": user,
    }


@app.post("/api/auth/register")
def register(payload: AuthRequest, response: Response) -> dict[str, Any]:
    username = clean_username(payload.username)
    password_hash = hash_password(payload.password)
    timestamp = now_iso()
    try:
        insert_query = "INSERT INTO users (username, password_hash, is_active, verified_at, created_at) VALUES (?, ?, ?, ?, ?)"
        if USE_POSTGRES:
            insert_query += " RETURNING id"
        user_id = db_insert(insert_query, (username, password_hash, 1, timestamp, timestamp))
    except Exception as exc:
        if "unique" not in str(exc).lower() and "duplicate" not in str(exc).lower():
            raise
        raise HTTPException(status_code=409, detail="This username is already in use.")
    create_session(response, user_id)
    return {"user": {"id": user_id, "username": username, "created_at": timestamp, "email_verified": True}, "stats": build_user_stats(user_id)}


@app.post("/api/auth/login")
def login(payload: AuthRequest, response: Response) -> dict[str, Any]:
    username = clean_username(payload.username)
    row = db_fetchone(
        "SELECT id, username, created_at, is_active, password_hash FROM users WHERE username = ?",
        (username,),
    )
    if not row or not verify_password(payload.password, str(row.get("password_hash", ""))):
        raise HTTPException(status_code=401, detail="Username or password is incorrect.")
    if password_hash_needs_upgrade(str(row.get("password_hash", ""))):
        db_execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (hash_password(payload.password), int(row["id"])),
        )
    create_session(response, int(row["id"]))
    return {"user": user_payload(row), "stats": build_user_stats(int(row["id"]))}


@app.post("/api/auth/resend-verification")
def resend_verification(payload: ResendVerificationRequest) -> dict[str, Any]:
    email = clean_username(payload.email)
    row = db_fetchone("SELECT id, username, is_active FROM users WHERE username = ?", (email,))
    if not row:
        raise HTTPException(status_code=404, detail="No account found for this email.")
    if bool(row.get("is_active", 1)):
        return {"ok": True, "message": "This email is already verified."}
    token = create_verification_token(int(row["id"]), email)
    send_verification_email(email, token)
    return {"ok": True, "message": "A fresh verification link has been sent."}


@app.get("/api/auth/verify-email", response_class=HTMLResponse)
def verify_email(token: str) -> str:
    row = db_fetchone(
        """
        SELECT id, user_id, email, expires_at, used_at
        FROM email_verifications
        WHERE token = ?
        """,
        (token,),
    )
    if not row:
        return """
        <html><body style="font-family:Arial,sans-serif;padding:40px;color:#183153;">
        <h2>Verification link is invalid.</h2>
        <p>Please go back to the app and request a new verification email.</p>
        </body></html>
        """
    if row.get("used_at"):
        return """
        <html><body style="font-family:Arial,sans-serif;padding:40px;color:#183153;">
        <h2>Email already verified.</h2>
        <p>You can return to the app and log in now.</p>
        </body></html>
        """
    if parse_iso_datetime(str(row["expires_at"])) < now_utc():
        return """
        <html><body style="font-family:Arial,sans-serif;padding:40px;color:#183153;">
        <h2>Verification link expired.</h2>
        <p>Please return to the app and request a new verification email.</p>
        </body></html>
        """
    timestamp = now_iso()
    db_execute(
        "UPDATE users SET is_active = 1, verified_at = ? WHERE id = ?",
        (timestamp, int(row["user_id"])),
    )
    db_execute(
        "UPDATE email_verifications SET used_at = ? WHERE id = ?",
        (timestamp, int(row["id"])),
    )
    return f"""
    <html><body style="font-family:Arial,sans-serif;padding:40px;color:#183153;">
    <h2>Email verified successfully.</h2>
    <p>{row["email"]} is now active.</p>
    <p><a href="{APP_BASE_URL}" style="display:inline-block;padding:12px 18px;border-radius:999px;background:#58cc02;color:#0f2c49;text-decoration:none;font-weight:700;">Open ReadLex</a></p>
    </body></html>
    """


@app.post("/api/auth/logout")
def logout(response: Response, session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, bool]:
    clear_session(response, session_token)
    return {"ok": True}


@app.get("/api/auth/me")
def me(session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    user = optional_user(session_token)
    if not user:
        return {
            "user": None,
            "stats": {
                "saved_words": 0,
                "mastered_words": 0,
                "saved_today": 0,
                "readings_today": 0,
                "total_readings": 0,
                "daily_goal": 5,
                "streak": 0,
                "hard_words": 0,
            },
            "recent_words": [],
            "history": [],
            "progress_history": [],
        }
    return {
        "user": user,
        "stats": build_user_stats(int(user["id"])),
        "recent_words": get_recent_words(int(user["id"])),
        "history": get_reading_history(int(user["id"])),
        "progress_history": get_progress_history(int(user["id"])),
    }


@app.get("/api/social")
def social_overview(session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    user = require_user(session_token)
    user_id = int(user["id"])
    cheer_row = db_fetchone(
        """
        SELECT COUNT(*) AS total
        FROM social_events
        WHERE receiver_id = ? AND event_type = 'cheer'
        """,
        (user_id,),
    ) or {"total": 0}
    return {
        "friends": list_social_friends(user_id),
        "incoming": list_social_requests(user_id, "incoming"),
        "outgoing": list_social_requests(user_id, "outgoing"),
        "suggestions": list_social_suggestions(user_id),
        "cheers_received": int(cheer_row["total"] or 0),
    }


@app.post("/api/social/request")
def social_request_friend(
    payload: FriendRequestPayload,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    user_id = int(user["id"])
    target_username = clean_username(payload.username)
    target = db_fetchone("SELECT id, username FROM users WHERE username = ?", (target_username,))
    if not target:
        raise HTTPException(status_code=404, detail="User not found.")
    target_id = int(target["id"])
    if target_id == user_id:
        raise HTTPException(status_code=400, detail="You cannot add yourself.")
    existing = get_friendship_between(user_id, target_id)
    if existing:
        status = str(existing.get("status") or "")
        if status == "accepted":
            raise HTTPException(status_code=400, detail="You are already friends.")
        if int(existing["requester_id"]) == target_id and int(existing["addressee_id"]) == user_id:
            db_execute(
                "UPDATE friendships SET status = 'accepted', updated_at = ? WHERE id = ?",
                (now_iso(), int(existing["id"])),
            )
            return social_overview(session_token)
        raise HTTPException(status_code=400, detail="Friend request already sent.")
    timestamp = now_iso()
    insert_query = (
        "INSERT INTO friendships (requester_id, addressee_id, status, created_at, updated_at) "
        "VALUES (?, ?, 'pending', ?, ?)"
    )
    if USE_POSTGRES:
        insert_query += " RETURNING id"
        db_insert(insert_query, (user_id, target_id, timestamp, timestamp))
    else:
        db_execute(insert_query, (user_id, target_id, timestamp, timestamp))
    return social_overview(session_token)


@app.post("/api/social/requests/{request_id}")
def social_respond_request(
    request_id: int,
    payload: FriendRespondPayload,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    user_id = int(user["id"])
    row = db_fetchone(
        """
        SELECT id
        FROM friendships
        WHERE id = ? AND addressee_id = ? AND status = 'pending'
        """,
        (request_id, user_id),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Friend request not found.")
    if payload.action == "accept":
        db_execute(
            "UPDATE friendships SET status = 'accepted', updated_at = ? WHERE id = ?",
            (now_iso(), request_id),
        )
    else:
        db_execute("DELETE FROM friendships WHERE id = ? AND addressee_id = ?", (request_id, user_id))
    return social_overview(session_token)


@app.delete("/api/social/friends/{friendship_id}")
def social_remove_friend(
    friendship_id: int,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    user_id = int(user["id"])
    db_execute(
        """
        DELETE FROM friendships
        WHERE id = ?
          AND status = 'accepted'
          AND (requester_id = ? OR addressee_id = ?)
        """,
        (friendship_id, user_id, user_id),
    )
    return social_overview(session_token)


@app.post("/api/social/friends/{friendship_id}/cheer")
def social_cheer_friend(
    friendship_id: int,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    user_id = int(user["id"])
    friendship = db_fetchone(
        """
        SELECT requester_id, addressee_id
        FROM friendships
        WHERE id = ?
          AND status = 'accepted'
          AND (requester_id = ? OR addressee_id = ?)
        """,
        (friendship_id, user_id, user_id),
    )
    if not friendship:
        raise HTTPException(status_code=404, detail="Friend not found.")
    receiver_id = int(friendship["addressee_id"]) if int(friendship["requester_id"]) == user_id else int(friendship["requester_id"])
    insert_query = "INSERT INTO social_events (sender_id, receiver_id, event_type, created_at) VALUES (?, ?, 'cheer', ?)"
    if USE_POSTGRES:
        insert_query += " RETURNING id"
        db_insert(insert_query, (user_id, receiver_id, now_iso()))
    else:
        db_execute(insert_query, (user_id, receiver_id, now_iso()))
    return social_overview(session_token)


@app.get("/api/quiz/next")
def quiz_next(
    exclude_word_id: int | None = Query(default=None),
    mode: str = Query(default="saved"),
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    question = build_quiz_question(int(user["id"]), exclude_word_id, mode=mode)
    if not question:
        return {"question": None, "min_words_needed": 4}
    return {"question": {key: value for key, value in question.items() if key != "answer"}}


@app.get("/api/history/{history_id}")
def reading_history_item(
    history_id: int,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    row = db_fetchone(
        """
        SELECT id, title, text, level, topic, content_source, viewed_at
        FROM reading_history
        WHERE id = ? AND user_id = ?
        """,
        (history_id, int(user["id"])),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Reading history item not found.")
    glossary = build_library_glossary(str(row["text"])) if str(row["content_source"]) == "library" else {}
    return {
        "reading": {
            "id": row["id"],
            "title": row["title"],
            "text": row["text"],
            "level": row["level"],
            "topic": row["topic"],
            "content_source": row["content_source"],
            "glossary": glossary,
        }
    }


@app.post("/api/saved-words/clear")
def clear_saved_words(session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    user = require_user(session_token)
    db_execute("DELETE FROM saved_words WHERE user_id = ?", (int(user["id"]),))
    return {"ok": True, "stats": build_user_stats(int(user["id"]))}


@app.get("/api/saved-words")
def list_saved_words(
    mode: str = Query(default="recent"),
    limit: int = Query(default=20, ge=1, le=50),
    exclude_ids: str = Query(default=""),
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    parsed_exclude_ids = [int(piece) for piece in exclude_ids.split(",") if piece.strip().isdigit()]
    return {
        "words": get_recent_words(
            int(user["id"]),
            limit=limit,
            randomize=(mode == "random"),
            exclude_ids=parsed_exclude_ids,
        ),
    }


@app.delete("/api/saved-words/{word_id}")
def delete_saved_word(
    word_id: int,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    db_execute("DELETE FROM saved_words WHERE id = ? AND user_id = ?", (word_id, int(user["id"])))
    return {
        "ok": True,
        "stats": build_user_stats(int(user["id"])),
        "recent_words": get_recent_words(int(user["id"]), limit=20),
    }


@app.post("/api/quiz/check")
def quiz_check(payload: QuizAnswerRequest, session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    user = require_user(session_token)
    row = db_fetchone(
        "SELECT id, word, turkish, context, example FROM saved_words WHERE id = ? AND user_id = ?",
        (payload.word_id, int(user["id"])),
    )
    if not row:
        raise HTTPException(status_code=404, detail=repair_mojibake("Quiz kelimesi bulunamadı."))
    expected_answer = row["word"] if payload.question_type == "blank" else row["turkish"]
    is_correct = payload.answer.strip().lower() == expected_answer.strip().lower()
    db_execute(
        "UPDATE saved_words SET last_result = ?, updated_at = ? WHERE id = ?",
        ("correct" if is_correct else "wrong", now_iso(), row["id"]),
    )
    return {
        "correct": is_correct,
        "answer": expected_answer,
        "word": row["word"],
        "question_type": payload.question_type,
        "context": row["context"],
        "example": row["example"],
        "stats": build_user_stats(int(user["id"])),
    }


@app.post("/api/generate")
def generate(payload: GenerateRequest, session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    keywords = sanitize_keywords(payload.keywords)
    if payload.level not in LEVEL_CONFIG:
        raise HTTPException(status_code=400, detail=repair_mojibake("Geçersiz seviye."))
    if payload.source not in {"library", "ai"}:
        raise HTTPException(status_code=400, detail=repair_mojibake("Geçersiz içerik kaynağı."))
    if payload.source == "ai" and (len(keywords) < 2 or len(keywords) > 12):
        raise HTTPException(status_code=400, detail=repair_mojibake("2 ile 12 arasında anahtar kelime gerekli."))
    if payload.source == "library":
        library_match = pick_library_reading(
            payload.level,
            payload.topic,
            keywords,
            payload.length_target,
            payload.exclude_title,
        )
        if library_match:
            user = optional_user(session_token)
            if user:
                record_reading_history(
                    int(user["id"]),
                    title=str(library_match["title"]),
                    text=str(library_match["text"]),
                    level=payload.level,
                    topic=str(library_match["topic"]),
                    content_source="library",
                )
            return {
                "text": library_match["text"],
                "title": library_match["title"],
                "topic": library_match["topic"],
                "content_source": "library",
                "glossary": build_library_glossary(library_match["text"]),
            }
        raise HTTPException(status_code=404, detail=repair_mojibake("Bu filtreler için library içinde uygun bir metin bulunamadı."))
    prompt = build_text_prompt(payload.level, payload.topic, keywords, payload.length_target)
    try:
        text = request_text(prompt, payload.level, payload.topic, keywords)
        user = optional_user(session_token)
        if user:
            record_reading_history(
                int(user["id"]),
                title="AI Reading",
                text=text,
                level=payload.level,
                topic=payload.topic,
                content_source="ai",
            )
        return {
            "text": text,
            "title": "",
            "topic": payload.topic,
            "content_source": "ai",
            "glossary": {},
        }
    except Exception as exc:
        raise normalize_api_error(exc)


@app.get("/api/library/readings")
def list_library_readings(level: str | None = None, topic: str | None = None) -> dict[str, Any]:
    source_clause, source_params = library_source_filter()
    query = """
        SELECT id, title, level, topic, keywords, word_count, source
        FROM readings
        WHERE is_published = 1
    """
    params: list[Any] = list(source_params)
    if source_clause:
        query += source_clause
    if level:
        query += " AND level = ?"
        params.append(level)
    query += " ORDER BY level, topic, id"
    rows = db_fetchall(query, tuple(params))
    if topic:
        normalized_topic = normalize_library_topic(topic)
        rows = [row for row in rows if normalize_library_topic(str(row["topic"])) == normalized_topic]
    for row in rows:
        row["topic"] = normalize_library_topic(str(row["topic"]))
        row["keywords"] = parse_keywords_field(row["keywords"])
    return {"readings": rows}


@app.get("/api/library/stats")
def library_stats() -> dict[str, Any]:
    source_clause, source_params = library_source_filter()
    total_row = db_fetchone(
        f"SELECT COUNT(*) AS total FROM readings WHERE is_published = 1{source_clause}",
        source_params,
    )
    level_rows = db_fetchall(
        f"""
        SELECT level, COUNT(*) AS total
        FROM readings
        WHERE is_published = 1{source_clause}
        GROUP BY level
        ORDER BY level
        """,
        source_params,
    )
    topic_rows = db_fetchall(
        f"""
        SELECT topic, COUNT(*) AS total
        FROM readings
        WHERE is_published = 1{source_clause}
        GROUP BY topic
        ORDER BY topic
        """,
        source_params,
    )
    level_topic_rows = db_fetchall(
        f"""
        SELECT level, topic, COUNT(*) AS total
        FROM readings
        WHERE is_published = 1{source_clause}
        GROUP BY level, topic
        ORDER BY level, topic
        """,
        source_params,
    )
    by_topic: dict[str, int] = {}
    for row in topic_rows:
        normalized_topic = normalize_library_topic(str(row["topic"]))
        if normalized_topic == "Random":
            continue
        by_topic[normalized_topic] = by_topic.get(normalized_topic, 0) + int(row["total"])
    by_level_topic: dict[tuple[str, str], int] = {}
    for row in level_topic_rows:
        normalized_topic = normalize_library_topic(str(row["topic"]))
        if normalized_topic == "Random":
            continue
        key = (str(row["level"]), normalized_topic)
        by_level_topic[key] = by_level_topic.get(key, 0) + int(row["total"])
    return {
        "total": int((total_row or {}).get("total", 0)),
        "by_level": level_rows,
        "by_topic": [{"topic": topic, "total": total} for topic, total in sorted(by_topic.items())],
        "by_level_topic": [
            {"level": level, "topic": topic, "total": total}
            for (level, topic), total in sorted(by_level_topic.items())
        ],
    }


@app.post("/api/explain")
def explain(payload: ExplainRequest) -> dict[str, str]:
    safe_word = sanitize_word(payload.word)
    if not safe_word:
        raise HTTPException(status_code=400, detail="Geçerli bir kelime gerekli.")
    try:
        return {"explanation": request_manual_explanation(payload.text, safe_word)}
    except Exception as exc:
        raise normalize_api_error(exc)


@app.post("/api/library/fill-missing")
def fill_missing_library_words(payload: FillMissingRequest) -> dict[str, Any]:
    text = str(payload.text or "")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Geçerli bir metin gerekli.")
    max_words = int(payload.max_words or 180)
    tokens = extract_unique_words(text)[:max_words]
    filled = 0
    skipped = 0
    new_entries: dict[str, str] = {}
    for token in tokens:
        if not token or len(token) <= 2:
            skipped += 1
            continue
        if token in WORD_MEANING_OVERRIDES or token in LOCAL_WORD_MAP or token in IRREGULAR_WORD_MAP:
            skipped += 1
            continue
        if any(candidate in LIBRARY_WORD_MAP or candidate in EXTRA_WORD_MAP for candidate in word_root_candidates(token)):
            skipped += 1
            continue
        translated = translate_library_word_with_fallback(token, token)
        if translated and not should_use_local_meaning(token, translated):
            filled += 1
            new_entries[token] = translated
            if len(new_entries) >= 24:
                break
        else:
            skipped += 1
    return {
        "ok": True,
        "filled": filled,
        "skipped": skipped,
        "sample": new_entries,
    }


@app.post("/api/word-detail")
def word_detail(payload: ExplainRequest, session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, Any]:
    safe_word = sanitize_word(payload.word)
    if not safe_word:
        raise HTTPException(status_code=400, detail="Geçerli bir kelime gerekli.")
    try:
        if (payload.content_source or "").lower() == "library":
            detail = build_library_word_detail(payload.text, safe_word)
        else:
            detail = request_word_detail(payload.text, safe_word)
        user = optional_user(session_token)
        if user and detail_is_saveable(safe_word, detail):
            save_word_for_user(int(user["id"]), safe_word, payload.text, detail)
        return detail
    except Exception as exc:
        raise normalize_api_error(exc)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="127.0.0.1", port=8045)
