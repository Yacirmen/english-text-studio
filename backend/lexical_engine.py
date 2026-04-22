import re
from dataclasses import dataclass


TOKEN_RE = re.compile(r"[A-Za-z]+(?:['-][A-Za-z]+)*")

CORE_PHRASE_MEANINGS: dict[str, str] = {
    "take off": "havalanmak / hızla yükselmek",
    "turn out": "sonuçlanmak / ortaya çıkmak",
    "give up": "vazgeçmek",
    "break up": "ayrılmak / parçalanmak",
    "look after": "ilgilenmek / bakmak",
    "run into": "karşılaşmak",
    "figure out": "çözmek / anlamak",
    "calm down": "sakinleşmek",
    "get along": "iyi geçinmek",
    "set up": "kurmak",
    "carry out": "gerçekleştirmek",
    "point out": "işaret etmek / belirtmek",
    "bring about": "neden olmak / meydana getirmek",
    "deal with": "ilgilenmek / ele almak",
    "lead to": "yol açmak",
    "rely on": "güvenmek / dayanmak",
    "depend on": "bağlı olmak",
    "result in": "sonuçlanmak",
    "stem from": "kaynaklanmak",
    "give rise to": "yol açmak",
    "come up with": "aklına getirmek / üretmek",
    "keep up with": "ayak uydurmak",
    "make up": "oluşturmak / uydurmak",
    "bring up": "gündeme getirmek",
    "phase out": "kademeli olarak kaldırmak",
    "scale up": "ölçek büyütmek",
    "roll out": "kullanıma sunmak",
    "root cause": "temel neden",
    "long run": "uzun vade",
    "short run": "kısa vade",
    "in the long run": "uzun vadede",
    "in the short run": "kısa vadede",
    "by contrast": "buna karşılık",
    "on the other hand": "öte yandan",
    "as a result": "sonuç olarak",
    "as well as": "yanı sıra",
    "rather than": "yerine",
    "due to": "nedeniyle",
    "in favor of": "lehine",
    "in light of": "... ışığında",
    "in terms of": "açısından",
    "with regard to": "ile ilgili olarak",
    "at the expense of": "pahasına",
    "at the same time": "aynı zamanda",
    "to some extent": "bir ölçüde",
    "for the sake of": "uğruna",
    "far more than": "...den çok daha fazla",
    "regardless of": "...den bağımsız olarak / ...e bakılmaksızın",
    "no longer": "artık değil",
    "not merely": "sadece ... değil",
    "not only": "yalnızca ... değil",
    "human rights": "insan hakları",
    "public safety": "kamu güvenliği",
    "social cohesion": "toplumsal uyum",
    "social capital": "sosyal sermaye",
    "work-life balance": "iş-yaşam dengesi",
    "personal data": "kişisel veri",
    "machine learning": "makine öğrenmesi",
    "artificial intelligence": "yapay zeka",
    "universal basic income": "evrensel temel gelir",
    "space exploration": "uzay araştırmaları",
    "climate change": "iklim değişikliği",
    "mental health": "ruh sağlığı",
    "gene editing": "gen düzenleme",
    "genetic modification": "genetik değişim",
    "surveillance capitalism": "gözetim kapitalizmi",
    "restorative justice": "onarıcı adalet",
    "false equivalence": "sahte eşdeğerlik",
    "hate speech": "nefret söylemi",
    "low-earth orbit": "alçak dünya yörüngesi",
    "home-cooked": "ev yapımı",
    "face-to-face": "yüz yüze",
    "decision-making": "karar verme",
    "well-being": "iyi oluş",
    "post-truth": "hakikat sonrası",
    "de-extinction": "tür diriltme",
    "always-connected": "sürekli bağlantıda",
}

LEMMA_OVERRIDES = {
    "arose": "arise",
    "arisen": "arise",
    "became": "become",
    "began": "begin",
    "begun": "begin",
    "brought": "bring",
    "broke": "break",
    "broken": "break",
    "came": "come",
    "dealt": "deal",
    "driven": "drive",
    "drove": "drive",
    "fell": "fall",
    "felt": "feel",
    "found": "find",
    "gave": "give",
    "given": "give",
    "got": "get",
    "gotten": "get",
    "kept": "keep",
    "led": "lead",
    "left": "leave",
    "looked": "look",
    "made": "make",
    "paid": "pay",
    "ran": "run",
    "rose": "rise",
    "risen": "rise",
    "said": "say",
    "saw": "see",
    "seen": "see",
    "set": "set",
    "spent": "spend",
    "stuck": "stick",
    "took": "take",
    "taken": "take",
    "told": "tell",
    "turned": "turn",
    "went": "go",
    "worked": "work",
    "written": "write",
    "wrote": "write",
}

PARTICLES = {
    "about",
    "across",
    "after",
    "against",
    "along",
    "around",
    "away",
    "back",
    "by",
    "down",
    "for",
    "forward",
    "in",
    "into",
    "off",
    "on",
    "out",
    "over",
    "through",
    "to",
    "up",
    "with",
}


@dataclass(frozen=True)
class PhraseMatch:
    key: str
    canonical: str
    surface: str
    meaning: str
    start_token: int
    end_token: int
    start_char: int
    end_char: int
    source: str


def normalize_key(value: str) -> str:
    cleaned = str(value or "").strip().lower()
    cleaned = (
        cleaned.replace("’", "'")
        .replace("`", "'")
        .replace("–", "-")
        .replace("—", "-")
    )
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" -'")


def lemma_token(word: str) -> str:
    raw = normalize_key(word)
    if not raw:
        return ""
    if raw in LEMMA_OVERRIDES:
        return LEMMA_OVERRIDES[raw]
    if raw.endswith("ies") and len(raw) > 4:
        return raw[:-3] + "y"
    if raw.endswith("ing") and len(raw) > 5:
        stem = raw[:-3]
        if len(stem) > 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        if stem and not stem.endswith("e"):
            return stem
        return stem
    if raw.endswith("ied") and len(raw) > 4:
        return raw[:-3] + "y"
    if raw.endswith("ed") and len(raw) > 4:
        stem = raw[:-2]
        if len(stem) > 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        if stem.endswith("i"):
            return stem[:-1] + "y"
        return stem
    if raw.endswith("es") and len(raw) > 4:
        return raw[:-2]
    if raw.endswith("s") and len(raw) > 4:
        return raw[:-1]
    return raw


def phrase_variants(value: str) -> list[str]:
    base = normalize_key(value)
    if not base:
        return []
    candidates: list[str] = []

    def add(item: str) -> None:
        cleaned = normalize_key(item)
        if cleaned and cleaned not in candidates:
            candidates.append(cleaned)

    add(base)
    add(base.replace("-", " "))
    add(base.replace(" ", "-"))
    add(base.replace("'", ""))
    add(base.replace("'", " "))
    for candidate in list(candidates):
        parts = candidate.split()
        if len(parts) > 1:
            add(" ".join(lemma_token(part) for part in parts))
            add("-".join(lemma_token(part) for part in parts))
    return candidates


def is_compound_key(key: str) -> bool:
    cleaned = normalize_key(key)
    return " " in cleaned or "-" in cleaned


def build_phrase_inventory(*maps: dict[str, str]) -> dict[str, dict[str, str]]:
    inventory: dict[str, dict[str, str]] = {}

    def add(key: str, meaning: str, source: str) -> None:
        canonical = normalize_key(key)
        cleaned_meaning = str(meaning or "").strip()
        if not canonical or not cleaned_meaning or not is_compound_key(canonical):
            return
        existing = inventory.get(canonical)
        if existing and existing.get("meaning"):
            return
        inventory[canonical] = {"meaning": cleaned_meaning, "source": source}

    for key, meaning in CORE_PHRASE_MEANINGS.items():
        add(key, meaning, "core")
    for index, mapping in enumerate(maps):
        source = "local" if index == 0 else "map"
        for key, meaning in (mapping or {}).items():
            add(key, meaning, source)
    return inventory


def resolve_phrase(value: str, *maps: dict[str, str]) -> dict[str, str] | None:
    inventory = build_phrase_inventory(*maps)
    for candidate in phrase_variants(value):
        if candidate in inventory:
            return {
                "canonical": candidate,
                "meaning": inventory[candidate]["meaning"],
                "source": inventory[candidate].get("source", "map"),
            }
    return None


def token_records(text: str) -> list[dict[str, object]]:
    return [
        {
            "text": match.group(0),
            "start": match.start(),
            "end": match.end(),
            "key": normalize_key(match.group(0)),
            "lemma": lemma_token(match.group(0)),
        }
        for match in TOKEN_RE.finditer(text or "")
    ]


def window_variants(tokens: list[dict[str, object]], start: int, end: int) -> list[str]:
    surface = " ".join(str(item["key"]) for item in tokens[start:end])
    lemmas = " ".join(str(item["lemma"]) for item in tokens[start:end])
    variants = phrase_variants(surface)
    for variant in phrase_variants(lemmas):
        if variant not in variants:
            variants.append(variant)
    if end - start == 1:
        raw = str(tokens[start]["key"])
        for variant in phrase_variants(raw):
            if variant not in variants:
                variants.append(variant)
    return variants


def match_phrases(text: str, *maps: dict[str, str], max_words: int = 5) -> list[PhraseMatch]:
    inventory = build_phrase_inventory(*maps)
    tokens = token_records(text)
    matches: list[PhraseMatch] = []
    occupied: set[int] = set()
    for start in range(len(tokens)):
        if start in occupied:
            continue
        best: PhraseMatch | None = None
        max_end = min(len(tokens), start + max_words)
        for end in range(max_end, start, -1):
            if any(index in occupied for index in range(start, end)):
                continue
            for variant in window_variants(tokens, start, end):
                meta = inventory.get(variant)
                if not meta:
                    continue
                surface = text[int(tokens[start]["start"]): int(tokens[end - 1]["end"])]
                best = PhraseMatch(
                    key=normalize_key(surface),
                    canonical=variant,
                    surface=surface,
                    meaning=meta["meaning"],
                    start_token=start,
                    end_token=end,
                    start_char=int(tokens[start]["start"]),
                    end_char=int(tokens[end - 1]["end"]),
                    source=meta.get("source", "map"),
                )
                break
            if best:
                break
        if best:
            matches.append(best)
            occupied.update(range(best.start_token, best.end_token))
    return matches


def covered_token_indexes(matches: list[PhraseMatch]) -> set[int]:
    covered: set[int] = set()
    for match in matches:
        if match.end_token - match.start_token > 1 or is_compound_key(match.key):
            covered.update(range(match.start_token, match.end_token))
    return covered


def extract_phrase_keys_for_frontend(text: str, *maps: dict[str, str]) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    for match in match_phrases(text, *maps):
        for key in (match.key, match.canonical):
            cleaned = normalize_key(key)
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                keys.append(cleaned)
    return keys
