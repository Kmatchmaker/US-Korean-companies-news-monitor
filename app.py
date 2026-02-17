import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 및 산업군 핵심 키워드 설정
STATES = {
    "Alabama": "앨라배마 (GMB코리아 등)",
    "Tennessee": "테네시 (LG엔솔, 한국타이어 등)",
    "Georgia": "조지아 (현대차 협력사 등)",
    "South Carolina": "사우스캐롤라이나 (삼성, 세방 등)",
    "Florida": "플로리다"
}

# 사용자 예시 기반 핵심 기업/산업 키워드
BIZ_KEYWORDS = "GMB, 효성중공업, 현대일렉트릭, LG엔솔, 한국타이어, 변압기, 배터리, LFP, 증설, 출자"

st.set_page_config(page_title="2026 韓 기업 미국 진출 실시간 보드", layout="wide")
st.title("🏭 2026년 미 동남부 한국 기업 진출·투자 정밀 보드")
st.caption(f"대상 기업/산업: {BIZ_KEYWORDS}")

def fetch_latest_news(query, lang, gl, period="30d"):
    # 1차 시도: 최근 30일(period) 내 데이터
    # 2차 시도: 데이터가 없으면 'after:2025-01-01'로 범위를 넓혀 '가장 최근' 것 확보
    encoded_query = urllib.parse.quote(f"{query} when:{period}")
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    feed = feedparser.parse(url)
    
    # 만약 30일 내 뉴스가 없으면 전체 기간에서 가장 최근 것을 가져오도록 재시도
    if not feed.entries and period == "30d":
        encoded_query = urllib.parse.quote(f"{query} after:2025-01-01")
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
        feed = feedparser.parse(url)

    # 중복 제거 및 날짜순 정렬
    seen = set()
    verified = []
    for entry in feed.entries:
        if entry.link not in seen:
            verified.append(entry)
            seen.add(entry.link)
    
    return sorted(verified, key=lambda x: x.get('published_parsed'), reverse=True)

# --- 보드 설계 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 (주정부/경제지)", "🇰🇷 한국 언론 보도 (기업공시/주요경제지)"])

with tab_us:
    st.info("💡 주 정부(Official) 및 현지 경제지 발 '신규 투자/증설' 소식")
    for en_name, display_name in STATES.items():
        with st.expander(f"📍 {display_name}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.caption("🏛️ 주 정부 공식 발표 (site:.gov)")
                # 주 정부 사이트에서 한국 기업(South Korea) 관련 투자 발표 검색
                q = f'site:.gov "{en_name}" "South Korea" (investment OR factory OR expansion)'
                items = fetch_latest_news(q, "en-US", "US")
                for e in items[:3]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.published[:16]}]")
            
            with col2:
                st.caption("📰 현지 경제 매체 (Biz Journals 등)")
                # 주별 기업명 및 산업 키워드 검색
                q = f'"{en_name}" "South Korea" (battery OR transformer OR manufacturing)'
                items = fetch_latest_news(q, "en-US", "US")
                for e in items[:3]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.source.title} | {e.published[:16]}]")

with tab_kr:
    st.success("💡 한국 내 주요 언론 및 기업 공시 관련 보도")
    for en_name, display_name in STATES.items():
        ko_name = display_name.split(" ")[0]
        with st.expander(f"📍 {display_name}", expanded=True):
            col_press, col_dia = st.columns(2)
            
            with col_press:
                st.caption("🗞️ 국내 주요 경제지 (투자/공시/증설)")
                # 사용자 예시 키워드를 반영한 검색
                q = f'{ko_name} ("출자" OR "증설" OR "양산" OR "수주")'
                items = fetch_latest_news(q, "ko", "KR")
                for e in items[:5]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.source.title} | {e.published[:16]}]")
                    
            with col_dia:
                st.caption("🇺🇸 미 현지 동포 소식 (한인 경제)")
                q = f'{ko_name} "투자" OR "공장" OR "진출"'
                items = fetch_latest_news(q, "ko", "US")
                for e in items[:5]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})  \n  :gray[{e.source.title} | {e.published[:16]}]")
