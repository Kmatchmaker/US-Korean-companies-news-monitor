import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 설정 (한국어/영어 매핑)
STATES = {
    "Georgia": "조지아",
    "Alabama": "앨라배마",
    "Tennessee": "테네시",
    "South Carolina": "사우스캐롤라이나",
    "Florida": "플로리다"
}

st.set_page_config(page_title="2026 韓 기업 미국 진출 실시간 보드", layout="wide")
st.title("🏭 2026년 2월 미 동남부 한국 기업 진출 모니터링")

# --- 최신 뉴스 추출 및 날짜 검증 함수 ---
def fetch_verified_latest(query, lang, gl):
    # '2026년 2월 1일 이후' + '날짜순 정렬' 강제 쿼리
    final_query = f"{query} after:2026-02-01"
    encoded_query = urllib.parse.quote(final_query)
    
    # 정렬 순서를 명확히 하기 위해 구글 RSS URL 구조 사용
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    
    feed = feedparser.parse(url)
    verified = []
    
    for entry in feed.entries:
        # 1. 발행 연도가 2026년인지 2중 체크 (과거 뉴스 원천 배제)
        if entry.get('published_parsed') and entry.published_parsed.tm_year == 2026:
            verified.append(entry)
            
    # 최신 날짜순으로 재정렬
    return sorted(verified, key=lambda x: x.get('published_parsed'), reverse=True)

# --- 화면 구성: 공신력 있는 미국 vs 한국 보드 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 보드", "🇰🇷 한국 언론 및 동포 보드"])

# 보드 1: 미국 현지 (주정부/지역경제지/메이저)
with tab_us:
    st.markdown("### 🏛️ 주 정부 공식 발표 및 미국 경제 매체")
    for en_name, ko_name in STATES.items():
        with st.expander(f"📍 {en_name} ({ko_name}) - 최신 현지 뉴스 보기", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1: # 주 정부 공식 (site:.gov)
                st.caption("🏛️ 주 정부 발표 (.gov)")
                items = fetch_verified_latest(f'site:.gov "{en_name}" "South Korea" (investment OR factory)', "en-US", "US")
                for e in items[:3]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.published[:16]}]")
            
            with col2: # 지역 주요 경제지
                st.caption("📰 지역 경제지 (Business Journal 등)")
                items = fetch_verified_latest(f'"{en_name}" "South Korea" investment (journal OR chronicle)', "en-US", "US")
                for e in items[:3]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.source.title} | {e.published[:16]}]")

            with col3: # 메이저 언론
                st.caption("🌐 메이저 (Reuters/Bloomberg 등)")
                items = fetch_verified_latest(f'"{en_name}" "South Korea" investment (Bloomberg OR Reuters)', "en-US", "US")
                for e in items[:3]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.source.title} | {e.published[:16]}]")

# 보드 2: 한국 언론 (주요 경제지/미 현지 동포지)
with tab_kr:
    st.markdown("### 🗞️ 한국 언론사 및 현지 동포 소식")
    for en_name, ko_name in STATES.items():
        with st.expander(f"📍 {ko_name} ({en_name}) - 최신 한국 보도 보기", expanded=True):
            col_press, col_diaspora = st.columns(2)
            
            with col_press:
                st.caption("🗞️ 한국 주요 언론 (연합/경제지 등)")
                items = fetch_verified_latest(f'{ko_name} "미국" (진출 OR 투자 OR 공장)', "ko", "KR")
                for e in items[:5]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.source.title} | {e.published[:16]}]")
                    
            with col_diaspora:
                st.caption("🇺🇸 미 현지 동포 신문 (한인 뉴스)")
                items = fetch_verified_latest(f'{ko_name} (투자 OR 진출 OR 공장)', "ko", "US")
                for e in items[:5]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.source.title} | {e.published[:16]}]")
