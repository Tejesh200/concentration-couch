from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import joblib

# Initialize FastAPI app
app = FastAPI()

# Paths
DB_PATH = "logs.db"
MODEL_PATH = "model.pkl"
VEC_PATH = "vectorizer.pkl"

# Load ML model + vectorizer
clf = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)


# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            url TEXT,
            label TEXT,
            score REAL,
            action TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


init_db()


# ---------- Request Schema ----------
class ClassifyRequest(BaseModel):
    url: str
    title: str | None = None


# ---------- Endpoints ----------
@app.post("/classify")
async def classify(req: ClassifyRequest):
    text = req.url
    if req.title:
        text = req.title + " " + text

    X = vectorizer.transform([text])
    prob = clf.predict_proba(X)[0]
    pred = clf.predict(X)[0]

    idx = list(clf.classes_).index(pred)
    
    # Log the visit to database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs(user_id, url, label, score, action) VALUES(?, ?, ?, ?, ?)",
        ("default_user", req.url, str(pred), float(prob[idx]), "visit")
    )
    conn.commit()
    conn.close()

    return {
        "label": str(pred),
        "score": float(prob[idx]),
        "classes": list(clf.classes_),
        "classification": str(pred),  # Add for compatibility with app.py format
    }



@app.post("/log")
async def log(payload: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs(user_id,url,label,score,action) VALUES(?,?,?,?,?)",
        (
            payload.get("user_id"),
            payload.get("url"),
            payload.get("label"),
            payload.get("score"),
            payload.get("action"),
        ),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/stats")
async def get_stats():
    """
    Returns statistics about website visits: counts of productive vs distractive visits
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get total visit counts by classification
    c.execute("SELECT label, COUNT(*) FROM logs WHERE label IS NOT NULL GROUP BY label")
    rows = c.fetchall()
    
    stats = {}
    for label, count in rows:
        # Normalize label names
        normalized_label = label.lower() if label else "unknown"
        if normalized_label in ["distractive", "distracting"]:
            stats["distractive"] = stats.get("distractive", 0) + count
        else:
            stats["productive"] = stats.get("productive", 0) + count
    
    # Ensure both keys exist
    if "distractive" not in stats:
        stats["distractive"] = 0
    if "productive" not in stats:
        stats["productive"] = 0
    
    conn.close()
    return stats


@app.get("/health")
async def health():
    return {"ok": True}
