import streamlit as st
import feedparser
import urllib.parse

st.set_page_config(page_title="2026 韓 기업 미국 투자 보드", layout="wide")
st.title("🏭 2026년 2월 한국 기업 미국 진출·수주 정밀 보드")

# 1. 사용자님이 알고자 하는 핵심 타겟 기업 및 주
TARGETS = {
    "Georgia": "조지아 (동원오토, 덕신EPC)",
    "Alabama": "앨라배마 (지엠비코리아, 현대일렉)",
    "Tennessee": "테네시 (효성, LG엔솔, 한국타이어)"
}

def fetch_latest_biz_news(query, gl):
    # 날짜 필터를 빼고 '2026' 키워드를 쿼리에 직접 넣는 것이 더 확실합니다.
    full_query = f'{query} 2026 (투자 OR 출자 OR 수주 OR 공장 OR investment)'
    encoded_query = urllib.parse.quote(full_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl={gl}&ceid={gl}:ko"
    
    feed = feedparser.parse(url)
    # 제목에 '구금'이나 '수사'가 들어간 노이즈는 코드에서 제외
    noise = ["구금", "수사", "레이드", "arrest", "raid"]
    return [e for e in feed.entries if not any(w in e.title.lower() for w in noise)][:5]

tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 뉴스 (Gov & Biz)", "🇰🇷 한국 언론 & 공시"])

with tab_us:
    for en, display in TARGETS.items():
        st.subheader(f"📍 {display}")
        # 미국 현지 소스 검색 (gl=US)
        items = fetch_latest_biz_news(f'"{en}" "South Korea"', "US")
        if not items: st.write("최신 오피셜 뉴스 대기 중")
        for e in items:
            # 주정부 발표(.gov)는 강조 표시
            style = "success" if ".gov" in e.link else "info"
            getattr(st, style)(f"**[{e.title}]({e.link})**")
            st.caption(f"📅 {e.published}")

with tab_kr:
    for en, display in TARGETS.items():
        ko_state = display.split(" ")[0]
        st.subheader(f"📍 {ko_state}")
        # 한국 언론 소스 검색 (gl=KR)
        items = fetch_latest_biz_news(ko_state, "KR")
        for e in items:
            with st.container(border=True):
                st.markdown(f"**[{e.title}]({e.link})**")
                st.caption(f"📅 {e.published} | {e.source.title}")
