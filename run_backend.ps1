# Start the backend using the repo venv
$venv = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $venv -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
