import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 및 핵심 기업 리스트 (검색 정확도 향상용)
STATES_MAP = {
    "Georgia": "조지아",
    "Alabama": "앨라배마",
    "Tennessee": "테네시",
    "South Carolina": "사우스캐롤라이나",
    "Florida": "플로리다"
}

# 2026년 2월 뉴스에 자주 등장하는 핵심 타겟 기업
TARGET_CORPS = ["Dongwon", "동원금속", "Duckshin", "덕신EPC", "Hyundai", "HMGMA", "LG Energy", "SK On"]

st.set_page_config(page_title="2026 미 동남부 기업 모니터", layout="wide")
st.title("🏭 2026년 2월 한국 기업 진출·투자 정밀 보드")

# --- 정밀 수집 및 날짜/내용 검증 함수 ---
def fetch_precise_investment_news(query, lang, gl):
    # 날짜 필터: 2026년 2월 1일 이후
    date_filter = "after:2026-02-01"
    # 투자 관련 핵심 키워드 강제 결합
    precise_query = f'({query}) (investment OR factory OR "new plant" OR "투자" OR "공장") {date_filter}'
    
    encoded_query = urllib.parse.quote(precise_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    
    feed = feedparser.parse(url)
    results = []
    
    for entry in feed.entries:
        # [검증 1] 2026년 발행 여부
        if entry.get('published_parsed') and entry.published_parsed.tm_year == 2026:
            # [검증 2] 사건/사고(노이즈) 제목은 과감히 제외하고 '기업명'이나 '투자' 위주 필터
            title = entry.title.lower()
            if any(k.lower() in title for k in TARGET_CORPS + ["korea", "invest"]):
                results.append(entry)
                
    return sorted(results, key=lambda x: x.get('published_parsed'), reverse=True)

# --- 보드 구성: 미국 오피셜 vs 한국/동포 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 (US Media & Gov)", "🇰🇷 한국 및 동포 뉴스 (KR Press & Diaspora)"])

with tab_us:
    for en_name, ko_name in STATES_MAP.items():
        st.markdown(f"### 📍 {en_name} ({ko_name})")
        col1, col2, col3 = st.columns(3)
        
        with col1: # 주 정부/경제국
            st.caption("🏛️ 주 정부/경제개발국 (.gov)")
            # 동원오토 같은 주지사 발표를 잡기 위한 전용 쿼리
            q = f'site:.gov "{en_name}" "South Korea" investment'
            items = fetch_precise_investment_news(q, "en-US", "US")
            for e in items[:5]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]}")
        
        with col2: # 지역 경제지
            st.caption("📰 지역 경제지 (Business Journal 등)")
            q = f'"{en_name}" "South Korea" investment'
            items = fetch_precise_investment_news(q, "en-US", "US")
            for e in items[:5]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")

        with col3: # 메이저/글로벌
            st.caption("🌐 메이저 뉴스 (Reuters/Bloomberg)")
            q = f'"{en_name}" "South Korea" investment'
            items = fetch_precise_investment_news(q, "en-US", "US")
            for e in items[:3]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")

with tab_kr:
    for en_name, ko_name in STATES_MAP.items():
        st.markdown(f"### 📍 {ko_name} ({en_name})")
        col_kr, col_dia = st.columns(2)
        
        with col_kr:
            st.caption("🗞️ 한국 주요 언론 (경제지/일간지)")
            q = f'{ko_name} "미국" (투자 OR 공장 OR 진출)'
            items = fetch_precise_investment_news(q, "ko", "KR")
            for e in items[:6]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")
                    
        with col_dia:
            st.caption("🇺🇸 미 현지 동포 신문 (한인 뉴스)")
            q = f'{ko_name} (투자 OR 공장 OR 진출)'
            items = fetch_precise_investment_news(q, "ko", "US")
            for e in items[:6]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")
