# Concentration Couch

Local development and run instructions

Prerequisites
- Python 3.10+ and a virtual environment

Quick start (Windows PowerShell)

1. Activate venv

```powershell
& .venv/Scripts/Activate.ps1
```

2. Install backend deps

```powershell
pip install -r backend/app/requirements.txt
```

3. Start backend (from repo root)

```powershell
.venv/Scripts/python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

4. (Optional) Retrain model

```powershell
.venv/Scripts/python.exe train/train.py
```

5. Load Chrome extension
- Go to `chrome://extensions/` -> Developer mode -> Load unpacked -> select the `extension/` folder.

Notes
- Two FastAPI entrypoints exist: the primary used here is `backend/app/main.py`.
- Pickled models were saved with scikit-learn 1.7.0. We pin `scikit-learn==1.7.0` in backend requirements to avoid incompatibility warnings. If you retrain in this environment the new pickles will match your installed version.

Files added
- `run_backend.ps1` — simple Windows script to start uvicorn
- `run_train.ps1` — runs the training script

If you want, I can also create a Windows service or scheduled task to start the backend automatically.
