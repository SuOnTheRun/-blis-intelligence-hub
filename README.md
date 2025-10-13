# Blis Intelligence Hub (Open-Source Signals)

A quiet, executive-grade media intelligence dashboard that runs on **open data** only and refreshes every 5 minutes.  
No placeholders. Optional Excel **plug-and-view** to overlay your foot traffic / loyalty series.

## Features
- **Regions & Countries**: EU, SEA, LATAM, MENA (with country dropdowns) + first-class US/UK/CA/CN/JP/IN.
- **Categories**: Automotive, Tech, Energy, Financials, Consumer Staples, Healthcare, Media & Advertising.
- **Open Signals**: Reuters RSS, Yahoo Finance quotes, Google Trends, Wikipedia Pageviews, Reddit (optional).
- **Sentiment & Momentum**: VADER headline sentiment; simple composite CCS; Reddit momentum.
- **Excel Uploads**: Volume / Loyalty / RTFs / Trend / MABLE (wide sheets) and Crossover matrices; instant overlays.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
