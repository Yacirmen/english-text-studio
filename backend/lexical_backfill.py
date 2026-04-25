from __future__ import annotations

import argparse
import json
import re
import sqlite3
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from backend import main as app
from backend.lexical_engine import covered_token_indexes, match_phrases, token_records


REVIEW_REQUIRED_MEANING = "çeviri gerekli"
GENERIC_MEANINGS = {
    "bağlama göre kullanılan ifade",
    "bağlama göre işlevsel kelime",
    "kısaltma / özel ad",
}
CURATED_BACKFILL_MEANINGS: dict[str, str] = {
    "absolves": "aklar / sorumluluktan kurtarır",
    "absurdity": "saçmalık",
    "accelerate": "hızlandırmak",
    "accelerating": "hızlandıran / hızlanmakta olan",
    "acceleration": "hızlanma",
    "advent": "ortaya çıkış / geliş",
    "aestheticization": "estetikleştirme",
    "aestheticized": "estetikleştirilmiş",
    "agrochemical": "tarım kimyasalı",
    "aimlessly": "amaçsızca",
    "alarming": "endişe verici",
    "alarm": "alarm / endişe",
    "alhambra": "özel isim / yer adı",
    "algorithmic": "algoritmik",
    "allure": "çekicilik / cazibe",
    "ancestral": "atalardan kalan",
    "anonymity": "anonimlik",
    "arendt": "özel isim / kişi adı",
    "arena": "alan / arena",
    "argumentation": "akıl yürütme / tartışma biçimi",
    "articulate": "açıkça ifade etmek",
    "articulated": "açıkça ifade edilmiş",
    "artifacts": "eserler / yapay nesneler",
    "artistry": "ustalık / sanatsal beceri",
    "assert": "ileri sürmek / savunmak",
    "astonishingly": "şaşırtıcı derecede",
    "astronauts": "astronotlar",
    "attained": "ulaşılmış / elde edilmiş",
    "augment": "artırmak / güçlendirmek",
    "authoritarian": "otoriter",
    "authenticity": "özgünlük / sahicilik",
    "automate": "otomatikleştirmek",
    "auschwitz": "özel isim / yer adı",
    "back": "geri / arka",
    "barrage": "yoğun bombardıman / sağanak",
    "baseline": "başlangıç düzeyi / temel çizgi",
    "behemoths": "dev kuruluşlar",
    "big": "büyük",
    "biochemical": "biyokimyasal",
    "biodiversity": "biyoçeşitlilik",
    "biofuels": "biyoyakıtlar",
    "biometric": "biyometrik",
    "biometrics": "biyometri",
    "biosphere": "biyosfer",
    "bioterrorist": "biyoterörist",
    "bilingual": "iki dilli",
    "blaring": "yüksek sesle çalan",
    "blueprints": "planlar / taslaklar",
    "boulevards": "bulvarlar",
    "bribe": "rüşvet",
    "bureaucratic": "bürokratik",
    "can't": "yapamaz / edemez",
    "catastrophic": "felaket düzeyinde / yıkıcı",
    "catchy": "akılda kalıcı",
    "categorize": "sınıflandırmak",
    "cater": "hitap etmek / karşılamak",
    "chaotic": "kaotik / düzensiz",
    "charisma": "karizma",
    "chernobyl": "özel isim / yer adı",
    "choreographed": "kurgulanmış / koreografisi yapılmış",
    "chronological": "kronolojik",
    "citizenry": "yurttaşlar / halk",
    "civilized": "uygar",
    "clogged": "tıkanmış",
    "colder": "daha soğuk",
    "colosseum": "özel isim / yer adı",
    "commercialization": "ticarileştirme",
    "commentators": "yorumcular",
    "communal": "toplulukla ilgili / ortak",
    "commute": "işe gidip gelmek",
    "commuting": "işe gidip gelme",
    "compatibilist": "bağdaşırcı / uyumcu görüşe ait",
    "compassionate": "şefkatli",
    "comprehend": "kavramak / anlamak",
    "comprehending": "kavrama / anlamakta olan",
    "conceptual": "kavramsal",
    "conceptualized": "kavramsallaştırılmış",
    "conceptualizing": "kavramsallaştırma",
    "concedes": "kabul eder / teslim eder",
    "condensed": "yoğunlaştırılmış / kısaltılmış",
    "confines": "sınırlar",
    "confrontation": "yüzleşme / çatışma",
    "consolidation": "pekiştirme / güçlendirme",
    "contagious": "bulaşıcı",
    "contend": "savunmak / iddia etmek",
    "contradictory": "çelişkili",
    "cortisol": "kortizol",
    "courageous": "cesur",
    "couriers": "kuryeler",
    "cowardly": "korkakça",
    "creamy": "kremamsı",
    "crises": "krizler",
    "crispr": "CRISPR gen düzenleme tekniği",
    "crispr-cas": "CRISPR-Cas gen düzenleme sistemi",
    "cultivate": "geliştirmek / yetiştirmek",
    "cultivated": "geliştirilmiş / yetiştirilmiş",
    "cultivates": "geliştirir / yetiştirir",
    "cultivating": "geliştirme / yetiştirme",
    "cultivation": "yetiştirme / geliştirme",
    "curricula": "müfredatlar",
    "cursive": "el yazısı",
    "cyclist": "bisikletli / bisiklet süren kişi",
    "cyclists": "bisikletliler",
    "customized": "kişiselleştirilmiş",
    "cybercrime": "siber suç",
    "cybercriminals": "siber suçlular",
    "cybersecurity": "siber güvenlik",
    "cynical": "kinik / alaycı",
    "cynicism": "kinizm / alaycı kuşkuculuk",
    "debilitating": "güçten düşüren / zayıflatıcı",
    "decipher": "çözmek / anlamını çıkarmak",
    "deepfake": "deepfake / sahte video",
    "deepfakes": "deepfake içerikler",
    "degradation": "bozulma / yıpranma",
    "degraded": "bozulmuş / yıpranmış",
    "delegitimize": "meşruiyetini zayıflatmak",
    "deliberation": "müzakere / dikkatli düşünme",
    "democratization": "demokratikleşme / yaygınlaşma",
    "democratize": "demokratikleştirmek / erişilebilir kılmak",
    "dependency": "bağımlılık",
    "depicting": "tasvir eden",
    "depressive": "depresif",
    "deprived": "yoksun bırakılmış",
    "determinism": "determinizm",
    "deterministic": "determinist / belirlenimci",
    "detractors": "karşı çıkanlar / eleştirenler",
    "detrimental": "zararlı",
    "devaluing": "değerini düşürme",
    "deviation": "sapma",
    "devolves": "bozulup dönüşür / devredilir",
    "dictate": "belirlemek / dayatmak",
    "dictated": "belirlenmiş / dayatılmış",
    "dictates": "belirler / dayatır",
    "didn't": "yapmadı / etmedi",
    "digestible": "kolay anlaşılır / sindirilebilir",
    "dilemma": "ikilem",
    "dilemmas": "ikilemler",
    "diminishing": "azalan",
    "disadvantage": "dezavantaj",
    "discarded": "atılmış / gözden çıkarılmış",
    "discrepancy": "uyuşmazlık / fark",
    "discriminatory": "ayrımcı",
    "dishonest": "dürüst olmayan",
    "disinformation": "dezenformasyon",
    "disneyfication": "Disney tarzı ticarileştirme / yumuşatma",
    "disparate": "birbirinden farklı / kopuk",
    "displacement": "yerinden edilme / yer değiştirme",
    "disposable": "tek kullanımlık / gözden çıkarılabilir",
    "disrespectful": "saygısız",
    "disruptions": "aksamalar / bozulmalar",
    "dissemination": "yayılma / yayma",
    "distracts": "dikkatini dağıtır",
    "divisive": "bölücü / ayrıştırıcı",
    "dizzying": "baş döndürücü",
    "dna": "DNA",
    "dogma": "dogma / katı inanç",
    "don't": "yapma / etme",
    "drastically": "köklü biçimde / ciddi ölçüde",
    "dread": "derin korku / kaygı",
    "driverless": "sürücüsüz",
    "dwellers": "sakinler / yaşayanlar",
    "eight": "sekiz",
    "egalitarian": "eşitlikçi",
    "elevate": "yükseltmek / artırmak",
    "elevates": "yükseltir / artırır",
    "electorate": "seçmen kitlesi",
    "electorates": "seçmen kitleleri",
    "empirical": "ampirik / kanıta dayalı",
    "emptiness": "boşluk hissi",
    "enact": "yürürlüğe koymak / sahnelemek",
    "enacting": "yürürlüğe koyma / gerçekleştirme",
    "encompassing": "kapsayan",
    "endeavor": "çaba / girişim",
    "endeavors": "çabalar / girişimler",
    "enforceable": "uygulanabilir / yaptırımı olan",
    "enlightenment": "aydınlanma",
    "ensnared": "tuzağa düşmüş / yakalanmış",
    "enthusiastically": "coşkuyla",
    "entitlements": "hak edişler / sosyal haklar",
    "entrepreneurial": "girişimci",
    "environmentalists": "çevreciler",
    "envision": "zihinde canlandırmak / öngörmek",
    "envisions": "öngörür / tasavvur eder",
    "epistemic": "bilgiyle ilgili / epistemik",
    "equilibriums": "dengeler",
    "equips": "donatır",
    "equitable": "adil / hakkaniyetli",
    "eradicate": "ortadan kaldırmak",
    "eradicated": "ortadan kaldırılmış",
    "eradicates": "ortadan kaldırır",
    "eradicating": "ortadan kaldırma",
    "erode": "aşındırmak",
    "eroded": "aşınmış",
    "erodes": "aşındırır",
    "eroding": "aşındıran / aşınan",
    "erosion": "aşınma / erozyon",
    "euros": "avro",
    "evading": "kaçınma / atlatma",
    "evaporation": "buharlaşma",
    "ever": "hiç / şimdiye kadar",
    "evolutionarily": "evrimsel olarak",
    "exclusionary": "dışlayıcı",
    "exhaustion": "tükenmişlik / bitkinlik",
    "existential": "varoluşsal",
    "expansive": "geniş kapsamlı",
    "extinguish": "söndürmek / yok etmek",
    "familial": "ailevi",
    "favorite": "favori / en sevilen",
    "fertile": "verimli",
    "five": "beş",
    "fixating": "takılıp kalma",
    "fluctuations": "dalgalanmalar",
    "fluency": "akıcılık",
    "formidable": "zorlu / etkileyici",
    "formulate": "formüle etmek / oluşturmak",
    "formulation": "formülasyon / oluşturma",
    "fortified": "güçlendirilmiş",
    "found": "buldu / bulundu",
    "foundational": "temel / kurucu",
    "four": "dört",
    "fragmentation": "parçalanma",
    "frantically": "telaşla / çılgınca",
    "frictionless": "sürtünmesiz / zahmetsiz",
    "genetically": "genetik olarak",
    "genomic": "genomik",
    "geopolitics": "jeopolitik",
    "globalization": "küreselleşme",
    "got": "aldı / oldu",
    "grammatical": "dilbilgisel",
    "granada": "özel isim / yer adı",
    "grandiose": "gösterişli / abartılı",
    "grappling": "uğraşma / boğuşma",
    "gravitates": "yönelir / çekilir",
    "greener": "daha yeşil / daha çevreci",
    "hackers": "bilgisayar korsanları",
    "handwriting": "el yazısı",
    "handwritten": "elle yazılmış",
    "hannah": "özel isim / kişi adı",
    "harness": "yararlanmak / dizginlemek",
    "hastily": "aceleyle",
    "hazardous": "tehlikeli",
    "here": "burada",
    "hierarchical": "hiyerarşik",
    "holi": "özel isim / festival adı",
    "homeschooling": "evde eğitim",
    "homeschooled": "evde eğitim almış",
    "homogenous": "homojen / tek tip",
    "honorifics": "saygı ifadeleri / hitap ekleri",
    "hurdles": "engeller",
    "hyperloop": "Hyperloop ulaşım sistemi",
    "idealized": "idealleştirilmiş",
    "ignited": "ateşledi / başlattı",
    "igniting": "ateşleyen / başlatan",
    "impair": "bozmak / zayıflatmak",
    "imperfect": "kusurlu",
    "impending": "yaklaşan",
    "implicitly": "örtük biçimde",
    "impossibility": "imkansızlık",
    "incapable": "yetersiz / aciz",
    "incentivizes": "teşvik eder",
    "incentivizing": "teşvik etme",
    "incomprehensible": "anlaşılmaz",
    "incomprehension": "anlayamama",
    "indispensable": "vazgeçilmez",
    "individuality": "bireysellik / kişiye özgülük",
    "inescapable": "kaçınılmaz",
    "inflict": "zarar vermek / acı çektirmek",
    "inflicted": "verilmiş / uygulanmış",
    "inflicting": "verme / uygulama",
    "inflicts": "verir / uygular",
    "injected": "enjekte edilmiş",
    "injects": "enjekte eder / sokar",
    "insecurity": "güvensizlik",
    "insidious": "sinsi",
    "insulating": "yalıtan / koruyan",
    "intellectualism": "entelektüalizm",
    "intentionality": "niyetlilik / kasıtlılık",
    "interbreed": "çapraz üremek",
    "internet": "internet",
    "intolerance": "hoşgörüsüzlük",
    "intoxicating": "sarhoş edici / baş döndürücü",
    "intricate": "karmaşık / ince detaylı",
    "introspection": "içe bakış",
    "introspective": "içe dönük / öz değerlendirmeye dayalı",
    "invariably": "değişmez biçimde / daima",
    "invasive": "müdahaleci / istilacı",
    "invent": "icat etmek",
    "invincibility": "yenilmezlik",
    "iris": "iris / gözün renkli tabakası",
    "irreversible": "geri döndürülemez",
    "irresistibly": "karşı konulamaz biçimde",
    "known": "bilinen",
    "knowledgeable": "bilgili",
    "laziness": "tembellik",
    "lethality": "öldürücülük",
    "levers": "kaldıraçlar / etki araçları",
    "levitation": "havada kalma / yükselme",
    "lexicon": "söz varlığı / sözlükçe",
    "lifecycles": "yaşam döngüleri",
    "lifeline": "can simidi / hayati destek",
    "linguistic": "dilsel",
    "linguists": "dilbilimciler",
    "liters": "litreler",
    "livability": "yaşanabilirlik",
    "livable": "yaşanabilir",
    "livelihoods": "geçim kaynakları",
    "logistical": "lojistik",
    "looming": "yaklaşan / beliren",
    "louvre": "özel isim / müze adı",
    "luminous": "ışıklı / parlak",
    "macroeconomic": "makroekonomik",
    "madrid": "özel isim / yer adı",
    "maize": "mısır",
    "malicious": "kötü niyetli",
    "manifestation": "belirti / dışavurum",
    "manipulative": "manipülatif",
    "manipulators": "manipülatörler / yönlendiriciler",
    "marginal": "marjinal / kenarda kalan",
    "marginalization": "marjinalleştirme / dışlama",
    "marginalized": "dışlanmış / marjinalleştirilmiş",
    "masterful": "ustaca",
    "masterfully": "ustalıkla",
    "megacities": "mega kentler",
    "melancholic": "melankolik",
    "meme": "meme / internet esprisi",
    "menu": "menü",
    "mesmerizing": "büyüleyici",
    "meticulous": "titiz",
    "meticulously": "titizlikle",
    "metropolises": "metropoller",
    "microscopic": "mikroskobik",
    "microorganisms": "mikroorganizmalar",
    "microplastics": "mikroplastikler",
    "midday": "öğle vakti",
    "migrate": "göç etmek",
    "milliseconds": "milisaniyeler",
    "mimic": "taklit etmek",
    "mimics": "taklit eder",
    "minimalism": "minimalizm",
    "minimalist": "minimalist",
    "minimalists": "minimalistler",
    "misidentify": "yanlış tanımlamak",
    "mockery": "alay",
    "mode": "mod / kip",
    "monopolize": "tekeline almak",
    "monopolized": "tekeline alınmış",
    "monumental": "anıtsal / çok büyük",
    "morbid": "hastalıklı / karanlık",
    "motorized": "motorlu",
    "mourning": "yas",
    "multilingual": "çok dilli",
    "multimedia": "çoklu ortam",
    "multinational": "çok uluslu",
    "mushroom": "mantar",
    "mythical": "efsanevi",
    "naivety": "saflık",
    "napoli": "özel isim / yer adı",
    "navigational": "yön bulmayla ilgili",
    "necessitates": "gerektirir",
    "neurological": "nörolojik",
    "neurochemical": "nörokimyasal",
    "neuroimaging": "nörogörüntüleme",
    "neurological": "nörolojik",
    "neuroplasticity": "nöroplastisite",
    "neuroscience": "sinirbilim",
    "neuroscientific": "sinirbilimsel",
    "neuroscientists": "sinirbilimciler",
    "never": "asla / hiç",
    "nine": "dokuz",
    "noisier": "daha gürültülü",
    "nonsensical": "anlamsız / saçma",
    "normal": "normal",
    "normalized": "normalleştirilmiş",
    "nostalgia": "nostalji",
    "nostalgic": "nostaljik",
    "nouns": "isimler",
    "nuanced": "ince ayrımlı / nüanslı",
    "nuances": "nüanslar / ince farklar",
    "obedience": "itaat",
    "obsolete": "modası geçmiş / kullanımdan kalkmış",
    "obscurity": "belirsizlik / bilinmezlik",
    "oceanic": "okyanusla ilgili",
    "orchestrate": "organize etmek / kurgulamak",
    "organism": "organizma",
    "our": "bizim",
    "outsiders": "dışarıdakiler / yabancılar",
    "overstimulated": "aşırı uyarılmış",
    "pacifying": "yatıştıran / pasifleştiren",
    "panopticon": "panoptikon / gözetim düzeni",
    "paradigm": "paradigma / düşünce modeli",
    "paradox": "paradoks",
    "paralysis": "felç / donakalma",
    "paris": "özel isim / yer adı",
    "park": "park",
    "patent": "patent",
    "penmanship": "el yazısı becerisi",
    "performative": "gösteriye dayalı / performatif",
    "peril": "tehlike",
    "perilous": "tehlikeli / riskli",
    "perpetual": "sürekli / daimi",
    "perfectionism": "mükemmeliyetçilik",
    "personalized": "kişiselleştirilmiş",
    "pesticides": "tarım ilaçları",
    "pests": "zararlılar",
    "phishing": "oltalama",
    "photogenic": "fotojenik",
    "physiological": "fizyolojik",
    "pizza": "pizza",
    "pizzas": "pizzalar",
    "pitfalls": "tuzaklar / sakıncalar",
    "pivot": "eksen / yön değiştirme noktası",
    "planners": "planlamacılar",
    "plausibly": "makul biçimde",
    "playful": "oyuncu / neşeli",
    "pluralistic": "çoğulcu",
    "pods": "kapsüller",
    "poignant": "dokunaklı",
    "polarization": "kutuplaşma",
    "polarizing": "kutuplaştırıcı",
    "policymakers": "politika yapıcılar",
    "poorer": "daha yoksul / daha zayıf",
    "pop": "pop / popüler tarz",
    "populace": "halk / nüfus",
    "populist": "popülist",
    "posit": "ileri sürmek",
    "posits": "ileri sürer",
    "postmodern": "postmodern",
    "postmodernism": "postmodernizm",
    "pottery": "çömlekçilik / seramik",
    "precedes": "öncesinde gelir",
    "predictably": "tahmin edilebilir biçimde",
    "preservationists": "korumacılar",
    "prevailing": "hakim / yaygın",
    "prioritization": "önceliklendirme",
    "proactive": "proaktif / ön alıcı",
    "procrastinate": "erteleme yapmak",
    "procrastinating": "erteleme",
    "programmable": "programlanabilir",
    "propaganda": "propaganda",
    "prose": "düzyazı",
    "protagonist's": "başkahramanın",
    "prowess": "üstün beceri",
    "punitive": "cezalandırıcı",
    "punitively": "cezalandırıcı biçimde",
    "purported": "iddia edilen / sözde",
    "put": "koymak",
    "quo": "mevcut durum",
    "radioactive": "radyoaktif",
    "reactionary": "gerici / tepkisel",
    "reactivity": "tepkisellik",
    "recycle": "geri dönüştürmek",
    "recycled": "geri dönüştürülmüş",
    "rectify": "düzeltmek",
    "redefinition": "yeniden tanımlama",
    "redesign": "yeniden tasarlamak",
    "rediscover": "yeniden keşfetmek",
    "reform": "reform / düzeltim",
    "rehabilitative": "iyileştirici / rehabilite edici",
    "relativity": "görelilik",
    "reliant": "bağımlı / dayanan",
    "remembrance": "anma / hatırlama",
    "replicate": "kopyalamak / tekrarlamak",
    "resilient": "dayanıklı",
    "resonance": "yankı / etki gücü",
    "respectful": "saygılı",
    "restructure": "yeniden yapılandırmak",
    "rethink": "yeniden düşünmek",
    "retorts": "karşılık verir / ters cevaplar",
    "revolutionize": "devrim yaratmak",
    "rhetorical": "retorik / söz sanatına ait",
    "ridiculed": "alay edilen",
    "ridiculousness": "saçmalık",
    "rightful": "haklı / meşru",
    "rigor": "titizlik / sıkılık",
    "rigorous": "titiz / sıkı",
    "rigors": "zorluklar / titiz süreçler",
    "role": "rol",
    "rooftop": "çatı katı / çatı",
    "sacredness": "kutsallık",
    "safeguard": "koruma / güvence",
    "safeguarding": "koruma altına alma",
    "sapir-whorf": "Sapir-Whorf hipotezi",
    "sarcastic": "alaycı",
    "sartre": "Sartre / filozof",
    "saturated": "doymuş / aşırı dolu",
    "scanners": "tarayıcılar",
    "scooters": "scooterlar",
    "sculpts": "şekillendirir",
    "seductive": "baştan çıkarıcı / çekici",
    "segregated": "ayrıştırılmış",
    "sensory": "duyusal",
    "seven": "yedi",
    "seville": "özel isim / yer adı",
    "sharper": "daha keskin",
    "shatter": "paramparça etmek",
    "shoppers": "alışveriş yapanlar",
    "shrinking": "küçülen",
    "sidewalks": "kaldırımlar",
    "silos": "silolar / kopuk alanlar",
    "sincerity": "samimiyet",
    "siren": "siren",
    "site": "site / alan",
    "skeptical": "kuşkucu / şüpheci",
    "skepticism": "kuşkuculuk / şüphecilik",
    "slogans": "sloganlar",
    "socioeconomic": "sosyoekonomik",
    "societal": "toplumsal",
    "sociological": "sosyolojik",
    "solemn": "ciddi / ağırbaşlı",
    "solitary": "yalnız / tek başına",
    "sophistication": "incelik / gelişmişlik",
    "spectacle": "gösteri",
    "spectacles": "gösteriler",
    "splicing": "birleştirme / gen ekleme",
    "stagecraft": "sahneleme ustalığı",
    "stagnation": "durgunluk",
    "starvation": "açlık / açlıktan ölme",
    "startling": "şaşırtıcı / irkiltici",
    "stifle": "bastırmak / boğmak",
    "stifles": "bastırır / boğar",
    "stifling": "boğucu / bastırıcı",
    "stimulate": "uyarmak / canlandırmak",
    "stricter": "daha sıkı",
    "stylish": "şık / tarz sahibi",
    "subsidize": "sübvanse etmek / desteklemek",
    "subsidized": "sübvanse edilmiş",
    "substantive": "özlü / esaslı",
    "suffocating": "boğucu",
    "sunglasses": "güneş gözlüğü",
    "superficiality": "yüzeysellik",
    "superweeds": "süper yabani otlar",
    "suppressing": "bastırma",
    "surreal": "gerçeküstü",
    "sustainably": "sürdürülebilir biçimde",
    "swelling": "şişme / artış",
    "symbolism": "sembolizm",
    "systematic": "sistematik",
    "systematically": "sistematik biçimde",
    "systemic": "sisteme yayılan / yapısal",
    "tailored": "özel uyarlanmış",
    "tangible": "somut",
    "tapas": "tapas / İspanyol mezesi",
    "tapestry": "dokuma / zengin bütün",
    "tedious": "sıkıcı / zahmetli",
    "ten": "on",
    "terminology": "terminoloji",
    "thames": "özel isim / nehir adı",
    "theatrical": "teatral",
    "theorists": "kuramcılar",
    "then": "sonra / o zaman",
    "think": "düşünmek",
    "thinkers": "düşünürler",
    "third": "üçüncü",
    "three": "üç",
    "thrill": "heyecan",
    "thrive": "gelişmek / serpilmek",
    "tidal": "gelgitle ilgili / dalga gibi",
    "tiramisu": "tiramisu",
    "tons": "tonlarca",
    "totality": "bütünlük / tamamı",
    "touchscreens": "dokunmatik ekranlar",
    "trajectory": "gidişat / yörünge",
    "trampoline": "trambolin",
    "transcend": "aşmak / ötesine geçmek",
    "transcribe": "yazıya dökmek",
    "transformative": "dönüştürücü",
    "trevi": "özel isim / yer adı",
    "tribalism": "kabilecilik / grupçuluk",
    "trivial": "önemsiz / sıradan",
    "trousers": "pantolon",
    "tutoring": "özel ders / rehberlik",
    "unalterable": "değiştirilemez",
    "unambiguous": "açık / belirsiz olmayan",
    "unattainable": "ulaşılamaz",
    "unavoidable": "kaçınılmaz",
    "uncritical": "eleştirel olmayan",
    "undeniable": "inkar edilemez",
    "undermined": "zayıflatılmış / baltalanmış",
    "undernourished": "yetersiz beslenmiş",
    "undivided": "bölünmemiş / tam",
    "unfulfilling": "tatmin etmeyen",
    "unglamorous": "gösterişsiz",
    "uniformity": "tekdüzelik / birlik",
    "unintended": "istenmeyen / amaçlanmamış",
    "uninterrupted": "kesintisiz",
    "unleashes": "serbest bırakır / ortaya çıkarır",
    "unpaid": "ücretsiz / ödenmemiş",
    "unparalleled": "benzersiz / eşi görülmemiş",
    "unquestioning": "sorgusuz sualsiz",
    "unravel": "çözülmek / ortaya çıkarmak",
    "unregulated": "düzenlenmemiş",
    "unrelenting": "acımasız / durmak bilmeyen",
    "unrest": "huzursuzluk / toplumsal çalkantı",
    "unsustainable": "sürdürülemez",
    "unviable": "uygulanamaz / yaşama şansı olmayan",
    "utilization": "kullanım / yararlanma",
    "utmost": "azami / en yüksek",
    "validate": "doğrulamak / geçerli kılmak",
    "validation": "doğrulama / onaylanma",
    "vehemently": "şiddetle / hararetle",
    "very": "çok",
    "via": "aracılığıyla / üzerinden",
    "violin": "keman",
    "viral": "viral / hızla yayılan",
    "visionaries": "vizyonerler",
    "visionary": "vizyoner",
    "vitae": "yaşam / özgeçmiş",
    "volatilities": "oynaklıklar / dalgalanmalar",
    "vulnerability": "kırılganlık / savunmasızlık",
    "vulnerabilities": "kırılganlıklar / güvenlik açıkları",
    "wander": "dolaşmak / gezinmek",
    "want": "istemek",
    "weaponized": "silaha dönüştürülmüş",
    "whims": "kaprisler / ani istekler",
    "who": "kim / ki",
    "won't": "yapmayacak / etmeyecek",
    "woodworking": "ahşap işçiliği",
    "worldview": "dünya görüşü",
    "wreckage": "enkaz",
    "wrongful": "haksız / yanlış",
    "yearning": "özlem",
    "york": "özel isim / yer adı",
    "you": "sen / siz",
    "your": "senin / sizin",
}


@dataclass
class TermResolution:
    term: str
    canonical: str
    meaning: str
    kind: str
    source: str
    confidence: float
    sample_context: str = ""


@dataclass
class LexicalBackfillReport:
    readings_scanned: int = 0
    tokens_seen: int = 0
    unique_terms_seen: int = 0
    approved_inserted: int = 0
    approved_updated: int = 0
    approved_existing: int = 0
    approved_conflicts: int = 0
    queued_inserted: int = 0
    queued_updated: int = 0
    queued_existing: int = 0
    skipped_generic: int = 0
    skipped_short: int = 0
    dry_run: bool = False


def compact_text(value: str) -> str:
    return re.sub(r"\s+", " ", app.repair_mojibake(str(value or ""))).strip()


def clean_meaning(value: str) -> str:
    return compact_text(value).strip("\"'")


def useful_approved_meaning(term: str, meaning: str, *, allow_name: bool = False) -> bool:
    cleaned = clean_meaning(meaning)
    if not cleaned:
        return False
    if allow_name and cleaned == "özel isim":
        return True
    if cleaned.lower() in GENERIC_MEANINGS:
        return False
    if app.is_suspicious_meaning(term, cleaned):
        return False
    return app.translation_looks_usable(cleaned)


def useful_curated_meaning(meaning: str) -> bool:
    cleaned = clean_meaning(meaning)
    if not cleaned:
        return False
    if cleaned.lower() in GENERIC_MEANINGS:
        return False
    if "?" in cleaned:
        return False
    return app.translation_looks_usable(cleaned)


def low_quality_existing_meaning(meaning: str) -> bool:
    cleaned = clean_meaning(meaning).lower()
    return cleaned in GENERIC_MEANINGS or cleaned.startswith("bağlama göre kullanılan ifade")


def ordered_candidates(term: str) -> list[str]:
    candidates: list[str] = []

    def add(value: str) -> None:
        cleaned = app.sanitize_word(value)
        if cleaned and cleaned not in candidates:
            candidates.append(cleaned)

    add(term)
    profile = app.resolve_cefr_entry(term)
    if profile and profile.get("lemma"):
        add(str(profile["lemma"]))
    for candidate in app.word_root_candidates(term):
        add(candidate)
    return candidates


def lookup_static_meaning(term: str) -> tuple[str, str, str] | None:
    for candidate in ordered_candidates(term):
        curated = clean_meaning(CURATED_BACKFILL_MEANINGS.get(candidate, ""))
        if useful_curated_meaning(curated):
            return curated, "curated", candidate

    maps: tuple[tuple[str, dict[str, str]], ...] = (
        ("override", app.WORD_MEANING_OVERRIDES),
        ("local", app.LOCAL_WORD_MAP),
        ("irregular", app.IRREGULAR_WORD_MAP),
        ("library", app.LIBRARY_WORD_MAP),
        ("extra", app.EXTRA_WORD_MAP),
    )
    for candidate in ordered_candidates(term):
        for source, mapping in maps:
            meaning = clean_meaning(mapping.get(candidate, ""))
            if useful_approved_meaning(term, meaning):
                return meaning, source, candidate
    return None


def resolve_word(term: str, sentence: str = "") -> TermResolution | None:
    cleaned = app.sanitize_word(term)
    if not cleaned:
        return None
    if app.is_library_name(cleaned):
        return TermResolution(
            term=cleaned,
            canonical=cleaned,
            meaning="özel isim",
            kind="word",
            source="backfill_name",
            confidence=0.72,
            sample_context=sentence,
        )

    static_hit = lookup_static_meaning(cleaned)
    if static_hit:
        meaning, source, canonical = static_hit
        return TermResolution(
            term=cleaned,
            canonical=canonical,
            meaning=meaning,
            kind="word",
            source=f"backfill_{source}",
            confidence=0.96 if source in {"override", "local", "irregular"} else 0.9,
            sample_context=sentence,
        )

    profile = app.resolve_cefr_entry(cleaned)
    lemma = str(profile.get("lemma") or cleaned) if profile else cleaned
    contextual = clean_meaning(app.infer_contextual_library_meaning(lemma, sentence))
    if useful_approved_meaning(cleaned, contextual):
        return TermResolution(
            term=cleaned,
            canonical=lemma,
            meaning=contextual,
            kind="word",
            source="backfill_contextual",
            confidence=0.82,
            sample_context=sentence,
        )

    inferred = clean_meaning(app.infer_turkish_meaning(lemma))
    if useful_approved_meaning(cleaned, inferred):
        return TermResolution(
            term=cleaned,
            canonical=lemma,
            meaning=inferred,
            kind="word",
            source="backfill_inferred",
            confidence=0.78,
            sample_context=sentence,
        )
    return None


def upsert_approved_term(resolution: TermResolution, *, dry_run: bool = False) -> str:
    existing = app.db_fetchone(
        "SELECT id, meaning FROM lexical_entries WHERE term = ?",
        (resolution.term,),
    )
    if existing:
        existing_meaning = clean_meaning(str(existing.get("meaning") or ""))
        if not dry_run:
            app.db_execute("DELETE FROM lexical_review_queue WHERE term = ?", (resolution.term,))
        if existing_meaning == resolution.meaning:
            return "existing"
        if low_quality_existing_meaning(existing_meaning):
            if dry_run:
                return "updated"
            app.db_execute(
                """
                UPDATE lexical_entries
                SET meaning = ?, kind = ?, source = ?, confidence = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    resolution.meaning,
                    resolution.kind,
                    resolution.source,
                    float(resolution.confidence),
                    app.now_iso(),
                    int(existing["id"]),
                ),
            )
            return "updated"
        return "conflict"
    if dry_run:
        return "inserted"
    timestamp = app.now_iso()
    app.db_execute(
        """
        INSERT INTO lexical_entries (term, meaning, kind, source, confidence, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            resolution.term,
            resolution.meaning,
            resolution.kind,
            resolution.source,
            float(resolution.confidence),
            timestamp,
            timestamp,
        ),
    )
    app.db_execute("DELETE FROM lexical_review_queue WHERE term = ?", (resolution.term,))
    return "inserted"


def execute_many(query: str, rows: list[tuple[Any, ...]]) -> None:
    if not rows:
        return
    if app.USE_POSTGRES:
        if app.psycopg is None:
            raise RuntimeError("psycopg is required for PostgreSQL connections.")
        with app.psycopg.connect(app.DATABASE_URL, row_factory=app.dict_row) as conn:
            with conn.cursor() as cur:
                cur.executemany(app._pg_query(query), rows)
            conn.commit()
        return
    connection = sqlite3.connect(app.DB_PATH)
    try:
        connection.executemany(query, rows)
        connection.commit()
    finally:
        connection.close()


def queue_missing_term(
    term: str,
    canonical: str,
    *,
    sample_context: str = "",
    occurrence_count: int = 1,
    dry_run: bool = False,
) -> str:
    cleaned_term = app.sanitize_word(term)
    cleaned_canonical = app.sanitize_word(canonical) or cleaned_term
    if not cleaned_term:
        return "skipped"
    if app.db_fetchone("SELECT id FROM lexical_entries WHERE term = ?", (cleaned_term,)):
        return "existing"
    existing = app.db_fetchone(
        "SELECT id, occurrence_count FROM lexical_review_queue WHERE term = ? AND meaning = ?",
        (cleaned_term, REVIEW_REQUIRED_MEANING),
    )
    if existing:
        if dry_run:
            return "updated"
        app.db_execute(
            """
            UPDATE lexical_review_queue
            SET occurrence_count = ?, sample_context = COALESCE(NULLIF(?, ''), sample_context), updated_at = ?
            WHERE id = ?
            """,
            (
                int(existing.get("occurrence_count") or 0) + max(1, occurrence_count),
                sample_context[:500],
                app.now_iso(),
                int(existing["id"]),
            ),
        )
        return "updated"
    if dry_run:
        return "inserted"
    timestamp = app.now_iso()
    app.db_execute(
        """
        INSERT INTO lexical_review_queue (
            term, canonical, meaning, kind, source, status, confidence,
            sample_context, occurrence_count, created_at, updated_at
        )
        VALUES (?, ?, ?, 'word', 'backfill_missing', 'pending', 0.35, ?, ?, ?, ?)
        """,
        (
            cleaned_term,
            cleaned_canonical,
            REVIEW_REQUIRED_MEANING,
            sample_context[:500],
            max(1, occurrence_count),
            timestamp,
            timestamp,
        ),
    )
    return "inserted"


def published_reading_items() -> list[dict[str, Any]]:
    rows = app.db_fetchall(
        """
        SELECT id, title, text, level, topic
        FROM readings
        WHERE is_published = 1
        ORDER BY id
        """
    )
    if rows:
        return rows
    return app.parse_curated_readings_file()


def resolve_terms_from_texts(text_items: Iterable[dict[str, Any]]) -> tuple[dict[str, TermResolution], dict[str, TermResolution], Counter[str], LexicalBackfillReport]:
    approved: dict[str, TermResolution] = {}
    missing: dict[str, TermResolution] = {}
    occurrences: Counter[str] = Counter()
    report = LexicalBackfillReport()

    for item in text_items:
        text = str(item.get("text") or "")
        if not text.strip():
            continue
        report.readings_scanned += 1
        phrase_matches = match_phrases(text, *app.runtime_lexical_maps())
        covered_tokens = covered_token_indexes(phrase_matches)

        for match in phrase_matches:
            term = app.sanitize_word(match.canonical or match.key)
            if not term:
                continue
            meaning = clean_meaning(match.meaning)
            occurrences[term] += 1
            sentence = compact_text(app.find_sentence_for_word(text, match.surface or term))
            if useful_approved_meaning(term, meaning):
                approved.setdefault(
                    term,
                    TermResolution(
                        term=term,
                        canonical=app.sanitize_word(match.canonical or term),
                        meaning=meaning,
                        kind="phrase",
                        source=f"backfill_phrase_{match.source}",
                        confidence=0.94,
                        sample_context=sentence,
                    ),
                )
                missing.pop(term, None)
                continue
            word_resolution = resolve_word(term, sentence)
            if word_resolution:
                word_resolution.kind = "phrase"
                approved.setdefault(term, word_resolution)
                missing.pop(term, None)
            elif term not in approved:
                missing.setdefault(
                    term,
                    TermResolution(term, term, REVIEW_REQUIRED_MEANING, "phrase", "backfill_missing", 0.35, sentence),
                )

        for index, token in enumerate(token_records(text)):
            report.tokens_seen += 1
            if index in covered_tokens:
                continue
            term = app.sanitize_word(str(token.get("key") or ""))
            if not term:
                continue
            occurrences[term] += 1
            if len(term) <= 1:
                report.skipped_short += 1
                continue
            if term in approved:
                continue
            sentence = compact_text(app.find_sentence_for_word(text, term))
            resolution = resolve_word(term, sentence)
            if resolution:
                approved[term] = resolution
                missing.pop(term, None)
                continue
            if len(term) <= 2:
                report.skipped_short += 1
                continue
            canonical = ordered_candidates(term)[-1] if ordered_candidates(term) else term
            missing.setdefault(
                term,
                TermResolution(term, canonical, REVIEW_REQUIRED_MEANING, "word", "backfill_missing", 0.35, sentence),
            )

    report.unique_terms_seen = len(occurrences)
    return approved, missing, occurrences, report


def backfill_lexical_entries(
    text_items: Iterable[dict[str, Any]] | None = None,
    *,
    dry_run: bool = False,
    limit: int | None = None,
) -> LexicalBackfillReport:
    items = list(text_items if text_items is not None else published_reading_items())
    if limit is not None:
        items = items[: max(0, int(limit))]
    approved, missing, occurrences, report = resolve_terms_from_texts(items)
    report.dry_run = dry_run
    existing_entries = {
        str(row.get("term") or ""): row
        for row in app.db_fetchall("SELECT id, term, meaning FROM lexical_entries")
        if str(row.get("term") or "")
    }
    existing_queue = {
        (str(row.get("term") or ""), str(row.get("meaning") or "")): row
        for row in app.db_fetchall("SELECT id, term, meaning, occurrence_count FROM lexical_review_queue")
        if str(row.get("term") or "")
    }
    timestamp = app.now_iso()
    entries_to_insert: list[tuple[Any, ...]] = []
    entries_to_update: list[tuple[Any, ...]] = []
    queue_terms_to_delete: set[str] = set()

    for resolution in sorted(approved.values(), key=lambda item: item.term):
        if resolution.meaning.lower() in GENERIC_MEANINGS:
            report.skipped_generic += 1
            continue
        existing = existing_entries.get(resolution.term)
        if not existing:
            report.approved_inserted += 1
            queue_terms_to_delete.add(resolution.term)
            entries_to_insert.append(
                (
                    resolution.term,
                    resolution.meaning,
                    resolution.kind,
                    resolution.source,
                    float(resolution.confidence),
                    timestamp,
                    timestamp,
                )
            )
            continue
        existing_meaning = clean_meaning(str(existing.get("meaning") or ""))
        queue_terms_to_delete.add(resolution.term)
        if existing_meaning == resolution.meaning:
            report.approved_existing += 1
        elif low_quality_existing_meaning(existing_meaning):
            report.approved_updated += 1
            entries_to_update.append(
                (
                    resolution.meaning,
                    resolution.kind,
                    resolution.source,
                    float(resolution.confidence),
                    timestamp,
                    int(existing["id"]),
                )
            )
        else:
            report.approved_conflicts += 1

    if not dry_run:
        execute_many(
            """
            INSERT INTO lexical_entries (term, meaning, kind, source, confidence, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            entries_to_insert,
        )
        execute_many(
            """
            UPDATE lexical_entries
            SET meaning = ?, kind = ?, source = ?, confidence = ?, updated_at = ?
            WHERE id = ?
            """,
            entries_to_update,
        )
        execute_many(
            "DELETE FROM lexical_review_queue WHERE term = ?",
            [(term,) for term in sorted(queue_terms_to_delete)],
        )

    queue_to_insert: list[tuple[Any, ...]] = []
    queue_to_update: list[tuple[Any, ...]] = []
    for resolution in sorted(missing.values(), key=lambda item: item.term):
        if resolution.term in existing_entries:
            report.queued_existing += 1
            continue
        key = (resolution.term, REVIEW_REQUIRED_MEANING)
        existing = existing_queue.get(key)
        occurrence_count = max(1, occurrences.get(resolution.term, 1))
        if existing:
            report.queued_updated += 1
            queue_to_update.append(
                (
                    int(existing.get("occurrence_count") or 0) + occurrence_count,
                    resolution.sample_context[:500],
                    timestamp,
                    int(existing["id"]),
                )
            )
        else:
            report.queued_inserted += 1
            queue_to_insert.append(
                (
                    resolution.term,
                    resolution.canonical,
                    REVIEW_REQUIRED_MEANING,
                    resolution.sample_context[:500],
                    occurrence_count,
                    timestamp,
                    timestamp,
                )
            )

    if not dry_run:
        execute_many(
            """
            UPDATE lexical_review_queue
            SET occurrence_count = ?, sample_context = COALESCE(NULLIF(?, ''), sample_context), updated_at = ?
            WHERE id = ?
            """,
            queue_to_update,
        )
        execute_many(
            """
            INSERT INTO lexical_review_queue (
                term, canonical, meaning, kind, source, status, confidence,
                sample_context, occurrence_count, created_at, updated_at
            )
            VALUES (?, ?, ?, 'word', 'backfill_missing', 'pending', 0.35, ?, ?, ?, ?)
            """,
            queue_to_insert,
        )

    app.get_approved_lexical_map(force=True)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Backfill ReadWave lexical_entries from published readings.")
    parser.add_argument("--dry-run", action="store_true", help="Compute the report without writing to the database.")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of published readings to scan.")
    parser.add_argument("--json", action="store_true", help="Print a JSON report.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    report = backfill_lexical_entries(dry_run=bool(args.dry_run), limit=args.limit)
    payload = asdict(report)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    for key, value in payload.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
