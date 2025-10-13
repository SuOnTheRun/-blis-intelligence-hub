# Lightweight persistence for uploads and last-known open-data pulls (SQLite via pandas).
# Works on Replit/Render; no external DB required.

from __future__ import annotations
import os, sqlite3, json
from contextlib import closing

DB_PATH = os.getenv("HUB_DB_PATH", "hub.sqlite3")

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS user_dataset(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  sheet TEXT NOT NULL,
  metric TEXT NOT NULL,
  source_file TEXT NOT NULL,
  uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_timeseries(
  dataset_id INTEGER NOT NULL,
  brand TEXT,
  country TEXT,
  market_group TEXT,
  date TEXT NOT NULL,
  value REAL,
  PRIMARY KEY(dataset_id, brand, country, date),
  FOREIGN KEY(dataset_id) REFERENCES user_dataset(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_cross(
  dataset_id INTEGER NOT NULL,
  country TEXT,
  brand_a TEXT,
  brand_b TEXT,
  value REAL,
  PRIMARY KEY(dataset_id, brand_a, brand_b, country),
  FOREIGN KEY(dataset_id) REFERENCES user_dataset(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ref_brand(
  brand TEXT PRIMARY KEY,
  sector TEXT
);

CREATE TABLE IF NOT EXISTS ref_geo(
  country TEXT NOT NULL,
  region TEXT NOT NULL,
  market_group TEXT,
  PRIMARY KEY(country, region)
);

-- cache last pulls (open sources)
CREATE TABLE IF NOT EXISTS cache_blob(
  key TEXT PRIMARY KEY,
  payload TEXT,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init():
    with closing(get_conn()) as c:
        c.executescript(SCHEMA)
        c.commit()

def put_cache(key: str, payload: dict):
    with closing(get_conn()) as c:
        c.execute("REPLACE INTO cache_blob(key,payload,ts) VALUES(?,?,CURRENT_TIMESTAMP)",
                  (key, json.dumps(payload)))
        c.commit()

def get_cache(key: str):
    with closing(get_conn()) as c:
        cur = c.execute("SELECT payload FROM cache_blob WHERE key=?", (key,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None
