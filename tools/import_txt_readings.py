from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TXT_DIR = Path(r"C:\Users\PC\Desktop\txt")
CURATED_PATH = ROOT / "backend" / "curated_readings.txt"
LIBRARY_MAP_PATH = ROOT / "backend" / "library_word_map.json"


BAD_CHARS = ("Ã", "Å", "Ä", "â", "�")
SMART_PUNCT = {
    "’": "'",
    "‘": "'",
    "“": '"',
    "”": '"',
    "—": " - ",
    "–": " - ",
    "\u00a0": " ",
}


TOPIC_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Science", ("genetic", "biotechnology", "crispr", "embryo", "genomic", "scientific", "biology")),
    ("Technology", ("artificial intelligence", "algorithm", "digital", "automation", "smartphone", "platform", "surveillance", "data")),
    ("Environment", ("climate", "geoengineering", "ecological", "biodiversity", "degrowth", "ecosystem", "sustainable")),
    ("Health", ("health", "mental", "psychological", "exercise", "medicine", "healthcare", "burnout")),
    ("Education", ("school", "academic", "university", "student", "teacher", "learning", "education")),
    ("Work Life", ("work", "labor", "gig economy", "employment", "productivity", "career", "office")),
    ("Finance", ("consumer", "capitalist", "economic", "market", "income", "capital", "ubi", "meritocracy")),
    ("Culture", ("language", "linguistic", "culture", "architecture", "brutalist", "journalism", "tolerance", "society")),
    ("Communication", ("communication", "relationship", "friend", "family", "social", "conversation")),
    ("Travel", ("travel", "holiday", "city", "airport", "tourism", "journey")),
    ("Food", ("food", "meal", "cooking", "restaurant", "shopping", "supermarket")),
]

MANUAL_COMPLETIONS = {
    "after-hours": "mesai sonrası",
    "backward-looking": "geçmişe dönük",
    "bio-containment": "biyolojik muhafaza / biyogüvenlik kontrolü",
    "break up": "ayrılmak / parçalanmak",
    "carbon-based": "karbon temelli",
    "climate-induced": "iklim kaynaklı",
    "come up with": "aklına getirmek / üretmek",
    "counter-terrorism": "terörle mücadele",
    "cringe-inducing": "utanç verici / rahatsız edici",
    "double-parking": "çift sıra park etme",
    "drop-offs": "bırakma noktaları / düşüşler",
    "drought-stricken": "kuraklıktan etkilenen",
    "dual-use": "çift kullanımlı",
    "fact-checkers": "doğrulama uzmanları",
    "factory-made": "fabrikada üretilmiş",
    "figure out": "çözmek / anlamak",
    "five-star": "beş yıldızlı",
    "forward-looking": "ileriye dönük",
    "get along": "iyi geçinmek",
    "god-like": "tanrısal",
    "give up": "vazgeçmek",
    "human-centric": "insan odaklı",
    "human-created": "insan yapımı",
    "hyper-connectivity": "aşırı bağlantılılık",
    "hyper-density": "aşırı yoğunluk",
    "hyper-fast": "aşırı hızlı",
    "hyper-specialization": "aşırı uzmanlaşma",
    "hyper-stimulation": "aşırı uyarılma",
    "ill-equipped": "yetersiz donanımlı",
    "jean-paul": "özel isim",
    "law-abiding": "yasalara uyan",
    "life-saving": "hayat kurtaran",
    "long-lasting": "uzun süreli",
    "look after": "ilgilenmek / bakmak",
    "low-grade": "düşük düzeyli",
    "machine-made": "makine yapımı",
    "mass-produced": "seri üretilmiş",
    "means-testing": "gelir testi",
    "micro-entertainment": "mikro eğlence",
    "much-needed": "çok ihtiyaç duyulan",
    "multi-day": "birkaç gün süren",
    "non-consensual": "rıza dışı",
    "non-fiction": "kurgu dışı",
    "non-profit": "kâr amacı gütmeyen",
    "o'clock": "saat",
    "one-star": "tek yıldızlı",
    "paradigm-shifting": "paradigma değiştiren",
    "paragraph-length": "paragraf uzunluğunda",
    "peer-reviewed": "hakemli",
    "platform-based": "platform tabanlı",
    "post-ironic": "post-ironik",
    "post-irony": "post-ironi",
    "pre-existing": "önceden var olan",
    "problem-solving": "problem çözme",
    "re-enter": "yeniden girmek",
    "re-evaluate": "yeniden değerlendirmek",
    "real-time": "gerçek zamanlı",
    "ride-hail": "araç çağırma hizmeti",
    "ride-hailing": "araç çağırma hizmeti",
    "ride-sharing": "yolculuk paylaşımı",
    "risk-taking": "risk alma",
    "run into": "karşılaşmak",
    "sapir-whorf": "Sapir-Whorf hipotezi",
    "self-actualization": "kendini gerçekleştirme",
    "self-aware": "öz farkındalığı olan",
    "self-driving": "sürücüsüz",
    "self-help": "kişisel gelişim",
    "self-reflection": "öz değerlendirme",
    "self-regulate": "kendini düzenlemek",
    "short-circuiting": "kısa devreye uğratma",
    "silicon-based": "silikon temelli",
    "socio-political": "sosyo-politik",
    "sub-disciplines": "alt disiplinler",
    "t-shirts": "tişörtler",
    "take off": "havalanmak / hızla yükselmek",
    "take-make-dispose": "al-yap-at modeli",
    "techno-utopian": "tekno-ütopyacı",
    "tree-lined": "ağaçlıklı",
    "turn out": "sonuçlanmak / ortaya çıkmak",
    "truth-seeking": "hakikat arayışı",
    "twenty-first": "yirmi birinci",
    "twenty-five-minute": "yirmi beş dakikalık",
    "twenty-two": "yirmi iki",
    "two-factor": "iki faktörlü",
    "vaccine-resistant": "aşıya dirençli",
    "voice-to-text": "sesten metne",
    "well-functioning": "iyi işleyen",
    "well-rested": "dinlenmiş",
}

MANUAL_COMPLETIONS.update(
    {
        "about": "hakk\u0131nda",
        "because": "\u00e7\u00fcnk\u00fc",
        "before": "\u00f6nce",
        "between": "aras\u0131nda",
        "by": "taraf\u0131ndan / ile",
        "cross-functional": "fonksiyonlar aras\u0131",
        "current-affairs": "g\u00fcncel olaylar",
        "did": "yapt\u0131",
        "down": "a\u015fa\u011f\u0131",
        "during": "s\u0131ras\u0131nda",
        "errands": "i\u015fler / ufak i\u015fler",
        "for": "i\u00e7in",
        "how": "nas\u0131l",
        "in": "i\u00e7inde",
        "inside": "i\u00e7inde",
        "keep": "s\u00fcrd\u00fcrmek / tutmak",
        "late-stage": "ge\u00e7 a\u015fama",
        "living-room": "oturma odas\u0131",
        "many": "bir\u00e7ok",
        "most": "en \u00e7ok",
        "much": "\u00e7ok",
        "need": "ihtiya\u00e7 duymak",
        "needs": "ihtiya\u00e7 duyar",
        "no": "hay\u0131r / yok",
        "not": "de\u011fil",
        "note": "not / kay\u0131t",
        "on": "\u00fczerinde",
        "outside": "d\u0131\u015f\u0131nda",
        "over": "\u00fczerinde",
        "than": "-den / k\u0131yasla",
        "the": "belirli tan\u0131ml\u0131k",
        "under": "alt\u0131nda",
        "when": "-d\u0131\u011f\u0131 zaman",
    }
)


def score_badness(value: str) -> int:
    return sum(value.count(ch) for ch in BAD_CHARS)


def repair_text(value: str) -> str:
    if not value:
        return value
    candidates = [value]
    for encoding in ("cp1252", "latin1"):
        try:
            candidates.append(value.encode(encoding, errors="strict").decode("utf-8", errors="strict"))
        except Exception:
            pass
    best = min(candidates, key=lambda item: (score_badness(item), item.count("�")))
    for src, dst in SMART_PUNCT.items():
        best = best.replace(src, dst)
    best = re.sub(r"[ \t]+", " ", best)
    best = re.sub(r" *\n *", "\n", best)
    return best.strip()


def normalize_key(value: str) -> str:
    value = repair_text(value).lower()
    value = re.sub(r"[^a-z0-9' -]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip(" -'")
    return value


def clean_title(value: str) -> str:
    value = repair_text(value)
    return value.replace("[", "(").replace("]", ")").strip()


def derive_topic(title: str, body: str) -> str:
    haystack = f"{title}\n{body}".lower()
    best_topic = "Daily Life"
    best_score = 0
    for topic, needles in TOPIC_RULES:
        score = sum(1 for needle in needles if needle in haystack)
        if score > best_score:
            best_topic = topic
            best_score = score
    return best_topic


def word_count(body: str) -> int:
    return len(re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)?", body))


def parse_txt_file(path: Path) -> list[dict[str, object]]:
    raw = repair_text(path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n"))
    level = path.stem.upper()
    header_pattern = re.compile(r"^###\s+Text\s+(\d+)\s*:\s*(.+)$", re.M)
    headers = list(header_pattern.finditer(raw))
    entries: list[dict[str, object]] = []
    for index, match in enumerate(headers):
        source_number = int(match.group(1))
        title = clean_title(match.group(2))
        start = match.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(raw)
        section = raw[start:end].strip()
        section = re.sub(r"^\*\*Word Count:\s*\d+\s*words\*\*\s*", "", section, flags=re.I)
        vocab_match = re.search(r"^\*\*Kelime.*?:\*\*\s*$", section, flags=re.I | re.M)
        if vocab_match:
            body = section[: vocab_match.start()].strip()
            vocab_block = section[vocab_match.end() :].strip()
        else:
            body = section.strip()
            vocab_block = ""
        body = re.sub(r"\n?---+\s*$", "", body).strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        vocab: dict[str, str] = {}
        for term, meaning in re.findall(r"^\s*\*\s+\*\*(.+?):\*\*\s*(.+)$", vocab_block, flags=re.M):
            key = normalize_key(term)
            value = repair_text(meaning).strip(" .;")
            if key and value:
                vocab[key] = value
        if body:
            entries.append(
                {
                    "level": level,
                    "source_number": source_number,
                    "title": title,
                    "topic": derive_topic(title, body),
                    "body": body,
                    "vocab": vocab,
                    "words": word_count(body),
                }
            )
    return entries


def load_json(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8", errors="replace") or "{}")
    return {normalize_key(k): repair_text(str(v)).strip() for k, v in data.items() if normalize_key(k) and str(v).strip()}


def save_json(path: Path, data: dict[str, str]) -> None:
    cleaned = {normalize_key(k): repair_text(v).strip() for k, v in data.items() if normalize_key(k) and str(v).strip()}
    path.write_text(json.dumps(dict(sorted(cleaned.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def existing_headers(text: str) -> tuple[dict[str, int], set[str]]:
    max_numbers: dict[str, int] = defaultdict(int)
    bodies: set[str] = set()
    headers = list(re.finditer(r"^\[(A1|A2|B1|B2|C1|C2)-(\d+).*?\]$", text, flags=re.M))
    for index, match in enumerate(headers):
        level = match.group(1)
        number = int(match.group(2))
        max_numbers[level] = max(max_numbers[level], number)
        start = match.end()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        body = re.sub(r"\s+", " ", text[start:end]).strip().lower()
        if body:
            bodies.add(body)
    return dict(max_numbers), bodies


def append_entries(entries: list[dict[str, object]]) -> list[dict[str, object]]:
    current = CURATED_PATH.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    max_numbers, body_fingerprints = existing_headers(current)
    additions: list[str] = []
    appended: list[dict[str, object]] = []
    for entry in entries:
        body = str(entry["body"]).strip()
        fingerprint = re.sub(r"\s+", " ", body).strip().lower()
        if fingerprint in body_fingerprints:
            continue
        level = str(entry["level"])
        max_numbers[level] = max_numbers.get(level, 0) + 1
        entry_number = max_numbers[level]
        entry["entry_number"] = entry_number
        title = clean_title(str(entry["title"]))
        topic = str(entry["topic"])
        words = int(entry["words"])
        additions.append(f"[{level}-{entry_number} | Topic: {topic} | Words: {words} | Title: {title}]\n{body}\n")
        appended.append(entry)
        body_fingerprints.add(fingerprint)
    if additions:
        next_text = current.rstrip() + "\n\n" + "\n".join(additions)
        CURATED_PATH.write_text(next_text.rstrip() + "\n", encoding="utf-8")
    return appended


def looks_bad(main: object, key: str, value: str) -> bool:
    value = repair_text(value).strip()
    if not value:
        return True
    try:
        return bool(main.is_suspicious_meaning(key, value))
    except Exception:
        return "?" in value or value.lower() == key.lower()


def enrich_word_map(entries: list[dict[str, object]]) -> tuple[int, int, list[str]]:
    sys.path.insert(0, str(ROOT))
    import backend.main as main  # noqa: WPS433

    # The import pass must be deterministic and fast; do not call online model
    # fallbacks while preparing a static vocabulary map.
    main.translate_library_word_with_fallback = lambda _word, _lemma: ""
    main.request_model = lambda *args, **kwargs: ""

    word_map = load_json(LIBRARY_MAP_PATH)
    before = len(word_map)
    for key, value in MANUAL_COMPLETIONS.items():
        word_map[normalize_key(key)] = repair_text(value)
        main.LIBRARY_WORD_MAP[normalize_key(key)] = repair_text(value)
    for entry in entries:
        for key, value in dict(entry["vocab"]).items():
            if key and value and not looks_bad(main, key, value):
                word_map[key] = repair_text(value)
                main.LIBRARY_WORD_MAP[key] = repair_text(value)

    missing: set[str] = set()
    for entry in entries:
        body = str(entry["body"])
        for phrase_match in main.match_phrases(body, *main.runtime_lexical_maps()):
            for phrase_key in (phrase_match.key, phrase_match.canonical):
                normalized = normalize_key(phrase_key)
                meaning = repair_text(str(phrase_match.meaning or ""))
                if normalized and meaning and not looks_bad(main, normalized, meaning):
                    word_map.setdefault(normalized, meaning)
                    main.LIBRARY_WORD_MAP.setdefault(normalized, meaning)
        lowered_body = body.lower()
        for phrase_key, phrase_meaning in main.LOCAL_PHRASE_MAP.items():
            normalized = normalize_key(phrase_key)
            if normalized and normalized in lowered_body and normalized not in word_map:
                meaning = repair_text(str(phrase_meaning or ""))
                if meaning and not looks_bad(main, normalized, meaning):
                    word_map[normalized] = meaning
                    main.LIBRARY_WORD_MAP[normalized] = meaning
        for token in main.token_records(body):
            key = normalize_key(str(token.get("key") or ""))
            if not key or key in word_map:
                continue
            sentence = main.find_sentence_for_word(body, key)
            profile = main.resolve_cefr_entry(key)
            lemma = normalize_key(str(profile.get("lemma") or key)) if profile else key
            meaning = (
                main.lookup_word_map_value(key)
                or main.lookup_word_map_value(lemma)
                or main.infer_contextual_library_meaning(lemma, sentence)
            )
            meaning = repair_text(str(meaning or ""))
            if meaning and not looks_bad(main, key, meaning):
                word_map[key] = meaning
                main.LIBRARY_WORD_MAP[key] = meaning
            elif key and not re.fullmatch(r"[a-z]+'?(s|m|re|ve|d|ll|t)?", key):
                missing.add(key)

    save_json(LIBRARY_MAP_PATH, word_map)
    main.LIBRARY_WORD_MAP.clear()
    main.LIBRARY_WORD_MAP.update(word_map)
    main.import_curated_readings()
    return before, len(word_map), sorted(missing)


def main() -> int:
    if not TXT_DIR.exists():
        raise SystemExit(f"TXT folder not found: {TXT_DIR}")
    all_entries: list[dict[str, object]] = []
    for path in sorted(TXT_DIR.glob("*.txt")):
        all_entries.extend(parse_txt_file(path))
    appended = append_entries(all_entries)
    before, after, missing = enrich_word_map(all_entries)
    level_counts: dict[str, int] = defaultdict(int)
    for entry in appended:
        level_counts[str(entry["level"])] += 1
    report = {
        "source_entries": len(all_entries),
        "newly_appended": len(appended),
        "new_by_level": dict(sorted(level_counts.items())),
        "word_map_before": before,
        "word_map_after": after,
        "word_map_added": after - before,
        "missing_after_enrichment": len(missing),
        "missing_sample": missing[:40],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
