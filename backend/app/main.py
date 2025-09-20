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

    return {
        "label": str(pred),
        "score": float(prob[idx]),
        "classes": list(clf.classes_),
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


@app.get("/health")
async def health():
    return {"ok": True}
