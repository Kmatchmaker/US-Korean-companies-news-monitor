import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 설정
STATES_MAP = {
    "Georgia": "조지아",
    "Alabama": "앨라배마",
    "Tennessee": "테네시",
    "South Carolina": "사우스캐롤라이나",
    "Florida": "플로리다"
}

st.set_page_config(page_title="2026 미 동남부 韓 기업 진출 모니터", layout="wide")
st.title("🚜 2026년 미 동남부 한국 기업 신규 진출·투자 전수 감시")
st.caption("2026년 2월 1일 이후 발표된 모든 한국 기업의 미국 현지 투자/공장 설립 소식을 수집합니다.")

# --- 전방위 수집 및 날짜/내용 정밀 검증 함수 ---
def fetch_all_korean_investments(query, lang, gl):
    # 날짜 필터: 2026년 2월 1일 이후 (과거 뉴스 차단)
    date_filter = "after:2026-02-01"
    # [핵심 필터] '한국' 관련 키워드와 '비즈니스 확장' 키워드 전방위 결합
    # 특정 기업명이 아닌 'Korean company', 'South Korea investment' 등으로 포괄 검색
    full_query = f'({query}) ("South Korea" OR Korean OR "한국 기업" OR "진출") (investment OR factory OR plant OR "announces") {date_filter}'
    
    encoded_query = urllib.parse.quote(full_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    
    feed = feedparser.parse(url)
    verified_results = []
    
    for entry in feed.entries:
        # [2중 검증] 2026년 뉴스만 통과
        if entry.get('published_parsed') and entry.published_parsed.tm_year == 2026:
            verified_results.append(entry)
                
    # 최신 날짜순 정렬
    return sorted(verified_results, key=lambda x: x.get('published_parsed'), reverse=True)

# --- 보드 구성: 1. 미국 공신력 소스 / 2. 한국/동포 공신력 소스 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 보드", "🇰🇷 한국 언론 및 현지 동포 보드"])

with tab_us:
    st.info("💡 주 정부(Governor's Office) 발표 및 미국 경제 전문지 리포트")
    for en_name, ko_name in STATES_MAP.items():
        with st.expander(f"📍 {en_name} ({ko_name}) - 현지 발 소식", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1: # 1. 주 정부 및 경제국 공식 발표
                st.caption("🏛️ 주 정부/경제국 (.gov)")
                # 'site:.gov'를 통해 조지아 주지사 발표 같은 1순위 오피셜 뉴스 포착
                q = f'site:.gov "{en_name}" "South Korea"'
                items = fetch_all_korean_investments(q, "en-US", "US")
                for e in items[:5]:
                    with st.container(border=True):
                        st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                        st.caption(f"📅 {e.published[:16]}")
            
            with col2: # 2. 주별 로컬 경제지
                st.caption("📰 지역 경제 매체 (Business Journal 등)")
                q = f'"{en_name}" "South Korea" investment'
                items = fetch_all_korean_investments(q, "en-US", "US")
                for e in items[:5]:
                    with st.container(border=True):
                        st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                        st.caption(f"📅 {e.published[:16]} | {e.source.title}")

            with col3: # 3. 메이저/글로벌 경제지
                st.caption("🌐 메이저 언론 (Reuters/Bloomberg)")
                q = f'"{en_name}" "South Korea" (investment OR factory)'
                items = fetch_all_korean_investments(q, "en-US", "US")
                for e in items[:3]:
                    with st.container(border=True):
                        st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                        st.caption(f"📅 {e.published[:16]} | {e.source.title}")

with tab_kr:
    st.success("💡 한국 내 주요 언론 및 미국 현지 한인 동포 신문 보도")
    for en_name, ko_name in STATES_MAP.items():
        with st.expander(f"📍 {ko_name} ({en_name}) - 한국어 보도", expanded=True):
            col_press, col_diaspora = st.columns(2)
            
            with col_press: # 1. 한국 주요 언론 (네이버 뉴스 등)
                st.caption("🗞️ 한국 주요 언론사 (경제지/일간지)")
                q = f'{ko_name} "미국 진출" OR "투자" OR "공장"'
                items = fetch_all_korean_investments(q, "ko", "KR")
                for e in items[:7]:
                    with st.container(border=True):
                        st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                        st.caption(f"📅 {e.published[:16]} | {e.source.title}")
                    
            with col_diaspora: # 2. 미 현지 동포 신문 (애틀랜타 중앙일보 등)
                st.caption("🇺🇸 미 현지 동포 신문 (한인 뉴스)")
                # 미국 내 한국어 서비스(gl=US)를 집중 검색
                q = f'{ko_name} "투자" OR "공장" OR "진출"'
                items = fetch_all_korean_investments(q, "ko", "US")
                for e in items[:7]:
                    with st.container(border=True):
                        st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                        st.caption(f"📅 {e.published[:16]} | {e.source.title}")
