const LEVEL_CONFIG = {
  A1: { min: 60, max: 100, hint: "Very simple and everyday" },
  A2: { min: 90, max: 130, hint: "Simple, clear, and familiar" },
  B1: { min: 120, max: 170, hint: "Natural and comfortably paced" },
  B2: { min: 150, max: 220, hint: "Richer but still easy to read" },
  C1: { min: 180, max: 260, hint: "Advanced, natural, and detailed" },
  C2: { min: 190, max: 280, hint: "Highly advanced and nuanced" },
};

const TOPIC_KEYWORDS = {
  Random: ["story", "daily", "idea", "change"],
  Arts: ["studio", "practice", "composition", "form"],
  Communication: ["message", "feedback", "clarity", "conversation"],
  Culture: ["ritual", "community", "memory", "tradition"],
  "Daily Life": ["morning", "routine", "balance", "habit"],
  Education: ["student", "teacher", "study", "exam"],
  Environment: ["energy", "waste", "climate", "action"],
  Finance: ["budget", "saving", "expense", "plan"],
  Food: ["meal", "kitchen", "nutrition", "recipe"],
  Health: ["exercise", "sleep", "balance", "habit"],
  Media: ["article", "story", "platform", "audience"],
  Psychology: ["attention", "emotion", "habit", "stress"],
  "Public Services": ["transport", "service", "access", "public"],
  Science: ["science", "evidence", "method", "observation"],
  Technology: ["smartphone", "internet", "screen", "tools"],
  Travel: ["travel", "city", "tourism", "journey"],
  "Work Life": ["meeting", "project", "office", "email"],
};

const TOPIC_ORDER = [
  "Random",
  "Education",
  "Travel",
  "Work Life",
  "Technology",
  "Health",
  "Daily Life",
  "Environment",
  "Communication",
  "Food",
  "Public Services",
  "Media",
  "Science",
  "Psychology",
  "Finance",
  "Arts",
  "Culture",
];

const GUEST_FLAG_KEY = "readlex_guest";
const THEME_STORAGE_KEY = "readlex_theme";

const state = {
  text: "",
  glossary: {},
  selectedWord: "",
  lastPayload: null,
  contentSource: "library",
  loadingWord: false,
  pendingFlip: false,
  dismissedMobileWord: "",
  authMode: "login",
  user: null,
  stats: {
    saved_words: 0,
    mastered_words: 0,
    saved_today: 0,
    readings_today: 0,
    total_readings: 0,
    daily_goal: 5,
    streak: 0,
    hard_words: 0,
  },
  recentWords: [],
  readingHistory: [],
  progressHistory: [],
  social: { friends: [], incoming: [], outgoing: [], suggestions: [], cheers_received: 0 },
  quiz: null,
  quizMode: "saved",
  libraryView: null,
  libraryStats: null,
  quizStats: { answered: 0, correct: 0, streak: 0 },
  loggingOut: false,
  hasEnteredApp: window.sessionStorage.getItem(GUEST_FLAG_KEY) === "1",
  viewMode: window.innerWidth < 860 ? "mobile" : "web",
};

const persistedSelectionKeys = new Set();
let sessionRefreshTimer = null;
let sessionRefreshInflight = null;

function emptyStats() {
  return {
    saved_words: 0,
    mastered_words: 0,
    saved_today: 0,
    readings_today: 0,
    total_readings: 0,
    daily_goal: 5,
    streak: 0,
    hard_words: 0,
  };
}

const $ = (selector) => document.querySelector(selector);
const welcomeGateEl = $("#welcomeGate");
const gateAuthCardEl = $("#gateAuthCard");
const gateLoginForm = $("#gateLoginForm");
const gateLoginUsernameEl = $("#gateLoginUsername");
const gateLoginPasswordEl = $("#gateLoginPassword");
const gateLoginErrorEl = $("#gateLoginError");
const gateLoginSubmitBtn = $("#gateLoginSubmitBtn");
const gateRegisterForm = $("#gateRegisterForm");
const gateRegisterUsernameEl = $("#gateRegisterUsername");
const gateRegisterPasswordEl = $("#gateRegisterPassword");
const gateRegisterErrorEl = $("#gateRegisterError");
const gateRegisterSubmitBtn = $("#gateRegisterSubmitBtn");
const gateShowLoginBtn = $("#gateShowLoginBtn");
const gateShowRegisterBtn = $("#gateShowRegisterBtn");
const continueGuestBtn = $("#continueGuestBtn");
const themeToggleBtn = $("#themeToggleBtn");
const profileTipTextEl = $("#profileTipText");
const generateForm = $("#generate-form");
const manualForm = $("#manual-form");
const authCardEl = $("#authCard");
const levelEl = $("#level");
const topicEl = $("#topic");
const lengthEl = $("#lengthTarget");
const lengthValueEl = $("#lengthValue");
const levelHintEl = $("#levelHint");
const keywordsEl = $("#keywords");
const keywordChipsEl = $("#keywordChips");
const keywordCountEl = $("#keywordCount");
const generateErrorEl = $("#generateError");
const previewStateEl = $("#previewState");
const readingExperienceEl = $("#readingExperience");
const metaTagsEl = $("#metaTags");
const readingTitleEl = $("#readingTitle");
const readingBodyEl = $("#readingBody");
const flipCardEl = $("#flipCard");
const selectedWordEl = $("#selectedWord");
const selectedMeaningEl = $("#selectedMeaning");
const selectedContextEl = $("#selectedContext");
const selectedExampleEl = $("#selectedExample");
const selectedCollocationsEl = $("#selectedCollocations");
const manualResultEl = $("#manualResult");
const manualWordEl = $("#manualWord");
const regenBtn = $("#regenBtn");
const clearBtn = $("#clearBtn");
const setupLevelBadgeEl = $("#setupLevelBadge");
const setupLengthBadgeEl = $("#setupLengthBadge");
const setupSummaryEl = $("#setupSummary");
const authGuestEl = $("#authGuest");
const authUserEl = $("#authUser");
const authLoginForm = $("#authLoginForm");
const authLoginUsernameEl = $("#authLoginUsername");
const authLoginPasswordEl = $("#authLoginPassword");
const authLoginErrorEl = $("#authLoginError");
const authLoginSubmitBtn = $("#authLoginSubmitBtn");
const authRegisterForm = $("#authRegisterForm");
const authRegisterUsernameEl = $("#authRegisterUsername");
const authRegisterPasswordEl = $("#authRegisterPassword");
const authRegisterErrorEl = $("#authRegisterError");
const authRegisterSubmitBtn = $("#authRegisterSubmitBtn");
const showLoginBtn = $("#showLoginBtn");
const showRegisterBtn = $("#showRegisterBtn");
const logoutBtn = $("#logoutBtn");
const accountNameEl = $("#accountName");
const savedWordsCountEl = $("#savedWordsCount");
const masteredWordsCountEl = $("#masteredWordsCount");
const dailyGoalTextEl = $("#dailyGoalText");
const streakBadgeEl = $("#streakBadge");
const goalBarFillEl = $("#goalBarFill");
const hardWordsTextEl = $("#hardWordsText");
const totalReadingsTextEl = $("#totalReadingsText");
const todayReadingsTextEl = $("#todayReadingsText");
const todayWordsTextEl = $("#todayWordsText");
const progressHistoryListEl = $("#progressHistoryList");
const readingHistoryListEl = $("#readingHistoryList");
const socialAddFormEl = $("#socialAddForm");
const socialUsernameInputEl = $("#socialUsernameInput");
const socialAddBtn = $("#socialAddBtn");
const socialGuestNoteEl = $("#socialGuestNote");
const socialFriendCountEl = $("#socialFriendCount");
const socialIncomingListEl = $("#socialIncomingList");
const socialFriendsListEl = $("#socialFriendsList");
const socialSuggestionsListEl = $("#socialSuggestionsList");
const savedWordsEmptyEl = $("#savedWordsEmpty");
const savedWordsListEl = $("#savedWordsList");
const clearSavedWordsBtn = $("#clearSavedWordsBtn");
const randomizeSavedWordsBtn = $("#randomizeSavedWordsBtn");
const savedWordsActionsEl = $("#savedWordsActions");
const savedWordsMetaEl = $("#savedWordsMeta");
const quizEmptyEl = $("#quizEmpty");
const quizCardEl = $("#quizCard");
const quizPromptEl = $("#quizPrompt");
const quizSentenceEl = $("#quizSentence");
const quizOptionsEl = $("#quizOptions");
const quizFeedbackEl = $("#quizFeedback");
const nextQuizBtn = $("#nextQuizBtn");
const quizAnsweredBadgeEl = $("#quizAnsweredBadge");
const quizStreakBadgeEl = $("#quizStreakBadge");
const quizTypeBadgeEl = $("#quizTypeBadge");
const quizModeSavedBtn = $("#quizModeSavedBtn");
const quizModeHardBtn = $("#quizModeHardBtn");
const quizModeReadingBtn = $("#quizModeReadingBtn");
const navMenuShellEl = $("#navMenuShell");
const navMenuTriggerEl = $("#navMenuTrigger");
const navMenuEl = $("#navMenu");
const navMenuSwitchEls = Array.from(document.querySelectorAll("[data-menu-category]"));
const navMenuPanelEls = Array.from(document.querySelectorAll("[data-menu-panel]"));
const openProfileBtn = $("#openProfileBtn");
const profileAvatarBtn = $("#profileAvatarBtn");
const profileTriggerInitialsEl = $("#profileTriggerInitials");
const openProgressBtn = $("#openProgressBtn");
const openSocialBtn = $("#openSocialBtn");
const openSavedWordsBtn = $("#openSavedWordsBtn");
const openQuizBtn = $("#openQuizBtn");
const openManualHelpBtn = $("#openManualHelpBtn");
const openInfoBtn = $("#openInfoBtn");
const libraryOverlayEl = $("#libraryOverlay");
const libraryPanelEl = $("#libraryPanel");
const profilePanelEl = $("#profilePanel");
const progressPanelEl = $("#progressPanel");
const socialPanelEl = $("#socialPanel");
const savedWordsPanelEl = $("#savedWordsPanel");
const quizPanelEl = $("#quizPanel");
const manualHelpPanelEl = $("#manualHelpPanel");
const infoPanelEl = $("#infoPanel");
const libraryTitleEl = $("#libraryTitle");
const libraryKickerEl = $("#libraryKicker");
const closeLibraryBtn = $("#closeLibraryBtn");
const libraryHandleBtn = $("#libraryHandleBtn");
const libraryPanelScrollEl = $("#libraryPanel");
const sourceSwitchEl = $("#sourceSwitch");
const libraryModeHintEl = $("#libraryModeHint");
const libraryControlsEl = $("#libraryControls");
const libraryLevelEl = $("#libraryLevel");
const libraryTopicEl = $("#libraryTopic");
const aiControlsEl = $("#aiControls");
const libraryCountBadgeEl = $("#libraryCountBadge");
const mobileWordSheetEl = $("#mobileWordSheet");
const mobileWordBackdropEl = $("#mobileWordBackdrop");
const closeMobileWordBtn = $("#closeMobileWordBtn");
const mobileWordHandleBtn = $("#mobileWordHandleBtn");
const mobileWordPanelEl = $(".mobile-word-panel");
const mobileWordTitleEl = $("#mobileWordTitle");
const mobileWordMeaningEl = $("#mobileWordMeaning");
const mobileWordContextEl = $("#mobileWordContext");
const mobileWordExampleEl = $("#mobileWordExample");
const pronounceWordBtn = $("#pronounceWordBtn");
const mobilePronounceWordBtn = $("#mobilePronounceWordBtn");
let mobileWordCollocationsEl = $("#mobileWordCollocations");
const authToggleEls = Array.from(document.querySelectorAll("[data-auth-toggle]"));
const MENU_DESKTOP_QUERY = window.matchMedia("(hover: hover) and (pointer: fine)");
let navMenuCloseTimer = null;

if (!mobileWordCollocationsEl && mobileWordExampleEl) {
  const hostBlock = mobileWordExampleEl.closest(".insight-block")?.parentElement;
  if (hostBlock) {
    const block = document.createElement("div");
    block.className = "insight-block";
    block.innerHTML = `
      <span class="mini-label">Collocations</span>
      <div id="mobileWordCollocations" class="collocation-list">
        <span class="helper-note">Useful word pairs appear here after you choose a word.</span>
      </div>
    `;
    hostBlock.appendChild(block);
    mobileWordCollocationsEl = $("#mobileWordCollocations");
  }
}

function applyTheme(mode) {
  const isDark = mode === "dark";
  document.body.classList.toggle("dark-mode", isDark);
  themeToggleBtn?.setAttribute("aria-pressed", String(isDark));
  window.localStorage.setItem(THEME_STORAGE_KEY, isDark ? "dark" : "light");
}

function toggleTheme() {
  const nextMode = document.body.classList.contains("dark-mode") ? "light" : "dark";
  applyTheme(nextMode);
}

async function parseApiResponse(response) {
  const raw = await response.text();
  try {
    return { ok: response.ok, status: response.status, data: JSON.parse(raw) };
  } catch {
    return { ok: response.ok, status: response.status, data: { detail: raw || "Unknown error" } };
  }
}

async function apiFetch(url, options = {}) {
  const response = await fetch(url, {
    credentials: "include",
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  return parseApiResponse(response);
}

function getToastLayer() {
  let layer = document.querySelector(".toast-layer");
  if (layer) return layer;
  layer = document.createElement("div");
  layer.className = "toast-layer";
  document.body.appendChild(layer);
  return layer;
}

function clearToasts(scope = "global") {
  const selector = scope === "global" ? '.site-toast[data-scope="global"]' : `.site-toast[data-scope="${scope}"]`;
  document.querySelectorAll(selector).forEach((toast) => toast.remove());
}

function showToast(message, { variant = "error", scope = "global", duration = 4200 } = {}) {
  const textValue = String(message || "").trim();
  if (!textValue) return;
  const layer = getToastLayer();
  const selector = scope === "global" ? '.site-toast[data-scope="global"]' : `.site-toast[data-scope="${scope}"]`;
  const existing = layer.querySelector(selector);
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.className = `site-toast site-toast-${variant}`;
  toast.dataset.scope = scope;
  toast.setAttribute("role", "status");
  toast.setAttribute("aria-live", "polite");

  const text = document.createElement("div");
  text.className = "site-toast-text";
  text.textContent = textValue;

  const closeBtn = document.createElement("button");
  closeBtn.className = "site-toast-close";
  closeBtn.type = "button";
  closeBtn.setAttribute("aria-label", "Close");
  closeBtn.textContent = "x";
  closeBtn.addEventListener("click", () => toast.remove());

  toast.append(text, closeBtn);
  layer.appendChild(toast);
  window.setTimeout(() => toast.remove(), duration);
}

function parseKeywords(raw) {
  const seen = new Set();
  return raw
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean)
    .filter((item) => {
      const lowered = item.toLowerCase();
      if (seen.has(lowered)) return false;
      seen.add(lowered);
      return true;
    });
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function highlightSelectedWord(text, selectedWord) {
  const escapedText = escapeHtml(text || "");
  if (!selectedWord) return escapedText.replace(/\n/g, "<br>");
  const pattern = new RegExp(`\\b(${selectedWord.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})\\b`, "gi");
  return escapedText.replace(pattern, '<strong class="inline-highlight">$1</strong>').replace(/\n/g, "<br>");
}

function buildInsightHtml(
  rawText,
  selectedWord,
  { emptyText = "", collapsedLines = 3, maxLines = 18 } = {}
) {
  const base = String(rawText || "").trim();
  if (!base) {
    return `<span class="helper-note">${escapeHtml(emptyText)}</span>`;
  }

  const lines = base
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .slice(0, maxLines);

  const highlighted = lines.map((line) => highlightSelectedWord(line, selectedWord));
  const preview = highlighted.slice(0, collapsedLines);
  const rest = highlighted.slice(collapsedLines);

  const previewHtml = `<ul class="insight-list">${preview.map((line) => `<li>${line}</li>`).join("")}</ul>`;
  if (!rest.length) return previewHtml;

  const restHtml = `<ul class="insight-list">${rest.map((line) => `<li>${line}</li>`).join("")}</ul>`;
  return `
    <details class="insight-details">
      <summary>Show more</summary>
      ${previewHtml}
      ${restHtml}
    </details>
  `.trim();
}

function tokenizeText(text) {
  return text.match(/[A-Za-z]+(?:['-][A-Za-z]+)*|\s+|[^A-Za-z\s]/g) || [];
}

const PHRASE_PREFERENCES = new Set([
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
  "work life",
  "work life balance",
  "social media",
  "mental health",
  "climate change",
  "space exploration",
  "space tourism",
  "basic income",
  "universal basic income",
  "blue collar",
  "white collar",
  "open plan",
  "mixed use",
  "face to face",
  "in conclusion",
  "to summarize",
  "for instance",
  "in contrast",
  "in reality",
  "in summary",
  "in light of",
  "due to",
  "rather than",
  "regardless of",
  "in favor of",
  "genetic modification",
  "human embryos",
  "science fiction",
  "gene editing",
  "designer babies",
  "human genome",
  "digital detox",
  "open plan offices",
  "biophilic design",
  "natural light",
  "social cohesion",
  "solar radiation management",
  "analysis paralysis",
  "buyer's remorse",
  "mother tongue",
  "gig economy",
  "short term contracts",
  "independent contractors",
  "collective bargaining",
  "artificial general intelligence",
  "structural unemployment",
  "machine learning",
  "mri scans",
  "ct scans",
  "orbital debris",
  "kessler syndrome",
  "space commercialization",
  "post truth era",
  "false equivalence",
  "restorative justice",
  "cognitive enhancers",
  "smart drugs",
  "surveillance capitalism",
  "personal data",
  "hate speech",
  "militant democracy",
  "de extinction",
]);

const PHRASE_LEMMA_OVERRIDES = {
  broke: "break",
  broken: "break",
  gave: "give",
  given: "give",
  looked: "look",
  ran: "run",
  taken: "take",
  took: "take",
  turned: "turn",
  worked: "work",
  set: "set",
  calmed: "calm",
  figured: "figure",
  getting: "get",
  got: "get",
};

function findAdjacentWordButton(fromEl, direction) {
  let node = direction === "prev" ? fromEl.previousSibling : fromEl.nextSibling;
  while (node) {
    if (node.nodeType === Node.ELEMENT_NODE && node.classList?.contains("word")) return node;
    node = direction === "prev" ? node.previousSibling : node.nextSibling;
  }
  return null;
}

function getWordByOffset(fromEl, steps) {
  let node = fromEl;
  const direction = steps >= 0 ? "next" : "prev";
  let remaining = Math.abs(steps);
  while (remaining > 0 && node) {
    node = findAdjacentWordButton(node, direction);
    remaining -= 1;
  }
  return node?.dataset?.word || "";
}

function normalizePhraseWord(word) {
  const raw = String(word || "").toLowerCase().trim();
  if (!raw) return "";
  if (PHRASE_LEMMA_OVERRIDES[raw]) return PHRASE_LEMMA_OVERRIDES[raw];
  if (raw.endsWith("ing") && raw.length > 5) return raw.slice(0, -3);
  if (raw.endsWith("ied") && raw.length > 4) return `${raw.slice(0, -3)}y`;
  if (raw.endsWith("ed") && raw.length > 4) {
    const base = raw.slice(0, -2);
    if (base.endsWith(base.slice(-1).repeat(1)) && /[b-df-hj-np-tv-z]$/.test(base) && base.length > 2) {
      return base.slice(0, -1);
    }
    return base;
  }
  return raw;
}

function normalizePhraseCandidate(candidate) {
  return String(candidate || "")
    .split(/\s+/)
    .filter(Boolean)
    .map((part) => normalizePhraseWord(part))
    .join(" ");
}

function getGlossaryPhraseKey(candidate) {
  const raw = String(candidate || "").toLowerCase().trim().replace(/\s+/g, " ");
  if (!raw) return "";
  const variants = [
    raw,
    raw.replace(/-/g, " "),
    raw.replace(/\s+/g, "-"),
    normalizePhraseCandidate(raw),
    normalizePhraseCandidate(raw.replace(/-/g, " ")),
  ];
  for (const variant of variants) {
    if (variant && state.glossary?.[variant]) return variant;
  }
  return "";
}

function getPhraseCandidatesAround(buttonEl, radius = 4) {
  const words = [];
  for (let offset = -radius; offset <= radius; offset += 1) {
    const word = offset === 0 ? buttonEl.dataset.word : getWordByOffset(buttonEl, offset);
    words.push({ offset, word });
  }
  const currentIndex = radius;
  const candidates = [];
  for (let length = radius + 1; length >= 2; length -= 1) {
    for (let start = 0; start <= words.length - length; start += 1) {
      const end = start + length - 1;
      if (start > currentIndex || end < currentIndex) continue;
      const parts = words.slice(start, start + length).map((item) => item.word);
      if (parts.some((part) => !part)) continue;
      candidates.push(parts.join(" "));
    }
  }
  return candidates;
}

function resolvePreferredPhrase(buttonEl) {
  if (!buttonEl?.dataset?.word) return "";
  const current = buttonEl.dataset.word;
  for (const candidate of getPhraseCandidatesAround(buttonEl)) {
    const glossaryKey = getGlossaryPhraseKey(candidate);
    if (glossaryKey) return glossaryKey;
  }
  const prevWord = getWordByOffset(buttonEl, -1);
  const prevPrevWord = getWordByOffset(buttonEl, -2);
  const nextWord = getWordByOffset(buttonEl, 1);
  const nextNextWord = getWordByOffset(buttonEl, 2);
  const candidates = [
    `${current} ${nextWord} ${nextNextWord}`.trim(),
    `${prevWord} ${current} ${nextWord}`.trim(),
    `${prevPrevWord} ${prevWord} ${current}`.trim(),
    `${current} ${nextWord}`.trim(),
    `${prevWord} ${current}`.trim(),
  ].filter((item) => item && !item.includes("  "));

  for (const candidate of candidates) {
    if (PHRASE_PREFERENCES.has(candidate)) return candidate;
    const normalizedCandidate = normalizePhraseCandidate(candidate);
    if (PHRASE_PREFERENCES.has(normalizedCandidate)) return normalizedCandidate;
  }
  return current;
}

function renderCollocations(targetEl, collocations = []) {
  if (!targetEl) return;
  if (!collocations.length) {
    targetEl.innerHTML = `<span class="helper-note">Useful word pairs appear here after you choose a word.</span>`;
    return;
  }
  targetEl.innerHTML = collocations
    .map((item) => `<span class="chip collocation-chip">${escapeHtml(item)}</span>`)
    .join("");
}

function playPronunciation(word) {
  if (!word || !("speechSynthesis" in window)) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(word);
  utterance.lang = "en-US";
  utterance.rate = 0.95;
  window.speechSynthesis.speak(utterance);
}

function buildReadingQuizQuestion(excludeWord = "") {
  const glossaryEntries = Object.entries(state.glossary || {}).filter(([, detail]) => detail?.turkish);
  if (glossaryEntries.length < 4) return null;
  const filtered = excludeWord ? glossaryEntries.filter(([word]) => word !== excludeWord) : glossaryEntries;
  const pool = filtered.length >= 4 ? filtered : glossaryEntries;
  const target = pool[Math.floor(Math.random() * pool.length)];
  const [word, detail] = target;
  const turkish = String(detail.turkish || "").trim();
  const exampleSource = String(detail.example || "").split("\n").find((line) => line.trim()) || "";
  const plainExample = exampleSource.replace(/^\d+\.\s*/, "").replace(/\s*\([^)]*\)\s*$/, "").trim();
  const canMakeBlank = plainExample && new RegExp(`\\b${word}\\b`, "i").test(plainExample);
  if (canMakeBlank && Math.random() < 0.5) {
    const sentence = plainExample.replace(new RegExp(`\\b${word}\\b`, "i"), "_____");
    const distractors = glossaryEntries
      .filter(([candidate]) => candidate !== word)
      .map(([candidate]) => candidate)
      .slice(0, 12)
      .sort(() => Math.random() - 0.5)
      .slice(0, 3);
    const options = [...new Set([...distractors, word])].sort(() => Math.random() - 0.5);
    return {
      word_id: `reading-${word}`,
      question_type: "blank",
      question: "Which word best completes the sentence?",
      sentence,
      word,
      answer: word,
      options,
      context: detail.context || "",
      example: detail.example || "",
      mode: "reading",
    };
  }
  const distractors = glossaryEntries
    .filter(([candidate, candidateDetail]) => candidate !== word && candidateDetail?.turkish)
    .map(([, candidateDetail]) => String(candidateDetail.turkish).trim())
    .filter(Boolean)
    .slice(0, 12)
    .sort(() => Math.random() - 0.5)
    .slice(0, 3);
  const options = [...new Set([...distractors, turkish])].sort(() => Math.random() - 0.5);
  return {
    word_id: `reading-${word}`,
    question_type: "meaning",
    question: `What is the best Turkish meaning of "${word}"?`,
    word,
    answer: turkish,
    options,
    context: detail.context || "",
    example: detail.example || "",
    mode: "reading",
  };
}

function setLoading(button, loadingText, isLoading) {
  if (!button) return;
  if (isLoading) {
    button.dataset.original = button.textContent;
    button.disabled = true;
    button.textContent = loadingText;
  } else {
    button.disabled = false;
    button.textContent = button.dataset.original || button.textContent;
  }
}

function showError(message) {
  generateErrorEl.textContent = "";
  generateErrorEl.classList.add("hidden");
  showToast(message, { variant: "error", scope: "generate" });
}

function clearError() {
  generateErrorEl.textContent = "";
  generateErrorEl.classList.add("hidden");
  clearToasts("generate");
}

function updateSetupSummary() {
  const cfg = LEVEL_CONFIG[levelEl.value];
  setupLevelBadgeEl.textContent = `${levelEl.value} · ${cfg.hint}`;
  setupLengthBadgeEl.textContent = `Around ${lengthEl.value} words`;
}

function updateRangeVisual() {
  const min = Number(lengthEl.min || 0);
  const max = Number(lengthEl.max || 100);
  const value = Number(lengthEl.value || min);
  const ratio = max === min ? 100 : ((value - min) / (max - min)) * 100;
  lengthEl.style.setProperty("--track-fill", `${ratio}%`);
}

function syncLevelPickers(value) {
  levelEl.value = value;
  if (libraryLevelEl) libraryLevelEl.value = value;
}

function syncTopicPickers(value) {
  topicEl.value = value;
  if (libraryTopicEl) libraryTopicEl.value = value;
}

function updateLevelUi() {
  const cfg = LEVEL_CONFIG[levelEl.value];
  lengthEl.min = cfg.min;
  lengthEl.max = cfg.max;
  if (Number(lengthEl.value) < cfg.min || Number(lengthEl.value) > cfg.max) {
    lengthEl.value = Math.round((cfg.min + cfg.max) / 20) * 10;
  }
  lengthValueEl.textContent = lengthEl.value;
  levelHintEl.textContent = cfg.hint;
  updateSetupSummary();
  updateRangeVisual();
  syncLevelPickers(levelEl.value);
}

function updateTopicDefaults() {
  const preset = TOPIC_KEYWORDS[topicEl.value];
  if (preset && state.contentSource === "ai") keywordsEl.value = preset.join(", ");
  renderKeywordChips();
  syncTopicPickers(topicEl.value);
}

function renderKeywordChips() {
  const keywords = parseKeywords(keywordsEl.value);
  keywordChipsEl.innerHTML = keywords.map((word) => `<span class="chip">${escapeHtml(word)}</span>`).join("");
  keywordCountEl.textContent = `${keywords.length} words`;
}

function updateSourceModeUi() {
  const isLibrary = state.contentSource === "library";
  document.body.classList.toggle("library-mode", isLibrary);
  document.body.classList.toggle("ai-mode", !isLibrary);
  setupSummaryEl.classList.toggle("hidden", isLibrary);
  libraryModeHintEl.classList.toggle("hidden", !isLibrary);
  libraryCountBadgeEl?.classList.toggle("hidden", !isLibrary);
  libraryControlsEl.classList.toggle("hidden", !isLibrary);
  aiControlsEl.classList.toggle("hidden", isLibrary);
  $("#generateBtn").textContent = isLibrary ? "Get Reading" : "Generate Text";
  regenBtn.textContent = isLibrary ? "Another Reading" : "Generate Again";
  previewStateEl.textContent = isLibrary
    ? "Ready. Pick a level and topic, then load a curated reading."
    : "Ready. Set your level, topic, and keywords, then generate a custom reading.";
  renderMeta(
    state.lastPayload?.level || levelEl.value,
    state.lastPayload?.resolved_topic || state.lastPayload?.topic || topicEl.value,
    state.text || ""
  );
}

function isMobilePreview() {
  return state.viewMode === "mobile";
}

function setMobileWordSheetOpen(isOpen) {
  if (!mobileWordSheetEl) return;
  mobileWordSheetEl.classList.toggle("hidden", !isOpen);
  mobileWordSheetEl.classList.toggle("sheet-open", isOpen);
  mobileWordSheetEl.setAttribute("aria-hidden", String(!isOpen));
  document.body.classList.toggle("mobile-sheet-open", isOpen);
  if (mobileWordPanelEl) mobileWordPanelEl.style.transform = "";
}

function closeMobileWordSheet() {
  if (state.selectedWord) state.dismissedMobileWord = state.selectedWord;
  setMobileWordSheetOpen(false);
}

function playDesktopFlip(word) {
  if (!flipCardEl || isMobilePreview() || state.selectedWord !== word) return;
  flipCardEl.classList.remove("flipped");
  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => {
      if (state.selectedWord === word && !isMobilePreview()) {
        flipCardEl.classList.add("flipped");
      }
    });
  });
}

function updateViewModeUi() {
  document.body.classList.toggle("mobile-mode", isMobilePreview());
  document.body.classList.toggle("web-mode", !isMobilePreview());
  if (!isMobilePreview()) {
    setMobileWordSheetOpen(false);
  } else if (
    state.selectedWord &&
    !state.loadingWord &&
    state.glossary[state.selectedWord] &&
    state.dismissedMobileWord !== state.selectedWord
  ) {
    setMobileWordSheetOpen(true);
  }
}

function syncViewModeFromViewport() {
  const nextMode = window.innerWidth < 860 ? "mobile" : "web";
  if (state.viewMode !== nextMode) {
    state.viewMode = nextMode;
  }
  updateViewModeUi();
}

function renderLibraryStats() {
  if (!libraryCountBadgeEl || !state.libraryStats) return;
  libraryCountBadgeEl.textContent = `${Number(state.libraryStats.total || 0)} curated readings inside`;
}

function buildTopicListFromStats() {
  const currentLevel = libraryLevelEl?.value || levelEl?.value || "B1";
  const statTopics = Array.isArray(state.libraryStats?.by_level_topic)
    ? state.libraryStats.by_level_topic
        .filter((item) => item.level === currentLevel)
        .map((item) => item.topic)
        .filter(Boolean)
    : [];
  const allowedTopics = new Set(TOPIC_ORDER);
  const visibleTopics = statTopics.filter((topic) => allowedTopics.has(topic));
  const ordered = TOPIC_ORDER.filter((topic) => topic === "Random" || visibleTopics.includes(topic));
  return ["Random", ...ordered.filter((topic) => topic !== "Random")];
}

function populateTopicOptions() {
  const topics = buildTopicListFromStats();
  if (!topics.length) return;
  const currentTopic = libraryTopicEl?.value || topicEl?.value || "Random";
  const html = topics
    .map((topic) => `<option value="${escapeHtml(topic)}">${escapeHtml(topic)}</option>`)
    .join("");
  if (topicEl) topicEl.innerHTML = html;
  if (libraryTopicEl) libraryTopicEl.innerHTML = html;
  const nextTopic = topics.includes(currentTopic) ? currentTopic : "Random";
  syncTopicPickers(nextTopic);
}

function renderMeta(level, topic, text) {
  if (!text) {
    metaTagsEl.innerHTML = "";
    return;
  }
  const count = text.split(/\s+/).filter(Boolean).length;
  const sourceLabel = state.lastPayload?.content_source === "library" ? "Library" : "AI";
  metaTagsEl.innerHTML = `
    <span class="tag">Level ${escapeHtml(level)}</span>
    <span class="tag">${escapeHtml(topic)}</span>
    <span class="tag">${count} words</span>
    <span class="tag">${sourceLabel}</span>
  `;
}

function renderSelection() {
  const item = state.glossary[state.selectedWord] || {};
  const meaning = item.turkish || "Choose a word";
  const contextHtml = state.loadingWord
    ? "Preparing Turkish context..."
    : buildInsightHtml(item.context, state.selectedWord, {
        emptyText: "Context appears here after you choose a word.",
        collapsedLines: 3,
        maxLines: 14,
      });
  const exampleHtml = state.loadingWord
    ? "Preparing example sentence..."
    : buildInsightHtml(item.example, state.selectedWord, {
        emptyText: "A short example appears here after you choose a word.",
        collapsedLines: 2,
        maxLines: 10,
      });

  selectedWordEl.textContent = state.selectedWord || "Word";
  selectedMeaningEl.textContent = meaning;
  selectedContextEl.innerHTML = contextHtml;
  selectedExampleEl.innerHTML = exampleHtml;
  renderCollocations(selectedCollocationsEl, item.collocations || []);
  flipCardEl.classList.remove("flipped");
  flipCardEl.classList.toggle("clickable", !state.loadingWord && Boolean(state.selectedWord));
  pronounceWordBtn?.classList.toggle("hidden", !state.selectedWord);

  if (mobileWordTitleEl) mobileWordTitleEl.textContent = state.selectedWord || "Word";
  if (mobileWordMeaningEl) mobileWordMeaningEl.textContent = meaning;
  if (mobileWordContextEl) mobileWordContextEl.innerHTML = contextHtml;
  if (mobileWordExampleEl) mobileWordExampleEl.innerHTML = exampleHtml;
  renderCollocations(mobileWordCollocationsEl, item.collocations || []);
  mobilePronounceWordBtn?.classList.toggle("hidden", !state.selectedWord);

  if (!isMobilePreview() || !state.selectedWord || state.loadingWord) {
    setMobileWordSheetOpen(false);
  } else if (state.glossary[state.selectedWord] && state.dismissedMobileWord !== state.selectedWord) {
    setMobileWordSheetOpen(true);
  }
}

function renderSavedWords() {
  if (!state.user || !state.recentWords.length) {
    savedWordsEmptyEl.classList.remove("hidden");
    savedWordsListEl.classList.add("hidden");
    savedWordsListEl.innerHTML = "";
    savedWordsActionsEl?.classList.add("hidden");
    return;
  }
  savedWordsEmptyEl.classList.add("hidden");
  savedWordsListEl.classList.remove("hidden");
  savedWordsActionsEl?.classList.remove("hidden");
  if (savedWordsMetaEl) {
    savedWordsMetaEl.textContent = `${state.recentWords.length} words on deck`;
  }
  savedWordsListEl.innerHTML = state.recentWords
    .map(
      (item) => `
        <div class="saved-word-row" data-word-id="${item.id}">
          <button class="saved-word-item" type="button" data-word="${escapeHtml(item.word)}">
            <strong>${escapeHtml(item.word)}</strong>
            <span>${escapeHtml(item.turkish)}</span>
          </button>
          <button class="saved-word-remove" type="button" data-word-id="${item.id}" aria-label="Remove ${escapeHtml(item.word)}">×</button>
        </div>
      `
    )
    .join("");
  savedWordsListEl.querySelectorAll(".saved-word-item").forEach((button) => {
    button.addEventListener("click", async () => {
      if (!state.text) return;
      state.selectedWord = button.dataset.word;
      state.pendingFlip = true;
      renderSelection();
      renderReadingText();
      await loadWordDetail(button.dataset.word);
    });
  });
  savedWordsListEl.querySelectorAll(".saved-word-remove").forEach((button) => {
    button.addEventListener("click", async (event) => {
      event.stopPropagation();
      const wordId = button.dataset.wordId;
      const parsed = await apiFetch(`/api/saved-words/${wordId}`, { method: "DELETE" });
      if (!parsed.ok) return;
      state.stats = parsed.data.stats || state.stats;
      state.recentWords = parsed.data.recent_words || [];
      renderUserPanel();
      if (state.quiz && String(state.quiz.word_id) === String(wordId)) {
        state.quiz = null;
        await loadQuiz();
      } else {
        renderQuiz();
      }
    });
  });
}

async function fetchSavedWords(mode = "recent") {
  if (!state.user) return;
  const excludeIds =
    mode === "random" ? state.recentWords.map((item) => item.id).filter(Boolean).join(",") : "";
  const query = new URLSearchParams({
    mode,
    limit: "20",
  });
  if (excludeIds) query.set("exclude_ids", excludeIds);
  const parsed = await apiFetch(`/api/saved-words?${query.toString()}`);
  if (!parsed.ok) return;
  state.recentWords = parsed.data.words || [];
  renderSavedWords();
}

function renderQuiz() {
  if (quizAnsweredBadgeEl) quizAnsweredBadgeEl.textContent = `${state.quizStats.answered} played`;
  if (quizStreakBadgeEl) quizStreakBadgeEl.textContent = `Streak ${state.quizStats.streak}`;
  quizModeSavedBtn?.classList.toggle("active", state.quizMode === "saved");
  quizModeHardBtn?.classList.toggle("active", state.quizMode === "hard");
  quizModeReadingBtn?.classList.toggle("active", state.quizMode === "reading");
  if (state.quizMode !== "reading" && !state.user) {
    quizEmptyEl.textContent = "Sign in first to unlock the quiz.";
    quizEmptyEl.classList.remove("hidden");
    quizCardEl.classList.add("hidden");
    return;
  }
  if (!state.quiz) {
    quizEmptyEl.textContent = state.quizMode === "reading"
      ? "Open a reading and tap into the glossary first to start a reading quiz."
      : state.quizMode === "hard"
        ? "You need at least 4 saved words before hard-word review can begin."
        : "You need at least 4 saved words to start the quiz.";
    quizEmptyEl.classList.remove("hidden");
    quizCardEl.classList.add("hidden");
    return;
  }
  quizEmptyEl.classList.add("hidden");
  quizCardEl.classList.remove("hidden");
  quizCardEl.classList.remove("quiz-refresh");
  void quizCardEl.offsetWidth;
  quizCardEl.classList.add("quiz-refresh");
  quizPromptEl.textContent = state.quiz.question;
  if (quizTypeBadgeEl) {
    quizTypeBadgeEl.textContent = state.quiz.question_type === "blank" ? "Blank Builder" : "Meaning Match";
  }
  if (quizSentenceEl) {
    if (state.quiz.sentence) {
      quizSentenceEl.textContent = state.quiz.sentence;
      quizSentenceEl.classList.remove("hidden");
    } else {
      quizSentenceEl.textContent = "";
      quizSentenceEl.classList.add("hidden");
    }
  }
  quizFeedbackEl.classList.add("hidden");
  quizFeedbackEl.textContent = "";
  quizOptionsEl.innerHTML = state.quiz.options
    .map((option) => `<button class="quiz-option" type="button" data-answer="${escapeHtml(option)}">${escapeHtml(option)}</button>`)
    .join("");
  quizOptionsEl.querySelectorAll(".quiz-option").forEach((button) => {
    button.addEventListener("click", async () => {
      if (state.quizMode === "reading") {
        const isCorrect = button.dataset.answer === state.quiz.answer;
        state.quizStats.answered += 1;
        state.quizStats.correct += isCorrect ? 1 : 0;
        state.quizStats.streak = isCorrect ? state.quizStats.streak + 1 : 0;
        quizFeedbackEl.textContent = isCorrect
          ? (state.quiz.question_type === "blank"
            ? `Correct. "${state.quiz.answer}" fits the sentence.`
            : `Correct. "${state.quiz.word}" = "${state.quiz.answer}".`)
          : (state.quiz.question_type === "blank"
            ? `Not this time. Correct word: ${state.quiz.answer}`
            : `Not this time. Correct answer: ${state.quiz.answer}`);
        quizFeedbackEl.classList.remove("hidden");
        quizOptionsEl.querySelectorAll(".quiz-option").forEach((optionButton) => {
          optionButton.disabled = true;
          optionButton.classList.toggle("correct", optionButton.dataset.answer === state.quiz.answer);
          optionButton.classList.toggle(
            "wrong",
            optionButton.dataset.answer === button.dataset.answer && button.dataset.answer !== state.quiz.answer
          );
        });
        if (quizAnsweredBadgeEl) quizAnsweredBadgeEl.textContent = `${state.quizStats.answered} played`;
        if (quizStreakBadgeEl) quizStreakBadgeEl.textContent = `Streak ${state.quizStats.streak}`;
        if (!isCorrect) {
          nextQuizBtn.disabled = true;
          nextQuizBtn.textContent = "Next incoming...";
          window.setTimeout(async () => {
            await loadQuiz(state.quiz?.word || null);
            nextQuizBtn.disabled = false;
            nextQuizBtn.textContent = "Next Question";
          }, 3000);
        }
        return;
      }
      const parsed = await apiFetch("/api/quiz/check", {
        method: "POST",
        body: JSON.stringify({
          word_id: state.quiz.word_id,
            answer: button.dataset.answer,
            question_type: state.quiz.question_type || "meaning",
          }),
        });
      if (!parsed.ok) {
        quizFeedbackEl.classList.add("hidden");
        showToast(parsed.data.detail || "Quiz answer could not be saved.", { variant: "error", scope: "quiz" });
        return;
      }
      state.quizStats.answered += 1;
      if (parsed.data.correct) {
        state.quizStats.correct += 1;
        state.quizStats.streak += 1;
      } else {
        state.quizStats.streak = 0;
      }
        quizFeedbackEl.textContent = parsed.data.correct
          ? (state.quiz.question_type === "blank"
            ? `Correct. "${parsed.data.answer}" fits the sentence.`
            : `Correct. "${parsed.data.word}" = "${parsed.data.answer}".`)
          : (state.quiz.question_type === "blank"
            ? `Not this time. Correct word: ${parsed.data.answer}`
            : `Not this time. Correct answer: ${parsed.data.answer}`);
      quizFeedbackEl.classList.remove("hidden");
      state.stats = parsed.data.stats;
      updateAccountStatsOnly();
      quizOptionsEl.querySelectorAll(".quiz-option").forEach((optionButton) => {
        optionButton.disabled = true;
        optionButton.classList.toggle("correct", optionButton.dataset.answer === parsed.data.answer);
        optionButton.classList.toggle(
          "wrong",
          optionButton.dataset.answer === button.dataset.answer && button.dataset.answer !== parsed.data.answer
        );
      });
        state.quiz = {
          ...state.quiz,
          context: parsed.data.context,
          example: parsed.data.example,
        };
        if (quizAnsweredBadgeEl) quizAnsweredBadgeEl.textContent = `${state.quizStats.answered} played`;
        if (quizStreakBadgeEl) quizStreakBadgeEl.textContent = `Streak ${state.quizStats.streak}`;
        if (!parsed.data.correct) {
          nextQuizBtn.disabled = true;
          nextQuizBtn.textContent = "Next incoming...";
          window.setTimeout(async () => {
            await loadQuiz(state.quiz?.word_id || null);
            nextQuizBtn.disabled = false;
            nextQuizBtn.textContent = "Next Question";
          }, 2200);
        }
      });
    });
  }

function setLibraryView(view) {
  state.libraryView = view;
  const isOpen = Boolean(view);
  libraryOverlayEl.classList.toggle("hidden", !isOpen);
  libraryPanelEl.classList.toggle("hidden", !isOpen);
  document.body.classList.toggle("library-open", isOpen);
  profileAvatarBtn?.setAttribute("aria-expanded", view === "profile" ? "true" : "false");
  profilePanelEl.classList.toggle("hidden", view !== "profile");
  progressPanelEl.classList.toggle("hidden", view !== "progress");
  socialPanelEl?.classList.toggle("hidden", view !== "social");
  savedWordsPanelEl.classList.toggle("hidden", view !== "saved");
  quizPanelEl.classList.toggle("hidden", view !== "quiz");
  manualHelpPanelEl.classList.toggle("hidden", view !== "manual");
  infoPanelEl.classList.toggle("hidden", view !== "info");
  if (libraryPanelScrollEl) libraryPanelScrollEl.style.transform = "";
  if (view === "profile") {
    libraryKickerEl.textContent = "Profile";
    libraryTitleEl.textContent = "Account access";
  } else if (view === "progress") {
    libraryKickerEl.textContent = "Progress";
    libraryTitleEl.textContent = "Your streak and history";
  } else if (view === "social") {
    libraryKickerEl.textContent = "Social";
    libraryTitleEl.textContent = "Friends and momentum";
  } else if (view === "saved") {
    libraryKickerEl.textContent = "Saved Words";
    libraryTitleEl.textContent = "Your saved words";
  } else if (view === "quiz") {
    libraryKickerEl.textContent = "Mini Quiz";
    libraryTitleEl.textContent = "Quick review";
  } else if (view === "manual") {
    libraryKickerEl.textContent = "Translate";
    libraryTitleEl.textContent = "Quick translation";
  } else if (view === "info") {
    libraryKickerEl.textContent = "Office";
    libraryTitleEl.textContent = "ReadLex company and trust notes";
  }
  setNavMenuOpen(false);
}

function isDesktopMenuMode() {
  return Boolean(MENU_DESKTOP_QUERY?.matches) && window.innerWidth > 768;
}

function setNavMenuOpen(isOpen) {
  if (navMenuCloseTimer) {
    window.clearTimeout(navMenuCloseTimer);
    navMenuCloseTimer = null;
  }
  navMenuShellEl?.classList.toggle("is-open", Boolean(isOpen));
  navMenuTriggerEl?.setAttribute("aria-expanded", isOpen ? "true" : "false");
}

function setNavMenuCategory(category = "account") {
  navMenuSwitchEls.forEach((button) => {
    const isActive = button.dataset.menuCategory === category;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-selected", isActive ? "true" : "false");
  });
  navMenuPanelEls.forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.menuPanel === category);
  });
}

async function openLibraryPanel(view) {
  if (view === "saved" && state.user) {
    await fetchSavedWords("recent");
  }
  if (view === "social" && state.user) {
    await loadSocial();
  }
  if (view === "quiz" && !state.quiz && state.user) {
    await loadQuiz();
  }
  setLibraryView(view);
}

function bindNavMenuAction(button, view) {
  if (!button) return;
  button.addEventListener("click", async (event) => {
    event.preventDefault();
    event.stopPropagation();
    await openLibraryPanel(view);
  });
}

function renderSocialCard(user, { action = "", requestId = "", friendshipId = "" } = {}) {
  const badge = user.streak > 0 ? `Streak ${user.streak}` : `${user.total_readings || 0} texts`;
  const actionHtml =
    action === "accept"
      ? `<div class="social-actions">
          <button class="ghost-btn ghost-btn-inline social-accept" type="button" data-request-id="${requestId}">Accept</button>
          <button class="ghost-btn ghost-btn-inline social-decline" type="button" data-request-id="${requestId}">Decline</button>
        </div>`
      : action === "add"
        ? `<button class="ghost-btn ghost-btn-inline social-add-suggested" type="button" data-username="${escapeHtml(user.username)}">Add</button>`
        : action === "friend"
          ? `<div class="social-actions">
              <button class="ghost-btn ghost-btn-inline social-cheer" type="button" data-friendship-id="${friendshipId}">Cheer</button>
              <button class="ghost-btn ghost-btn-inline social-remove" type="button" data-friendship-id="${friendshipId}">Remove</button>
            </div>`
          : `<span class="social-pending">Pending</span>`;
  return `
    <article class="social-card">
      <div class="social-avatar">${escapeHtml(String(user.username || "U").charAt(0).toUpperCase())}</div>
      <div class="social-card-copy">
        <strong>${escapeHtml(user.username || "user")}</strong>
        <span>${escapeHtml(badge)} · ${Number(user.saved_words || 0)} saved · ${Number(user.words_today || 0)} today</span>
      </div>
      ${actionHtml}
    </article>
  `;
}

function bindSocialActions() {
  socialIncomingListEl?.querySelectorAll(".social-accept, .social-decline").forEach((button) => {
    button.addEventListener("click", async () => {
      const action = button.classList.contains("social-accept") ? "accept" : "decline";
      await respondSocialRequest(button.dataset.requestId, action);
    });
  });
  socialSuggestionsListEl?.querySelectorAll(".social-add-suggested").forEach((button) => {
    button.addEventListener("click", async () => {
      if (socialUsernameInputEl) socialUsernameInputEl.value = button.dataset.username || "";
      await sendFriendRequest(button.dataset.username || "");
    });
  });
  socialFriendsListEl?.querySelectorAll(".social-cheer").forEach((button) => {
    button.addEventListener("click", async () => {
      const parsed = await apiFetch(`/api/social/friends/${button.dataset.friendshipId}/cheer`, { method: "POST" });
      if (!parsed.ok) {
        showToast(parsed.data.detail || "Cheer could not be sent.", { variant: "error", scope: "social" });
        return;
      }
      state.social = parsed.data;
      renderSocialPanel();
      showToast("Cheer sent. Tiny win, good energy.", { variant: "info", scope: "social" });
    });
  });
  socialFriendsListEl?.querySelectorAll(".social-remove").forEach((button) => {
    button.addEventListener("click", async () => {
      const parsed = await apiFetch(`/api/social/friends/${button.dataset.friendshipId}`, { method: "DELETE" });
      if (!parsed.ok) return;
      state.social = parsed.data;
      renderSocialPanel();
    });
  });
}

function renderSocialPanel() {
  const loggedIn = Boolean(state.user);
  socialAddFormEl?.classList.toggle("hidden", !loggedIn);
  socialGuestNoteEl?.classList.toggle("hidden", loggedIn);
  if (socialFriendCountEl) socialFriendCountEl.textContent = String(state.social.friends?.length || 0);
  if (!loggedIn) {
    if (socialIncomingListEl) socialIncomingListEl.innerHTML = "";
    if (socialFriendsListEl) socialFriendsListEl.innerHTML = `<p class="history-empty">Sign in to compare streaks with friends.</p>`;
    if (socialSuggestionsListEl) socialSuggestionsListEl.innerHTML = "";
    return;
  }
  const incoming = state.social.incoming || [];
  const outgoing = state.social.outgoing || [];
  const friends = state.social.friends || [];
  const suggestions = state.social.suggestions || [];
  if (socialIncomingListEl) {
    socialIncomingListEl.innerHTML = [
      ...incoming.map((item) => renderSocialCard(item.user, { action: "accept", requestId: item.request_id })),
      ...outgoing.map((item) => renderSocialCard(item.user, { action: "pending" })),
    ].join("");
  }
  if (socialFriendsListEl) {
    socialFriendsListEl.innerHTML = friends.length
      ? friends.map((user) => renderSocialCard(user, { action: "friend", friendshipId: user.friendship_id })).join("")
      : `<p class="history-empty">No friends yet. Add a username to start your circle.</p>`;
  }
  if (socialSuggestionsListEl) {
    socialSuggestionsListEl.innerHTML = suggestions.length
      ? suggestions.map((user) => renderSocialCard(user, { action: "add" })).join("")
      : `<p class="history-empty">Suggestions will appear when more learners join.</p>`;
  }
  bindSocialActions();
}

async function loadSocial() {
  if (!state.user) {
    renderSocialPanel();
    return;
  }
  const parsed = await apiFetch("/api/social");
  if (!parsed.ok) {
    showToast(parsed.data.detail || "Social panel could not load.", { variant: "error", scope: "social" });
    return;
  }
  state.social = parsed.data;
  renderSocialPanel();
}

async function sendFriendRequest(username) {
  const targetUsername = String(username || socialUsernameInputEl?.value || "").trim();
  if (!targetUsername) return;
  setLoading(socialAddBtn, "Adding...", true);
  try {
    const parsed = await apiFetch("/api/social/request", {
      method: "POST",
      body: JSON.stringify({ username: targetUsername }),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Friend request failed.");
    state.social = parsed.data;
    if (socialUsernameInputEl) socialUsernameInputEl.value = "";
    renderSocialPanel();
  } catch (error) {
    showToast(error.message || "Friend request failed.", { variant: "error", scope: "social" });
  } finally {
    setLoading(socialAddBtn, "", false);
  }
}

async function respondSocialRequest(requestId, action) {
  const parsed = await apiFetch(`/api/social/requests/${requestId}`, {
    method: "POST",
    body: JSON.stringify({ action }),
  });
  if (!parsed.ok) return;
  state.social = parsed.data;
  renderSocialPanel();
}

function formatProgressDate(isoDate) {
  const [year, month, day] = String(isoDate || "").split("-");
  if (!year || !month || !day) return String(isoDate || "Today");
  return `${day}.${month}.${year}`;
}

function renderUserPanel() {
  const loggedIn = Boolean(state.user);
  authGuestEl.classList.toggle("hidden", loggedIn);
  authUserEl.classList.toggle("hidden", !loggedIn);
  if (profileTriggerInitialsEl) {
    profileTriggerInitialsEl.textContent = loggedIn
      ? String(state.user?.username || "U").trim().charAt(0).toUpperCase() || "U"
      : "G";
  }
  profileAvatarBtn?.classList.toggle("signed-in", loggedIn);
  if (loggedIn) {
    const uniqueReadingHistory = state.readingHistory.filter((item, index, items) => {
      const key = [
        String(item.title || "").trim().toLowerCase(),
        String(item.level || "").trim().toLowerCase(),
        String(item.topic || "").trim().toLowerCase(),
        String(item.content_source || "").trim().toLowerCase(),
      ].join("|");
      return index === items.findIndex((candidate) => {
        const candidateKey = [
          String(candidate.title || "").trim().toLowerCase(),
          String(candidate.level || "").trim().toLowerCase(),
          String(candidate.topic || "").trim().toLowerCase(),
          String(candidate.content_source || "").trim().toLowerCase(),
        ].join("|");
        return candidateKey === key;
      });
    });

    accountNameEl.textContent = state.user.username;
    savedWordsCountEl.textContent = state.stats.saved_words || 0;
    masteredWordsCountEl.textContent = state.stats.mastered_words || 0;
    if (totalReadingsTextEl) totalReadingsTextEl.textContent = state.stats.total_readings || 0;
    if (todayReadingsTextEl) todayReadingsTextEl.textContent = state.stats.readings_today || 0;
    if (todayWordsTextEl) todayWordsTextEl.textContent = state.stats.saved_today || 0;
    if (profileTipTextEl) {
      profileTipTextEl.textContent =
        (state.stats.total_readings || 0) > 0
          ? "Keep the loop simple: read, save useful phrases, then return through quiz."
          : "Open your first reading and this desk will start tracking your rhythm.";
    }
    if (dailyGoalTextEl) {
      dailyGoalTextEl.textContent = `${state.stats.saved_today || 0} / ${state.stats.daily_goal || 5} today`;
    }
    if (streakBadgeEl) {
      streakBadgeEl.textContent = `Streak ${state.stats.streak || 0}`;
    }
    if (goalBarFillEl) {
      const ratio = Math.min(100, ((state.stats.saved_today || 0) / Math.max(1, state.stats.daily_goal || 5)) * 100);
      goalBarFillEl.style.width = `${ratio}%`;
    }
    if (hardWordsTextEl) {
      hardWordsTextEl.textContent = `${state.stats.hard_words || 0} hard words ready for review.`;
    }
    if (progressHistoryListEl) {
      const rows = Array.isArray(state.progressHistory) ? state.progressHistory : [];
      if (!rows.length) {
        progressHistoryListEl.innerHTML = `<p class="history-empty">Daily totals will appear after your first signed-in reading.</p>`;
      } else {
        progressHistoryListEl.innerHTML = rows
          .map((item) => {
            const texts = Number(item.texts || 0);
            const words = Number(item.words || 0);
            return `
              <article class="progress-history-item">
                <div>
                  <span>${escapeHtml(formatProgressDate(item.date))}</span>
                  <strong>${texts} Text${texts === 1 ? "" : "s"}</strong>
                </div>
                <em>${words} Word${words === 1 ? "" : "s"}</em>
              </article>
            `;
          })
          .join("");
      }
    }
    if (readingHistoryListEl) {
      if (!uniqueReadingHistory.length) {
        readingHistoryListEl.innerHTML = `<p class="history-empty">Your recent readings will appear here.</p>`;
      } else {
        readingHistoryListEl.innerHTML = uniqueReadingHistory
          .map((item) => `
            <button class="history-item" type="button" data-history-id="${item.id}">
              <strong>${escapeHtml(item.title)}</strong>
              <span>${escapeHtml(item.level)} · ${escapeHtml(item.topic)}</span>
            </button>
          `)
          .join("");
        readingHistoryListEl.querySelectorAll(".history-item").forEach((button) => {
          button.addEventListener("click", async () => {
            const parsed = await apiFetch(`/api/history/${button.dataset.historyId}`, { method: "GET", headers: {} });
            if (!parsed.ok) return;
            const reading = parsed.data.reading;
            state.text = reading.text;
            state.glossary = reading.glossary || {};
            state.lastPayload = {
              level: reading.level,
              topic: reading.topic,
              resolved_topic: reading.topic,
              title: reading.title,
              content_source: reading.content_source,
              source: reading.content_source,
            };
            setLibraryView(null);
            renderExperience();
          });
        });
      }
    }
  } else {
    if (readingHistoryListEl) readingHistoryListEl.innerHTML = `<p class="history-empty">Sign in to keep your reading trail.</p>`;
    if (progressHistoryListEl) progressHistoryListEl.innerHTML = `<p class="history-empty">Sign in to track daily text and word history.</p>`;
    if (totalReadingsTextEl) totalReadingsTextEl.textContent = "0";
    if (todayReadingsTextEl) todayReadingsTextEl.textContent = "0";
    if (todayWordsTextEl) todayWordsTextEl.textContent = "0";
    if (dailyGoalTextEl) dailyGoalTextEl.textContent = "0 / 5 today";
    if (streakBadgeEl) streakBadgeEl.textContent = "Streak 0";
    if (goalBarFillEl) goalBarFillEl.style.width = "0%";
    if (hardWordsTextEl) hardWordsTextEl.textContent = "0 hard words ready for review.";
  }
  renderSocialPanel();
  renderSavedWords();
  renderQuiz();
}

function registerSheetDrag(handleEl, panelEl, closeFn, isOpenFn) {
  if (!handleEl || !panelEl) return;
  let startY = 0;
  let dragging = false;

  handleEl.addEventListener("touchstart", (event) => {
    if (!isOpenFn()) return;
    const touch = event.touches[0];
    startY = touch.clientY;
    dragging = true;
    panelEl.style.transition = "none";
  }, { passive: true });

  handleEl.addEventListener("touchmove", (event) => {
    if (!dragging) return;
    const touch = event.touches[0];
    const deltaY = Math.max(0, touch.clientY - startY);
    panelEl.style.transform = `translateY(${deltaY}px)`;
  }, { passive: true });

  const finishDrag = (event) => {
    if (!dragging) return;
    const touch = event.changedTouches?.[0];
    const deltaY = touch ? Math.max(0, touch.clientY - startY) : 0;
    dragging = false;
    panelEl.style.transition = "";
    panelEl.style.transform = "";
    if (deltaY > 72) closeFn();
  };

  handleEl.addEventListener("touchend", finishDrag, { passive: true });
  handleEl.addEventListener("touchcancel", finishDrag, { passive: true });
}

function updateAccountStatsOnly() {
  if (!state.user) return;
  savedWordsCountEl.textContent = state.stats.saved_words || 0;
  masteredWordsCountEl.textContent = state.stats.mastered_words || 0;
}

function clearAuthToasts() {
  document.querySelectorAll(".auth-toast").forEach((toast) => {
    toast.remove();
  });
}

function showAuthToast(message, anchorEl) {
  const host = anchorEl?.closest?.(".auth-face") || anchorEl?.closest?.(".welcome-auth") || document.body;
  const existing = host.querySelector(".auth-toast");
  if (existing) {
    existing.remove();
  }

  const toast = document.createElement("div");
  toast.className = "auth-toast";
  toast.setAttribute("role", "status");
  toast.setAttribute("aria-live", "polite");

  const text = document.createElement("div");
  text.className = "auth-toast-text";
  text.textContent = String(message || "");

  const closeBtn = document.createElement("button");
  closeBtn.className = "auth-toast-close";
  closeBtn.type = "button";
  closeBtn.setAttribute("aria-label", "Close");
  closeBtn.textContent = "x";
  closeBtn.addEventListener("click", () => {
    toast.remove();
  });

  toast.append(text, closeBtn);
  host.appendChild(toast);

  window.setTimeout(() => {
    toast.remove();
  }, 5000);
}

function hideAuthErrors() {
  [authLoginErrorEl, authRegisterErrorEl, gateLoginErrorEl, gateRegisterErrorEl].forEach((el) => el?.classList.add("hidden"));
}

function syncInputPair(sourceEl, targetEl) {
  if (!sourceEl || !targetEl) return;
  sourceEl.addEventListener("input", () => {
    targetEl.value = sourceEl.value;
  });
}

async function submitAuthForm({
  endpoint,
  usernameEl,
  passwordEl,
  errorEl,
  submitBtn,
  mirrorUsernameEls = [],
  mirrorPasswordEls = [],
}) {
  const formatAuthError = (detail) => {
    if (!detail) return "Authentication failed.";
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      const parts = detail
        .map((item) => {
          if (!item) return "";
          if (typeof item === "string") return item;
          if (typeof item !== "object") return String(item);
          const msg = typeof item.msg === "string" ? item.msg : "";
          const loc = Array.isArray(item.loc) ? item.loc : [];
          const field = loc.length ? String(loc[loc.length - 1]) : "";
          if (field && msg) return `${field}: ${msg}`;
          return msg || String(item.message || item.error || item.title || "") || "";
        })
        .filter(Boolean);
      return parts.join("\n") || "Authentication failed.";
    }
    if (typeof detail === "object") {
      if (Array.isArray(detail.detail)) return formatAuthError(detail.detail);
      if (typeof detail.message === "string") return detail.message;
      if (typeof detail.error === "string") return detail.error;
      if (typeof detail.title === "string") return detail.title;
      if (typeof detail.msg === "string") return detail.msg;
    }
    return "Authentication failed.";
  };

  if (errorEl) {
    errorEl.textContent = "";
    errorEl.classList.add("hidden");
  }
  setLoading(submitBtn, endpoint.includes("/login") ? "Logging in..." : "Creating account...", true);
  try {
    const payload = {
      username: usernameEl.value.trim(),
      password: passwordEl.value.trim(),
    };
    const parsed = await apiFetch(endpoint, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!parsed.ok) throw new Error(formatAuthError(parsed?.data?.detail));
    [...mirrorUsernameEls, usernameEl].forEach((el) => {
      if (el) el.value = payload.username;
    });
    [...mirrorPasswordEls, passwordEl].forEach((el) => {
      if (el) el.value = "";
    });
    state.user = parsed.data.user;
    state.stats = parsed.data.stats || emptyStats();
    completeAppEntry(false);
    try {
      await refreshSession();
    } catch (sessionError) {
      console.warn("Session refresh failed after auth success.", sessionError);
      state.user = parsed.data.user;
      state.stats = parsed.data.stats || state.stats;
    }
    if (!state.user) {
      state.user = parsed.data.user;
      state.stats = parsed.data.stats || state.stats;
    }
    try {
      await loadQuiz();
    } catch (quizError) {
      console.warn("Quiz bootstrap failed after auth success.", quizError);
    }
  } catch (error) {
    if (errorEl) {
      const message =
        typeof error === "string"
          ? error
          : error && typeof error === "object" && typeof error.message === "string"
            ? error.message
            : "Authentication failed.";
      errorEl.textContent = message;
      errorEl.classList.add("hidden");
      showAuthToast(message, errorEl);
    }
  } finally {
    setLoading(submitBtn, "", false);
  }
}

function renderAuthMode() {
  const isLogin = state.authMode === "login";
  showLoginBtn.classList.toggle("active", isLogin);
  showRegisterBtn.classList.toggle("active", !isLogin);
  gateShowLoginBtn?.classList.toggle("active", isLogin);
  gateShowRegisterBtn?.classList.toggle("active", !isLogin);
  authCardEl?.classList.toggle("flipped", !isLogin);
  gateAuthCardEl?.classList.toggle("flipped", !isLogin);
  authToggleEls.forEach((el) => {
    el.dataset.mode = isLogin ? "login" : "register";
  });
  hideAuthErrors();
  clearAuthToasts();
}

function renderWelcomeGate() {
  const shouldShow = !state.user && !state.hasEnteredApp;
  welcomeGateEl?.classList.toggle("hidden", !shouldShow);
  document.body.classList.toggle("gate-open", shouldShow);
}

function completeAppEntry(asGuest = false) {
  state.hasEnteredApp = true;
  if (asGuest) {
    window.sessionStorage.setItem(GUEST_FLAG_KEY, "1");
  } else {
    window.sessionStorage.removeItem(GUEST_FLAG_KEY);
  }
  renderWelcomeGate();
}

async function loadFeaturedPhrasalReadingIfEmpty() {
  if (state.text || state.lastPayload) return;
  try {
    const payload = {
      level: "B1",
      topic: "Random",
      length_target: 150,
      keywords: [],
      source: "library",
      exclude_title: null,
    };
    const parsed = await apiFetch("/api/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!parsed.ok) return;
    if (String(parsed.data.title || "") !== "Phrasal Verbs Demo (B1)") return;
    state.text = parsed.data.text;
    state.glossary = parsed.data.glossary || {};
    state.lastPayload = {
      ...payload,
      title: parsed.data.title || "",
      resolved_topic: parsed.data.topic || payload.topic,
      content_source: parsed.data.content_source || payload.source,
    };
    renderExperience();
    void fillMissingLibraryWords();
  } catch {
    // Silent: the app still works even if the featured reading cannot load.
  }
}

async function fillMissingLibraryWords() {
  if (!state.text) return;
  if ((state.lastPayload?.content_source || state.contentSource) !== "library") return;
  try {
    const parsed = await apiFetch("/api/library/fill-missing", {
      method: "POST",
      body: JSON.stringify({ text: state.text, max_words: 220 }),
    });
    if (!parsed.ok) return;
    const sample = parsed.data.sample || {};
    Object.entries(sample).forEach(([word, turkish]) => {
      const key = String(word || "").toLowerCase().trim();
      const value = String(turkish || "").trim();
      if (!key || !value) return;
      if (!state.glossary[key]) {
        state.glossary[key] = {
          turkish: value,
          context: "",
          example: "",
          collocations: [],
        };
      } else if (!state.glossary[key].turkish) {
        state.glossary[key].turkish = value;
      }
    });
    renderSelection();
  } catch {
    // keep silent
  }
}
async function refreshSession() {
  const parsed = await apiFetch("/api/auth/me", { method: "GET", headers: {} });
  if (parsed.ok) {
    state.user = parsed.data.user;
    state.stats = parsed.data.stats || emptyStats();
    state.recentWords = parsed.data.recent_words || [];
    state.readingHistory = parsed.data.history || [];
    state.progressHistory = parsed.data.progress_history || [];
    if (state.libraryView === "social") {
      await loadSocial();
    }
  } else {
    state.user = null;
    state.stats = emptyStats();
    state.recentWords = [];
    state.readingHistory = [];
    state.progressHistory = [];
    state.social = { friends: [], incoming: [], outgoing: [], suggestions: [], cheers_received: 0 };
  }
  renderUserPanel();
}

function buildSelectionPersistenceKey(word) {
  const source = state.lastPayload?.content_source || state.contentSource || "";
  const title = state.lastPayload?.title || "";
  return `${source}::${title}::${String(word || "").toLowerCase()}`;
}

function scheduleSessionRefresh({ includeQuiz = false, excludeWordId = null, delay = 180 } = {}) {
  if (!state.user) return Promise.resolve();
  if (sessionRefreshTimer) {
    window.clearTimeout(sessionRefreshTimer);
    sessionRefreshTimer = null;
  }
  return new Promise((resolve) => {
    sessionRefreshTimer = window.setTimeout(async () => {
      sessionRefreshTimer = null;
      if (!sessionRefreshInflight) {
        sessionRefreshInflight = (async () => {
          await refreshSession();
          if (includeQuiz) {
            await loadQuiz(excludeWordId);
          }
        })().finally(() => {
          sessionRefreshInflight = null;
        });
      }
      await sessionRefreshInflight;
      resolve();
    }, delay);
  });
}

async function loadLibraryStats() {
  const parsed = await apiFetch("/api/library/stats", { method: "GET", headers: {} });
  if (parsed.ok) {
    state.libraryStats = parsed.data;
    populateTopicOptions();
    renderLibraryStats();
  } else if (libraryCountBadgeEl) {
    libraryCountBadgeEl.textContent = "Library count unavailable";
  }
}

async function loadQuiz(excludeWordId = null) {
  if (state.quizMode === "reading") {
    state.quiz = buildReadingQuizQuestion(excludeWordId || "");
    renderQuiz();
    return;
  }
  if (!state.user) {
    state.quiz = null;
    renderQuiz();
    return;
  }
  const query = new URLSearchParams({ mode: state.quizMode });
  if (excludeWordId) query.set("exclude_word_id", excludeWordId);
  const suffix = `?${query.toString()}`;
  const parsed = await apiFetch(`/api/quiz/next${suffix}`, { method: "GET", headers: {} });
  state.quiz = parsed.ok ? parsed.data.question : null;
  renderQuiz();
}

async function saveWordSelection(word) {
  if (!state.user || !word || !state.text) return;
  const persistenceKey = buildSelectionPersistenceKey(word);
  if (persistedSelectionKeys.has(persistenceKey)) return;
  try {
    const parsed = await apiFetch("/api/word-detail", {
      method: "POST",
      body: JSON.stringify({
        text: state.text,
        word,
        content_source: state.lastPayload?.content_source || state.contentSource,
      }),
    });
    if (!parsed.ok) return;
    state.glossary[word] = parsed.data;
    persistedSelectionKeys.add(persistenceKey);
    await scheduleSessionRefresh({ includeQuiz: true, excludeWordId: state.quiz?.word || null });
  } catch {
    // Keep the UI responsive even if the save side-effect fails.
  }
}

async function loadWordDetail(word) {
  if (!word) return;
  if (state.glossary[word]) {
    if (state.user && (state.lastPayload?.content_source || state.contentSource) === "library") {
      void saveWordSelection(word);
    }
    if (state.pendingFlip && state.selectedWord === word) playDesktopFlip(word);
    if (state.selectedWord === word && isMobilePreview() && state.dismissedMobileWord !== word) {
      setMobileWordSheetOpen(true);
    }
    state.pendingFlip = false;
    return;
  }
  state.loadingWord = true;
  renderSelection();
  try {
    const parsed = await apiFetch("/api/word-detail", {
      method: "POST",
      body: JSON.stringify({
        text: state.text,
        word,
        content_source: state.lastPayload?.content_source || state.contentSource,
      }),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Word detail could not be loaded.");
    state.glossary[word] = parsed.data;
    if (state.user) {
      persistedSelectionKeys.add(buildSelectionPersistenceKey(word));
      await scheduleSessionRefresh({ includeQuiz: true });
    }
  } catch (error) {
    state.glossary[word] = {
      turkish: "Türkçe anlam alınamadı.",
      context: error.message || "Word detail is not available right now.",
      example: "No example sentence available.",
      collocations: [],
    };
  } finally {
    state.loadingWord = false;
    renderSelection();
    if (state.pendingFlip && state.selectedWord === word && state.glossary[word]) playDesktopFlip(word);
    if (
      state.selectedWord === word &&
      state.glossary[word] &&
      isMobilePreview() &&
      state.dismissedMobileWord !== word
    ) {
      setMobileWordSheetOpen(true);
    }
    state.pendingFlip = false;
  }
}

function renderReadingText() {
  const tokens = tokenizeText(state.text);
  readingBodyEl.innerHTML = tokens
    .map((token) => {
      const isWord = /^[A-Za-z]+(?:['-][A-Za-z]+)*$/.test(token);
      if (!isWord) return escapeHtml(token).replace(/\n/g, "<br>");
      const key = token.toLowerCase();
      return `<button class="word" data-word="${escapeHtml(key)}">${escapeHtml(token)}</button>`;
    })
    .join("");
  const wordButtons = Array.from(readingBodyEl.querySelectorAll(".word"));
  wordButtons.forEach((button) => {
    const resolved = resolvePreferredPhrase(button);
    const isActive = resolved === state.selectedWord || button.dataset.word === state.selectedWord;
    button.classList.toggle("active", isActive);
  });

  wordButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const nextWord = resolvePreferredPhrase(button);
      if (state.selectedWord !== nextWord) {
        selectedMeaningEl.textContent = "Loading...";
        selectedContextEl.textContent = "Preparing Turkish context...";
        selectedExampleEl.textContent = "Preparing example sentence...";
      }
      state.selectedWord = nextWord;
      state.dismissedMobileWord = "";
      state.pendingFlip = true;
      renderSelection();
      renderReadingText();
      await loadWordDetail(nextWord);
    });
  });
}

function renderExperience() {
  previewStateEl.classList.add("hidden");
  readingExperienceEl.classList.remove("hidden");
  if (state.lastPayload?.content_source) {
    state.contentSource = state.lastPayload.content_source;
    updateSourceModeUi();
  }
  if (state.lastPayload?.level) {
    syncLevelPickers(state.lastPayload.level);
    updateSetupSummary();
  }
  if (state.lastPayload?.resolved_topic || state.lastPayload?.topic) {
    syncTopicPickers(state.lastPayload.resolved_topic || state.lastPayload.topic);
  }
  renderMeta(state.lastPayload.level, state.lastPayload.resolved_topic || state.lastPayload.topic, state.text);
  if (state.lastPayload.title) {
    readingTitleEl.textContent = state.lastPayload.title;
    readingTitleEl.classList.remove("hidden");
  } else {
    readingTitleEl.textContent = "";
    readingTitleEl.classList.add("hidden");
  }
  renderReadingText();
  state.selectedWord = "";
  state.loadingWord = false;
  state.pendingFlip = false;
  state.dismissedMobileWord = "";
  if (state.quizMode === "reading") {
    state.quiz = buildReadingQuizQuestion();
  }
  renderSelection();
  selectedContextEl.textContent = "The reading is ready. Tap a word to open its Turkish context.";
  selectedExampleEl.textContent = "A short example will appear here after you choose a word.";
  renderQuiz();
}

async function generateExperience(payload, triggerButton) {
  clearError();
  setLoading(triggerButton, payload.source === "library" ? "Loading..." : "Generating...", true);
  try {
    const parsed = await apiFetch("/api/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Something went wrong.");
    state.text = parsed.data.text;
    persistedSelectionKeys.clear();
    state.glossary = parsed.data.glossary || {};
    state.lastPayload = {
      ...payload,
      title: parsed.data.title || "",
      topic: payload.topic,
      resolved_topic: parsed.data.topic || payload.topic,
      content_source: parsed.data.content_source || payload.source,
    };
    manualResultEl.classList.add("hidden");
    if (state.user) {
      await refreshSession();
    }
    renderExperience();
    void fillMissingLibraryWords();
  } catch (error) {
    showError(error.message);
  } finally {
    setLoading(triggerButton, "", false);
  }
}

function buildPayload() {
  const keywords = parseKeywords(keywordsEl.value);
  const level = state.contentSource === "library" && libraryLevelEl ? libraryLevelEl.value : levelEl.value;
  const topic = state.contentSource === "library" && libraryTopicEl ? libraryTopicEl.value : topicEl.value;
  return {
    level,
    topic,
    length_target: Number(lengthEl.value),
    keywords,
    source: state.contentSource,
    exclude_title: state.contentSource === "library" ? (state.lastPayload?.title || null) : null,
  };
}

function bindPointerGlow() {
  document.addEventListener("pointermove", (event) => {
    const x = `${event.clientX}px`;
    const y = `${event.clientY}px`;
    document.documentElement.style.setProperty("--pointer-x", x);
    document.documentElement.style.setProperty("--pointer-y", y);
  });
}

generateForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = buildPayload();
  if (payload.source === "ai" && (payload.keywords.length < 2 || payload.keywords.length > 12)) {
    showError("Use 2 to 12 keywords in AI mode.");
    return;
  }
  await generateExperience(payload, $("#generateBtn"));
});

manualForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.text) {
    manualResultEl.classList.add("hidden");
    showToast("Open a reading first.", { variant: "info", scope: "manual" });
    return;
  }
  const word = manualWordEl.value.trim();
  if (!word) return;
  setLoading($("#manualBtn"), "Explaining...", true);
  try {
    const parsed = await apiFetch("/api/word-detail", {
      method: "POST",
      body: JSON.stringify({
        text: state.text,
        word,
        content_source: state.lastPayload?.content_source || state.contentSource,
      }),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Something went wrong.");
    if (state.user) {
      await refreshSession();
      await loadQuiz();
    }
    manualResultEl.innerHTML = `
      <div class="manual-result-block">
        <span class="mini-label">Turkish Meaning</span>
        <strong>${escapeHtml(parsed.data.turkish || "No match")}</strong>
      </div>
      <div class="manual-result-block">
        <span class="mini-label">Context in Turkish</span>
        <p>${highlightSelectedWord(parsed.data.context || "No context available.", word.toLowerCase())}</p>
      </div>
      <div class="manual-result-block">
        <span class="mini-label">Simple Example</span>
        <p>${highlightSelectedWord(parsed.data.example || "No example sentence available.", word.toLowerCase())}</p>
      </div>
    `;
    manualResultEl.classList.remove("hidden");
  } catch (error) {
    manualResultEl.classList.add("hidden");
    showToast(error.message, { variant: "error", scope: "manual" });
  } finally {
    setLoading($("#manualBtn"), "", false);
  }
});

authLoginForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  await submitAuthForm({
    endpoint: "/api/auth/login",
    usernameEl: authLoginUsernameEl,
    passwordEl: authLoginPasswordEl,
    errorEl: authLoginErrorEl,
    submitBtn: authLoginSubmitBtn,
    mirrorUsernameEls: [authRegisterUsernameEl, gateLoginUsernameEl, gateRegisterUsernameEl],
    mirrorPasswordEls: [authRegisterPasswordEl, gateLoginPasswordEl, gateRegisterPasswordEl],
  });
});

authRegisterForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  await submitAuthForm({
    endpoint: "/api/auth/register",
    usernameEl: authRegisterUsernameEl,
    passwordEl: authRegisterPasswordEl,
    errorEl: authRegisterErrorEl,
    submitBtn: authRegisterSubmitBtn,
    mirrorUsernameEls: [authLoginUsernameEl, gateLoginUsernameEl, gateRegisterUsernameEl],
    mirrorPasswordEls: [authLoginPasswordEl, gateLoginPasswordEl, gateRegisterPasswordEl],
  });
});

gateLoginForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  await submitAuthForm({
    endpoint: "/api/auth/login",
    usernameEl: gateLoginUsernameEl,
    passwordEl: gateLoginPasswordEl,
    errorEl: gateLoginErrorEl,
    submitBtn: gateLoginSubmitBtn,
    mirrorUsernameEls: [gateRegisterUsernameEl, authLoginUsernameEl, authRegisterUsernameEl],
    mirrorPasswordEls: [gateRegisterPasswordEl, authLoginPasswordEl, authRegisterPasswordEl],
  });
});

gateRegisterForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  await submitAuthForm({
    endpoint: "/api/auth/register",
    usernameEl: gateRegisterUsernameEl,
    passwordEl: gateRegisterPasswordEl,
    errorEl: gateRegisterErrorEl,
    submitBtn: gateRegisterSubmitBtn,
    mirrorUsernameEls: [gateLoginUsernameEl, authLoginUsernameEl, authRegisterUsernameEl],
    mirrorPasswordEls: [gateLoginPasswordEl, authLoginPasswordEl, authRegisterPasswordEl],
  });
});

showLoginBtn.addEventListener("click", () => {
  state.authMode = "login";
  renderAuthMode();
});

showRegisterBtn.addEventListener("click", () => {
  state.authMode = "register";
  renderAuthMode();
});

gateShowLoginBtn?.addEventListener("click", () => {
  state.authMode = "login";
  renderAuthMode();
});

gateShowRegisterBtn?.addEventListener("click", () => {
  state.authMode = "register";
  renderAuthMode();
});

[
  [authLoginUsernameEl, authRegisterUsernameEl],
  [authLoginUsernameEl, gateLoginUsernameEl],
  [authLoginUsernameEl, gateRegisterUsernameEl],
  [authLoginPasswordEl, authRegisterPasswordEl],
  [authLoginPasswordEl, gateLoginPasswordEl],
  [authLoginPasswordEl, gateRegisterPasswordEl],
  [authRegisterUsernameEl, gateLoginUsernameEl],
  [authRegisterUsernameEl, gateRegisterUsernameEl],
  [authRegisterPasswordEl, gateLoginPasswordEl],
  [authRegisterPasswordEl, gateRegisterPasswordEl],
  [gateLoginUsernameEl, gateRegisterUsernameEl],
  [gateLoginPasswordEl, gateRegisterPasswordEl],
].forEach(([firstEl, secondEl]) => {
  syncInputPair(firstEl, secondEl);
  syncInputPair(secondEl, firstEl);
});

continueGuestBtn?.addEventListener("click", () => completeAppEntry(true));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setLibraryView(null);
    setNavMenuOpen(false);
    setMobileWordSheetOpen(false);
  }
});

document.addEventListener("click", (event) => {
  if (!navMenuShellEl?.contains(event.target)) {
    setNavMenuOpen(false);
  }
});

async function handleLogout(event) {
  event?.preventDefault?.();
  event?.stopPropagation?.();
  if (state.loggingOut) return;
  const logoutTrigger =
    event?.target?.closest?.("#logoutBtn") ||
    logoutBtn ||
    document.getElementById("logoutBtn");
  state.loggingOut = true;
  setLoading(logoutTrigger, "Logging out...", true);
  try {
    await apiFetch("/api/auth/logout", { method: "POST" });
    state.user = null;
    state.stats = emptyStats();
    state.recentWords = [];
    state.readingHistory = [];
    state.progressHistory = [];
    state.social = { friends: [], incoming: [], outgoing: [], suggestions: [], cheers_received: 0 };
    state.quiz = null;
    state.hasEnteredApp = false;
    window.sessionStorage.removeItem(GUEST_FLAG_KEY);
    renderUserPanel();
    renderWelcomeGate();
    setLibraryView(null);
  } finally {
    state.loggingOut = false;
    setLoading(logoutTrigger, "", false);
  }
}

logoutBtn?.addEventListener("click", handleLogout);
logoutBtn?.addEventListener("touchend", handleLogout, { passive: false });
logoutBtn?.addEventListener("pointerup", handleLogout);

clearSavedWordsBtn?.addEventListener("click", async () => {
  const parsed = await apiFetch("/api/saved-words/clear", { method: "POST" });
  if (!parsed.ok) return;
  state.stats = parsed.data.stats || emptyStats();
  state.recentWords = [];
  state.quiz = null;
  state.quizStats = { answered: 0, correct: 0, streak: 0 };
  renderUserPanel();
});

randomizeSavedWordsBtn?.addEventListener("click", async () => {
  await fetchSavedWords("random");
});

quizModeSavedBtn?.addEventListener("click", async () => {
  state.quizMode = "saved";
  await loadQuiz();
});

quizModeHardBtn?.addEventListener("click", async () => {
  state.quizMode = "hard";
  await loadQuiz();
});

quizModeReadingBtn?.addEventListener("click", async () => {
  state.quizMode = "reading";
  await loadQuiz();
});

regenBtn.addEventListener("click", async () => {
  if (!state.lastPayload) return;
  const payload = {
    ...state.lastPayload,
    exclude_title: state.lastPayload.content_source === "library" ? state.lastPayload.title : null,
  };
  await generateExperience(payload, regenBtn);
});

clearBtn.addEventListener("click", () => {
  state.text = "";
  state.glossary = {};
  state.selectedWord = "";
  state.loadingWord = false;
  state.pendingFlip = false;
  state.quiz = null;
  setMobileWordSheetOpen(false);
  previewStateEl.classList.remove("hidden");
  readingExperienceEl.classList.add("hidden");
  manualResultEl.classList.add("hidden");
  clearError();
});

nextQuizBtn.addEventListener("click", () => loadQuiz(state.quizMode === "reading" ? state.quiz?.word || null : state.quiz?.word_id || null));
profileAvatarBtn?.addEventListener("click", (event) => {
  event.preventDefault();
  event.stopPropagation();
  openLibraryPanel("profile");
});
navMenuTriggerEl?.addEventListener("click", (event) => {
  event.preventDefault();
  event.stopPropagation();
  if (isDesktopMenuMode()) {
    setNavMenuOpen(true);
    return;
  }
  setNavMenuOpen(!navMenuShellEl?.classList.contains("is-open"));
});
navMenuShellEl?.addEventListener("mouseenter", () => {
  if (isDesktopMenuMode()) setNavMenuOpen(true);
});
navMenuShellEl?.addEventListener("mouseleave", () => {
  if (!isDesktopMenuMode()) return;
  navMenuCloseTimer = window.setTimeout(() => {
    setNavMenuOpen(false);
  }, 140);
});
navMenuShellEl?.addEventListener("focusin", () => {
  if (isDesktopMenuMode()) setNavMenuOpen(true);
});
navMenuShellEl?.addEventListener("focusout", () => {
  window.setTimeout(() => {
    if (!navMenuShellEl?.contains(document.activeElement)) {
      setNavMenuOpen(false);
    }
  }, 0);
});
bindNavMenuAction(openProfileBtn, "profile");
bindNavMenuAction(openProgressBtn, "progress");
bindNavMenuAction(openSocialBtn, "social");
bindNavMenuAction(openSavedWordsBtn, "saved");
bindNavMenuAction(openQuizBtn, "quiz");
bindNavMenuAction(openManualHelpBtn, "manual");
bindNavMenuAction(openInfoBtn, "info");
navMenuSwitchEls.forEach((button) => {
  button.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();
    setNavMenuCategory(button.dataset.menuCategory || "account");
  });
});
socialAddFormEl?.addEventListener("submit", async (event) => {
  event.preventDefault();
  await sendFriendRequest();
});
closeMobileWordBtn?.addEventListener("click", closeMobileWordSheet);
mobileWordHandleBtn?.addEventListener("click", closeMobileWordSheet);
mobileWordBackdropEl?.addEventListener("click", closeMobileWordSheet);
pronounceWordBtn?.addEventListener("click", (event) => {
  event.stopPropagation();
  playPronunciation(state.selectedWord);
});
mobilePronounceWordBtn?.addEventListener("click", (event) => {
  event.stopPropagation();
  playPronunciation(state.selectedWord);
});
closeLibraryBtn.addEventListener("click", () => setLibraryView(null));
libraryHandleBtn?.addEventListener("click", () => setLibraryView(null));
libraryOverlayEl.addEventListener("click", () => setLibraryView(null));

registerSheetDrag(mobileWordHandleBtn, mobileWordPanelEl, closeMobileWordSheet, () => mobileWordSheetEl?.classList.contains("sheet-open"));
registerSheetDrag(libraryHandleBtn, libraryPanelScrollEl, () => setLibraryView(null), () => !libraryPanelEl?.classList.contains("hidden"));

themeToggleBtn?.addEventListener("click", toggleTheme);

flipCardEl.addEventListener("click", () => {
  if (state.loadingWord || !state.selectedWord) return;
  flipCardEl.classList.toggle("flipped");
});

flipCardEl.addEventListener("keydown", (event) => {
  if (state.loadingWord || !state.selectedWord) return;
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    flipCardEl.classList.toggle("flipped");
  }
});

levelEl.addEventListener("change", updateLevelUi);
topicEl.addEventListener("change", updateTopicDefaults);
lengthEl.addEventListener("input", () => {
  lengthValueEl.textContent = lengthEl.value;
  updateSetupSummary();
  updateRangeVisual();
});
keywordsEl.addEventListener("input", renderKeywordChips);

sourceSwitchEl.querySelectorAll(".source-pill").forEach((button) => {
  button.addEventListener("click", () => {
    state.contentSource = button.dataset.source;
    sourceSwitchEl.querySelectorAll(".source-pill").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    updateSourceModeUi();
    clearError();
  });
});

libraryLevelEl?.addEventListener("change", () => {
  levelEl.value = libraryLevelEl.value;
  populateTopicOptions();
  updateLevelUi();
});

libraryTopicEl?.addEventListener("change", () => {
  topicEl.value = libraryTopicEl.value;
  syncTopicPickers(libraryTopicEl.value);
});

bindPointerGlow();
updateLevelUi();
updateTopicDefaults();
updateRangeVisual();
renderAuthMode();
renderUserPanel();
setLibraryView(null);
updateSourceModeUi();
const savedTheme = window.localStorage.getItem(THEME_STORAGE_KEY);
applyTheme(savedTheme === "dark" ? "dark" : "light");
syncViewModeFromViewport();
renderKeywordChips();
renderWelcomeGate();
setNavMenuCategory("account");
window.addEventListener("resize", syncViewModeFromViewport);
refreshSession().then(async () => {
  if (state.user) completeAppEntry(false);
  renderWelcomeGate();
  await loadQuiz();
  await loadFeaturedPhrasalReadingIfEmpty();
});
loadLibraryStats();
