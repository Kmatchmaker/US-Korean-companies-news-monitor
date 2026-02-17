import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 설정: 주별 매핑
STATES_INFO = {
    "Georgia": "조지아",
    "Alabama": "앨라배마",
    "Tennessee": "테네시",
    "South Carolina": "사우스캐롤라이나",
    "Florida": "플로리다"
}

st.set_page_config(page_title="2026 미 동남부 기업 모니터", layout="wide")
st.title("🏛️ 2026년 2월 미 동남부 진출 기업 정밀 모니터링")
st.caption(f"검색 기준일: 2026-02-01 이후 기사만 수집 (2025년 이전 기사 강제 차단)")

# --- 뉴스 수집 및 엄격한 날짜 필터 함수 ---
def fetch_verified_news(query, lang, gl):
    # 쿼리에 날짜를 명시하여 구글 검색 단계에서 과거 기사 차단
    precise_query = f"{query} after:2026-02-01"
    encoded_query = urllib.parse.quote(precise_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    
    feed = feedparser.parse(url)
    verified_entries = []
    
    for entry in feed.entries:
        # [2중 검증] 기사 발행일의 연도가 2026년인지 다시 확인
        if entry.get('published_parsed') and entry.published_parsed.tm_year == 2026:
            verified_entries.append(entry)
            
    # 최신 날짜순으로 정렬
    return sorted(verified_entries, key=lambda x: x.get('published_parsed'), reverse=True)

# --- 화면 구성 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 뉴스 (Gov/Local/Major)", "🇰🇷 한국 및 동포 뉴스 (Press/Diaspora)"])

# 보드 A: 미국 현지 뉴스 (주정부/지역지/메이저)
with tab_us:
    for en_name, ko_name in STATES_INFO.items():
        st.markdown(f"### 📍 {en_name} ({ko_name})")
        gov_col, local_col, major_col = st.columns(3)
        
        with gov_col:
            st.caption("🏛️ 1. 주 정부 (.gov)")
            items = fetch_verified_news(f'site:.gov "{en_name}" "South Korea" investment', "en-US", "US")
            for entry in items[:3]:
                with st.container(border=True):
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                    st.caption(f"📅 {entry.published[:16]}")
        
        with local_col:
            st.caption("📰 2. 주별 지역 신문")
            items = fetch_verified_news(f'"{en_name}" "South Korea" investment (journal OR gazette OR times)', "en-US", "US")
            for entry in items[:3]:
                with st.container(border=True):
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                    st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")

        with major_col:
            st.caption("🌐 3. 메이저 뉴스")
            items = fetch_verified_news(f'"{en_name}" "South Korea" investment (Bloomberg OR Reuters OR AP)', "en-US", "US")
            for entry in items[:3]:
                with st.container(border=True):
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                    st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")

# 보드 B: 한국 및 동포 뉴스 (국내 주요 언론/동포 신문)
with tab_kr:
    for en_name, ko_name in STATES_INFO.items():
        st.markdown(f"### 📍 {ko_name} ({en_name}) 보도")
        main_press_col, diaspora_col = st.columns(2)
        
        with main_press_col:
            st.caption("🗞️ 1. 한국 주요 언론사 (경제지/일간지)")
            # 국내 주요 언론사 타겟팅 (정확도를 위해 주 이름을 한국어로 검색)
            q_main = f'{ko_name} "미국" (투자 OR 진출 OR 공장)'
            items = fetch_verified_news(q_main, "ko", "KR")
            for entry in items[:5]:
                with st.container(border=True):
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                    st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")

        with diaspora_col:
            st.caption("🇺🇸 2. 미 현지 동포 신문 (한인 뉴스)")
            # 미 현지 동포 신문(중앙일보USA, 한국일보USA, 애틀랜타K 등) 타겟팅
            # 미국 내 한국어 검색(gl=US)을 통해 동포 뉴스를 수집합니다.
            q_dia = f'{ko_name} "투자" OR "공장" OR "진출"'
            items = fetch_verified_news(q_dia, "ko", "US")
            for entry in items[:5]:
                with st.container(border=True):
                    st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                    st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
