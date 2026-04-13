const LEVEL_CONFIG = {
  A1: { min: 60, max: 100, hint: "Very simple and everyday" },
  A2: { min: 90, max: 130, hint: "Simple, clear, and familiar" },
  B1: { min: 120, max: 170, hint: "Natural and comfortably paced" },
  B2: { min: 150, max: 220, hint: "Richer but still easy to read" },
  C1: { min: 180, max: 260, hint: "Advanced, natural, and detailed" },
  Academic: { min: 190, max: 280, hint: "Analytical and academic" },
};

const TOPIC_KEYWORDS = {
  "Günlük Hayat": ["morning", "coffee", "routine", "friend"],
  Okul: ["student", "teacher", "library", "study"],
  Seyahat: ["travel", "city", "hotel", "ticket"],
  "İş Hayatı": ["meeting", "project", "office", "email"],
  Akademik: ["research", "analysis", "evidence", "study"],
  Science: ["science", "evidence", "method", "observation"],
  Health: ["health", "routine", "balance", "habit"],
  Sport: ["team", "practice", "focus", "goal"],
  Serbest: ["morning", "project", "travel", "friend"],
};

const state = {
  text: "",
  glossary: {},
  selectedWord: "",
  lastPayload: null,
  contentSource: "library",
  loadingWord: false,
  pendingFlip: false,
  authMode: "login",
  user: null,
  stats: { saved_words: 0, mastered_words: 0 },
  recentWords: [],
  quiz: null,
  libraryView: null,
  libraryStats: null,
  quizStats: { answered: 0, correct: 0, streak: 0 },
};

const $ = (selector) => document.querySelector(selector);
const pageShell = $(".page-shell");
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
const savedWordsEmptyEl = $("#savedWordsEmpty");
const savedWordsListEl = $("#savedWordsList");
const clearSavedWordsBtn = $("#clearSavedWordsBtn");
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
const sourceSwitchEl = $("#sourceSwitch");
const libraryModeHintEl = $("#libraryModeHint");
const libraryControlsEl = $("#libraryControls");
const libraryLevelEl = $("#libraryLevel");
const libraryTopicEl = $("#libraryTopic");
const aiControlsEl = $("#aiControls");
const libraryCountBadgeEl = $("#libraryCountBadge");

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
  if (!selectedWord) return escapedText;
  const pattern = new RegExp(`\\b(${selectedWord.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})\\b`, "gi");
  return escapedText.replace(pattern, '<strong class="inline-highlight">$1</strong>');
}

function tokenizeText(text) {
  return text.match(/[A-Za-z]+(?:['-][A-Za-z]+)*|\s+|[^A-Za-z\s]/g) || [];
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
  renderMeta(state.lastPayload?.level || levelEl.value, state.lastPayload?.topic || topicEl.value, state.text || "");
}

function renderLibraryStats() {
  if (!libraryCountBadgeEl || !state.libraryStats) return;
  libraryCountBadgeEl.textContent = `${Number(state.libraryStats.total || 0)} curated readings inside`;
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
  selectedWordEl.textContent = state.selectedWord || "Word";
  selectedMeaningEl.textContent = item.turkish || "Choose a word";
  selectedContextEl.innerHTML = state.loadingWord
    ? "Preparing Turkish context..."
    : highlightSelectedWord(item.context || "Context appears here after you choose a word.", state.selectedWord);
  selectedExampleEl.innerHTML = state.loadingWord
    ? "Preparing example sentence..."
    : highlightSelectedWord(item.example || "A short example appears here after you choose a word.", state.selectedWord);
  flipCardEl.classList.remove("flipped");
  flipCardEl.classList.toggle("clickable", !state.loadingWord && Boolean(state.selectedWord));
}

function renderSavedWords() {
  if (!state.user || !state.recentWords.length) {
    savedWordsEmptyEl.classList.remove("hidden");
    savedWordsListEl.classList.add("hidden");
    savedWordsListEl.innerHTML = "";
    clearSavedWordsBtn?.classList.add("hidden");
    return;
  }
  savedWordsEmptyEl.classList.add("hidden");
  savedWordsListEl.classList.remove("hidden");
  clearSavedWordsBtn?.classList.remove("hidden");
  savedWordsListEl.innerHTML = state.recentWords
    .map(
      (item) => `
        <button class="saved-word-item" type="button" data-word="${escapeHtml(item.word)}">
          <strong>${escapeHtml(item.word)}</strong>
          <span>${escapeHtml(item.turkish)}</span>
        </button>
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
}

function renderQuiz() {
  if (quizAnsweredBadgeEl) quizAnsweredBadgeEl.textContent = `${state.quizStats.answered} played`;
  if (quizStreakBadgeEl) quizStreakBadgeEl.textContent = `Streak ${state.quizStats.streak}`;
  if (!state.user) {
    quizEmptyEl.textContent = "Sign in first to unlock the quiz.";
    quizEmptyEl.classList.remove("hidden");
    quizCardEl.classList.add("hidden");
    return;
  }
  if (!state.quiz) {
    quizEmptyEl.textContent = "You need at least 4 saved words to start the quiz.";
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
      const parsed = await apiFetch("/api/quiz/check", {
        method: "POST",
        body: JSON.stringify({ word_id: state.quiz.word_id, answer: button.dataset.answer }),
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
        ? `Correct. "${parsed.data.word}" = "${parsed.data.answer}".`
        : `Not this time. Correct answer: ${parsed.data.answer}`;
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
    });
  });
}

function setLibraryView(view) {
  state.libraryView = view;
  const isOpen = Boolean(view);
  libraryOverlayEl.classList.toggle("hidden", !isOpen);
  libraryPanelEl.classList.toggle("hidden", !isOpen);
  savedWordsPanelEl.classList.toggle("hidden", view !== "saved");
  quizPanelEl.classList.toggle("hidden", view !== "quiz");
  manualHelpPanelEl.classList.toggle("hidden", view !== "manual");
  if (view === "saved") {
    libraryKickerEl.textContent = "Saved Words";
    libraryTitleEl.textContent = "Your saved words";
  } else if (view === "quiz") {
    libraryKickerEl.textContent = "Mini Quiz";
    libraryTitleEl.textContent = "Quick review";
  } else if (view === "manual") {
    libraryKickerEl.textContent = "Quick Word Help";
    libraryTitleEl.textContent = "Fast word support";
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
  }
  renderSavedWords();
  renderQuiz();
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
  authSubmitBtn.textContent = isLogin ? "Log In" : "Sign Up";
}

async function refreshSession() {
  const parsed = await apiFetch("/api/auth/me", { method: "GET", headers: {} });
  if (parsed.ok) {
    state.user = parsed.data.user;
    state.stats = parsed.data.stats || { saved_words: 0, mastered_words: 0 };
    state.recentWords = parsed.data.recent_words || [];
  }
  renderUserPanel();
}

async function loadLibraryStats() {
  const parsed = await apiFetch("/api/library/stats", { method: "GET", headers: {} });
  if (parsed.ok) {
    state.libraryStats = parsed.data;
    renderLibraryStats();
  }
}

async function loadQuiz() {
  if (!state.user) {
    state.quiz = null;
    renderQuiz();
    return;
  }
  const parsed = await apiFetch("/api/quiz/next", { method: "GET", headers: {} });
  state.quiz = parsed.ok ? parsed.data.question : null;
  renderQuiz();
}

async function loadWordDetail(word) {
  if (!word) return;
  if (state.glossary[word]) {
    if (state.pendingFlip && state.selectedWord === word) flipCardEl.classList.add("flipped");
    state.pendingFlip = false;
    return;
  }
  state.loadingWord = true;
  renderSelection();
  try {
    const parsed = await apiFetch("/api/word-detail", {
      method: "POST",
      body: JSON.stringify({ text: state.text, word }),
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
    };
  } finally {
    state.loadingWord = false;
    renderSelection();
    if (state.pendingFlip && state.selectedWord === word && state.glossary[word]) flipCardEl.classList.add("flipped");
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
  renderMeta(state.lastPayload.level, state.lastPayload.topic, state.text);
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
  renderSelection();
  selectedContextEl.textContent = "The reading is ready. Tap a word to open its Turkish context.";
  selectedExampleEl.textContent = "A short example will appear here after you choose a word.";
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
    state.glossary = {};
    state.lastPayload = {
      ...payload,
      title: parsed.data.title || "",
      content_source: parsed.data.content_source || payload.source,
    };
    manualResultEl.classList.add("hidden");
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
      body: JSON.stringify({ text: state.text, word }),
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
    await refreshSession();
    await loadQuiz();
  } catch (error) {
    authErrorEl.textContent = error.message;
    authErrorEl.classList.remove("hidden");
  } finally {
    setLoading(authSubmitBtn, "", false);
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

logoutBtn.addEventListener("click", async () => {
  await apiFetch("/api/auth/logout", { method: "POST" });
  state.user = null;
  state.stats = { saved_words: 0, mastered_words: 0 };
  state.recentWords = [];
  state.quiz = null;
  renderUserPanel();
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
  previewStateEl.classList.remove("hidden");
  readingExperienceEl.classList.add("hidden");
  manualResultEl.classList.add("hidden");
  clearError();
});

nextQuizBtn.addEventListener("click", loadQuiz);
openSavedWordsBtn.addEventListener("click", () => setLibraryView("saved"));
openQuizBtn.addEventListener("click", async () => {
  if (!state.quiz && state.user) await loadQuiz();
  setLibraryView("quiz");
});
openManualHelpBtn.addEventListener("click", () => setLibraryView("manual"));
closeLibraryBtn.addEventListener("click", () => setLibraryView(null));
libraryOverlayEl.addEventListener("click", () => setLibraryView(null));

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
renderKeywordChips();
refreshSession().then(loadQuiz);
loadLibraryStats();
