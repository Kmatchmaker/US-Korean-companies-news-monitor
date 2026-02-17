import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 5개 주 설정
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]

st.set_page_config(page_title="2026 미 동남부 진출 기업 모니터", layout="wide")
st.title("🏛️ 미 동남부 주 정부 공식 보도 및 최신 뉴스")

def fetch_news(state):
    # [전략 변경] 한국어/영어 모두 검색하되, 특정 주 정부 사이트와 'South Korea'를 결합
    # site:gov 키워드로 공식 보도자료 우선 순위를 높임
    query = f"{state} (South Korea OR Korean) (investment OR factory OR plant) when:30d"
    encoded_query = urllib.parse.quote(query)
    
    # 글로벌(영어) 검색 결과로 확장 (영문 보도자료가 더 빠르기 때문)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
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
                # 30일 내 뉴스가 없으면 기간 제한을 풀어 6개월치 시도
                alt_query = urllib.parse.quote(f"{state} South Korea investment")
                alt_url = f"https://news.google.com/rss/search?q={alt_query}&hl=en-US&gl=US&ceid=US:en"
                news_items = feedparser.parse(alt_url).entries[:5]
                st.info("최근 30일 내 소식이 없어 이전 소식을 표시합니다.")

            for entry in news_items:
                with st.expander(f"{entry.title[:45]}..."):
                    st.write(f"**{entry.title}**")
                    st.caption(f"출처: {entry.source.title} | 날짜: {entry.published}")
                    st.markdown(f"[기사 원문 보기]({entry.link})")
        except Exception as e:
            st.error("뉴스 데이터를 불러올 수 없습니다.")

st.sidebar.markdown("### 🔗 주요 주 정부 뉴스룸 바로가기")
st.sidebar.page_link("https://www.georgia.org/newsroom", label="Georgia Newsroom", icon="🍑")
st.sidebar.page_link("https://www.madeinalabama.com/news/", label="Alabama News", icon="🐘")
st.sidebar.page_link("https://tnecd.com/news/", label="Tennessee News", icon="🎸")
