# ReadLex iOS App Notes

ReadLex can ship to iPhone in two steps:

1. PWA install for quick testing from Safari.
2. Capacitor iOS shell for App Store packaging.

## Local Windows Preparation

This repository includes:

- `frontend/manifest.webmanifest`
- `frontend/sw.js`
- `capacitor.config.json`
- `package.json`

The frontend automatically talks to the live Render API when it runs inside Capacitor.

## iOS Build Requirements

Apple release builds require:

- macOS
- Xcode
- Apple Developer Program membership
- App Store Connect app record

## Mac Build Commands

```bash
npm install
npm run ios:add
npm run ios:sync
npm run ios:open
```

Then in Xcode:

1. Select a real iPhone or simulator.
2. Set signing team and bundle identifier.
3. Run the app.
4. Archive for App Store Connect when ready.

## Backend Settings

For the hosted API, keep these compatible with iOS WebView auth:

```env
CORS_ALLOWED_ORIGINS=https://english-text-studio-staging.onrender.com,capacitor://localhost,ionic://localhost
COOKIE_SECURE=true
COOKIE_SAMESITE=none
```
