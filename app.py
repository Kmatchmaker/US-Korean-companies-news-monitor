import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 설정: 5개 주
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]

st.set_page_config(page_title="2026 미 동남부 韓 기업 모니터", layout="wide")
st.title("🇰🇷 미국 동남부 진출 한국 기업 실시간 뉴스 (2026)")

def fetch_news(state):
    # 최신 뉴스를 위해 2026년 키워드와 한국어 키워드를 혼합
    # 'when:7d'를 붙이면 최근 7일 이내 뉴스만 가져옵니다.
    query = f"{state} (한국 기업 OR Korean company) investment 2026 when:30d"
    encoded_query = urllib.parse.quote(query)
    
    # 구글 뉴스 RSS (최신순 정렬 보정)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    feed = feedparser.parse(url)
    return feed.entries[:10]

# 대시보드 구성
cols = st.columns(len(STATES))

for i, state in enumerate(STATES):
    with cols[i]:
        st.subheader(f"📍 {state}")
        try:
            news_items = fetch_news(state)
            if not news_items:
                st.write("최근 30일 내 뉴스가 없습니다.")
            for entry in news_items:
                with st.expander(f"{entry.title[:40]}..."):
                    st.write(f"**{entry.title}**")
                    st.caption(f"출처: {entry.source.title} | 날짜: {entry.published}")
                    st.markdown(f"[기사 읽기]({entry.link})")
        except Exception as e:
            st.error("데이터 로드 실패")

st.sidebar.markdown("### 🔔 2026년 2월 주요 헤드라인")
st.sidebar.write("- **동원금속**: 조지아주 3,000만 달러 신규 투자 발표 (2/5)")
st.sidebar.write("- **현대차-LG**: 조지아 합작공장 인력 수급 및 가동 준비 중")
st.sidebar.write("- **LG엔솔**: 애리조나 및 동남부 LFP 배터리 라인 2026년 가동 예정")
