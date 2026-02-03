# Stops the background backend process using the PID stored in backend.pid
$pidFile = Join-Path $PSScriptRoot 'backend.pid'

if (-Not (Test-Path $pidFile)) {
    Write-Output "PID file not found: $pidFile"
    exit 1
}

$pid = Get-Content $pidFile
try {
    Stop-Process -Id $pid -Force -ErrorAction Stop
    Remove-Item $pidFile -ErrorAction SilentlyContinue
    Write-Output "Stopped backend (PID $pid)."
} catch {
    Write-Error "Failed to stop process $pid: $_"
    exit 1
}
