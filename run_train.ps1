# Run the training script in the repo venv
$venv = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
& $venv train/train.py
