import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 설정: 5개 주
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]

st.set_page_config(page_title="2026 미 동남부 기업 투자 모니터", layout="wide")
st.title("📊 미 동남부 한국 기업 진출 실시간 보드 (2026)")

# --- 뉴스 수집 함수 ---
def fetch_news(query, lang="en-US", gl="US"):
    # 2026년 최신성 보장을 위해 when:30d 필터 유지
    encoded_query = urllib.parse.quote(f"{query} when:30d")
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    feed = feedparser.parse(url)
    # 발행 시간순 정렬
    entries = sorted(feed.entries, key=lambda x: x.get('published_parsed', (0,0,0,0,0,0,0,0,0)), reverse=True)
    return entries

# --- 화면 레이아웃 (Tabs) ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 뉴스 (US Media & Gov)", "🇰🇷 한국 언론 보도 (Korean Media)"])

# --- TAB 1: 미국 현지 보도 (필터 수정 완료) ---
with tab_us:
    st.info("💡 미국 현지 매체가 보도한 '한국 기업'의 진출 및 투자 뉴스입니다.")
    cols = st.columns(len(STATES))
    for i, state in enumerate(STATES):
        with cols[i]:
            st.header(f"📍 {state}")
            # [수정] 주 이름과 'South Korea'를 필수 결합하고 비즈니스 키워드 추가
            # 단순 주 정부 사이트 검색을 넘어 현지 경제지도 포함하도록 확장
            query = f'"{state}" "South Korea" (investment OR factory OR plant OR jobs)'
            news_items = fetch_news(query, lang="en-US", gl="US")
            
            if not news_items:
                st.write("해당 주의 신규 기업 뉴스가 없습니다.")
            
            for entry in news_items[:8]:
                with st.container(border=True):
                    # 제목에서 주 이름이 있는지 재검증하여 데이터 섞임 방지
                    if state.lower() in entry.title.lower() or state.lower().replace(" ", "") in entry.link.lower():
                        st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
                        st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                        if 'summary' in entry:
                            st.write(f"📝 {entry.summary.split('<')[0][:120]}...")

# --- TAB 2: 한국 언론 보도 ---
with tab_kr:
    st.success("💡 한국 내 언론사가 보도한 미국 현지 진출 소식입니다.")
    cols = st.columns(len(STATES))
    for i, state in enumerate(STATES):
        with cols[i]:
            st.header(f"📍 {state}")
            # 한국어 키워드 정밀화
            query = f'"{state}" "한국 기업" (투자 OR 진출 OR 공장 OR 채용)'
            news_items = fetch_news(query, lang="ko", gl="KR")
            
            if not news_items:
                st.write("관련 보도가 없습니다.")
            
            for entry in news_items[:8]:
                with st.container(border=True):
                    st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                    if 'summary' in entry:
                        st.write(f"📝 {entry.summary.split('<')[0][:120]}...")
