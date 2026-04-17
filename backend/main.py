import hashlib
import json
import os
import random
import re
import secrets
import smtplib
import sqlite3
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any

import httpx
from fastapi import Cookie, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field
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
DB_PATH = ROOT_DIR / "backend" / "app.db"
EXTRA_WORD_MAP_PATH = ROOT_DIR / "backend" / "extra_word_map.json"
LIBRARY_WORD_MAP_PATH = ROOT_DIR / "backend" / "library_word_map.json"
SESSION_COOKIE = "ets_session"
WORD_DETAIL_CACHE: dict[str, dict[str, str]] = {}
GENERATE_CACHE: dict[str, str] = {}
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
    "Academic": {"min_words": 190, "max_words": 280, "label": "Akademik ve daha analitik"},
}
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
    "theory": "kuram",
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
        "resource": "kaynak",
        "review": "gÃ¶zden geÃ§irmek",
        "role": "rol",
        "science": "bilim",
        "schedule": "program",
        "section": "bÃ¶lÃ¼m",
        "seem": "gÃ¶rÃ¼nmek",
        "sense": "his",
        "service": "hizmet",
        "share": "paylaÅŸmak",
        "shift": "deÄŸiÅŸim",
        "skill": "beceri",
        "social": "sosyal",
        "solution": "Ã§Ã¶zÃ¼m",
        "source": "kaynak",
        "space": "alan",
        "specific": "belirli",
        "sport": "spor",
        "standard": "standart",
        "strategy": "strateji",
        "stress": "stres",
        "subject": "konu",
        "success": "baÅŸarÄ±",
        "support": "destek",
        "system": "sistem",
        "together": "birlikte",
        "topic": "konu",
        "understand": "anlamak",
        "update": "gÃ¼ncelleme",
        "useful": "yararlÄ±",
        "usual": "alÄ±ÅŸÄ±lmÄ±ÅŸ",
        "value": "deÄŸer",
        "visual": "gÃ¶rsel",
        "voice": "ses",
        "week": "hafta",
        "weekend": "hafta sonu",
        "welcome": "hoÅŸ karÅŸÄ±lamak",
        "workflow": "iÅŸ akÄ±ÅŸÄ±",
        "world": "dÃ¼nya",
        "write": "yazmak",
    }
)
LOCAL_WORD_MAP.update(
    {
        "i": "ben",
        "we": "biz",
        "you": "sen",
        "he": "o",
        "she": "o",
        "they": "onlar",
        "it": "o",
        "my": "benim",
        "our": "bizim",
        "your": "senin",
        "his": "onun",
        "her": "onun",
        "their": "onların",
        "me": "beni",
        "us": "bizi",
        "them": "onları",
        "this": "bu",
        "that": "şu",
        "these": "bunlar",
        "those": "şunlar",
        "with": "ile",
        "without": "olmadan",
        "before": "önce",
        "after": "sonra",
        "during": "sırasında",
        "between": "arasında",
        "under": "altında",
        "over": "üzerinde",
        "into": "içine",
        "across": "boyunca",
        "through": "içinden",
        "around": "etrafında",
        "inside": "içinde",
        "outside": "dışında",
        "near": "yakınında",
        "behind": "arkasında",
        "front": "ön",
        "beforehand": "önceden",
        "sit": "oturmak",
        "sits": "oturur",
        "write": "yazmak",
        "writes": "yazar",
        "begin": "başlamak",
        "begins": "başlar",
        "notebook": "not defteri",
        "ability": "yetenek",
        "accept": "kabul etmek",
        "access": "erişim",
        "account": "hesap",
        "achievable": "ulaşılabilir",
        "across": "boyunca",
        "action": "eylem",
        "additional": "ek",
        "administration": "yönetim",
        "adult": "yetişkin",
        "advance": "ilerleme",
        "advantage": "avantaj",
        "agency": "kurum",
        "agenda": "gündem",
        "alarm": "alarm",
        "alternative": "alternatif",
        "ambition": "hırs",
        "annual": "yıllık",
        "application": "uygulama",
        "appointment": "randevu",
        "area": "alan",
        "arrange": "düzenlemek",
        "arrival": "varış",
        "assignment": "ödev",
        "assistant": "asistan",
        "attempt": "girişim",
        "audience": "izleyici",
        "author": "yazar",
        "average": "ortalama",
        "aware": "farkında",
        "background": "arka plan",
        "basic": "temel",
        "behavior": "davranış",
        "believe": "inanmak",
        "belong": "ait olmak",
        "brief": "kısa",
        "budget": "bütçe",
        "building": "bina",
        "business": "iş dünyası",
        "campaign": "kampanya",
        "cancel": "iptal etmek",
        "candidate": "aday",
        "capacity": "kapasite",
        "category": "kategori",
        "celebrate": "kutlamak",
        "central": "merkezi",
        "certain": "belirli",
        "chair": "sandalye",
        "chapter": "bölüm",
        "character": "karakter",
        "chart": "grafik",
        "client": "müşteri",
        "close": "yakın",
        "collect": "toplamak",
        "comment": "yorum",
        "commercial": "ticari",
        "commitment": "bağlılık",
        "compare": "karşılaştırmak",
        "complete": "tamamlamak",
        "complex": "karmaşık",
        "conclusion": "sonuç bölümü",
        "condition": "durum",
        "confirm": "doğrulamak",
        "connect": "bağlamak",
        "connection": "bağlantı",
        "consideration": "değerlendirme",
        "consistent": "tutarlı",
        "construct": "oluşturmak",
        "contact": "iletişim kurmak",
        "content": "içerik",
        "context": "bağlam",
        "contract": "sözleşme",
        "contribute": "katkı sağlamak",
        "contribution": "katkı",
        "convenient": "uygun",
        "cooperate": "iş birliği yapmak",
        "core": "temel",
        "course": "kurs",
        "creative": "yaratıcı",
        "critical": "kritik",
        "customer": "müşteri",
        "daily": "günlük",
        "debate": "tartışma",
        "define": "tanımlamak",
        "degree": "derece",
        "department": "departman",
        "depend": "bağlı olmak",
        "describe": "tanımlamak",
        "develop": "geliştirmek",
        "development": "gelişim",
        "device": "cihaz",
        "direct": "doğrudan",
        "director": "yönetmen",
        "documented": "belgelenmiş",
        "domestic": "yerel",
        "draft": "taslak",
        "duration": "süre",
        "economic": "ekonomik",
        "editor": "editör",
        "elderly": "yaşlı",
        "element": "öğe",
        "emergency": "acil durum",
        "emphasis": "vurgu",
        "employee": "çalışan",
        "employer": "işveren",
        "encourage": "cesaretlendirmek",
        "ensure": "garanti etmek",
        "entire": "tamamı",
        "entry": "giriş",
        "essential": "temel",
        "estate": "mülk",
        "estimate": "tahmin",
        "evaluate": "değerlendirmek",
        "event": "etkinlik",
        "eventually": "sonunda",
        "exact": "tam",
        "exchange": "değişim",
        "executive": "yönetici",
        "exist": "var olmak",
        "expect": "beklemek",
        "expense": "gider",
        "expert": "uzman",
        "exposure": "maruz kalma",
        "external": "harici",
        "facility": "tesis",
        "factor": "etken",
        "failure": "başarısızlık",
        "familiar": "tanıdık",
        "file": "dosya",
        "finance": "finans",
        "finding": "bulgu",
        "firm": "şirket",
        "flight": "uçuş",
        "formal": "resmi",
        "framework": "çerçeve",
        "frequent": "sık",
        "function": "işlev",
        "fund": "fon",
        "further": "daha ileri",
        "generate": "üretmek",
        "global": "küresel",
        "guidance": "rehberlik",
        "handle": "ele almak",
        "housing": "barınma",
        "identify": "belirlemek",
        "impact": "etki",
        "impression": "izlenim",
        "impressive": "etkileyici",
        "improvement": "iyileşme",
        "income": "gelir",
        "industry": "sektör",
        "influence": "etkilemek",
        "initial": "ilk",
        "instance": "örnek durum",
        "instruction": "talimat",
        "instrument": "araç",
        "intention": "niyet",
        "interaction": "etkileşim",
        "internal": "iç",
        "issue": "mesele",
        "item": "öğe",
        "journal": "dergi",
        "judge": "yargılamak",
        "key": "anahtar",
        "landscape": "manzara",
        "language": "dil",
        "largely": "büyük ölçüde",
        "leading": "öncü",
        "legal": "yasal",
        "lesson": "ders",
        "limited": "sınırlı",
        "location": "konum",
        "logic": "mantık",
        "mainly": "çoğunlukla",
        "maintain": "sürdürmek",
        "major": "büyük",
        "manual": "manuel",
        "margin": "marj",
        "master": "ustalaşmak",
        "match": "eşleşmek",
        "meanwhile": "bu arada",
        "media": "medya",
        "medical": "tıbbi",
        "memory": "hafıza",
        "message": "mesaj",
        "movement": "hareket",
        "nearly": "neredeyse",
        "negative": "olumsuz",
        "normal": "normal",
        "objective": "amaç",
        "obvious": "açık",
        "occasion": "fırsat",
        "operate": "işletmek",
        "operation": "operasyon",
        "option": "seçenek",
        "ordinary": "sıradan",
        "original": "orijinal",
        "overall": "genel olarak",
        "participant": "katılımcı",
        "particular": "belirli",
        "passage": "parça metin",
        "payment": "ödeme",
        "peaceful": "huzurlu",
        "period": "dönem",
        "perspective": "bakış açısı",
        "persuade": "ikna etmek",
        "platform": "platform",
        "policy": "politika",
        "population": "nüfus",
        "position": "pozisyon",
        "potential": "potansiyel",
        "practical": "pratik",
        "predict": "tahmin etmek",
        "prefer": "tercih etmek",
        "primary": "birincil",
        "principle": "ilke",
        "professional": "profesyonel",
        "progress": "ilerleme",
        "property": "özellik",
        "proposal": "öneri",
        "protect": "korumak",
        "public": "kamusal",
        "publish": "yayınlamak",
        "quality": "kalite",
        "range": "aralık",
        "rapid": "hızlı",
        "reader": "okur",
        "reference": "referans",
        "region": "bölge",
        "relevant": "ilgili",
        "rely": "güvenmek",
        "remove": "kaldırmak",
        "replace": "değiştirmek",
        "report": "rapor",
        "represent": "temsil etmek",
        "require": "gerektirmek",
        "response": "yanıt",
        "responsibility": "sorumluluk",
        "responsible": "sorumlu",
        "retain": "korumak",
        "return": "geri dönmek",
        "route": "rota",
        "safety": "güvenlik",
        "sample": "örnek",
        "screen": "ekran",
        "search": "arama",
        "secure": "güvenli",
        "select": "seçmek",
        "senior": "kıdemli",
        "separate": "ayrı",
        "series": "dizi",
        "settle": "yerleşmek",
        "significant": "önemli",
        "similar": "benzer",
        "society": "toplum",
        "software": "yazılım",
        "solve": "çözmek",
        "speaker": "konuşmacı",
        "special": "özel",
        "staff": "personel",
        "statement": "ifade",
        "store": "saklamak",
        "structure": "yapı",
        "style": "stil",
        "sudden": "ani",
        "supply": "sağlamak",
        "surface": "yüzey",
        "survey": "anket",
        "target": "hedef",
        "technical": "teknik",
        "technology": "teknoloji",
        "temporary": "geçici",
        "text": "metin",
        "theme": "tema",
        "therefore": "bu nedenle",
        "tool": "araç",
        "training": "eğitim",
        "transport": "ulaşım",
        "trend": "eğilim",
        "use": "kullanmak",
        "version": "sürüm",
        "view": "görüş",
        "village": "köy",
        "warning": "uyarı",
        "waste": "israf etmek",
        "window": "pencere",
        "worker": "çalışan",
        "youth": "gençlik",
    }
)
LOCAL_PHRASE_MAP = {
    "work life": "iÅŸ hayatÄ±",
    "daily life": "gÃ¼nlÃ¼k hayat",
    "saved words": "kayÄ±tlÄ± kelimeler",
    "quick review": "hÄ±zlÄ± tekrar",
    "word history": "kelime geÃ§miÅŸi",
    "reading stage": "okuma alanÄ±",
    "reading setup": "okuma ayarlarÄ±",
}
IRREGULAR_WORD_MAP = {
    "felt": "hissetmek",
    "made": "yapmak",
    "meant": "anlamÄ±na gelmek",
    "found": "bulmak",
    "thought": "dÃ¼ÅŸÃ¼nmek",
    "brought": "getirmek",
    "caught": "yakalamak",
    "built": "inÅŸa etmek",
    "left": "ayrÄ±lmak",
    "spent": "harcamak",
    "kept": "sÃ¼rdÃ¼rmek",
    "grew": "bÃ¼yÃ¼mek",
    "known": "bilinmek",
    "shown": "gÃ¶stermek",
    "taken": "almak",
    "written": "yazmak",
    "chosen": "seÃ§mek",
    "spoken": "konuÅŸmak",
    "driven": "sÃ¼rmek",
    "cluttered": "karÄ±ÅŸÄ±k",
    "interpreted": "yorumlanmÄ±ÅŸ",
    "narrow": "dar",
}
WORD_MEANING_OVERRIDES = {
    "simplified": "sadeleÅŸtirilmiÅŸ",
    "irritated": "sinirli",
    "misguided": "yanlÄ±ÅŸ yÃ¶nlendirilmiÅŸ",
    "disciplined": "disiplinli",
    "blurred": "bulanÄ±k",
    "unsupported": "desteklenmeyen",
    "wanted": "istenen",
    "needed": "gerekli",
    "looked": "gÃ¶rÃ¼ndÃ¼",
    "unfocused": "odaksÄ±z",
    "unresolved": "Ã§Ã¶zÃ¼lmemiÅŸ",
}
if EXTRA_WORD_MAP_PATH.exists():
    try:
        EXTRA_WORD_MAP: dict[str, str] = json.loads(EXTRA_WORD_MAP_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        EXTRA_WORD_MAP = {}
else:
    EXTRA_WORD_MAP = {}
if LIBRARY_WORD_MAP_PATH.exists():
    try:
        LIBRARY_WORD_MAP: dict[str, str] = json.loads(LIBRARY_WORD_MAP_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        LIBRARY_WORD_MAP = {}
else:
    LIBRARY_WORD_MAP = {}
TOPIC_SENTENCE_BANK = {
    "Serbest": [
        "The day starts quietly, but it soon becomes full of small decisions and new plans.",
        "There is always a balance between routine, personal goals, and unexpected moments.",
        "People often move through the day by solving simple problems and adjusting their plans.",
        "By the evening, even an ordinary day can feel meaningful when it includes progress and connection.",
    ],
    "GÃ¼nlÃ¼k Hayat": [
        "Most days begin with simple habits like breakfast, getting ready, and checking the time.",
        "Daily life feels smoother when familiar routines create a sense of comfort and rhythm.",
        "Small moments, such as talking to someone or taking a short walk, can change the mood of the day.",
        "Even when nothing dramatic happens, ordinary life can still feel full and satisfying.",
    ],
    "Okul": [
        "School life often mixes responsibility, curiosity, and the pressure to stay organized.",
        "Students move between lessons, assignments, and conversations with classmates throughout the day.",
        "A good class can make difficult ideas feel more manageable and interesting.",
        "By the end of the day, school is not only about grades but also about growth and routine.",
    ],
    "Seyahat": [
        "Travel usually brings a mix of excitement, planning, and small surprises.",
        "Moving through a new place makes people notice different sounds, habits, and rhythms.",
        "Even a short trip can create strong memories through simple details and unexpected encounters.",
        "The best part of travel is often the feeling of discovery that stays with you afterwards.",
    ],
    "Ä°ÅŸ HayatÄ±": [
        "Work life is often shaped by planning, communication, and the need to stay flexible.",
        "A normal day can include meetings, messages, and moments that require quick decisions.",
        "Professional life becomes easier when people know how to organize their time and energy.",
        "Even busy schedules feel more manageable when there is a clear goal and steady teamwork.",
    ],
    "Akademik": [
        "Academic work often begins with a question, a method, and a clear reason for exploring the topic.",
        "A careful reading process helps students connect evidence, ideas, and interpretation.",
        "Strong academic writing balances clarity with detail, so each sentence supports the central claim.",
        "In the end, the value of academic practice comes from thoughtful analysis and precise communication.",
    ],
}
TOPIC_SCENARIOS = {
    "Serbest": ["a personal routine", "a small decision", "an ordinary day with meaningful details"],
    "GÃ¼nlÃ¼k Hayat": ["a simple day at home", "a walk through the neighborhood", "a relaxed plan with a friend"],
    "Okul": ["preparing for class", "finishing an assignment", "talking with classmates after a lesson"],
    "Seyahat": ["arriving in a new city", "preparing for a short trip", "moving through an airport or station"],
    "Ä°ÅŸ HayatÄ±": ["handling a busy workday", "preparing for an important meeting", "balancing deadlines and communication"],
    "Akademik": ["preparing a research summary", "analyzing an article for class", "connecting evidence to an academic argument"],
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
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "").strip()
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "").strip()
SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "587").strip() or "587")
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "").strip()
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME).strip()
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").strip().lower() != "false"


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


class AuthRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6, max_length=72)


class ResendVerificationRequest(BaseModel):
    email: str = Field(min_length=5, max_length=120)


class QuizAnswerRequest(BaseModel):
    word_id: int
    answer: str
    question_type: str = "meaning"


def build_http_client() -> httpx.Client:
    return httpx.Client(timeout=90.0, trust_env=False)


def build_openai_compatible_client(base_url: str, api_key: str) -> OpenAI:
    return OpenAI(base_url=base_url, api_key=api_key, http_client=build_http_client())


def _pg_query(query: str) -> str:
    return query.replace("?", "%s")


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
        return int(row["id"])
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.execute(query, params)
        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()


def seed_readings() -> None:
    existing_rows = db_fetchall("SELECT id, title, source FROM readings")
    existing_by_title = {str(row["title"]): row for row in existing_rows}
    seed_titles = {item["title"] for item in READING_SEEDS}

    for row in existing_rows:
        if str(row.get("source")) == "manual" and str(row["title"]) not in seed_titles:
            db_execute("DELETE FROM readings WHERE id = ?", (row["id"],))

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
        existing = existing_by_title.get(item["title"])
        if existing:
            db_execute(
                """
                UPDATE readings
                SET title = ?, text = ?, level = ?, topic = ?, keywords = ?,
                    word_count = ?, source = ?, is_published = ?
                WHERE id = ?
                """,
                payload + (existing["id"],),
            )
            continue

        insert_query = (
            "INSERT INTO readings (title, text, level, topic, keywords, word_count, source, is_published) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        if USE_POSTGRES:
            insert_query += " RETURNING id"
        db_insert(insert_query, payload)


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
seed_readings()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


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
    subject = "Verify your English Text Studio account"
    text_body = (
        "Welcome to English Text Studio.\n\n"
        f"Verify your email by opening this link:\n{verify_url}\n\n"
        "This link expires in 24 hours."
    )
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #183153;">
        <h2>Verify your English Text Studio account</h2>
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
        raise HTTPException(status_code=401, detail="Ã–nce giriÅŸ yapmalÄ±sÄ±n.")
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
        secure=False,
        max_age=60 * 60 * 24 * 30,
    )
    return token


def clear_session(response: Response, session_token: str | None) -> None:
    if session_token:
        db_execute("DELETE FROM sessions WHERE token = ?", (session_token,))
    response.delete_cookie(SESSION_COOKIE)


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
    return {
        "saved_words": int(row["saved_words"] or 0),
        "mastered_words": int(row["mastered_words"] or 0),
    }


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
    if "alÄ±namadÄ±" in lowered or "bulunamadÄ±" in lowered:
        return False
    if lowered == word.strip().lower():
        return False
    return True


def classify_turkish_meaning(value: str) -> str:
    lowered = value.strip().lower()
    if lowered.endswith(("mek", "mak")):
        return "verb"
    if lowered.endswith(("yor", "?yor", "iyor", "uyor", "?yor", "ilir", "?l?r", "ulur", "?l?r", "lan?r", "lenir")):
        return "verb"
    if lowered.endswith(("li", "l?", "lu", "l?", "siz", "s?z", "suz", "s?z", "sel", "sal")):
        return "adjective"
    if lowered.endswith(("ik", "?k", "uk", "?k")):
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
        if any(mark in candidate for mark in ["al?namad?", "bulunamad?", "not available"]):
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


def build_quiz_question(user_id: int, exclude_word_id: int | None = None) -> dict[str, Any] | None:
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
    target = sorted(
        words,
        key=lambda row: (row["last_result"] == "correct", row["click_count"], row["id"]),
    )[0]
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


def sanitize_word(word: str) -> str:
    return re.sub(r"[^A-Za-z -]", "", word).strip()


def parse_keywords_field(value: str) -> list[str]:
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in value.split(",") if item.strip()]


def pick_library_reading(
    level: str,
    topic: str,
    keywords: list[str],
    length_target: int,
    exclude_title: str | None = None,
) -> dict[str, Any] | None:
    normalized_topic = normalize_topic(topic)
    rows = db_fetchall(
        """
        SELECT id, title, text, level, topic, keywords, word_count, source
        FROM readings
        WHERE is_published = 1 AND level = ?
        ORDER BY id
        """,
        (level,),
    )
    if not rows:
        return None
    filtered_rows = rows
    if normalized_topic not in {"Open", "Serbest", "Random"}:
        exact_topic_rows = [row for row in filtered_rows if row["topic"] == normalized_topic]
        if exact_topic_rows:
            filtered_rows = exact_topic_rows
    if exclude_title:
        alternate_rows = [row for row in filtered_rows if str(row["title"]) != exclude_title]
        if alternate_rows:
            filtered_rows = alternate_rows
    if not filtered_rows:
        filtered_rows = rows
    scored: list[tuple[int, dict[str, Any]]] = []
    for row in filtered_rows:
        length_score = abs(int(row["word_count"]) - int(length_target))
        scored.append((length_score, row))
    scored.sort(key=lambda item: (item[0], item[1]["id"]))
    candidate_pool = [row for _score, row in scored[: min(24, len(scored))]]
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
    if not any(token in value for token in suspicious):
        return value
    for source_encoding in ("latin1", "cp1252"):
        try:
            repaired = value.encode(source_encoding).decode("utf-8")
            if repaired:
                return repaired
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return value


def is_suspicious_meaning(source_word: str, candidate: str) -> bool:
    cleaned = repair_mojibake(candidate).strip().lower()
    source = source_word.strip().lower()
    if not cleaned:
        return True
    if cleaned == source or cleaned.startswith(source + " "):
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
    if lowered in WORD_MEANING_OVERRIDES:
        return repair_mojibake(WORD_MEANING_OVERRIDES[lowered])
    if lowered in LOCAL_WORD_MAP:
        return repair_mojibake(LOCAL_WORD_MAP[lowered])
    if lowered in IRREGULAR_WORD_MAP:
        return repair_mojibake(IRREGULAR_WORD_MAP[lowered])
    if lowered in EXTRA_WORD_MAP:
        return repair_mojibake(EXTRA_WORD_MAP[lowered])
    return None


def infer_turkish_meaning(word: str) -> str:
    lowered = word.lower().strip()
    if lowered in LOCAL_PHRASE_MAP:
        return repair_mojibake(LOCAL_PHRASE_MAP[lowered])
    direct = lookup_word_map_value(lowered)
    if direct:
        return direct
    if lowered.endswith("ies") and len(lowered) > 4:
        singular = lowered[:-3] + "y"
        resolved = lookup_word_map_value(singular)
        if resolved:
            return resolved
    if lowered.endswith("es") and len(lowered) > 3:
        singular = lowered[:-2]
        resolved = lookup_word_map_value(singular)
        if resolved:
            return resolved
    if lowered.endswith("s") and len(lowered) > 3:
        singular = lowered[:-1]
        resolved = lookup_word_map_value(singular)
        if resolved:
            return resolved
    if lowered.endswith("ing") and len(lowered) > 4:
        stem = lowered[:-3]
        for candidate in [stem, stem + "e", stem[:-1] if len(stem) > 2 and stem[-1] == stem[-2] else ""]:
            if not candidate:
                continue
            resolved = lookup_word_map_value(candidate)
            if resolved:
                return resolved
        return f"{stem} yapmak"
    if lowered.endswith("ed") and len(lowered) > 3:
        stem = lowered[:-2]
        candidate_roots = [stem, stem + "e"]
        if stem.endswith("i"):
            candidate_roots.append(stem[:-1] + "y")
        if len(stem) > 2 and stem[-1] == stem[-2]:
            candidate_roots.append(stem[:-1])
        for candidate in candidate_roots:
            if not candidate:
                continue
            resolved = lookup_word_map_value(candidate)
            if resolved:
                return resolved
        return stem
    if lowered.endswith("ly") and len(lowered) > 4:
        root = lowered[:-2]
        if root in LOCAL_WORD_MAP:
            return repair_mojibake(f"{LOCAL_WORD_MAP[root]} bir ÅŸekilde")
        if root in EXTRA_WORD_MAP:
            return repair_mojibake(f"{EXTRA_WORD_MAP[root]} bir ÅŸekilde")
    return lowered


def infer_contextual_library_meaning(word: str, sentence: str) -> str:
    lowered_word = word.lower().strip()
    compact_sentence = re.sub(r"\s+", " ", sentence).strip().lower()
    if lowered_word.startswith("treat") and " as " in compact_sentence:
        return "ele almak"
    if lowered_word in {"illustrates", "illustrated", "illustrating"}:
        return "örnekleyerek göstermek"
    if lowered_word in {"simplified", "simplifies", "simplifying"}:
        return "sadeleştirmek"
    return infer_turkish_meaning(word)


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


def build_local_word_detail(text: str, word: str) -> dict[str, str]:
    if word.lower() in LIBRARY_WORD_MAP:
        return build_library_word_detail(text, word)
    meaning = infer_turkish_meaning(word)
    sentence = find_sentence_for_word(text, word)
    context = repair_mojibake(f'"{word}" burada bÃ¼yÃ¼k olasÄ±lÄ±kla "{meaning}" anlamÄ±nda kullanÄ±lÄ±yor.')
    example = f"The word {word} appears in this reading text."
    if sentence:
        compact_sentence = re.sub(r"\s+", " ", sentence).strip()
        context = repair_mojibake(
            f'Bu metinde "{word}" kelimesi "{meaning}" fikrini veriyor. GeÃ§tiÄŸi bÃ¶lÃ¼m: {compact_sentence}'
        )
        example = compact_sentence
    return {"turkish": meaning, "context": context, "example": example}


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
        raise HTTPException(status_code=500, detail="GOOGLE_TRANSLATE_API_KEY bulunamadÄ±.")
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
    root = lowered
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


def build_library_word_detail(text: str, word: str) -> dict[str, str]:
    lowered_word = word.lower()
    raw_library_meaning = repair_mojibake(str(LIBRARY_WORD_MAP.get(lowered_word, "")))
    sentence = find_sentence_for_word(text, word)
    library_meaning = infer_contextual_library_meaning(word, sentence) if is_suspicious_meaning(word, raw_library_meaning) else raw_library_meaning
    if not library_meaning:
        library_meaning = infer_contextual_library_meaning(word, sentence)
    compact_sentence = re.sub(r"\s+", " ", sentence).strip() if sentence else ""
    translated_sentence = ""
    if compact_sentence and GOOGLE_TRANSLATE_API_KEY:
        try:
            translated_sentence = translate_text_google(compact_sentence, target_language="tr", source_language="en")
        except Exception:
            translated_sentence = ""
    form_info = describe_word_form(lowered_word)
    context_lines = [
        f'Bu metindeki karşılığı: "{library_meaning}"',
        f'Kök: {form_info["root"]}',
        f'Çekim / biçim: {form_info["note"]}',
    ]
    if compact_sentence:
        context_lines.append(f"Geçtiği bölüm: {compact_sentence}")
    if translated_sentence:
        context_lines.append(f"Yaklaşık Türkçesi: {translated_sentence}")
    example_sentences = gather_library_examples(lowered_word, compact_sentence)
    example_lines = [f"{index}. {sentence}" for index, sentence in enumerate(example_sentences, start=1)]
    if not example_lines:
        example_lines = [f"1. The word {word} appears in this reading text."]
    return {
        "turkish": repair_mojibake(library_meaning),
        "context": repair_mojibake("\n".join(context_lines)),
        "example": repair_mojibake("\n".join(example_lines)),
    }


def build_library_glossary(text: str) -> dict[str, dict[str, str]]:
    glossary: dict[str, dict[str, str]] = {}
    for word in extract_unique_words(text):
        glossary[word] = build_library_word_detail(text, word)
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
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY bulunamadÄ±.")
        return
    if MODEL_PROVIDER == "hf":
        if not HF_TOKEN:
            raise HTTPException(status_code=500, detail="HF_TOKEN bulunamadÄ±.")
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
        raise RuntimeError("Gemini boÅŸ yanÄ±t dÃ¶ndÃ¼.")
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
        raise RuntimeError("HF Router boÅŸ yanÄ±t dÃ¶ndÃ¼.")
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
            return HTTPException(status_code=401, detail="HF token geÃ§ersiz veya yetkisiz.")
        return HTTPException(status_code=401, detail="Gemini API key geÃ§ersiz veya yetkisiz.")
    if "429" in lowered or "quota" in lowered or "rate limit" in lowered:
        if MODEL_PROVIDER == "hf":
            return HTTPException(status_code=429, detail="HF Ã¼cretsiz limitine ulaÅŸÄ±ldÄ±.")
        return HTTPException(status_code=429, detail="Gemini free tier limiti aÅŸÄ±ldÄ±.")
    if "403" in lowered:
        return HTTPException(status_code=403, detail="SeÃ§ili saÄŸlayÄ±cÄ± bu isteÄŸe izin vermedi.")
    if "404" in lowered:
        return HTTPException(status_code=404, detail="SeÃ§ili model bulunamadÄ±.")
    if "503" in lowered or "connection" in lowered or "timed out" in lowered:
        if MODEL_PROVIDER == "hf":
            return HTTPException(status_code=503, detail="HF Router servisine ÅŸu anda ulaÅŸÄ±lamÄ±yor.")
        return HTTPException(status_code=503, detail="Gemini servisine ÅŸu anda ulaÅŸÄ±lamÄ±yor.")
    return HTTPException(status_code=500, detail=raw)


app = FastAPI(title="English Text Studio")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    password_hash = hash_password(payload.password)
    row = db_fetchone(
        "SELECT id, username, created_at, is_active FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash),
    )
    if not row:
        raise HTTPException(status_code=401, detail="Username or password is incorrect.")
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
    <p><a href="{APP_BASE_URL}" style="display:inline-block;padding:12px 18px;border-radius:999px;background:#58cc02;color:#0f2c49;text-decoration:none;font-weight:700;">Open English Text Studio</a></p>
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
        return {"user": None, "stats": {"saved_words": 0, "mastered_words": 0}, "recent_words": []}
    return {
        "user": user,
        "stats": build_user_stats(int(user["id"])),
        "recent_words": get_recent_words(int(user["id"])),
    }


@app.get("/api/quiz/next")
def quiz_next(
    exclude_word_id: int | None = Query(default=None),
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> dict[str, Any]:
    user = require_user(session_token)
    question = build_quiz_question(int(user["id"]), exclude_word_id)
    if not question:
        return {"question": None, "min_words_needed": 4}
    return {"question": {key: value for key, value in question.items() if key != "answer"}}


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
        raise HTTPException(status_code=404, detail="Quiz kelimesi bulunamadÄ±.")
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
def generate(payload: GenerateRequest) -> dict[str, Any]:
    keywords = sanitize_keywords(payload.keywords)
    if payload.level not in LEVEL_CONFIG:
        raise HTTPException(status_code=400, detail="GeÃ§ersiz seviye.")
    if payload.source not in {"library", "ai"}:
        raise HTTPException(status_code=400, detail="GeÃ§ersiz iÃ§erik kaynaÄŸÄ±.")
    if payload.source == "ai" and (len(keywords) < 2 or len(keywords) > 12):
        raise HTTPException(status_code=400, detail="2 ile 12 arasÄ±nda anahtar kelime gerekli.")
    if payload.source == "library":
        library_match = pick_library_reading(
            payload.level,
            payload.topic,
            keywords,
            payload.length_target,
            payload.exclude_title,
        )
        if library_match:
            return {
                "text": library_match["text"],
                "title": library_match["title"],
                "topic": library_match["topic"],
                "content_source": "library",
                "glossary": build_library_glossary(library_match["text"]),
            }
        raise HTTPException(status_code=404, detail="Bu filtreler iÃ§in library iÃ§inde uygun bir metin bulunamadÄ±.")
    prompt = build_text_prompt(payload.level, payload.topic, keywords, payload.length_target)
    try:
        return {
            "text": request_text(prompt, payload.level, payload.topic, keywords),
            "title": "",
            "topic": payload.topic,
            "content_source": "ai",
            "glossary": {},
        }
    except Exception as exc:
        raise normalize_api_error(exc)


@app.get("/api/library/readings")
def list_library_readings(level: str | None = None, topic: str | None = None) -> dict[str, Any]:
    query = """
        SELECT id, title, level, topic, keywords, word_count, source
        FROM readings
        WHERE is_published = 1
    """
    params: list[Any] = []
    if level:
        query += " AND level = ?"
        params.append(level)
    if topic:
        query += " AND topic = ?"
        params.append(normalize_topic(topic))
    query += " ORDER BY level, topic, id"
    rows = db_fetchall(query, tuple(params))
    for row in rows:
        row["keywords"] = parse_keywords_field(row["keywords"])
    return {"readings": rows}


@app.get("/api/library/stats")
def library_stats() -> dict[str, Any]:
    total_row = db_fetchone("SELECT COUNT(*) AS total FROM readings WHERE is_published = 1")
    level_rows = db_fetchall(
        """
        SELECT level, COUNT(*) AS total
        FROM readings
        WHERE is_published = 1
        GROUP BY level
        ORDER BY level
        """
    )
    topic_rows = db_fetchall(
        """
        SELECT topic, COUNT(*) AS total
        FROM readings
        WHERE is_published = 1
        GROUP BY topic
        ORDER BY topic
        """
    )
    return {
        "total": int((total_row or {}).get("total", 0)),
        "by_level": level_rows,
        "by_topic": topic_rows,
    }


@app.post("/api/explain")
def explain(payload: ExplainRequest) -> dict[str, str]:
    safe_word = sanitize_word(payload.word)
    if not safe_word:
        raise HTTPException(status_code=400, detail="GeÃ§erli bir kelime gerekli.")
    try:
        return {"explanation": request_manual_explanation(payload.text, safe_word)}
    except Exception as exc:
        raise normalize_api_error(exc)


@app.post("/api/word-detail")
def word_detail(payload: ExplainRequest, session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE)) -> dict[str, str]:
    safe_word = sanitize_word(payload.word)
    if not safe_word:
        raise HTTPException(status_code=400, detail="GeÃ§erli bir kelime gerekli.")
    try:
        if (payload.content_source or "").lower() == "library":
            detail = build_local_word_detail(payload.text, safe_word)
        else:
            detail = request_word_detail(payload.text, safe_word)
        user = optional_user(session_token)
        if user and detail_is_saveable(safe_word, detail):
            save_word_for_user(int(user["id"]), safe_word, payload.text, detail)
        return detail
    except Exception as exc:
        raise normalize_api_error(exc)

