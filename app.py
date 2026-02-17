import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 설정: 5개 주
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]

st.set_page_config(page_title="2026 미 동남부 기업 투자 모니터", layout="wide")
st.title("📊 미 동남부 한국 기업 진출 이원화 모니터링")

# --- 뉴스 수집 함수 ---
def fetch_news(query, lang="en-US", gl="US"):
    encoded_query = urllib.parse.quote(f"{query} when:30d")
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    feed = feedparser.parse(url)
    # 최신순 정렬
    entries = sorted(feed.entries, key=lambda x: x.get('published_parsed', (0,0,0,0,0,0,0,0,0)), reverse=True)
    return entries

# --- 화면 레이아웃 (Tabs) ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 보도 (Gov/Local News)", "🇰🇷 한국 언론 보도 (Korean Media)"])

# --- TAB 1: 미국 현지 보도 ---
with tab_us:
    st.info("💡 주 정부 발표자료 및 미국 현지 언론의 오피셜 리포트입니다.")
    cols = st.columns(len(STATES))
    for i, state in enumerate(STATES):
        with cols[i]:
            st.subheader(f"📍 {state}")
            # 주 정부 및 투자 관련 영어 키워드 검색
            query = f'site:.gov OR site:.org "{state}" "South Korea" investment factory'
            news_items = fetch_news(query)
            
            if not news_items: st.write("최근 소식이 없습니다.")
            for entry in news_items[:6]:
                with st.container(border=True):
                    st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")

# --- TAB 2: 한국 언론 보도 ---
with tab_kr:
    st.success("💡 한국 내 주요 언론사가 보도하는 미국 진출 기업 소식입니다.")
    cols = st.columns(len(STATES))
    for i, state in enumerate(STATES):
        with cols[i]:
            st.subheader(f"📍 {state}")
            # 한국어 키워드 검색
            query = f'{state} "미국 진출" OR "투자" OR "공장"'
            news_items = fetch_news(query, lang="ko", gl="KR")
            
            if not news_items: st.write("최근 소식이 없습니다.")
            for entry in news_items[:6]:
                with st.container(border=True):
                    st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
