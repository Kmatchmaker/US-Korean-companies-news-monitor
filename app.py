import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 및 산업별 핵심 키워드 설정
STATES = {
    "Georgia": "조지아 (동원오토·덕신EPC 등)",
    "Alabama": "앨라배마 (지엠비코리아·현대일렉 등)",
    "Tennessee": "테네시 (효성중공업·LG엔솔·한국타이어)",
    "South Carolina": "사우스캐롤라이나",
    "Florida": "플로리다"
}

st.set_page_config(page_title="2026 韓 기업 미국 진출 인텔리전스", layout="wide")
st.title("🚜 2026년 2월 미 동남부 韓 기업 진출·투자 정밀 보드")
st.markdown("### 🏛️ 주 정부 공식 발표(Official) 및 핵심 비즈니스 정보 우선 브리핑")

# --- 뉴스 수집 및 비즈니스 중요도 필터 엔진 ---
def fetch_high_priority_news(query, lang, gl):
    # 2026년 2월 이후 데이터 + 투자 확장 키워드
    biz_terms = '(investment OR "new plant" OR "announces" OR "expansion" OR "contract")'
    date_filter = "after:2026-02-01"
    
    full_query = f'{query} {biz_terms} {date_filter}'
    encoded_query = urllib.parse.quote(full_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    
    feed = feedparser.parse(url)
    verified = []
    
    # [노이즈 캔슬러] 사용자님이 지적하신 과거 사건사고 키워드 제거
    noise_words = ["arrest", "raid", "detain", "investigation", "구금", "레이드", "수사"]
    
    for entry in feed.entries:
        title = entry.title.lower()
        # 2026년도 발행 기사만 통과
        if entry.get('published_parsed') and entry.published_parsed.tm_year == 2026:
            if not any(noise in title for noise in noise_words):
                # 중요도 가점: 주 정부 발표(.gov)거나 핵심 기업명 포함 시 가산점
                priority_score = 0
                if ".gov" in entry.link: priority_score += 10
                if any(target in title for target in ["dongwon", "gmb", "hyosung", "lg", "hankook"]): priority_score += 5
                
                verified.append({"entry": entry, "score": priority_score})
                
    # 점수 높은 순(중요도) -> 최신순 정렬
    sorted_results = sorted(verified, key=lambda x: (x['score'], x['entry'].published_parsed), reverse=True)
    return [x['entry'] for x in sorted_results]

# --- 화면 레이아웃 구성 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 (Gov & Biz)", "🇰🇷 한국 언론 & 공시 (Press)"])

with tab_us:
    st.info("💡 주지사실(.gov) 보도자료 및 지역 경제 매체 정밀 필터링")
    for en_name, display_name in STATES.items():
        with st.expander(f"📍 {display_name}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.caption("🏛️ 1. 주 정부 공식 발표 (Official Press Release)")
                # site:.gov 필터로 주지사 발표 원문을 강제 검색
                q = f'site:.gov "{en_name}" "South Korea" investment'
                items = fetch_high_priority_news(q, "en-US", "US")
                for e in items[:3]:
                    st.success(f"**[GOV] [{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]}")

            with col2:
                st.caption("📰 2. 현지 유력 경제지 (Business News)")
                q = f'"{en_name}" "South Korea" (Journal OR Chronicle OR News) investment'
                items = fetch_high_priority_news(q, "en-US", "US")
                for e in items[:3]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")

with tab_kr:
    st.success("🗞️ 한국 주요 경제지 및 기업 공시 기반 투자 보도")
    for en_name, display_name in STATES.items():
        ko_name = display_name.split(" ")[0]
        with st.expander(f"📍 {ko_name} ({en_name})", expanded=True):
            col_press, col_dia = st.columns(2)
            
            with col_press:
                st.caption("🗞️ 1. 한국 주요 언론 (출자/수주/증설)")
                # 사용자님 요청 키워드 최우선 배치
                q = f'{ko_name} ("출자" OR "수주" OR "증설" OR "양산" OR "투자")'
                items = fetch_high_priority_news(q, "ko", "KR")
                for e in items[:5]:
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")
                    
            with col_dia:
                st.caption("🇺🇸 2. 미 현지 유력 동포 소식")
                q = f'{ko_name} "투자" OR "공장" OR "진출"'
                items = fetch_high_priority_news(q, "ko", "US")
                for e in items[:5]:
                    st.markdown(f"• [{e.title.split(' - ')[0]}]({e.link})")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")
