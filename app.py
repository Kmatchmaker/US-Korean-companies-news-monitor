import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 설정: 주별 한글/영어 매핑
STATES_INFO = {
    "Georgia": "조지아",
    "Alabama": "앨라배마",
    "Tennessee": "테네시",
    "South Carolina": "사우스캐롤라이나",
    "Florida": "플로리다"
}

st.set_page_config(page_title="2026 韓 기업 미국 진출 실시간 보드", layout="wide")
st.title("🏭 2026년 2월 미 동남부 진출 기업 정밀 모니터링")
st.caption(f"기준일: {datetime.now().strftime('%Y-%m-%d')} | 과거 기사 필터링 활성화")

# --- 뉴스 수집 함수 (날짜 연산자 강제 주입) ---
def fetch_precise_news(query, lang, gl):
    # 'after:2026-02-01'을 붙여 2025년 뉴스를 물리적으로 차단합니다.
    final_query = f"{query} after:2026-02-01"
    encoded_query = urllib.parse.quote(final_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    feed = feedparser.parse(url)
    # 완벽한 날짜순 정렬
    return sorted(feed.entries, key=lambda x: x.get('published_parsed', (0,0,0,0,0,0,0,0,0)), reverse=True)

# --- 보드 설계 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 (Gov & Local Media)", "🇰🇷 한국 주요 언론 (Korean Press)"])

# 보드 A: 미국 현지 뉴스
with tab_us:
    st.markdown("### 🏛️ 주 정부 및 현지 경제 매체 리포트")
    cols = st.columns(len(STATES_INFO))
    for i, (en_name, ko_name) in enumerate(STATES_INFO.items()):
        with cols[i]:
            st.info(f"📍 {en_name}")
            # 미국 내 한국 기업(South Korea/Korean)의 진출(Investment/Plant/Jobs) 소식
            q_us = f'"{en_name}" ("South Korea" OR Korean) (investment OR factory OR plant)'
            items = fetch_precise_news(q_us, "en-US", "US")
            
            if not items:
                st.write("2월 신규 소식 없음")
            for entry in items[:7]:
                with st.container(border=True):
                    st.caption(f"📅 {entry.published[:16]}")
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                    st.caption(f"Source: {entry.source.title}")

# 보드 B: 한국 언론 뉴스
with tab_kr:
    st.markdown("### 🗞️ 한국 언론사의 미국 현지 보도")
    cols = st.columns(len(STATES_INFO))
    for i, (en_name, ko_name) in enumerate(STATES_INFO.items()):
        with cols[i]:
            st.success(f"📍 {ko_name}")
            # 한글 지명 + 미국 진출 관련 키워드
            q_kr = f'{ko_name} "미국" (진출 OR 투자 OR 공장 OR 채용)'
            items = fetch_precise_news(q_kr, "ko", "KR")
            
            if not items:
                st.write("2월 신규 보도 없음")
            for entry in items[:7]:
                with st.container(border=True):
                    st.caption(f"📅 {entry.published[:16]}")
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                    st.caption(f"출처: {entry.source.title}")
