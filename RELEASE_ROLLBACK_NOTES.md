# ReadLex Release and Rollback Notes

Date: 2026-04-25

## Release Snapshot

- Release branch before merge: `readlex-design-recovery`
- Production branch after release: `master`
- Previous stable main commit: `d813c85d368423288e72d3253cadaba35e39669c`
- Backup branch: `backup/main-before-social-release-20260425`
- Backup tag: `main-before-social-release-20260425`
- Current asset query version: `20260425social3`
- Current service worker cache: `readlex-shell-v65`

## What This Release Contains

- Controlled recovery styling after the rejected broad redesign.
- Premium but restrained body surfaces for light and dark mode.
- Dark-mode page background separation so the main cards do not blend into the body.
- Sticky, calmer word meaning panel behavior so the card stays reachable while reading.
- Turkish microcopy refinements so the interface feels warmer and less like direct translation.
- Social panel redesign and overflow fixes for large, narrow, and mobile viewports.
- Responsive account/profile, setup, study hub, and panel refinements.
- Cache and asset version bumps to prevent stale frontend files after deploy.

## Safety Contract

- The old `master` state is preserved at `d813c85d368423288e72d3253cadaba35e39669c`.
- The backup branch and tag must stay in the remote repository until this release is proven stable.
- This release should be published with normal commits and normal pushes only.
- Do not force-push or delete the backup branch/tag during routine deploys.

## Verification

Run before and after deployment when possible:

```bash
git diff --check
node --check frontend/assets/app.js
.venv313/bin/python -m pytest
```

Manual checks used for this release:

- Desktop landing and setup flow
- Mobile landing and header controls
- Guest reading flow
- Library reading flow
- Word tap and meaning panel
- Turkish/English toggle
- Dark/light mode
- Social panel on a narrow large-resolution viewport
- Social panel overflow check with headless Chrome at `864x1200`

## Rollback

First inspect the backup without touching production:

```bash
git fetch origin
git checkout -b rollback-test backup/main-before-social-release-20260425
```

If production must be restored to the previous stable main, do this only after explicit approval:

```bash
git checkout master
git reset --hard backup/main-before-social-release-20260425
git push origin master
```

After rollback, clear browser/service-worker cache or bump the asset query version again so clients do not keep the released frontend files.
