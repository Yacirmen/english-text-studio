const LEVEL_CONFIG = {
  A1: { min: 60, max: 100, hint: "Çok temel ve günlük" },
  A2: { min: 90, max: 130, hint: "Basit ve günlük" },
  B1: { min: 120, max: 170, hint: "Doğal ve akıcı" },
  B2: { min: 150, max: 220, hint: "Daha zengin ama rahat okunur" },
  C1: { min: 180, max: 260, hint: "İleri, doğal ve detaylı" },
  Academic: { min: 190, max: 280, hint: "Akademik ve analitik" },
};

const TOPIC_KEYWORDS = {
  "Günlük Hayat": ["morning", "coffee", "bus", "friend"],
  Okul: ["student", "exam", "library", "teacher"],
  Seyahat: ["airport", "hotel", "ticket", "city"],
  "İş Hayatı": ["meeting", "project", "office", "email"],
  Akademik: ["research", "analysis", "evidence", "study"],
  Serbest: ["morning", "project", "travel", "friend"],
};

const state = {
  text: "",
  glossary: {},
  selectedWord: "",
  lastPayload: null,
  loadingWord: false,
  pendingFlip: false,
  authMode: "login",
  user: null,
  stats: { saved_words: 0, mastered_words: 0 },
  recentWords: [],
  quiz: null,
  libraryView: null,
};

const $ = (selector) => document.querySelector(selector);
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
const quizEmptyEl = $("#quizEmpty");
const quizCardEl = $("#quizCard");
const quizPromptEl = $("#quizPrompt");
const quizOptionsEl = $("#quizOptions");
const quizFeedbackEl = $("#quizFeedback");
const nextQuizBtn = $("#nextQuizBtn");
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

async function parseApiResponse(response) {
  const raw = await response.text();
  try {
    return { ok: response.ok, status: response.status, data: JSON.parse(raw) };
  } catch {
    return { ok: response.ok, status: response.status, data: { detail: raw || "Bilinmeyen hata" } };
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
  return escapedText.replace(pattern, "<strong class=\"inline-highlight\">$1</strong>");
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
  setupLengthBadgeEl.textContent = `${lengthEl.value} kelime civarı`;
}

function updateRangeVisual() {
  const min = Number(lengthEl.min || 0);
  const max = Number(lengthEl.max || 100);
  const value = Number(lengthEl.value || min);
  const ratio = max === min ? 100 : ((value - min) / (max - min)) * 100;
  lengthEl.style.setProperty("--track-fill", `${ratio}%`);
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
}

function updateTopicDefaults() {
  const preset = TOPIC_KEYWORDS[topicEl.value];
  if (preset) keywordsEl.value = preset.join(", ");
  renderKeywordChips();
}

function renderKeywordChips() {
  const keywords = parseKeywords(keywordsEl.value);
  keywordChipsEl.innerHTML = keywords.map((word) => `<span class="chip">${escapeHtml(word)}</span>`).join("");
  keywordCountEl.textContent = `${keywords.length} kelime`;
}

function renderMeta(level, topic, text) {
  metaTagsEl.innerHTML = `
    <span class="tag">Level ${escapeHtml(level)}</span>
    <span class="tag">${escapeHtml(topic)}</span>
    <span class="tag">${text.split(/\s+/).filter(Boolean).length} words</span>
  `;
}

function renderSelection() {
  const item = state.glossary[state.selectedWord] || {};
  selectedWordEl.textContent = state.selectedWord || "Word";
  selectedMeaningEl.textContent = item.turkish || "Bir kelime seç.";
  selectedContextEl.innerHTML = state.loadingWord
    ? "Seçilen kelime için açıklama hazırlanıyor..."
    : highlightSelectedWord(item.context || "Bağlam açıklaması burada görünecek.", state.selectedWord);
  selectedExampleEl.innerHTML = state.loadingWord
    ? "Örnek cümle hazırlanıyor..."
    : highlightSelectedWord(item.example || "Örnek cümle burada görünecek.", state.selectedWord);
  flipCardEl.classList.remove("flipped");
  flipCardEl.classList.toggle("clickable", !state.loadingWord && Boolean(state.selectedWord));
}

function renderSavedWords() {
  if (!state.user || !state.recentWords.length) {
    savedWordsEmptyEl.classList.remove("hidden");
    savedWordsListEl.classList.add("hidden");
    savedWordsListEl.innerHTML = "";
    return;
  }
  savedWordsEmptyEl.classList.add("hidden");
  savedWordsListEl.classList.remove("hidden");
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
  if (!state.user) {
    quizEmptyEl.textContent = "Quiz için önce giriş yapmalısın.";
    quizEmptyEl.classList.remove("hidden");
    quizCardEl.classList.add("hidden");
    return;
  }
  if (!state.quiz) {
    quizEmptyEl.textContent = "Quiz için en az 4 kaydedilmiş kelime gerekiyor.";
    quizEmptyEl.classList.remove("hidden");
    quizCardEl.classList.add("hidden");
    return;
  }
  quizEmptyEl.classList.add("hidden");
  quizCardEl.classList.remove("hidden");
  quizPromptEl.textContent = state.quiz.question;
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
        quizFeedbackEl.textContent = parsed.data.detail || "Quiz cevabı kaydedilemedi.";
        quizFeedbackEl.classList.remove("hidden");
        return;
      }
      quizFeedbackEl.textContent = parsed.data.correct
        ? `Doğru. "${parsed.data.word}" = "${parsed.data.answer}".`
        : `Olmadı. Doğru cevap: ${parsed.data.answer}`;
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
    if (!parsed.ok) throw new Error(parsed.data.detail || "Kelime detayı alınamadı.");
    state.glossary[word] = parsed.data;
    if (state.user) {
      await refreshSession();
      await loadQuiz();
    }
  } catch (error) {
    state.glossary[word] = {
      turkish: "Türkçe anlam alınamadı.",
      context: error.message || "Kelime detayı şu anda yüklenemedi.",
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
        selectedMeaningEl.textContent = "Hazırlanıyor...";
        selectedContextEl.textContent = "Seçilen kelime için açıklama hazırlanıyor...";
        selectedExampleEl.textContent = "Örnek cümle hazırlanıyor...";
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
  renderReadingText();
  state.selectedWord = "";
  state.loadingWord = false;
  state.pendingFlip = false;
  renderSelection();
  selectedContextEl.textContent = "Metin hazır. Detayını görmek için bir kelimeye tıkla.";
  selectedExampleEl.textContent = "Kelime seçildiğinde örnek cümle burada görünecek.";
}

async function generateExperience(payload, triggerButton) {
  clearError();
  setLoading(triggerButton, "Hazırlanıyor...", true);
  try {
    const parsed = await apiFetch("/api/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Bir hata oluştu.");
    state.text = parsed.data.text;
    state.glossary = {};
    state.lastPayload = payload;
    manualResultEl.classList.add("hidden");
    renderExperience();
  } catch (error) {
    showError(error.message);
  } finally {
    setLoading(triggerButton, "", false);
  }
}

generateForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const keywords = parseKeywords(keywordsEl.value);
  if (keywords.length < 2 || keywords.length > 12) {
    showError("2 ile 12 arasında anahtar kelime girmelisin.");
    return;
  }
  const payload = {
    level: levelEl.value,
    topic: topicEl.value,
    length_target: Number(lengthEl.value),
    keywords,
  };
  await generateExperience(payload, $("#generateBtn"));
});

manualForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!state.text) {
    manualResultEl.textContent = "Önce bir metin üretmelisin.";
    manualResultEl.classList.remove("hidden");
    return;
  }
  const word = manualWordEl.value.trim();
  if (!word) return;
  setLoading($("#manualBtn"), "Açıklanıyor...", true);
  try {
    const parsed = await apiFetch("/api/explain", {
      method: "POST",
      body: JSON.stringify({ text: state.text, word }),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Bir hata oluştu.");
    manualResultEl.textContent = parsed.data.explanation;
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
  setLoading(authSubmitBtn, state.authMode === "login" ? "Giriş yapılıyor..." : "Hesap açılıyor...", true);
  try {
    const parsed = await apiFetch(endpoint, {
      method: "POST",
      body: JSON.stringify({
        username: authUsernameEl.value.trim(),
        password: authPasswordEl.value.trim(),
      }),
    });
    if (!parsed.ok) throw new Error(parsed.data.detail || "Kimlik işlemi başarısız.");
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

regenBtn.addEventListener("click", async () => {
  if (!state.lastPayload) return;
  await generateExperience(state.lastPayload, regenBtn);
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

updateLevelUi();
updateTopicDefaults();
updateRangeVisual();
renderAuthMode();
renderUserPanel();
setLibraryView(null);
previewStateEl.textContent = "Hazır. Metin önce hızlıca üretilir, kelime detayları ise yalnızca tıklandığında yüklenir.";
refreshSession().then(loadQuiz);
