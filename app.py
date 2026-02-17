import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 설정
STATES = {
    "Georgia": "조지아",
    "Alabama": "앨라배마",
    "Tennessee": "테네시",
    "South Carolina": "사우스캐롤라이나",
    "Florida": "플로리다"
}

st.set_page_config(page_title="2026 韓 기업 미국 진출 실시간 보드", layout="wide")
st.title("🏭 2026년 2월 韓 기업 미국 진출·신규 투자 리포트")

# --- 정밀 필터링 함수 ---
def fetch_top_tier_news(query, lang, gl):
    # 2026년 2월 1일 이후 데이터 강제
    date_filter = "after:2026-02-01"
    full_query = f'{query} {date_filter}'
    encoded_query = urllib.parse.quote(full_query)
    
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    feed = feedparser.parse(url)
    
    verified = []
    seen_links = set()
    
    for entry in feed.entries:
        # 연도 검증 (2026년만 통과)
        if entry.get('published_parsed') and entry.published_parsed.tm_year == 2026:
            if entry.link not in seen_links:
                verified.append(entry)
                seen_links.add(entry.link)
                
    return sorted(verified, key=lambda x: x.get('published_parsed'), reverse=True)

# --- 화면 구성 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 오피셜 뉴스 (Gov & Biz)", "🇰🇷 한국/동포 뉴스 (Press)"])

with tab_us:
    st.info("💡 주 정부(Governor's Office) 발표 및 미국 경제 전문지 보도")
    for en_name, ko_name in STATES.items():
        st.markdown(f"#### 📍 {en_name} ({ko_name})")
        col1, col2 = st.columns(2)
        
        with col1:
            st.caption("🏛️ 주 정부 공식 발표 (Official Release)")
            # [핵심] 주 정부 사이트(.gov)에서 발표한 한국 기업 투자 소식 
            # 예: 2월 4일 동원오토 조지아 투자 발표 등
            q = f'site:.gov "{en_name}" "South Korea" investment'
            items = fetch_top_tier_news(q, "en-US", "US")
            for e in items[:5]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]}")
        
        with col2:
            st.caption("📰 지역/전국 경제지 (Business Media)")
            # 조지아의 경우 AJC나 Business Chronicle 등 유력지 중심
            q = f'"{en_name}" "South Korea" investment (Journal OR Chronicle OR News)'
            items = fetch_top_tier_news(q, "en-US", "US")
            for e in items[:5]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")

with tab_kr:
    st.success("💡 국내 경제지 및 미국 현지 한인 매체 보도")
    for en_name, ko_name in STATES.items():
        st.markdown(f"#### 📍 {ko_name} ({en_name})")
        col_main, col_dia = st.columns(2)
        
        with col_main:
            st.caption("🗞️ 한국 주요 언론 (네이버 뉴스 등)")
            q = f'{ko_name} "미국" (투자 OR 진출 OR 공장)'
            items = fetch_top_tier_news(q, "ko", "KR")
            for e in items[:7]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")
                    
        with col_dia:
            st.caption("🇺🇸 미 현지 동포 신문 (한인 뉴스)")
            q = f'{ko_name} "투자" OR "공장" OR "진출"'
            items = fetch_top_tier_news(q, "ko", "US")
            for e in items[:7]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")
