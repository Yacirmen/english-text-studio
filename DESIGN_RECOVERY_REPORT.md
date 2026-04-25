# ReadWave Design Recovery Report

## What was broken or worsened

- The previous experimental redesign was too broad for the current product state and risked turning ReadWave into a generic landing-page style product instead of a focused reading tool.
- Some light-mode auth surfaces had poor contrast, especially inside account access panels.
- Library, saved words, and hub cards carried too much decorative gradient treatment and felt visually noisy for a reading-first product.
- Primary buttons had a toy-like heavy shadow and oversized pill feeling in several places.
- The reading text affordance was too loud in places and could distract from long-form reading.
- Mobile reading needed a stronger reading-first order once a text was opened.
- Several microcopy lines were generic or over-promising instead of clearly explaining the read, tap, save, review loop.

## What was restored

- Kept the original stable header, profile, theme, language, auth, setup, reading, saved words, quiz, progress, and social structures.
- Did not port the large experimental redesign layer into this branch.
- Preserved existing DOM structure and JavaScript behavior for login, signup, guest mode, library readings, AI readings, word tapping, saved words, quiz, progress, theme, and language.
- Kept ReadWave closer to the working main design while reducing visual roughness.

## What was improved

- Added a restrained recovery design layer instead of a full redesign.
- Warmed the global background without adding heavy decorative effects.
- Reduced excessive radius, shadow, and visual weight on welcome, rail, reading, insight, and auth surfaces.
- Converted light-mode welcome auth and profile auth panels into readable light surfaces.
- Simplified library and hub item cards into calmer white panels with clear borders and readable text.
- Softened primary and secondary buttons so they feel clickable without looking toy-like.
- Improved reading paper contrast and reduced background decoration inside the reading body.
- Reworked word hover/active treatment into a subtle reading affordance instead of a noisy highlight.
- Improved mobile typography and padding for reading text.
- When a reading is visible in mobile mode, the reading stage is prioritized before setup.
- Rewrote key English and Turkish microcopy around the core loop: read, tap, save, review.
- Bumped service worker and asset query versions to avoid stale UI after recovery changes.

## 2026-04-25 social release addendum

- Reworked the social panel into a calmer, more useful friends and motivation area.
- Fixed wide/narrow viewport clipping where social cards, username search, and the send button could overflow the panel.
- Added `min-width: 0`, `max-width: 100%`, and panel-level overflow guards to keep social content inside the body cards.
- Verified the panel with a headless Chrome overflow check at `864x1200`.
- Preserved the previous `master` as `backup/main-before-social-release-20260425` and `main-before-social-release-20260425`.
- Added detailed release and rollback notes in `RELEASE_ROLLBACK_NOTES.md`.

## Files changed

- `frontend/index.html`
- `frontend/assets/app.js`
- `frontend/assets/styles.css`
- `frontend/sw.js`
- `DESIGN_RECOVERY_REPORT.md`
- `RELEASE_ROLLBACK_NOTES.md`
- `README.md`

## Tests and checks

- `git diff --check` passed.
- `node --check frontend/assets/app.js` passed.
- `.venv313/bin/python -m pytest` passed: 18 tests.
- Manual browser QA on the local dev server covered:
  - guest reading flow
  - curated reading open
  - word tap and meaning panel
  - Study Hub open
  - profile/account panel open
  - saved words panel open
  - Turkish/English toggle
  - dark/light toggle

## Remaining risks

- The CSS file already contains several older override layers; this pass intentionally avoided a full cleanup to reduce regression risk.
- The local in-app browser can hold stale service worker assets, so cache version bumps are still necessary during visual QA.
- There is no frontend lint, typecheck, or build script available in `package.json`; `npm` was also unavailable in the current shell.
- Visual regression coverage is manual only. A future pass should add screenshot checks for welcome, setup, reading, profile, saved words, quiz, and mobile states.
