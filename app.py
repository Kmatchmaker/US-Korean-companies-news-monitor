import streamlit as st
import feedparser
import urllib.parse

st.set_page_config(page_title="2026 韓 기업 미국 진출 보드", layout="wide")
st.title("🚜 2026년 2월 미 동남부 한국 기업 진출·투자 정밀 보드")

# 핵심 타겟 주
STATES = {"Georgia": "조지아", "Alabama": "앨라배마", "Tennessee": "테네시"}

def fetch_top_news(query, gl):
    # 날짜 필터와 핵심 키워드(투자, 수주, 증설) 결합
    full_query = f'{query} (investment OR expansion OR contract) after:2026-02-01'
    encoded_query = urllib.parse.quote(full_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl={gl}&ceid={gl}:ko"
    
    feed = feedparser.parse(url)
    return [e for e in feed.entries if "2026" in e.published][:5]

tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 뉴스", "🇰🇷 한국 언론 & 공시"])

with tab_us:
    for en, ko in STATES.items():
        st.subheader(f"📍 {en} ({ko})")
        # 주정부 사이트(.gov) 직접 검색
        gov_items = fetch_top_news(f'site:.gov "{en}" "South Korea"', "US")
        for e in gov_items:
            st.success(f"**[GOV] [{e.title}]({e.link})**")
            st.caption(f"📅 {e.published}")

with tab_kr:
    for en, ko in STATES.items():
        st.subheader(f"📍 {ko} ({en})")
        # 한국 주요 경제지 검색
        kr_items = fetch_top_news(f'{ko} ("투자" OR "출자" OR "수주" OR "증설")', "KR")
        for e in kr_items:
            st.info(f"**[{e.title}]({e.link})**")
            st.caption(f"📅 {e.published} | {e.source.title}")
