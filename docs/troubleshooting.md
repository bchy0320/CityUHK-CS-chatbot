# Troubleshooting / Lessons Learned

Short notes on mistakes made and how to fix them. Read this first when something breaks — it saves time.

## Local preview server (Quartz)

### Symptom: Homepage loads but subpages return 404
- **Cause:** Port `8080` was already taken by another server (`node --experimental-sqlite src/server.js`, bound to IPv6 `::`). Requests to `localhost` route to IPv6 first, so the *other* server answered with a JSON 404 (`{"error":"not found"}`) instead of `serve.py`.
- **Fix:** Start `serve.py` on a different port and access via `127.0.0.1` (forces IPv4):
  ```bash
  cd .site
  python serve.py 8090 public
  # open http://127.0.0.1:8090/
  ```
- **Quick check first:** `Get-NetTCPConnection -LocalPort 8080 -State Listen` — if more than one process is listening, a port conflict is the cause.

### Symptom: `make site-serve` / `npx quartz build -d content` finds almost no files
- **Cause:** On Windows, git `core.symlinks=false` checks out `.site/content/*` symlinks as plain text files (containing the target path), so Quartz can't read them as directories.
- **Fix:** Build directly from the notes folder instead:
  ```bash
  cd .site
  npx quartz build -d ../notes
  ```

### Symptom: Local plugins fail to symlink (EPERM) during build
- **Cause:** Quartz's `install-plugins` uses `fs.symlinkSync` for local plugins (`note-dates`, `heading-ids`, `ai-chat`), which fails on Windows without Developer Mode.
- **Fix (partial):** `.site/quartz/plugins/loader/gitLoader.ts` falls back to `fs.cpSync` when symlink fails. Site still builds without these plugins; features may be degraded.

## Environment quirks (Windows)

- **git** is not in PATH — use `C:\ProgramData\hycheun456\GitHubDesktop\app-3.6.10\resources\app\git\cmd\git.exe`
- **node/npm** not in PATH — use `C:\Program Files\nodejs\node.exe` and `npm.cmd` (not `npm.ps1`; execution policy blocks scripts)
- **python** not in PATH — use `C:\Users\hycheun456\AppData\Local\Programs\Python\Python312\python.exe`
- **PowerShell** has no `&&` / `||`; use `;` and `if ($?) { ... }`
- `Test-Path` fails on `[` / `]` in filenames — use `-LiteralPath`
- Each PowerShell call is a fresh process — `cd` and env vars do not persist between calls

## Notes reorganization (2026-11)

- `notes/` is the git-tracked content source (551 files: 412 original + 139 new)
- `notes_backup/` is a local backup (412 files), gitignored
- `.site/content/*` symlinks were updated to point to `../../notes/<folder>`
- `notes/index.md` was copied from root `index.md` so the homepage builds