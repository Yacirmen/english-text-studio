const LEVEL_CONFIG = {
  A1: { min: 60, max: 100, hint: "Very simple and everyday" },
  A2: { min: 90, max: 130, hint: "Simple, clear, and familiar" },
  B1: { min: 120, max: 170, hint: "Natural and comfortably paced" },
  B2: { min: 150, max: 220, hint: "Richer but still easy to read" },
  C1: { min: 180, max: 260, hint: "Advanced, natural, and detailed" },
  Academic: { min: 190, max: 280, hint: "Analytical and academic" },
};

const TOPIC_KEYWORDS = {
  Random: ["story", "daily", "idea", "change"],
  Open: ["morning", "project", "travel", "friend"],
  "Daily Life": ["morning", "coffee", "routine", "friend"],
  School: ["student", "teacher", "library", "study"],
  Travel: ["travel", "city", "hotel", "ticket"],
  "Work Life": ["meeting", "project", "office", "email"],
  Academic: ["research", "analysis", "evidence", "study"],
  Science: ["science", "evidence", "method", "observation"],
  Health: ["health", "routine", "balance", "habit"],
  Sport: ["team", "practice", "focus", "goal"],
  "Data Science": ["dataset", "model", "pattern", "analysis"],
  "Computer Science": ["algorithm", "logic", "system", "code"],
  Technology: ["product", "interface", "tool", "feature"],
  Finance: ["budget", "saving", "expense", "plan"],
  Environment: ["energy", "waste", "climate", "action"],
  Psychology: ["attention", "emotion", "habit", "stress"],
  Communication: ["message", "feedback", "clarity", "conversation"],
  Arts: ["studio", "practice", "composition", "form"],
  Culture: ["ritual", "community", "memory", "tradition"],
  Food: ["meal", "kitchen", "recipe", "flavor"],
  "Public Services": ["service", "system", "access", "public"],
  Media: ["article", "story", "platform", "audience"],
};

const TOPIC_ORDER = [
  "Random",
  "Open",
  "Daily Life",
  "School",
  "Travel",
  "Work Life",
  "Science",
  "Health",
  "Sport",
  "Academic",
  "Data Science",
  "Computer Science",
  "Technology",
  "Finance",
  "Environment",
  "Psychology",
  "Communication",
  "Arts",
  "Culture",
  "Food",
  "Public Services",
  "Media",
];

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
  stats: { saved_words: 0, mastered_words: 0, saved_today: 0, daily_goal: 5, streak: 0, hard_words: 0 },
  recentWords: [],
  readingHistory: [],
  quiz: null,
  quizMode: "saved",
  libraryView: null,
  libraryStats: null,
  quizStats: { answered: 0, correct: 0, streak: 0 },
  hasEnteredApp: window.sessionStorage.getItem("ets_guest") === "1",
  viewMode: window.innerWidth < 860 ? "mobile" : "web",
};

const $ = (selector) => document.querySelector(selector);
const welcomeGateEl = $("#welcomeGate");
const gateAuthForm = $("#gateAuthForm");
const gateAuthEmailEl = $("#gateAuthEmail");
const gateAuthPasswordEl = $("#gateAuthPassword");
const gateAuthErrorEl = $("#gateAuthError");
const gateAuthSubmitBtn = $("#gateAuthSubmitBtn");
const gateShowLoginBtn = $("#gateShowLoginBtn");
const gateShowRegisterBtn = $("#gateShowRegisterBtn");
const continueGuestBtn = $("#continueGuestBtn");
const pageShell = $(".page-shell");
const themeToggleBtn = $("#themeToggleBtn");
const profileTriggerBtn = $("#profileTriggerBtn");
const profileTriggerInitialsEl = $("#profileTriggerInitials");
const profileMenuEl = $("#profileMenu");
const profileOverlayEl = $("#profileOverlay");
const closeProfileMenuBtn = $("#closeProfileMenuBtn");
const profileHandleBtn = $("#profileHandleBtn");
const profileMenuTitleEl = $("#profileMenuTitle");
const profileMenuBadgeEl = $("#profileMenuBadge");
const profileTipTextEl = $("#profileTipText");
const generateForm = $("#generate-form");
const manualForm = $("#manual-form");
const authForm = $("#authForm");
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
const authUsernameEl = $("#authUsername");
const authPasswordEl = $("#authPassword");
const authErrorEl = $("#authError");
const authSubmitBtn = $("#authSubmitBtn");
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
const readingHistoryListEl = $("#readingHistoryList");
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
const openSavedWordsBtn = $("#openSavedWordsBtn");
const openQuizBtn = $("#openQuizBtn");
const openManualHelpBtn = $("#openManualHelpBtn");
const libraryOverlayEl = $("#libraryOverlay");
const libraryPanelEl = $("#libraryPanel");
const savedWordsPanelEl = $("#savedWordsPanel");
const quizPanelEl = $("#quizPanel");
const manualHelpPanelEl = $("#manualHelpPanel");
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
  window.localStorage.setItem("ets_theme", isDark ? "dark" : "light");
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

function tokenizeText(text) {
  return text.match(/[A-Za-z]+(?:['-][A-Za-z]+)*|\s+|[^A-Za-z\s]/g) || [];
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
  generateErrorEl.textContent = message;
  generateErrorEl.classList.remove("hidden");
}

function clearError() {
  generateErrorEl.textContent = "";
  generateErrorEl.classList.add("hidden");
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
  const statTopics = Array.isArray(state.libraryStats?.by_topic)
    ? state.libraryStats.by_topic.map((item) => item.topic).filter(Boolean)
    : [];
  const ordered = TOPIC_ORDER.filter((topic) => topic === "Random" || statTopics.includes(topic));
  const extras = statTopics.filter((topic) => !ordered.includes(topic)).sort((a, b) => a.localeCompare(b));
  return ["Random", ...ordered.filter((topic) => topic !== "Random"), ...extras];
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
    : highlightSelectedWord(item.context || "Context appears here after you choose a word.", state.selectedWord);
  const exampleHtml = state.loadingWord
    ? "Preparing example sentence..."
    : highlightSelectedWord(item.example || "A short example appears here after you choose a word.", state.selectedWord);

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
        quizFeedbackEl.textContent = parsed.data.detail || "Quiz answer could not be saved.";
        quizFeedbackEl.classList.remove("hidden");
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
  savedWordsPanelEl.classList.toggle("hidden", view !== "saved");
  quizPanelEl.classList.toggle("hidden", view !== "quiz");
  manualHelpPanelEl.classList.toggle("hidden", view !== "manual");
  if (libraryPanelScrollEl) libraryPanelScrollEl.style.transform = "";
  if (view === "saved") {
    libraryKickerEl.textContent = "Saved Words";
    libraryTitleEl.textContent = "Your saved words";
  } else if (view === "quiz") {
    libraryKickerEl.textContent = "Mini Quiz";
    libraryTitleEl.textContent = "Quick review";
  } else if (view === "manual") {
    libraryKickerEl.textContent = "Translate";
    libraryTitleEl.textContent = "Quick translation";
  }
}

function renderUserPanel() {
  const loggedIn = Boolean(state.user);
  authGuestEl.classList.toggle("hidden", loggedIn);
  authUserEl.classList.toggle("hidden", !loggedIn);
  if (loggedIn) {
    accountNameEl.textContent = state.user.username;
    savedWordsCountEl.textContent = state.stats.saved_words || 0;
    masteredWordsCountEl.textContent = state.stats.mastered_words || 0;
    if (profileMenuTitleEl) profileMenuTitleEl.textContent = state.user.username;
    if (profileMenuBadgeEl) profileMenuBadgeEl.textContent = `${state.stats.saved_words || 0} saved`;
    if (profileTipTextEl) {
      profileTipTextEl.textContent =
        (state.stats.saved_words || 0) > 0
          ? "Your saved words and quiz streak live here. Open review from the toolbar anytime."
          : "Start tapping words in a reading and your personal review stack will build here.";
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
    if (readingHistoryListEl) {
      if (!state.readingHistory.length) {
        readingHistoryListEl.innerHTML = `<p class="history-empty">Your recent readings will appear here.</p>`;
      } else {
        readingHistoryListEl.innerHTML = state.readingHistory
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
            setProfileMenuOpen(false);
            renderExperience();
          });
        });
      }
    }
    if (profileTriggerInitialsEl) {
      profileTriggerInitialsEl.textContent = state.user.username.slice(0, 1).toUpperCase();
    }
    profileTriggerBtn?.classList.add("signed-in");
  } else {
    if (profileMenuTitleEl) profileMenuTitleEl.textContent = "Guest mode";
    if (profileMenuBadgeEl) profileMenuBadgeEl.textContent = "Explore";
    if (profileTriggerInitialsEl) profileTriggerInitialsEl.textContent = "G";
    if (readingHistoryListEl) readingHistoryListEl.innerHTML = `<p class="history-empty">Sign in to keep your reading trail.</p>`;
    if (dailyGoalTextEl) dailyGoalTextEl.textContent = "0 / 5 today";
    if (streakBadgeEl) streakBadgeEl.textContent = "Streak 0";
    if (goalBarFillEl) goalBarFillEl.style.width = "0%";
    if (hardWordsTextEl) hardWordsTextEl.textContent = "0 hard words ready for review.";
    profileTriggerBtn?.classList.remove("signed-in");
  }
  renderSavedWords();
  renderQuiz();
}

function setProfileMenuOpen(isOpen) {
  profileMenuEl?.classList.toggle("hidden", !isOpen);
  profileOverlayEl?.classList.toggle("hidden", !isOpen || !isMobilePreview());
  profileTriggerBtn?.setAttribute("aria-expanded", isOpen ? "true" : "false");
  document.body.classList.toggle("profile-open", isOpen && isMobilePreview());
  if (profileMenuEl) profileMenuEl.style.transform = "";
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

function renderAuthMode() {
  const isLogin = state.authMode === "login";
  showLoginBtn.classList.toggle("active", isLogin);
  showRegisterBtn.classList.toggle("active", !isLogin);
  gateShowLoginBtn?.classList.toggle("active", isLogin);
  gateShowRegisterBtn?.classList.toggle("active", !isLogin);
  authSubmitBtn.textContent = isLogin ? "Log In" : "Sign Up";
  if (gateAuthSubmitBtn) gateAuthSubmitBtn.textContent = isLogin ? "Log In" : "Sign Up";
}

function renderWelcomeGate() {
  const shouldShow = !state.user && !state.hasEnteredApp;
  welcomeGateEl?.classList.toggle("hidden", !shouldShow);
  document.body.classList.toggle("gate-open", shouldShow);
}

function completeAppEntry(asGuest = false) {
  state.hasEnteredApp = true;
  if (asGuest) {
    window.sessionStorage.setItem("ets_guest", "1");
  } else {
    window.sessionStorage.removeItem("ets_guest");
  }
  renderWelcomeGate();
}
async function refreshSession() {
  const parsed = await apiFetch("/api/auth/me", { method: "GET", headers: {} });
  if (parsed.ok) {
    state.user = parsed.data.user;
    state.stats = parsed.data.stats || { saved_words: 0, mastered_words: 0, saved_today: 0, daily_goal: 5, streak: 0, hard_words: 0 };
    state.recentWords = parsed.data.recent_words || [];
    state.readingHistory = parsed.data.history || [];
  }
  renderUserPanel();
}

async function loadLibraryStats() {
  const parsed = await apiFetch("/api/library/stats", { method: "GET", headers: {} });
  if (parsed.ok) {
    state.libraryStats = parsed.data;
    populateTopicOptions();
    renderLibraryStats();
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
    await refreshSession();
    await loadQuiz(state.quiz?.word || null);
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
      await refreshSession();
      await loadQuiz();
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
      const active = key === state.selectedWord ? "active" : "";
      return `<button class="word ${active}" data-word="${escapeHtml(key)}">${escapeHtml(token)}</button>`;
    })
    .join("");
  readingBodyEl.querySelectorAll(".word").forEach((button) => {
    button.addEventListener("click", async () => {
      const nextWord = button.dataset.word;
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
    manualResultEl.textContent = "Open a reading first.";
    manualResultEl.classList.remove("hidden");
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
    manualResultEl.textContent = error.message;
    manualResultEl.classList.remove("hidden");
  } finally {
    setLoading($("#manualBtn"), "", false);
  }
});

authForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  authErrorEl.classList.add("hidden");
  const endpoint = state.authMode === "login" ? "/api/auth/login" : "/api/auth/register";
  setLoading(authSubmitBtn, state.authMode === "login" ? "Logging in..." : "Creating account...", true);
  try {
    const parsed = await apiFetch(endpoint, {
      method: "POST",
      body: JSON.stringify({
        username: authUsernameEl.value.trim(),
        password: authPasswordEl.value.trim(),
      }),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Authentication failed.");
    state.user = parsed.data.user;
    state.stats = parsed.data.stats || { saved_words: 0, mastered_words: 0 };
    authUsernameEl.value = "";
    authPasswordEl.value = "";
    completeAppEntry(false);
    await refreshSession();
    await loadQuiz();
  } catch (error) {
    authErrorEl.textContent = error.message;
    authErrorEl.classList.remove("hidden");
  } finally {
    setLoading(authSubmitBtn, "", false);
  }
});

gateAuthForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  gateAuthErrorEl.classList.add("hidden");
  const endpoint = state.authMode === "login" ? "/api/auth/login" : "/api/auth/register";
  setLoading(gateAuthSubmitBtn, state.authMode === "login" ? "Logging in..." : "Creating account...", true);
  try {
    const payload = {
      username: gateAuthEmailEl.value.trim(),
      password: gateAuthPasswordEl.value.trim(),
    };
    const parsed = await apiFetch(endpoint, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Authentication failed.");
    authUsernameEl.value = payload.username;
    authPasswordEl.value = "";
    gateAuthEmailEl.value = "";
    gateAuthPasswordEl.value = "";
    state.user = parsed.data.user;
    state.stats = parsed.data.stats || { saved_words: 0, mastered_words: 0 };
    completeAppEntry(false);
    await refreshSession();
    await loadQuiz();
  } catch (error) {
    gateAuthErrorEl.textContent = error.message;
    gateAuthErrorEl.classList.remove("hidden");
  } finally {
    setLoading(gateAuthSubmitBtn, "", false);
  }
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

continueGuestBtn?.addEventListener("click", () => completeAppEntry(true));

profileTriggerBtn?.addEventListener("click", (event) => {
  event.stopPropagation();
  const willOpen = profileMenuEl?.classList.contains("hidden");
  setProfileMenuOpen(Boolean(willOpen));
});

profileMenuEl?.addEventListener("click", (event) => {
  event.stopPropagation();
});

profileOverlayEl?.addEventListener("click", () => setProfileMenuOpen(false));
closeProfileMenuBtn?.addEventListener("click", () => setProfileMenuOpen(false));
profileHandleBtn?.addEventListener("click", () => setProfileMenuOpen(false));

document.addEventListener("click", () => setProfileMenuOpen(false));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setProfileMenuOpen(false);
    setMobileWordSheetOpen(false);
  }
});

logoutBtn.addEventListener("click", async () => {
  await apiFetch("/api/auth/logout", { method: "POST" });
  state.user = null;
  state.stats = { saved_words: 0, mastered_words: 0 };
  state.recentWords = [];
  state.readingHistory = [];
  state.quiz = null;
  state.hasEnteredApp = false;
  window.sessionStorage.removeItem("ets_guest");
  renderUserPanel();
  renderWelcomeGate();
  setProfileMenuOpen(false);
});

clearSavedWordsBtn?.addEventListener("click", async () => {
  const parsed = await apiFetch("/api/saved-words/clear", { method: "POST" });
  if (!parsed.ok) return;
  state.stats = parsed.data.stats || { saved_words: 0, mastered_words: 0 };
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
openSavedWordsBtn.addEventListener("click", async () => {
  if (state.user) await fetchSavedWords("recent");
  setLibraryView("saved");
});
openQuizBtn.addEventListener("click", async () => {
  if (!state.quiz && state.user) await loadQuiz();
  setLibraryView("quiz");
});
openManualHelpBtn.addEventListener("click", () => setLibraryView("manual"));
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
registerSheetDrag(profileHandleBtn, profileMenuEl, () => setProfileMenuOpen(false), () => !profileMenuEl?.classList.contains("hidden"));

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
applyTheme(window.localStorage.getItem("ets_theme") === "dark" ? "dark" : "light");
syncViewModeFromViewport();
renderKeywordChips();
renderWelcomeGate();
window.addEventListener("resize", syncViewModeFromViewport);
refreshSession().then(async () => {
  if (state.user) completeAppEntry(false);
  renderWelcomeGate();
  await loadQuiz();
});
loadLibraryStats();
