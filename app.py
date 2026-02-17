import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime, timedelta

# 1. 대상 주 및 핵심 기업 키워드 설정
TARGET_STATES = {
    "Georgia": "조지아 (동원금속, 덕신EPC 등)",
    "Alabama": "앨라배마 (지엠비코리아, 현대차 등)",
    "Tennessee": "테네시 (효성, LG엔솔, 한국타이어)",
    "South Carolina": "사우스캐롤라이나 (삼성, 세방 등)",
    "Florida": "플로리다 (물류, 신에너지)"
}

# 비즈니스 핵심 가중치 키워드
BIZ_KEYWORDS = ["investment", "expansion", "contract", "수주", "투자", "출자", "증설"]

st.set_page_config(page_title="2026 韓 기업 미국 진출 실시간 보드", layout="wide")
st.title("🚜 2026년 2월 미 동남부 韓 기업 진출 상황판")
st.caption(f"기준일: {datetime.now().strftime('%Y-%m-%d')} (매일 자동 업데이트)")

# --- 뉴스 수집 엔진 ---
def fetch_biz_news(query, lang, gl):
    # 오늘 기준 '최신' 뉴스를 우선 수집
    encoded_query = urllib.parse.quote(f"{query} when:7d") # 최근 7일 내
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    
    feed = feedparser.parse(url)
    scored_news = []
    
    for entry in feed.entries:
        title = entry.title.lower()
        # 중요도 점수 계산 (주 정부 발표나 핵심 키워드 포함 시 상단 노출)
        score = 0
        if ".gov" in entry.link: score += 10
        if any(k in title for k in BIZ_KEYWORDS): score += 5
        
        # 부정적 노이즈(구금, 레이드 등) 필터링
        if not any(n in title for n in ["arrest", "raid", "investigation", "구금"]):
            scored_news.append({"entry": entry, "score": score})
            
    # 점수 순, 그 다음 날짜 순 정렬
    sorted_news = sorted(scored_news, key=lambda x: (x['score'], x['entry'].published_parsed), reverse=True)
    return [x['entry'] for x in sorted_news]

# --- 화면 구성 (보드 형태) ---
for en_state, ko_display in TARGET_STATES.items():
    st.markdown(f"### 📍 {ko_display}")
    
    # 탭으로 정보 분류
    official_tab, press_tab = st.tabs(["🏛️ 주 정부 & 오피셜", "🗞️ 한국 공시 & 언론"])
    
    with official_tab:
        # 주 정부 사이트(.gov) 강제 타겟팅
        q = f'site:.gov "{en_state}" "South Korea" investment'
        news = fetch_biz_news(q, "en-US", "US")
        if news:
            for n in news[:3]:
                st.success(f"**[{n.title}]({n.link})** \n :gray[{n.published}]")
        else:
            st.write("새로운 주 정부 공식 발표를 기다리고 있습니다.")

    with press_tab:
        # 한국 언론 및 공시 위주
        ko_state = ko_display.split(" ")[0]
        q = f'{ko_state} (투자 OR 수주 OR 출자 OR 공장)'
        news = fetch_biz_news(q, "ko", "KR")
        if news:
            for n in news[:4]:
                st.info(f"**[{n.title}]({n.link})** \n :gray[{n.source.title} | {n.published}]")
    st.divider()
