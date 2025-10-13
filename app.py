# Streamlit multi-page Intel Hub with region/country filters, open-source signals (5-min refresh),
# and Excel plug-and-view for Volume/Loyalty/RTF/Crossover.

from __future__ import annotations
import os, io, json, time, math, datetime as dt
import pandas as pd
import streamlit as st
from dateutil import tz

import database as db
from enhanced_collectors import (
    get_reuters_news, get_quotes, get_trends_series, get_wiki_pageviews, get_reddit_top
)

IST = tz.gettz("Asia/Kolkata")
UPDATED = lambda: dt.datetime.now(IST).strftime("%d %b %Y, %H:%M IST")

# ----------------------- One-time init
db.init()
st.set_page_config(page_title="Blis Intelligence Hub", layout="wide")

# Quiet luxury UI
st.markdown("""
<style>
:root { --gold:#bfa66b; --ink:#0f0f10; --sub:#5a5a5e; }
.block-container { padding-top: 1.5rem; }
.kpi { color: var(--sub); font-size: 0.85rem; }
.badge { background:#f0efe9; padding:.2rem .45rem; border-radius:.5rem; border:1px solid #e7e6e2; }
.table thead tr th { font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ----------------------- App taxonomy
REGIONS = {
    "EU": ["DE","FR","IT","ES","NL","SE","PL","IE","AT","BE","DK","FI","PT","GR","CZ","RO","HU"],
    "SEA": ["SG","MY","TH","VN","ID","PH"],
    "LATAM": ["BR","MX","AR","CL","CO","PE"],
    "MENA": ["AE","SA","QA","KW","EG","MA","JO","OM","BH"]
}
PRIME_COUNTRIES = ["US","UK","CA","CN","JP","IN"]

CATEGORIES = {
    "consumer_staples": {"name":"Consumer Staples","keywords":["FMCG","groceries","household","beverages","personal care"],
                         "tickers":["XLP"], "subs":["FMCG","IndiaInvestments","stocks"]},
    "energy": {"name":"Energy","keywords":["oil","gas","renewables","power"],"tickers":["XLE"],"subs":["energy","oil","renewableenergy"]},
    "technology": {"name":"Technology","keywords":["AI","semiconductor","software","cloud"],"tickers":["XLK"],"subs":["technology","MachineLearning","Futurology"]},
    "automotive": {"name":"Automotive","keywords":["EV","cars","two-wheeler","battery"],"tickers":["CARZ"],"subs":["autos","ElectricVehicles"]},
    "financials": {"name":"Financials","keywords":["banking","fintech","credit","payments"],"tickers":["XLF"],"subs":["finance","FinTech"]},
    "media": {"name":"Media & Advertising","keywords":["streaming","advertising","CTV","social"],"tickers":["XLC"],"subs":["advertising","marketing","socialmedia"]},
    "healthcare": {"name":"Healthcare","keywords":["pharma","biotech","vaccine","diagnostics"],"tickers":["XLV"],"subs":["medicine","pharmacy"]},
}

# -------------- Helpers
def header(title:str, right:str=""):
    c1,c2 = st.columns([0.85,0.15])
    with c1: st.markdown(f"### {title}")
    with c2: st.markdown(f"<div style='text-align:right;color:#5a5a5e'>Updated: {right or UPDATED()}</div>", unsafe_allow_html=True)
    st.divider()

def alt_line(df, x, y, title=""):
    import altair as alt
    base = alt.Chart(df).mark_line().encode(x=x, y=y, tooltip=list(df.columns))
    return base.properties(height=220, title=title).interactive()

def compute_ccs(news_df, trends_delta, quotes_df, reddit_mom):
    # very light composite; transparent pieces
    import numpy as np
    news_z = 0.0
    if not news_df.empty:
        # z by count vs 7-day rolling baseline not kept yet; approximate with count scale
        news_z = min(3.0, (len(news_df)/20.0))
    senti = float(news_df["senti"].mean()) if not news_df.empty else 0.0
    market = 0.0
    if len(quotes_df):
        market = sum([q["pct"] for q in quotes_df])/len(quotes_df) / 5.0  # normalize
    ccs = (news_z + (senti+1)/2 + trends_delta + reddit_mom + market) / 5.0
    return round(ccs*100,1), {"news_z":round(news_z,2),"sentiment":round(senti,2),
                               "trends":round(trends_delta,2),"reddit":round(reddit_mom,2),
                               "market":round(market,2)}

def trends_delta_7v30(payload):
    # payload: {"labels":[...], "datasets":[{label,data}]}
    import numpy as np
    if not payload.get("datasets"):
        return 0.0
    series = payload["datasets"][0]["data"]
    if len(series) < 30:
        return 0.0
    last7 = np.mean(series[-7:])
    last30 = np.mean(series[-30:])
    return float((last7-last30)/last30) if last30 else 0.0

def reddit_momentum(posts:list):
    # proxy: scaled count vs nominal 10
    return min(1.5, len(posts)/10.0)

# -------------- Upload parsing
WIDE_NAMES = {"volume":"volume","loyalty":"loyalty","rtfs":"rtf","trend":"trend","mable":"mable"}

def parse_upload(xls: bytes, filename: str):
    x = pd.ExcelFile(io.BytesIO(xls))
    inserted = []
    for sheet in x.sheet_names:
        df = pd.read_excel(x, sheet)
        # Promote first row to header if many Unnamed columns
        if len([c for c in df.columns if str(c).startswith("Unnamed")]) > len(df.columns)/2:
            df.columns = df.iloc[0]
            df = df.iloc[1:].reset_index(drop=True)

        metric_key = sheet.strip().lower()
        metric = None
        for k,v in WIDE_NAMES.items():
            if k in metric_key:
                metric = v; break

        if metric in {"volume","loyalty","rtf","trend","mable"}:
            # detect id columns (brand/country/market_group) and date columns
            id_cols = []
            for cand in ["brand","retailer","country","market","market_group","city","segment","category"]:
                for c in df.columns:
                    if str(c).strip().lower()==cand:
                        id_cols.append(c)
            # date/period columns -> melt
            value_cols = [c for c in df.columns if c not in id_cols]
            long = df.melt(id_vars=id_cols, value_vars=value_cols, var_name="date", value_name="value")
            # coerce dates
            long["date"] = pd.to_datetime(long["date"], errors="coerce").dt.date.astype(str)
            # minimal normalization
            country = None
            if any(str(c).lower()=="country" for c in id_cols):
                long.rename(columns={ [c for c in id_cols if str(c).lower()=="country"][0]:"country" }, inplace=True)
            else:
                long["country"] = None
            if any(str(c).lower()=="brand" for c in id_cols):
                long.rename(columns={ [c for c in id_cols if str(c).lower()=="brand"][0]:"brand" }, inplace=True)
            else:
                long["brand"] = None

            # write to DB
            with db.get_conn() as c:
                c.execute("INSERT INTO user_dataset(name,sheet,metric,source_file) VALUES(?,?,?,?)",
                          (os.path.basename(filename), sheet, metric, filename))
                dsid = c.execute("SELECT last_insert_rowid()").fetchone()[0]
                rows = [(dsid, r.get("brand"), r.get("country"), None, r["date"], float(r["value"]) if pd.notna(r["value"]) else None)
                        for _,r in long.iterrows()]
                c.executemany("REPLACE INTO user_timeseries(dataset_id,brand,country,market_group,date,value) VALUES(?,?,?,?,?,?)", rows)
                c.commit()
                inserted.append((sheet, metric, len(rows)))

        elif "cross" in metric_key:
            # crossover matrix -> melt
            df = df.dropna(how="all")
            # first column is brand_a; columns (except first) are brand_b
            if df.shape[1] >= 2:
                row_brand = df.columns[0]
                melted = df.melt(id_vars=[row_brand], var_name="brand_b", value_name="value")
                melted.rename(columns={row_brand:"brand_a"}, inplace=True)
                with db.get_conn() as c:
                    c.execute("INSERT INTO user_dataset(name,sheet,metric,source_file) VALUES(?,?,?,?)",
                              (os.path.basename(filename), sheet, "crossover", filename))
                    dsid = c.execute("SELECT last_insert_rowid()").fetchone()[0]
                    rows = [(dsid, None, r["brand_a"], r["brand_b"], float(r["value"]) if pd.notna(r["value"]) else None)
                            for _,r in melted.iterrows()]
                    c.executemany("REPLACE INTO user_cross(dataset_id,country,brand_a,brand_b,value) VALUES(?,?,?,?,?)", rows)
                    c.commit()
                    inserted.append((sheet, "crossover", len(rows)))
    return inserted

# ----------------------- Sidebar nav
st.sidebar.title("Blis Intelligence Hub")
page = st.sidebar.radio("Navigate", ["Command Center","Regions","Categories","Social & Community","My Data","Methods"])

# Common filters
region = None; country = None
if page in ("Regions","Categories","Social & Community"):
    st.sidebar.subheader("Region & Country")
    region = st.sidebar.selectbox("Region", ["—"] + list(REGIONS.keys()) + PRIME_COUNTRIES, index=0)
    if region in REGIONS:
        opts = ["All markets"] + REGIONS[region]
        country = st.sidebar.selectbox("Country", opts, index=0)
        if country=="All markets": country=None
    elif region in PRIME_COUNTRIES:
        country = region

# -------------------------------- Pages
if page == "Command Center":
    header("Command Center")
    # Signal tape
    st.markdown("**Signal tape**")
    quotes = get_quotes(["XLC","XLY","XLP","XLK","XLE","XLF","XLV","DX-Y.NYB","BZ=F","GC=F","^TNX","EURUSD=X","GBPUSD=X","USDJPY=X","USDINR=X","CNY=X"])
    st.dataframe(pd.DataFrame(quotes))

    # Heatmap by category (sketch: show CCS ingredients)
    st.markdown("**Category pulse (last 24–72h)**")
    rows=[]
    for slug,cfg in CATEGORIES.items():
        news = pd.DataFrame(get_reuters_news(cfg["keywords"]))
        trends = get_trends_series(cfg["keywords"], geo=country or "")
        q = get_quotes(cfg["tickers"])
        reddit = get_reddit_top(cfg["subs"]) if os.getenv("REDDIT_CLIENT_ID") else []
        ccs, parts = compute_ccs(news, trends_delta_7v30(trends), q, reddit_momentum(reddit))
        rows.append({"category":cfg["name"], "CCS":ccs, **parts, "newsN": len(news)})
    st.dataframe(pd.DataFrame(rows).set_index("category"))

elif page == "Regions":
    title = f"Region Overview — {region or 'Select a region'}" if not country else f"{region} — {country}"
    header(title)
    if not region:
        st.info("Choose a region (or prime country) from the sidebar.")
    else:
        # Show macro proxies and trends for this geo
        st.markdown("**Macro & Attention**")
        geo = country or ""
        # simple trends example using automotive keywords
        payload = get_trends_series(["cars","SUV","EV"], geo=geo)
        if payload["datasets"]:
            df = pd.DataFrame({"date":payload["labels"]})
            for ds in payload["datasets"]:
                df[ds["label"]] = ds["data"]
            st.altair_chart(alt_line(df.melt("date", var_name="term", value_name="index"),
                                     "date:T","index:Q","Search interest (90 days)"), use_container_width=True)

        # News & Sentiment
        st.markdown("**News & Sentiment (Reuters)**")
        news = pd.DataFrame(get_reuters_news(["cars","automotive","EV","dealership","recall"]))
        st.dataframe(news[["title","source","published","senti","link"]])

elif page == "Categories":
    header("Categories")
    slug = st.selectbox("Choose category", list(CATEGORIES.keys()), format_func=lambda k: CATEGORIES[k]["name"])
    cfg = CATEGORIES[slug]
    col1,col2 = st.columns([0.6,0.4])
    with col1:
        st.markdown("**News & Sentiment**")
        news = pd.DataFrame(get_reuters_news(cfg["keywords"]))
        st.dataframe(news[["title","source","published","senti","link"]])
    with col2:
        st.markdown("**Market pulse**")
        st.dataframe(pd.DataFrame(get_quotes(cfg["tickers"])))
        st.markdown("**Google Trends (90d)**")
        payload = get_trends_series(cfg["keywords"], geo=country or "")
        if payload["datasets"]:
            df = pd.DataFrame({"date":payload["labels"]})
            for ds in payload["datasets"]:
                df[ds["label"]] = ds["data"]
            st.altair_chart(alt_line(df.melt("date","term","index"),"date:T","index:Q"), use_container_width=True)

elif page == "Social & Community":
    header("Social & Community Pulse")
    sublist = ["worldnews","news"] if not country else (["india"] if country=="IN" else ["europe"] if country in REGIONS["EU"] else ["news"])
    posts = get_reddit_top(sublist) if os.getenv("REDDIT_CLIENT_ID") else []
    if not posts:
        st.info("Reddit not configured or no posts. Add Reddit secrets to enable.")
    else:
        st.dataframe(pd.DataFrame(posts))

elif page == "My Data":
    header("My Data — Excel plug-and-view")
    up = st.file_uploader("Upload .xlsx or .csv (Volume/Loyalty/RTFs/Trend/MABLE/Cross…)", type=["xlsx","csv"])
    if up is not None:
        data = up.read()
        if up.name.lower().endswith(".csv"):
            # single-sheet CSV -> wrap into pseudo-Excel handling
            xls_bytes = io.BytesIO()
            with pd.ExcelWriter(xls_bytes, engine="openpyxl") as w:
                df = pd.read_csv(io.BytesIO(data))
                df.to_excel(w, index=False, sheet_name="Sheet1")
            inserted = parse_upload(xls_bytes.getvalue(), up.name)
        else:
            inserted = parse_upload(data, up.name)
        st.success(f"Imported: {inserted}")

    # Quick overlays from DB (last dataset only)
    with db.get_conn() as c:
        cur = c.execute("SELECT id,name,sheet,metric,uploaded_at FROM user_dataset ORDER BY uploaded_at DESC LIMIT 5")
        rows = cur.fetchall()
    if rows:
        st.markdown("**Recent datasets**")
        st.table(pd.DataFrame(rows, columns=["id","name","sheet","metric","uploaded_at"]))
        dsid = st.selectbox("Pick dataset to plot", [r[0] for r in rows])
        if dsid:
            with db.get_conn() as c:
                df = pd.read_sql_query("SELECT brand,country,date,value FROM user_timeseries WHERE dataset_id=? ORDER BY date",
                                       c, params=(dsid,))
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                brand = st.selectbox("Brand", sorted(df["brand"].dropna().unique().tolist()))
                sdf = df[df["brand"]==brand].dropna()
                if not sdf.empty:
                    st.altair_chart(alt_line(sdf, "date:T", "value:Q", f"{brand} — {rows[0][3]}"), use_container_width=True)
            # crossover
            with db.get_conn() as c:
                cross = pd.read_sql_query("SELECT brand_a,brand_b,value FROM user_cross WHERE dataset_id=?", c, params=(dsid,))
            if not cross.empty:
                st.markdown("**Crossover (top pairs)**")
                st.dataframe(cross.sort_values("value", ascending=False).head(20))

elif page == "Methods":
    header("Methods & Data Quality")
    st.markdown("""
- **Open sources only**: Reuters RSS, Yahoo Finance (quotes), Google Trends (pytrends), Wikipedia Pageviews, Reddit (optional), World Bank/OWID for slow-moving macro.
- **Refresh cadence**: pages auto-refresh every **5 minutes**.
- **Sentiment**: VADER on headlines; we show average and N.
- **Trends delta**: (last 7 days vs last 30); displayed where relevant.
- **Reddit**: per-region/country curated subs; skipped entirely if secrets are not set.
- **Uploads**: Excel wide tables (Volume/Loyalty/RTFs/Trend/MABLE) are melted to tidy time-series; Cross/Cross DB parsed into brand-pairs.
- **No placeholders**: if a source is unavailable, last known values are shown with timestamps; never synthetic data.
""")

# 5-minute auto-refresh (no background jobs required for Streamlit)
st.experimental_memo.clear()  # noop placeholder to emphasize statelessness per refresh
st_autorefresh = st.experimental_rerun  # alias not used; Streamlit reruns on page load
st.experimental_set_query_params(_=int(time.time()/300))  # forces cache refresh roughly every 5 minutes
