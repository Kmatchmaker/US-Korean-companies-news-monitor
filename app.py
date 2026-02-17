import streamlit as st
import feedparser
from datetime import datetime

# 설정: 5개 주 및 키워드
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]
TARGET_KEYWORDS = ["South Korea", "Korean", "Investment", "Factory", "Plant", "Jobs"]

st.set_page_config(page_title="미국 동남부 한국기업 뉴스 센터", layout="wide")
st.title("🇰🇷 미국 동남부 진출 한국 기업 실시간 모니터링")
st.sidebar.info("2026년 신규 진입 및 기존 50개 기업 뉴스를 매일 업데이트합니다.")

def fetch_news(state):
    # 기업명을 몰라도 '한국+투자' 키워드로 신규 기업을 낚아채는 쿼리
    query = f"{state} South Korea investment factory"
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    return feed.entries[:8]

# 대시보드 레이아웃
cols = st.columns(len(STATES))

for i, state in enumerate(STATES):
    with cols[i]:
        st.header(f"📍 {state}")
        news_items = fetch_news(state)
        if not news_items:
            st.write("새로운 소식이 없습니다.")
        for entry in news_items:
            with st.container():
                st.markdown(f"**[{entry.source.title}]**")
                st.write(f"[{entry.title}]({entry.link})")
                st.caption(f"발행일: {entry.published[:16]}")
                st.divider()

st.sidebar.warning("💡 팁: 현지 주 정부(Georgia.org 등)의 공식 발표가 가장 빠릅니다.")
