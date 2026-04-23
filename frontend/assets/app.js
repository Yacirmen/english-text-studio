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
const LANGUAGE_STORAGE_KEY = "readlex_ui_language";
const INSTALL_DISMISSED_KEY = "readlex_install_tip_dismissed";

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
    login_streak: 0,
    fire_level: 0,
    fire_label: "Cold start",
    fire_icon: "•",
    fire_next: 1,
    hard_words: 0,
  },
  recentWords: [],
  readingHistory: [],
  progressHistory: [],
  social: { friends: [], incoming: [], outgoing: [], suggestions: [], cheers_received: 0 },
  socialSearch: { query: "", results: [], loading: false },
  deferredInstallPrompt: null,
  quiz: null,
  quizMode: "saved",
  libraryView: null,
  libraryStats: null,
  quizStats: { answered: 0, correct: 0, streak: 0 },
  loggingOut: false,
  hasEnteredApp: window.sessionStorage.getItem(GUEST_FLAG_KEY) === "1",
  viewMode: window.innerWidth < 860 ? "mobile" : "web",
  uiLanguage: window.localStorage.getItem(LANGUAGE_STORAGE_KEY) === "tr" ? "tr" : "en",
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
    login_streak: 0,
    fire_level: 0,
    fire_label: "Cold start",
    fire_icon: "•",
    fire_next: 1,
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
const gateThemeToggleBtn = $("#gateThemeToggleBtn");
const languageToggleBtn = $("#languageToggleBtn");
const gateLanguageToggleBtn = $("#gateLanguageToggleBtn");
const profileTipTextEl = $("#profileTipText");
const installCoachEl = $("#installCoach");
const installCoachLabelEl = $("#installCoachLabel");
const installCoachTitleEl = $("#installCoachTitle");
const installCoachTextEl = $("#installCoachText");
const installCoachActionEl = $("#installCoachAction");
const installCoachDismissEl = $("#installCoachDismiss");
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
const insightCoachEl = $("#insightCoach");
const insightCoachTitleEl = $("#insightCoachTitle");
const insightCoachBodyEl = $("#insightCoachBody");
const insightCoachStateEl = $("#insightCoachState");
const selectedCollocationsEl = $("#selectedCollocations");
const manualResultEl = $("#manualResult");
const manualWordEl = $("#manualWord");
const regenBtn = $("#regenBtn");
const clearBtn = $("#clearBtn");
const setupLevelBadgeEl = $("#setupLevelBadge");
const setupLengthBadgeEl = $("#setupLengthBadge");
const setupSummaryEl = $("#setupSummary");
const topbarLevelChipEl = $("#topbarLevelChip");
const topbarTopicChipEl = $("#topbarTopicChip");
const topbarLibraryChipEl = $("#topbarLibraryChip");
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
const socialSearchResultsEl = $("#socialSearchResults");
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
const navMenuMarkTriggerEl = $("#navMenuMarkTrigger");
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

const UI_COPY = {
  en: {
    themeLabel: "Toggle dark mode",
    languageLabel: "Switch language",
    welcomeRead: "Read.",
    welcomeSave: "Save.",
    welcomeRemember: "Remember.",
    welcomeNote: "Stop forgetting what you learn.",
    welcomeSubnote: "Read it once. Keep it forever.",
    saveOneTap: "Save in one tap",
    saveOneTapBody: "Catch useful words without leaving the reading flow.",
    reviewContext: "Review with context",
    reviewContextBody: "Keep phrases, meanings, and examples tied together.",
    lessClutter: "Less clutter. Better recall.",
    lessClutterBody: "A calmer reading space built for retention, not noise.",
    login: "Log In",
    signup: "Sign Up",
    continueGuest: "Continue as Guest",
    welcomeBack: "Welcome back",
    welcomeBackBody: "Pick up where your saved words left off.",
    newAccount: "New account",
    newAccountBody: "Create your reading space and keep every win.",
    memberLogin: "Member login",
    memberLoginBody: "Open your saved words, streak, and recent reads.",
    startFresh: "Start fresh",
    startFreshBody: "Build a personal library and turn quick reads into review wins.",
    username: "Username",
    password: "Password",
    usernamePlaceholder: "your_username",
    passwordPlaceholder: "at least 6 characters",
    sessionDock: "Session Dock",
    studyHub: "Study Hub",
    workspace: "Workspace",
    workspaceBody: "Everything important, one tap away.",
    account: "Account",
    study: "Study",
    company: "Company",
    controlRoom: "Control room",
    progress: "Progress",
    progressBody: "Daily streak, reading log, and visible practice momentum.",
    stats: "Stats",
    socialCircle: "Social Circle",
    socialBody: "Add friends and keep accountability light, not noisy.",
    friends: "Friends",
    studyTools: "Study tools",
    savedWords: "Saved words",
    savedWordsBody: "Your saved words and phrases, ready for review.",
    words: "Words",
    quiz: "Quiz",
    quizBody: "English to Turkish checks from your saved deck.",
    review: "Review",
    translate: "Translate",
    translateBody: "Get a quick meaning when you need a second look.",
    help: "Help",
    office: "Office",
    setup: "Setup",
    setupTitle: "Read first. Review smarter.",
    setupBody: "Choose a mode, open a level-matched text, and turn useful taps into review material.",
    readingSetup: "Start a session",
    setupDescription: "Pick a source, then filter the reading without cluttering the page.",
    libraryOnly: "Library Only",
    aiOnly: "AI Only",
    level: "Level",
    topic: "Topic",
    targetWords: "Target word count",
    keywords: "Keywords",
    keywordHelp: "Add 2-12 keywords. Repeated words are removed automatically.",
    keywordPresetHelp: "Topic presets fill in starter keywords, but you can keep your own list.",
    getReading: "Get Reading",
    generateText: "Generate Text",
    anotherReading: "Another Reading",
    generateAgain: "Generate Again",
    clearReading: "Clear Reading",
    libraryHint: "One click opens a ready text. Your taps build saved words, quiz material, and progress history.",
    flowRead: "Read",
    flowReadBody: "Open a level-matched text.",
    flowTap: "Tap",
    flowTapBody: "Explore words and phrases in context.",
    flowReview: "Review",
    flowReviewBody: "Return through saved words and quiz.",
    previewLibrary: "Ready. Choose a level and topic, then open a curated reading that becomes your review deck.",
    previewAi: "Ready. Set level, topic, and keywords, then generate a custom text for focused practice.",
    selectedWord: "Selected Word",
    word: "Word",
    flipToMeaning: "Tap anywhere on the card to flip to the Turkish meaning.",
    turkishMeaning: "Turkish Meaning",
    flipBack: "Tap anywhere on the card to flip back.",
    contextTurkish: "Context in Turkish",
    simpleExample: "Simple Example",
    contextEmpty: "Choose a word and its Turkish context will appear here.",
    exampleEmpty: "A short learner-friendly example will appear here.",
    usageCoach: "Usage Coach",
    usageCoachReady: "Ready",
    usageCoachLoading: "Building",
    usageCoachActive: "Active",
    usageCoachEmptyTitle: "Pick a word to start.",
    usageCoachEmptyBody: "Tap a highlighted word. ReadLex will turn it into meaning, context, and a usable example.",
    usageCoachLoadingBody: "Reading the sentence, finding the sense, and preparing a clean example.",
    usageCoachActiveBody: "Use the meaning card first, then read the context and example together.",
    chooseWord: "Choose a word",
    preparingContext: "Preparing Turkish context...",
    preparingExample: "Preparing example sentence...",
    loadingLibrary: "Loading library count...",
    curatedInside: "{count} curated readings inside",
    libraryUnavailable: "Library count unavailable",
    texts: "{count} texts",
    curated: "Curated",
    ai: "AI",
    aroundWords: "Around {count} words",
    keywordCount: "{count} words",
    levelHintA1: "Very simple and everyday",
    levelHintA2: "Simple, clear, and familiar",
    levelHintB1: "Natural and comfortably paced",
    levelHintB2: "Richer but still easy to read",
    levelHintC1: "Advanced, natural, and detailed",
    levelHintC2: "Highly advanced and nuanced",
    signInQuiz: "Sign in first to unlock the quiz.",
    quizEmptyReading: "Open a reading and tap into the glossary first to start a reading quiz.",
    quizEmptyHard: "You need at least 4 saved words before hard-word review can begin.",
    quizEmptySaved: "You need at least 4 saved words to start the quiz.",
    englishToTurkish: "English to Turkish",
    nextQuestion: "Next Question",
    nextIncoming: "Next incoming...",
    correct: "Correct. \"{word}\" = \"{answer}\".",
    wrong: "Not this time. Correct answer: {answer}",
    savedMeta: "{count} words on deck",
    removeWord: "Remove {word}",
    savedEmpty: "Sign in, open a reading, and tap useful words. Your review deck will build itself here.",
    randomize: "Randomize",
    clearHistory: "Clear history",
    profileCopy: "Account access lives here. Sign in, create an account, or log out without leaving the reading flow.",
    accountSave: "Sign in to save words and unlock personal review.",
    activeAccount: "Active account",
    savedWordsLabel: "Saved words",
    mastered: "Mastered",
    dailyGoal: "Daily goal",
    streak: "Streak {count}",
    wordsToday: "{saved} / {goal} words today",
    hardWords: "{count} hard words ready for review.",
    readingLog: "Reading log",
    progressDeskTitle: "Your practice is becoming visible.",
    progressDeskBody: "Each reading you open and every word you save becomes part of this progress desk.",
    totalTexts: "Total texts",
    today: "Today",
    wordsTodayShort: "Words today",
    dailyHistory: "Daily history",
    dailyHistoryBody: "Text and word counts grouped by day, so progress feels concrete.",
    profileTipActive: "Keep the loop simple: read, save useful phrases, then return through quiz.",
    profileTipEmpty: "Open your first reading and this desk will start tracking your rhythm.",
    dailyTotalsEmpty: "Daily totals will appear after your first signed-in reading.",
    recentReadingsEmpty: "Your recent readings will appear here.",
    signInTrail: "Sign in to keep your reading trail.",
    signInProgress: "Sign in to track daily text and word history.",
    readingPrompt: "Choose any word to activate the meaning panel.",
    mobileTapTranslation: "Tap Translation",
    recentReadings: "Recent readings",
    recentReadingsBody: "Your latest library picks stay here for quick return.",
    socialPanelBody: "Build a small learning circle. Add friends by username, compare streak rhythm, and send a quick cheer when they keep going.",
    learningCircle: "Learning circle",
    socialHeroTitle: "Accountability without a noisy feed.",
    socialHeroBody: "Friends only see lightweight practice stats: streak, total texts, saved words, and today's word count.",
    findUsername: "Find by username",
    friendPlaceholder: "friend_username",
    socialFieldNote: "Type at least 3 characters. Exact usernames can be added instantly.",
    sendRequest: "Send request",
    socialGuest: "Sign in to add friends and unlock your social circle.",
    suggestions: "Suggestions",
    suggestionsBody: "Recent learners you can invite into your circle.",
    manualBody: "Ask for a quick explanation when a word needs a second look.",
    typeWord: "Type a word",
    explainWord: "Explain Word",
    infoBody: "A cleaner company-facing space for understanding the product, its current release posture, and where users can reach the team.",
    infoHeroLabel: "ReadLex Office",
    infoHeroTitle: "A calmer reading product with a clearer professional face.",
    infoHeroBody: "This panel explains what ReadLex does, how the current build should be understood, and where business or support communication should go during launch.",
  },
  tr: {
    themeLabel: "Koyu modu değiştir",
    languageLabel: "Dili değiştir",
    welcomeRead: "Oku.",
    welcomeSave: "Kaydet.",
    welcomeRemember: "Hatırla.",
    welcomeNote: "Öğrendiğini unutma.",
    welcomeSubnote: "Bir kez oku. Kalıcı hale getir.",
    saveOneTap: "Tek dokunuşla kaydet",
    saveOneTapBody: "Okuma akışından çıkmadan işe yarayan kelimeleri yakala.",
    reviewContext: "Bağlamla tekrar et",
    reviewContextBody: "Kelimeleri, anlamları ve örnekleri birlikte tut.",
    lessClutter: "Daha az kalabalık. Daha iyi hatırlama.",
    lessClutterBody: "Akılda kalıcılık için sadeleştirilmiş sakin bir okuma alanı.",
    login: "Giriş Yap",
    signup: "Kayıt Ol",
    continueGuest: "Misafir Olarak Devam Et",
    welcomeBack: "Tekrar hoş geldin",
    welcomeBackBody: "Kaldığın yerden kelimelerine dön.",
    newAccount: "Yeni hesap",
    newAccountBody: "Kendi okuma alanını oluştur ve her kazanımı sakla.",
    memberLogin: "Üye girişi",
    memberLoginBody: "Kayıtlı kelimelerini, serini ve son okumalarını aç.",
    startFresh: "Yeni başlangıç",
    startFreshBody: "Kişisel kitaplığını kur ve kısa okumaları tekrara dönüştür.",
    username: "Kullanıcı adı",
    password: "Şifre",
    usernamePlaceholder: "kullanici_adi",
    passwordPlaceholder: "en az 6 karakter",
    sessionDock: "Oturum Paneli",
    studyHub: "Çalışma Merkezi",
    workspace: "Çalışma alanı",
    workspaceBody: "Önemli her şey tek dokunuş uzakta.",
    account: "Hesap",
    study: "Çalışma",
    company: "Kurumsal",
    controlRoom: "Kontrol alanı",
    progress: "İlerleme",
    progressBody: "Günlük seri, okuma kaydı ve görünür çalışma ritmi.",
    stats: "İstatistik",
    socialCircle: "Sosyal Çevre",
    socialBody: "Arkadaş ekle, motivasyonu hafif ve düzenli tut.",
    friends: "Arkadaşlar",
    studyTools: "Çalışma araçları",
    savedWords: "Kayıtlı kelimeler",
    savedWordsBody: "Kaydettiğin kelimeler ve kalıplar tekrar için hazır.",
    words: "Kelimeler",
    quiz: "Quiz",
    quizBody: "Kayıtlı destenden İngilizce-Türkçe hızlı kontrol.",
    review: "Tekrar",
    translate: "Çeviri",
    translateBody: "İkinci bir bakış gerektiğinde hızlı anlam al.",
    help: "Yardım",
    office: "Ofis",
    setup: "Hazırlık",
    setupTitle: "Önce oku. Daha akıllı tekrar et.",
    setupBody: "Mod seç, seviyene uygun metin aç ve dokunuşlarını tekrar malzemesine dönüştür.",
    readingSetup: "Oturum başlat",
    setupDescription: "Kaynak seç, sonra sayfayı kalabalıklaştırmadan okumayı filtrele.",
    libraryOnly: "Kitaplık",
    aiOnly: "Yapay Zeka",
    level: "Seviye",
    topic: "Konu",
    targetWords: "Hedef kelime sayısı",
    keywords: "Anahtar kelimeler",
    keywordHelp: "2-12 anahtar kelime ekle. Tekrar edenler otomatik kaldırılır.",
    keywordPresetHelp: "Konu seçimi başlangıç kelimeleri doldurur; kendi listeni de koruyabilirsin.",
    getReading: "Okuma Aç",
    generateText: "Metin Üret",
    anotherReading: "Başka Okuma",
    generateAgain: "Tekrar Üret",
    clearReading: "Okumayı Temizle",
    libraryHint: "Tek tıkla hazır metin açılır. Dokunuşların kayıtlı kelime, quiz ve ilerleme geçmişi oluşturur.",
    flowRead: "Oku",
    flowReadBody: "Seviyene uygun metin aç.",
    flowTap: "Dokun",
    flowTapBody: "Kelimeleri ve kalıpları bağlam içinde keşfet.",
    flowReview: "Tekrar",
    flowReviewBody: "Kayıtlı kelimeler ve quiz ile geri dön.",
    previewLibrary: "Hazır. Seviye ve konu seç, sonra tekrar destene dönüşecek hazır bir okuma aç.",
    previewAi: "Hazır. Seviye, konu ve anahtar kelime seç; odaklı pratik için özel metin üret.",
    selectedWord: "Seçilen Kelime",
    word: "Kelime",
    flipToMeaning: "Türkçe anlamı görmek için karta dokun.",
    turkishMeaning: "Türkçe Anlam",
    flipBack: "Geri dönmek için karta dokun.",
    contextTurkish: "Türkçe Bağlam",
    simpleExample: "Basit Örnek",
    contextEmpty: "Bir kelime seç; Türkçe bağlam burada görünsün.",
    exampleEmpty: "Kısa, öğrenici dostu örnek burada görünsün.",
    usageCoach: "Kullanım Koçu",
    usageCoachReady: "Hazır",
    usageCoachLoading: "Hazırlanıyor",
    usageCoachActive: "Aktif",
    usageCoachEmptyTitle: "Başlamak için bir kelime seç.",
    usageCoachEmptyBody: "Vurgulu bir kelimeye dokun. ReadLex onu anlam, bağlam ve kullanılabilir örneğe çevirir.",
    usageCoachLoadingBody: "Cümle okunuyor, doğru anlam bulunuyor ve temiz bir örnek hazırlanıyor.",
    usageCoachActiveBody: "Önce anlam kartını kullan, sonra bağlam ve örneği birlikte oku.",
    chooseWord: "Bir kelime seç",
    preparingContext: "Türkçe bağlam hazırlanıyor...",
    preparingExample: "Örnek cümle hazırlanıyor...",
    loadingLibrary: "Kitaplık sayısı yükleniyor...",
    curatedInside: "{count} hazır okuma içeride",
    libraryUnavailable: "Kitaplık sayısı alınamadı",
    texts: "{count} metin",
    curated: "Hazır",
    ai: "YZ",
    aroundWords: "Yaklaşık {count} kelime",
    keywordCount: "{count} kelime",
    levelHintA1: "Çok basit ve günlük",
    levelHintA2: "Basit, net ve tanıdık",
    levelHintB1: "Doğal ve rahat tempolu",
    levelHintB2: "Daha zengin ama hâlâ okunabilir",
    levelHintC1: "İleri, doğal ve detaylı",
    levelHintC2: "Çok ileri ve nüanslı",
    signInQuiz: "Quizi açmak için önce giriş yap.",
    quizEmptyReading: "Okuma açıp sözlüğe dokun; sonra okuma quizi başlayabilir.",
    quizEmptyHard: "Zor kelime tekrarı için en az 4 kayıtlı kelime gerekir.",
    quizEmptySaved: "Quizi başlatmak için en az 4 kayıtlı kelime gerekir.",
    englishToTurkish: "İngilizce - Türkçe",
    nextQuestion: "Sonraki Soru",
    nextIncoming: "Sonraki geliyor...",
    correct: "Doğru. \"{word}\" = \"{answer}\".",
    wrong: "Bu değil. Doğru cevap: {answer}",
    savedMeta: "Destede {count} kelime",
    removeWord: "{word} kelimesini kaldır",
    savedEmpty: "Giriş yap, okuma aç ve işe yarayan kelimelere dokun. Tekrar desten burada oluşacak.",
    randomize: "Karıştır",
    clearHistory: "Geçmişi temizle",
    profileCopy: "Hesap erişimi burada. Okuma akışından çıkmadan giriş yap, hesap oluştur veya çıkış yap.",
    accountSave: "Kelimeleri kaydetmek ve kişisel tekrarı açmak için giriş yap.",
    activeAccount: "Aktif hesap",
    savedWordsLabel: "Kayıtlı kelimeler",
    mastered: "Öğrenildi",
    dailyGoal: "Günlük hedef",
    streak: "Seri {count}",
    wordsToday: "Bugün {saved} / {goal} kelime",
    hardWords: "{count} zor kelime tekrar için hazır.",
    readingLog: "Okuma kaydı",
    progressDeskTitle: "Pratiğin görünür hale geliyor.",
    progressDeskBody: "Açtığın her okuma ve kaydettiğin her kelime bu ilerleme masasına eklenir.",
    totalTexts: "Toplam metin",
    today: "Bugün",
    wordsTodayShort: "Bugünkü kelime",
    dailyHistory: "Günlük geçmiş",
    dailyHistoryBody: "Metin ve kelime sayıları güne göre gruplanır; ilerleme somutlaşır.",
    profileTipActive: "Döngüyü sade tut: oku, işe yarayan kalıpları kaydet, sonra quizle geri dön.",
    profileTipEmpty: "İlk okumayı aç; bu panel ritmini takip etmeye başlayacak.",
    dailyTotalsEmpty: "Günlük toplamlar ilk giriş yapılmış okumadan sonra görünür.",
    recentReadingsEmpty: "Son okumaların burada görünecek.",
    signInTrail: "Okuma izini saklamak için giriş yap.",
    signInProgress: "Günlük metin ve kelime geçmişi için giriş yap.",
    readingPrompt: "Anlam panelini açmak için herhangi bir kelime seç.",
    mobileTapTranslation: "Dokunma Çevirisi",
    recentReadings: "Son okumalar",
    recentReadingsBody: "Son kitaplık seçimlerin hızlı dönüş için burada kalır.",
    socialPanelBody: "Küçük bir öğrenme çevresi kur. Kullanıcı adıyla arkadaş ekle, seri ritmini karşılaştır ve devam edenlere küçük destek gönder.",
    learningCircle: "Öğrenme çevresi",
    socialHeroTitle: "Gürültülü akış olmadan sorumluluk hissi.",
    socialHeroBody: "Arkadaşlar yalnızca hafif pratik verilerini görür: seri, toplam metin, kayıtlı kelime ve bugünkü kelime sayısı.",
    findUsername: "Kullanıcı adıyla bul",
    friendPlaceholder: "arkadas_kullanici_adi",
    socialFieldNote: "En az 3 karakter yaz. Tam kullanıcı adları anında eklenebilir.",
    sendRequest: "İstek gönder",
    socialGuest: "Arkadaş eklemek ve sosyal çevreni açmak için giriş yap.",
    suggestions: "Öneriler",
    suggestionsBody: "Çevrene davet edebileceğin son öğrenenler.",
    manualBody: "Bir kelimeye ikinci bakış gerektiğinde hızlı açıklama al.",
    typeWord: "Kelime yaz",
    explainWord: "Kelimeyi Açıkla",
    infoBody: "Ürünü, mevcut yayın durumunu ve ekibe nereden ulaşılacağını anlatan daha temiz kurumsal alan.",
    infoHeroLabel: "ReadLex Ofis",
    infoHeroTitle: "Daha sakin ve daha profesyonel yüzü olan bir okuma ürünü.",
    infoHeroBody: "Bu panel ReadLex'in ne yaptığını, mevcut sürümün nasıl anlaşılması gerektiğini ve lansman sürecinde destek veya iş iletişiminin nereye gideceğini açıklar.",
  },
};

const uiText = (key, values = {}) => {
  const copy = UI_COPY[state.uiLanguage] || UI_COPY.en;
  let text = copy[key] || UI_COPY.en[key] || key;
  Object.entries(values).forEach(([name, value]) => {
    text = text.replaceAll(`{${name}}`, String(value));
  });
  return text;
};

function setText(selector, key, values) {
  const el = typeof selector === "string" ? $(selector) : selector;
  if (el) {
    el.textContent = uiText(key, values);
    if (el.tagName === "BUTTON") el.dataset.original = el.textContent;
  }
}

function setAllText(selector, key, values) {
  document.querySelectorAll(selector).forEach((el) => {
    el.textContent = uiText(key, values);
    if (el.tagName === "BUTTON") el.dataset.original = el.textContent;
  });
}

function setPlaceholder(selector, key) {
  const el = typeof selector === "string" ? $(selector) : selector;
  if (el) el.setAttribute("placeholder", uiText(key));
}

function setControlLabel(button, key) {
  if (!button) return;
  const label = uiText(key);
  button.setAttribute("aria-label", label);
  button.setAttribute("title", label);
}

function applyTheme(mode) {
  const isDark = mode === "dark";
  document.body.classList.toggle("dark-mode", isDark);
  themeToggleBtn?.setAttribute("aria-pressed", String(isDark));
  gateThemeToggleBtn?.setAttribute("aria-pressed", String(isDark));
  window.localStorage.setItem(THEME_STORAGE_KEY, isDark ? "dark" : "light");
}

function toggleTheme() {
  const nextMode = document.body.classList.contains("dark-mode") ? "light" : "dark";
  applyTheme(nextMode);
}

function applyLanguage(language) {
  state.uiLanguage = language === "tr" ? "tr" : "en";
  const isTurkish = state.uiLanguage === "tr";
  document.documentElement.lang = isTurkish ? "tr" : "en";
  document.body.dataset.language = state.uiLanguage;
  window.localStorage.setItem(LANGUAGE_STORAGE_KEY, state.uiLanguage);

  languageToggleBtn?.setAttribute("aria-pressed", String(isTurkish));
  gateLanguageToggleBtn?.setAttribute("aria-pressed", String(isTurkish));
  setControlLabel(languageToggleBtn, "languageLabel");
  setControlLabel(gateLanguageToggleBtn, "languageLabel");
  setControlLabel(themeToggleBtn, "themeLabel");
  setControlLabel(gateThemeToggleBtn, "themeLabel");

  setText(".welcome-headline-line-read", "welcomeRead");
  setText(".welcome-headline-line-save", "welcomeSave");
  setText(".welcome-headline-line-remember", "welcomeRemember");
  setText(".welcome-side-note span", "welcomeNote");
  setText(".welcome-side-note p", "welcomeSubnote");
  setText(".welcome-feature-card:nth-of-type(1) strong", "saveOneTap");
  setText(".welcome-feature-card:nth-of-type(1) p", "saveOneTapBody");
  setText(".welcome-feature-card:nth-of-type(2) strong", "reviewContext");
  setText(".welcome-feature-card:nth-of-type(2) p", "reviewContextBody");
  setText(".welcome-feature-card-wide strong", "lessClutter");
  setText(".welcome-feature-card-wide p", "lessClutterBody");

  [gateShowLoginBtn, showLoginBtn].forEach((button) => setText(button, "login"));
  [gateShowRegisterBtn, showRegisterBtn].forEach((button) => setText(button, "signup"));
  setText(continueGuestBtn, "continueGuest");
  setText(".auth-face-login .auth-face-kicker", "welcomeBack");
  setText(".auth-face-login .auth-face-title", "welcomeBackBody");
  setText(".auth-face-register .auth-face-kicker", "newAccount");
  setText(".auth-face-register .auth-face-title", "newAccountBody");
  setText("#authCard .auth-face-login .auth-face-kicker", "memberLogin");
  setText("#authCard .auth-face-login .auth-face-title", "memberLoginBody");
  setText("#authCard .auth-face-register .auth-face-kicker", "startFresh");
  setText("#authCard .auth-face-register .auth-face-title", "startFreshBody");
  [
    "#gateLoginForm .field:nth-of-type(1) span",
    "#gateRegisterForm .field:nth-of-type(1) span",
    "#authLoginForm .field:nth-of-type(1) span",
    "#authRegisterForm .field:nth-of-type(1) span",
  ].forEach((selector) => setText(selector, "username"));
  [
    "#gateLoginForm .field:nth-of-type(2) span",
    "#gateRegisterForm .field:nth-of-type(2) span",
    "#authLoginForm .field:nth-of-type(2) span",
    "#authRegisterForm .field:nth-of-type(2) span",
  ].forEach((selector) => setText(selector, "password"));
  [gateLoginUsernameEl, gateRegisterUsernameEl, authLoginUsernameEl, authRegisterUsernameEl].forEach((el) => setPlaceholder(el, "usernamePlaceholder"));
  [gateLoginPasswordEl, gateRegisterPasswordEl, authLoginPasswordEl, authRegisterPasswordEl].forEach((el) => setPlaceholder(el, "passwordPlaceholder"));
  [gateLoginSubmitBtn, authLoginSubmitBtn].forEach((button) => setText(button, "login"));
  [gateRegisterSubmitBtn, authRegisterSubmitBtn].forEach((button) => setText(button, "signup"));

  setText(".topbar-slogan-main", "sessionDock");
  setText(".menu-trigger-title", "studyHub");
  setText(".nav-menu-overview-kicker", "workspace");
  setText(".nav-menu-overview-title", "workspaceBody");
  setAllText('[data-menu-category="account"]', "account");
  setAllText('[data-menu-category="study"]', "study");
  setAllText('[data-menu-category="company"]', "company");
  setText('[data-menu-panel="account"] .nav-menu-label', "controlRoom");
  setText("#openProgressBtn strong", "progress");
  setText("#openProgressBtn small", "progressBody");
  setText("#openProgressBtn .nav-menu-badge", "stats");
  setText("#openSocialBtn strong", "socialCircle");
  setText("#openSocialBtn small", "socialBody");
  setText("#openSocialBtn .nav-menu-badge", "friends");
  setText('[data-menu-panel="study"] .nav-menu-label', "studyTools");
  setText("#openSavedWordsBtn strong", "savedWords");
  setText("#openSavedWordsBtn small", "savedWordsBody");
  setText("#openSavedWordsBtn .nav-menu-badge", "words");
  setText("#openQuizBtn strong", "quiz");
  setText("#openQuizBtn small", "quizBody");
  setText("#openQuizBtn .nav-menu-badge", "review");
  setText("#openManualHelpBtn strong", "translate");
  setText("#openManualHelpBtn small", "translateBody");
  setText("#openManualHelpBtn .nav-menu-badge", "help");
  setText("#openInfoBtn .nav-menu-badge", "office");

  setText(".rail-kicker", "setup");
  setText(".rail-intro h2", "setupTitle");
  setText(".rail-intro p", "setupBody");
  setText(".rail-panel .section-head h3", "readingSetup");
  setText(".rail-panel .section-head p", "setupDescription");
  setText('[data-source="library"]', "libraryOnly");
  setText('[data-source="ai"]', "aiOnly");
  setAllText(".compact-filters .field:first-child > span, #aiControls .form-row .field:first-child > span", "level");
  setAllText(".compact-filters .field:nth-child(2) > span, #topicLabel", "topic");
  setText("#lengthField > span", "targetWords");
  setText("#keywordsField .field-head > span:first-child", "keywords");
  setText("#keywordsField .field-note", "keywordHelp");
  setText("#keywordsHelper", "keywordPresetHelp");
  setPlaceholder(keywordsEl, "keywords");
  setText("#generateBtn", state.contentSource === "library" ? "getReading" : "generateText");
  setText(regenBtn, state.contentSource === "library" ? "anotherReading" : "generateAgain");
  setText(clearBtn, "clearReading");
  setText(libraryModeHintEl, "libraryHint");
  setText(".session-flow div:nth-child(1) strong", "flowRead");
  setText(".session-flow div:nth-child(1) small", "flowReadBody");
  setText(".session-flow div:nth-child(2) strong", "flowTap");
  setText(".session-flow div:nth-child(2) small", "flowTapBody");
  setText(".session-flow div:nth-child(3) strong", "flowReview");
  setText(".session-flow div:nth-child(3) small", "flowReviewBody");
  setText(".reading-header .muted-copy", "readingPrompt");

  setAllText(".flip-front .mini-label", "selectedWord");
  setText(selectedWordEl, state.selectedWord || uiText("word"));
  setText(".flip-front p", "flipToMeaning");
  setAllText(".flip-back .mini-label, .mobile-word-card .mini-label", "turkishMeaning");
  setText(".flip-back p", "flipBack");
  setAllText(".insight-context-block .mini-label, .mobile-insight-card .insight-block:nth-child(1) .mini-label", "contextTurkish");
  setAllText(".insight-example-block .mini-label, .mobile-insight-card .insight-block:nth-child(2) .mini-label", "simpleExample");
  setText(".insight-lab-kicker", "usageCoach");
  setText(".mobile-word-head .mini-label", "mobileTapTranslation");

  setText("#profilePanel > .library-copy", "profileCopy");
  setText("#authGuest .section-head p", "accountSave");
  setText(".account-card .mini-label", "activeAccount");
  setAllText(".account-stats div:nth-child(1) span", "savedWordsLabel");
  setAllText(".account-stats div:nth-child(2) span", "mastered");
  setText("#progressPanel > .library-copy", "progressBody");
  setText(".progress-command-card .mini-label", "readingLog");
  setText(".progress-command-card h3", "progressDeskTitle");
  setText(".progress-command-card p", "progressDeskBody");
  setText(".progress-command-stats article:nth-child(1) span", "totalTexts");
  setText(".progress-command-stats article:nth-child(2) span", "today");
  setText(".progress-command-stats article:nth-child(3) span", "wordsTodayShort");
  setText(".progress-goal-panel .mini-label", "dailyGoal");
  setText(".progress-daily-panel .section-head h3", "dailyHistory");
  setText(".progress-daily-panel .section-head p", "dailyHistoryBody");
  setText("#progressPanel .profile-panel:last-child .section-head h3", "recentReadings");
  setText("#progressPanel .profile-panel:last-child .section-head p", "recentReadingsBody");
  setText("#savedWordsPanel > .library-copy", "savedWordsBody");
  setText(randomizeSavedWordsBtn, "randomize");
  setText(clearSavedWordsBtn, "clearHistory");
  setText(savedWordsEmptyEl, "savedEmpty");
  setText("#socialPanel > .library-copy", "socialPanelBody");
  setText(".social-hero-card .mini-label", "learningCircle");
  setText(".social-hero-card h3", "socialHeroTitle");
  setText(".social-hero-card p", "socialHeroBody");
  setText(".social-hero-meter small", "friends");
  setText("#socialAddForm .field > span", "findUsername");
  setPlaceholder(socialUsernameInputEl, "friendPlaceholder");
  setText("#socialAddForm .field-note", "socialFieldNote");
  setText(socialAddBtn, "sendRequest");
  setText(socialGuestNoteEl, "socialGuest");
  setText(".social-panel-block:nth-of-type(1) .section-head h3", "friends");
  setText(".social-panel-block:nth-of-type(1) .section-head p", "socialBody");
  setText(".social-panel-block:nth-of-type(2) .section-head h3", "suggestions");
  setText(".social-panel-block:nth-of-type(2) .section-head p", "suggestionsBody");
  const socialBlocks = Array.from(document.querySelectorAll(".social-panel-block"));
  setText(socialBlocks[0]?.querySelector(".section-head h3"), "friends");
  setText(socialBlocks[0]?.querySelector(".section-head p"), "socialBody");
  setText(socialBlocks[1]?.querySelector(".section-head h3"), "suggestions");
  setText(socialBlocks[1]?.querySelector(".section-head p"), "suggestionsBody");
  setText("#quizPanel > .library-copy", "quizBody");
  setText(nextQuizBtn, "nextQuestion");
  setText("#manualHelpPanel > .library-copy", "manualBody");
  setText("#manual-form .field > span", "typeWord");
  setText("#manualBtn", "explainWord");
  setText("#infoPanel > .library-copy", "infoBody");
  setText(".info-panel-hero .mini-label", "infoHeroLabel");
  setText(".info-panel-hero h4", "infoHeroTitle");
  setText(".info-panel-hero > p", "infoHeroBody");

  updateLevelUi();
  renderKeywordChips();
  renderLibraryStats();
  updateSourceModeUi();
  renderSelection();
  renderUserPanel();
}

function toggleLanguage() {
  applyLanguage(state.uiLanguage === "tr" ? "en" : "tr");
}

function isStandaloneApp() {
  return Boolean(
    window.matchMedia?.("(display-mode: standalone)")?.matches ||
    window.navigator.standalone ||
    window.location.protocol === "capacitor:"
  );
}

function isIosDevice() {
  const ua = window.navigator.userAgent || "";
  return /iphone|ipad|ipod/i.test(ua) || (window.navigator.platform === "MacIntel" && window.navigator.maxTouchPoints > 1);
}

function syncAppModeClasses() {
  document.body.classList.toggle("is-standalone", isStandaloneApp());
  document.body.classList.toggle("is-ios", isIosDevice());
}

function syncInstallCoach() {
  if (!installCoachEl) return;
  const dismissed = window.localStorage.getItem(INSTALL_DISMISSED_KEY) === "1";
  const shouldShow = !dismissed && !isStandaloneApp() && (isIosDevice() || state.deferredInstallPrompt);
  installCoachEl.classList.toggle("hidden", !shouldShow);
  if (!shouldShow) return;
  installCoachLabelEl.textContent = state.uiLanguage === "tr" ? "Uygulama modu" : "App mode";
  if (state.deferredInstallPrompt) {
    installCoachTitleEl.textContent = state.uiLanguage === "tr" ? "Download" : "Download";
    installCoachTextEl.textContent = state.uiLanguage === "tr" ? "Daha temiz tam ekran okuma." : "Cleaner full-screen reading.";
    installCoachActionEl.textContent = state.uiLanguage === "tr" ? "Kur" : "Install";
  } else {
    installCoachTitleEl.textContent = state.uiLanguage === "tr" ? "Download" : "Download";
    installCoachTextEl.textContent = state.uiLanguage === "tr" ? "iPhone ana ekran kısayolu." : "iPhone Home Screen shortcut.";
    installCoachActionEl.textContent = state.uiLanguage === "tr" ? "Adımlar" : "Steps";
  }
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
  const apiBaseUrl =
    window.READLEX_CONFIG?.apiBaseUrl ||
    (window.location.protocol === "capacitor:" ? "https://english-text-studio-staging.onrender.com" : "");
  const requestUrl = apiBaseUrl && String(url).startsWith("/")
    ? `${apiBaseUrl.replace(/\/$/, "")}${url}`
    : url;
  const response = await fetch(requestUrl, {
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
  const hintKey = `levelHint${levelEl.value}`;
  setupLevelBadgeEl.textContent = `${levelEl.value} - ${uiText(hintKey)}`;
  setupLengthBadgeEl.textContent = uiText("aroundWords", { count: lengthEl.value });
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
  updateTopbarSessionDock();
}

function syncTopicPickers(value) {
  topicEl.value = value;
  if (libraryTopicEl) libraryTopicEl.value = value;
  updateTopbarSessionDock();
}

function updateLevelUi() {
  const cfg = LEVEL_CONFIG[levelEl.value];
  lengthEl.min = cfg.min;
  lengthEl.max = cfg.max;
  if (Number(lengthEl.value) < cfg.min || Number(lengthEl.value) > cfg.max) {
    lengthEl.value = Math.round((cfg.min + cfg.max) / 20) * 10;
  }
  lengthValueEl.textContent = lengthEl.value;
  levelHintEl.textContent = uiText(`levelHint${levelEl.value}`) || cfg.hint;
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
  keywordCountEl.textContent = uiText("keywordCount", { count: keywords.length });
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
  $("#generateBtn").textContent = uiText(isLibrary ? "getReading" : "generateText");
  regenBtn.textContent = uiText(isLibrary ? "anotherReading" : "generateAgain");
  previewStateEl.textContent = uiText(isLibrary ? "previewLibrary" : "previewAi");
  renderMeta(
    state.lastPayload?.level || levelEl.value,
    state.lastPayload?.resolved_topic || state.lastPayload?.topic || topicEl.value,
    state.text || ""
  );
  updateTopbarSessionDock();
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
  const total = Number(state.libraryStats.total || 0);
  libraryCountBadgeEl.textContent = uiText("curatedInside", { count: total });
  if (topbarLibraryChipEl) topbarLibraryChipEl.textContent = total ? uiText("texts", { count: total }) : uiText("curated");
}

function updateTopbarSessionDock() {
  const level = state.contentSource === "library" ? libraryLevelEl?.value : levelEl?.value;
  const topic = state.contentSource === "library" ? libraryTopicEl?.value : topicEl?.value;
  if (topbarLevelChipEl) topbarLevelChipEl.textContent = level || "B1";
  if (topbarTopicChipEl) topbarTopicChipEl.textContent = topic || "Random";
  if (topbarLibraryChipEl && !state.libraryStats) {
    topbarLibraryChipEl.textContent = state.contentSource === "library" ? uiText("curated") : uiText("ai");
  }
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
  const sourceLabel = state.lastPayload?.content_source === "library" ? uiText("curated") : uiText("ai");
  metaTagsEl.innerHTML = `
    <span class="tag">${escapeHtml(uiText("level"))} ${escapeHtml(level)}</span>
    <span class="tag">${escapeHtml(topic)}</span>
    <span class="tag">${escapeHtml(uiText("keywordCount", { count }))}</span>
    <span class="tag">${sourceLabel}</span>
  `;
}

function renderSelection() {
  const item = state.glossary[state.selectedWord] || {};
  const meaning = item.turkish || uiText("chooseWord");
  const contextHtml = state.loadingWord
    ? uiText("preparingContext")
    : buildInsightHtml(item.context, state.selectedWord, {
        emptyText: uiText("contextEmpty"),
        collapsedLines: 3,
        maxLines: 14,
      });
  const exampleHtml = state.loadingWord
    ? uiText("preparingExample")
    : buildInsightHtml(item.example, state.selectedWord, {
        emptyText: uiText("exampleEmpty"),
        collapsedLines: 2,
        maxLines: 10,
      });

  selectedWordEl.textContent = state.selectedWord || uiText("word");
  selectedMeaningEl.textContent = meaning;
  selectedContextEl.innerHTML = contextHtml;
  selectedExampleEl.innerHTML = exampleHtml;
  const hasSelection = Boolean(state.selectedWord);
  insightCoachEl?.classList.toggle("is-empty", !hasSelection && !state.loadingWord);
  insightCoachEl?.classList.toggle("is-loading", Boolean(state.loadingWord));
  insightCoachEl?.classList.toggle("has-word", hasSelection && !state.loadingWord);
  if (insightCoachTitleEl) {
    insightCoachTitleEl.textContent = state.loadingWord
      ? state.selectedWord || uiText("word")
      : hasSelection
        ? state.selectedWord
        : uiText("usageCoachEmptyTitle");
  }
  if (insightCoachBodyEl) {
    insightCoachBodyEl.textContent = state.loadingWord
      ? uiText("usageCoachLoadingBody")
      : hasSelection
        ? uiText("usageCoachActiveBody")
        : uiText("usageCoachEmptyBody");
  }
  if (insightCoachStateEl) {
    insightCoachStateEl.textContent = state.loadingWord
      ? uiText("usageCoachLoading")
      : hasSelection
        ? uiText("usageCoachActive")
        : uiText("usageCoachReady");
  }
  renderCollocations(selectedCollocationsEl, item.collocations || []);
  flipCardEl.classList.remove("flipped");
  flipCardEl.classList.toggle("clickable", !state.loadingWord && Boolean(state.selectedWord));
  pronounceWordBtn?.classList.toggle("hidden", !state.selectedWord);

  if (mobileWordTitleEl) mobileWordTitleEl.textContent = state.selectedWord || uiText("word");
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
    savedWordsMetaEl.textContent = uiText("savedMeta", { count: state.recentWords.length });
  }
  savedWordsListEl.innerHTML = state.recentWords
    .map(
      (item) => `
        <div class="saved-word-row" data-word-id="${item.id}">
          <button class="saved-word-item" type="button" data-word="${escapeHtml(item.word)}">
            <strong>${escapeHtml(item.word)}</strong>
            <span>${escapeHtml(item.turkish)}</span>
          </button>
          <button class="saved-word-remove" type="button" data-word-id="${item.id}" aria-label="${escapeHtml(uiText("removeWord", { word: item.word }))}">×</button>
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
  if (quizAnsweredBadgeEl) quizAnsweredBadgeEl.textContent = state.uiLanguage === "tr" ? `${state.quizStats.answered} çözüldü` : `${state.quizStats.answered} played`;
  if (quizStreakBadgeEl) quizStreakBadgeEl.textContent = uiText("streak", { count: state.quizStats.streak });
  quizModeSavedBtn?.classList.toggle("active", state.quizMode === "saved");
  quizModeHardBtn?.classList.toggle("active", state.quizMode === "hard");
  quizModeReadingBtn?.classList.toggle("active", state.quizMode === "reading");
  if (state.quizMode !== "reading" && !state.user) {
    quizEmptyEl.textContent = uiText("signInQuiz");
    quizEmptyEl.classList.remove("hidden");
    quizCardEl.classList.add("hidden");
    return;
  }
  if (!state.quiz) {
    quizEmptyEl.textContent = state.quizMode === "reading"
      ? uiText("quizEmptyReading")
      : state.quizMode === "hard"
        ? uiText("quizEmptyHard")
        : uiText("quizEmptySaved");
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
    quizTypeBadgeEl.textContent = uiText("englishToTurkish");
  }
  if (quizSentenceEl) {
    quizSentenceEl.textContent = "";
    quizSentenceEl.classList.add("hidden");
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
          ? uiText("correct", { word: state.quiz.word, answer: state.quiz.answer })
          : uiText("wrong", { answer: state.quiz.answer });
        quizFeedbackEl.classList.remove("hidden");
        quizOptionsEl.querySelectorAll(".quiz-option").forEach((optionButton) => {
          optionButton.disabled = true;
          optionButton.classList.toggle("correct", optionButton.dataset.answer === state.quiz.answer);
          optionButton.classList.toggle(
            "wrong",
            optionButton.dataset.answer === button.dataset.answer && button.dataset.answer !== state.quiz.answer
          );
        });
        if (quizAnsweredBadgeEl) quizAnsweredBadgeEl.textContent = state.uiLanguage === "tr" ? `${state.quizStats.answered} çözüldü` : `${state.quizStats.answered} played`;
        if (quizStreakBadgeEl) quizStreakBadgeEl.textContent = uiText("streak", { count: state.quizStats.streak });
        if (!isCorrect) {
          nextQuizBtn.disabled = true;
          nextQuizBtn.textContent = uiText("nextIncoming");
          window.setTimeout(async () => {
            await loadQuiz(state.quiz?.word || null);
            nextQuizBtn.disabled = false;
            nextQuizBtn.textContent = uiText("nextQuestion");
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
          ? uiText("correct", { word: parsed.data.word, answer: parsed.data.answer })
          : uiText("wrong", { answer: parsed.data.answer });
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
        if (quizAnsweredBadgeEl) quizAnsweredBadgeEl.textContent = state.uiLanguage === "tr" ? `${state.quizStats.answered} çözüldü` : `${state.quizStats.answered} played`;
        if (quizStreakBadgeEl) quizStreakBadgeEl.textContent = uiText("streak", { count: state.quizStats.streak });
        if (!parsed.data.correct) {
          nextQuizBtn.disabled = true;
          nextQuizBtn.textContent = uiText("nextIncoming");
          window.setTimeout(async () => {
            await loadQuiz(state.quiz?.word_id || null);
            nextQuizBtn.disabled = false;
            nextQuizBtn.textContent = uiText("nextQuestion");
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
    libraryKickerEl.textContent = state.uiLanguage === "tr" ? "Profil" : "Profile";
    libraryTitleEl.textContent = state.uiLanguage === "tr" ? "Hesap erişimi" : "Account access";
  } else if (view === "progress") {
    libraryKickerEl.textContent = uiText("progress");
    libraryTitleEl.textContent = state.uiLanguage === "tr" ? "Serin ve geçmişin" : "Your streak and history";
  } else if (view === "social") {
    libraryKickerEl.textContent = state.uiLanguage === "tr" ? "Sosyal" : "Social";
    libraryTitleEl.textContent = state.uiLanguage === "tr" ? "Arkadaşlar ve motivasyon" : "Friends and momentum";
  } else if (view === "saved") {
    libraryKickerEl.textContent = uiText("savedWords");
    libraryTitleEl.textContent = state.uiLanguage === "tr" ? "Kayıtlı kelimelerin" : "Your saved words";
  } else if (view === "quiz") {
    libraryKickerEl.textContent = "Mini Quiz";
    libraryTitleEl.textContent = state.uiLanguage === "tr" ? "Hızlı tekrar" : "Quick review";
  } else if (view === "manual") {
    libraryKickerEl.textContent = uiText("translate");
    libraryTitleEl.textContent = state.uiLanguage === "tr" ? "Hızlı çeviri" : "Quick translation";
  } else if (view === "info") {
    libraryKickerEl.textContent = uiText("office");
    libraryTitleEl.textContent = state.uiLanguage === "tr" ? "ReadLex şirket ve güven notları" : "ReadLex company and trust notes";
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
  navMenuMarkTriggerEl?.setAttribute("aria-expanded", isOpen ? "true" : "false");
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
  const relationship = user.relationship || "";
  const badge = user.reason || (user.streak > 0 ? `Streak ${user.streak}` : `${user.total_readings || 0} texts`);
  const fireLevel = Number(user.fire_level || 0);
  const fireText = fireLevel > 0 ? `${user.fire_icon || "🔥"} ${user.fire_label || "On fire"}` : "Cold start";
  const resolvedAction =
    relationship === "friend"
      ? "friend-label"
      : relationship === "pending_outgoing"
        ? "pending"
        : relationship === "pending_incoming"
          ? "accept"
          : action;
  const actionHtml =
    resolvedAction === "accept"
      ? `<div class="social-actions">
          <button class="ghost-btn ghost-btn-inline social-accept" type="button" data-request-id="${requestId}">Accept</button>
          <button class="ghost-btn ghost-btn-inline social-decline" type="button" data-request-id="${requestId}">Decline</button>
        </div>`
      : resolvedAction === "add"
        ? `<button class="ghost-btn ghost-btn-inline social-add-suggested" type="button" data-username="${escapeHtml(user.username)}">Add</button>`
        : resolvedAction === "friend"
          ? `<div class="social-actions">
              <button class="ghost-btn ghost-btn-inline social-cheer" type="button" data-friendship-id="${friendshipId}">Cheer</button>
              <button class="ghost-btn ghost-btn-inline social-remove" type="button" data-friendship-id="${friendshipId}">Remove</button>
            </div>`
          : resolvedAction === "friend-label"
            ? `<span class="social-pending social-status-good">Friend</span>`
            : `<span class="social-pending">Pending</span>`;
  return `
    <article class="social-card">
      <div class="social-avatar">${escapeHtml(String(user.username || "U").charAt(0).toUpperCase())}</div>
      <div class="social-card-copy">
        <strong>${escapeHtml(user.username || "user")}</strong>
        <span>${escapeHtml(fireText)} · ${escapeHtml(badge)} · ${Number(user.saved_words || 0)} saved · ${Number(user.words_today || 0)} today</span>
      </div>
      ${actionHtml}
    </article>
  `;
}

function renderSocialSearchResults() {
  if (!socialSearchResultsEl) return;
  const query = String(state.socialSearch.query || "").trim();
  if (!state.user || !query) {
    socialSearchResultsEl.classList.add("hidden");
    socialSearchResultsEl.innerHTML = "";
    return;
  }
  socialSearchResultsEl.classList.remove("hidden");
  if (state.socialSearch.loading) {
    socialSearchResultsEl.innerHTML = `<p class="history-empty">Searching learners...</p>`;
    return;
  }
  const results = state.socialSearch.results || [];
  socialSearchResultsEl.innerHTML = `
    <div class="social-search-head">
      <strong>Search results</strong>
      <span>${escapeHtml(query)}</span>
    </div>
    ${
      results.length
        ? results
            .map((user) =>
              renderSocialCard(user, {
                action: "add",
                requestId: user.friendship_id,
                friendshipId: user.friendship_id,
              })
            )
            .join("")
        : `<p class="history-empty">No learner found with that username yet.</p>`
    }
  `;
  bindSocialActions(socialSearchResultsEl);
}

function bindSocialActions(root = document) {
  if (!root) return;
  root.querySelectorAll?.(".social-accept, .social-decline").forEach((button) => {
    button.addEventListener("click", async () => {
      const action = button.classList.contains("social-accept") ? "accept" : "decline";
      await respondSocialRequest(button.dataset.requestId, action);
    });
  });
  root.querySelectorAll?.(".social-add-suggested").forEach((button) => {
    button.addEventListener("click", async () => {
      if (socialUsernameInputEl) socialUsernameInputEl.value = button.dataset.username || "";
      await sendFriendRequest(button.dataset.username || "");
    });
  });
  root.querySelectorAll?.(".social-cheer").forEach((button) => {
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
  root.querySelectorAll?.(".social-remove").forEach((button) => {
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
      : `<p class="history-empty">Search a username above to invite your first friend.</p>`;
  }
  renderSocialSearchResults();
  bindSocialActions(socialIncomingListEl);
  bindSocialActions(socialFriendsListEl);
  bindSocialActions(socialSuggestionsListEl);
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
    renderSocialSearchResults();
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
    state.socialSearch = { query: "", results: [], loading: false };
    if (socialUsernameInputEl) socialUsernameInputEl.value = "";
    renderSocialPanel();
    showToast("Friend request sent.", { variant: "info", scope: "social" });
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
  state.socialSearch = { query: "", results: [], loading: false };
  renderSocialPanel();
}

let socialSearchTimer = null;

async function searchSocialUsers(query) {
  const cleaned = String(query || "").trim();
  if (!state.user || cleaned.length < 3) {
    state.socialSearch = { query: "", results: [], loading: false };
    renderSocialSearchResults();
    return;
  }
  state.socialSearch = { query: cleaned, results: [], loading: true };
  renderSocialSearchResults();
  try {
    const parsed = await apiFetch(`/api/social/search?q=${encodeURIComponent(cleaned)}`);
    if (!parsed.ok) throw new Error(parsed.data.detail || "Search failed.");
    state.socialSearch = {
      query: parsed.data.query || cleaned,
      results: parsed.data.results || [],
      loading: false,
    };
  } catch (error) {
    state.socialSearch = { query: cleaned, results: [], loading: false };
    showToast(error.message || "Search failed.", { variant: "error", scope: "social" });
  }
  renderSocialSearchResults();
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
  if (profileAvatarBtn) {
    profileAvatarBtn.dataset.fireLevel = String(state.stats.fire_level || 0);
    profileAvatarBtn.setAttribute(
      "aria-label",
      loggedIn
        ? state.uiLanguage === "tr"
          ? `Profil panelini aç. ${state.stats.fire_label || "Cold start"} seri ${state.stats.login_streak || state.stats.streak || 0}.`
          : `Open profile panel. ${state.stats.fire_label || "Cold start"} streak ${state.stats.login_streak || state.stats.streak || 0}.`
        : state.uiLanguage === "tr" ? "Profil panelini aç" : "Open profile panel"
    );
  }
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
          ? uiText("profileTipActive")
          : uiText("profileTipEmpty");
    }
    if (dailyGoalTextEl) {
      dailyGoalTextEl.textContent = uiText("wordsToday", { saved: state.stats.saved_today || 0, goal: state.stats.daily_goal || 5 });
    }
    if (streakBadgeEl) {
      const streak = state.stats.login_streak || state.stats.streak || 0;
      const fireLabel = state.stats.fire_label || "Cold start";
      const next = Number(state.stats.fire_next || 0);
      streakBadgeEl.textContent = next > 0
        ? `${fireLabel} ${streak} · ${next} to next`
        : `${fireLabel} ${streak}`;
    }
    if (goalBarFillEl) {
      const ratio = Math.min(100, ((state.stats.saved_today || 0) / Math.max(1, state.stats.daily_goal || 5)) * 100);
      goalBarFillEl.style.width = `${ratio}%`;
    }
    if (hardWordsTextEl) {
      hardWordsTextEl.textContent = uiText("hardWords", { count: state.stats.hard_words || 0 });
    }
    if (progressHistoryListEl) {
      const rows = Array.isArray(state.progressHistory) ? state.progressHistory : [];
      if (!rows.length) {
        progressHistoryListEl.innerHTML = `<p class="history-empty">${escapeHtml(uiText("dailyTotalsEmpty"))}</p>`;
      } else {
        progressHistoryListEl.innerHTML = rows
          .map((item) => {
            const texts = Number(item.texts || 0);
            const words = Number(item.words || 0);
            return `
              <article class="progress-history-item">
                <div>
                  <span>${escapeHtml(formatProgressDate(item.date))}</span>
                  <strong>${texts} ${state.uiLanguage === "tr" ? "Metin" : `Text${texts === 1 ? "" : "s"}`}</strong>
                </div>
                <em>${words} ${state.uiLanguage === "tr" ? "Kelime" : `Word${words === 1 ? "" : "s"}`}</em>
              </article>
            `;
          })
          .join("");
      }
    }
    if (readingHistoryListEl) {
      if (!uniqueReadingHistory.length) {
        readingHistoryListEl.innerHTML = `<p class="history-empty">${escapeHtml(uiText("recentReadingsEmpty"))}</p>`;
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
    if (readingHistoryListEl) readingHistoryListEl.innerHTML = `<p class="history-empty">${escapeHtml(uiText("signInTrail"))}</p>`;
    if (progressHistoryListEl) progressHistoryListEl.innerHTML = `<p class="history-empty">${escapeHtml(uiText("signInProgress"))}</p>`;
    if (totalReadingsTextEl) totalReadingsTextEl.textContent = "0";
    if (todayReadingsTextEl) todayReadingsTextEl.textContent = "0";
    if (todayWordsTextEl) todayWordsTextEl.textContent = "0";
    if (dailyGoalTextEl) dailyGoalTextEl.textContent = state.uiLanguage === "tr" ? "Bugün 0 / 5" : "0 / 5 today";
    if (streakBadgeEl) streakBadgeEl.textContent = uiText("streak", { count: 0 });
    if (goalBarFillEl) goalBarFillEl.style.width = "0%";
    if (hardWordsTextEl) hardWordsTextEl.textContent = uiText("hardWords", { count: 0 });
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
    const translateAuthMessage = (message) => {
      const clean = String(message || "").trim();
      if (state.uiLanguage !== "tr") return clean || "Authentication failed.";
      const lower = clean.toLowerCase();
      if (!clean) return "Kimlik doğrulama başarısız.";
      if (lower.includes("already in use")) return "Bu kullanıcı adı zaten kullanılıyor.";
      if (lower.includes("invalid username") || lower.includes("invalid password")) return "Kullanıcı adı veya şifre hatalı.";
      if (lower.includes("at least 6")) return "Şifre en az 6 karakter olmalı.";
      if (lower.includes("authentication failed")) return "Kimlik doğrulama başarısız.";
      return clean;
    };
    if (!detail) return translateAuthMessage("Authentication failed.");
    if (typeof detail === "string") return translateAuthMessage(detail);
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
      return translateAuthMessage(parts.join("\n") || "Authentication failed.");
    }
    if (typeof detail === "object") {
      if (Array.isArray(detail.detail)) return formatAuthError(detail.detail);
      if (typeof detail.message === "string") return translateAuthMessage(detail.message);
      if (typeof detail.error === "string") return translateAuthMessage(detail.error);
      if (typeof detail.title === "string") return translateAuthMessage(detail.title);
      if (typeof detail.msg === "string") return translateAuthMessage(detail.msg);
    }
    return translateAuthMessage("Authentication failed.");
  };

  if (errorEl) {
    errorEl.textContent = "";
    errorEl.classList.add("hidden");
  }
  setLoading(submitBtn, endpoint.includes("/login")
    ? (state.uiLanguage === "tr" ? "Giriş yapılıyor..." : "Logging in...")
    : (state.uiLanguage === "tr" ? "Hesap oluşturuluyor..." : "Creating account..."), true);
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
            : (state.uiLanguage === "tr" ? "Kimlik doğrulama başarısız." : "Authentication failed.");
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
    state.socialSearch = { query: "", results: [], loading: false };
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
    libraryCountBadgeEl.textContent = uiText("libraryUnavailable");
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
        selectedMeaningEl.textContent = state.uiLanguage === "tr" ? "Yükleniyor..." : "Loading...";
        selectedContextEl.textContent = uiText("preparingContext");
        selectedExampleEl.textContent = uiText("preparingExample");
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
  selectedContextEl.textContent = state.uiLanguage === "tr"
    ? "Okuma hazır. Türkçe bağlamı açmak için bir kelimeye dokun."
    : "The reading is ready. Tap a word to open its Turkish context.";
  selectedExampleEl.textContent = uiText("exampleEmpty");
  renderQuiz();
}

async function generateExperience(payload, triggerButton) {
  clearError();
  setLoading(triggerButton, payload.source === "library"
    ? (state.uiLanguage === "tr" ? "Yükleniyor..." : "Loading...")
    : (state.uiLanguage === "tr" ? "Üretiliyor..." : "Generating..."), true);
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
        <span class="mini-label">${escapeHtml(uiText("turkishMeaning"))}</span>
        <strong>${escapeHtml(parsed.data.turkish || "No match")}</strong>
      </div>
      <div class="manual-result-block">
        <span class="mini-label">${escapeHtml(uiText("contextTurkish"))}</span>
        <p>${highlightSelectedWord(parsed.data.context || "No context available.", word.toLowerCase())}</p>
      </div>
      <div class="manual-result-block">
        <span class="mini-label">${escapeHtml(uiText("simpleExample"))}</span>
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

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  state.deferredInstallPrompt = event;
  syncInstallCoach();
});

window.addEventListener("appinstalled", () => {
  state.deferredInstallPrompt = null;
  window.localStorage.setItem(INSTALL_DISMISSED_KEY, "1");
  syncAppModeClasses();
  syncInstallCoach();
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
    state.socialSearch = { query: "", results: [], loading: false };
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
navMenuMarkTriggerEl?.addEventListener("click", (event) => {
  event.preventDefault();
  event.stopPropagation();
  if (isDesktopMenuMode()) {
    setNavMenuOpen(true);
    return;
  }
  setNavMenuOpen(!navMenuShellEl?.classList.contains("is-open"));
});
navMenuMarkTriggerEl?.addEventListener("mouseenter", () => {
  if (isDesktopMenuMode()) setNavMenuOpen(true);
});
navMenuMarkTriggerEl?.addEventListener("mouseleave", () => {
  if (!isDesktopMenuMode()) return;
  navMenuCloseTimer = window.setTimeout(() => {
    setNavMenuOpen(false);
  }, 160);
});
navMenuMarkTriggerEl?.addEventListener("focus", () => {
  if (isDesktopMenuMode()) setNavMenuOpen(true);
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
installCoachActionEl?.addEventListener("click", async () => {
  if (state.deferredInstallPrompt) {
    state.deferredInstallPrompt.prompt();
    await state.deferredInstallPrompt.userChoice.catch(() => null);
    state.deferredInstallPrompt = null;
    window.localStorage.setItem(INSTALL_DISMISSED_KEY, "1");
    syncInstallCoach();
    return;
  }
  showToast("iPhone: Safari'de Paylaş düğmesine dokun, sonra Add to Home Screen seç.", {
    variant: "success",
    scope: "install",
    duration: 6800,
  });
});
installCoachDismissEl?.addEventListener("click", () => {
  window.localStorage.setItem(INSTALL_DISMISSED_KEY, "1");
  syncInstallCoach();
});
socialAddFormEl?.addEventListener("submit", async (event) => {
  event.preventDefault();
  await sendFriendRequest();
});
socialUsernameInputEl?.addEventListener("input", () => {
  window.clearTimeout(socialSearchTimer);
  const query = socialUsernameInputEl.value || "";
  socialSearchTimer = window.setTimeout(() => {
    void searchSocialUsers(query);
  }, 260);
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
gateThemeToggleBtn?.addEventListener("click", toggleTheme);
languageToggleBtn?.addEventListener("click", toggleLanguage);
gateLanguageToggleBtn?.addEventListener("click", toggleLanguage);

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
  updateTopbarSessionDock();
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
applyLanguage(state.uiLanguage);
syncAppModeClasses();
syncInstallCoach();
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
