# Run / Restart the Local Preview Server

How to manually start and restart the Quartz local preview server on Windows.

## Prerequisites

- **Python** (not in PATH) — use the full path:
  ```
  C:\Users\hycheun456\AppData\Local\Programs\Python\Python312\python.exe
  ```
- The site must already be built (`.site/public/` exists). If not, see [Build the site](#build-the-site).

## Start the server

Open **PowerShell** and run:

```powershell
cd C:\Users\hycheun456\Documents\GitHub\CityUHK-CS-chatbot\.site
& "C:\Users\hycheun456\AppData\Local\Programs\Python\Python312\python.exe" serve.py 8090 public
```

Then open **http://127.0.0.1:8090/** in your browser.

> **Use `127.0.0.1`, not `localhost`.** Port 8080 is often taken by another server
> (a Node.js process bound to IPv6). `localhost` may route to that server and show
> 404s. `127.0.0.1` forces IPv4 and always reaches `serve.py`.

## Restart the server

1. **Stop** the running server. Find its process ID:
   ```powershell
   Get-NetTCPConnection -LocalPort 8090 -State Listen
   ```
   Note the `OwningProcess` number, then stop it:
   ```powershell
   Stop-Process -Id <PID> -Force
   ```
2. **Start** it again with the same command as above.

## Verify it's working

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8090/" -UseBasicParsing
Invoke-WebRequest -Uri "http://127.0.0.1:8090/00_vault-map/" -UseBasicParsing
```

Both should return `200`. If you get a JSON `{"error":"not found"}`, another server is
answering — see [Port conflict](#port-conflict).

## Build the site

If `.site/public/` is missing or outdated, rebuild from the notes folder:

```powershell
cd C:\Users\hycheun456\Documents\GitHub\CityUHK-CS-chatbot\.site
& "C:\Program Files\nodejs\npm.cmd" exec quartz build -d ../notes
```

> Use `npm.cmd`, not `npm.ps1` (execution policy blocks scripts). Build from `../notes`
> because the `.site/content/*` symlinks don't work on Windows.

## Port conflict

If port 8090 is already in use, or you see JSON 404s, check what's listening:

```powershell
Get-NetTCPConnection -LocalPort 8080 -State Listen
Get-NetTCPConnection -LocalPort 8090 -State Listen
```

If another process holds the port, either stop it or start `serve.py` on a different
port (e.g. `serve.py 8091 public`) and open `http://127.0.0.1:8091/`.

## Notes

- The server runs in the foreground of the PowerShell window. Keep that window open
  while you preview; close it to stop the server.
- `serve.py` strips the `/CityUHK-CS-Admission-FAQ` baseUrl prefix and serves
  extensionless URLs as `.html`, so both `/00_vault-map/` and `/00_vault-map/index.html`
  work.