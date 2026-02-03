# Starts the backend in the background and writes PID to backend.pid
$venv = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$uvicornArgs = '-m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload'

if (-Not (Test-Path $venv)) {
    Write-Error "Virtualenv python not found at $venv. Activate venv or adjust path."
    exit 1
}

$process = Start-Process -FilePath $venv -ArgumentList $uvicornArgs -WindowStyle Hidden -PassThru
$pidFile = Join-Path $PSScriptRoot 'backend.pid'
$process.Id | Out-File -FilePath $pidFile -Encoding ascii
Write-Output "Started backend (PID $($process.Id)). PID saved to $pidFile"
