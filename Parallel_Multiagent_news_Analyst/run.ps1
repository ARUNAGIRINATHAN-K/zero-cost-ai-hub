$repoRoot = $PSScriptRoot
if (-not $repoRoot) {
    $repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
}

$pythonExe = Join-Path $repoRoot 'venv\Scripts\python.exe'

if (-not (Test-Path $pythonExe)) {
    Write-Error 'Virtual environment not found. Create it first with: python -m venv venv'
    exit 1
}

$backendCommand = "& '$pythonExe' -m uvicorn api.main:app --reload"
$frontendCommand = "& '$pythonExe' -m streamlit run ui\streamlit_app.py"

Start-Process -FilePath powershell.exe -WorkingDirectory $repoRoot -ArgumentList @('-NoExit', '-Command', $backendCommand)
Start-Process -FilePath powershell.exe -WorkingDirectory $repoRoot -ArgumentList @('-NoExit', '-Command', $frontendCommand)

Write-Host 'Started backend at http://127.0.0.1:8000 and frontend at http://localhost:8501.'
Write-Host 'Close the two PowerShell windows to stop both services.'