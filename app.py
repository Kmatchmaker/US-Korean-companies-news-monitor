import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 및 산업별 핵심 키워드 (가중치 부여)
STATES = {
    "Georgia": "조지아 (현대차·동원·덕신 등)",
    "Alabama": "앨라배마 (GMB코리아·부품사 등)",
    "Tennessee": "테네시 (LG엔솔·한국타이어 등)",
    "South Carolina": "사우스캐롤라이나 (전력기기·삼성 등)",
    "Florida": "플로리다 (신에너지·물류 등)"
}

st.set_page_config(page_title="2026 韓 기업 미국 진출 실시간 보드", layout="wide")
st.title("🚀 2026년 2월 미 동남부 韓 기업 진출·투자 인텔리전스")
st.caption("주 정부 공식 발표 및 핵심 경제지의 '성장·투자' 뉴스만 선별 브리핑합니다.")

# --- 고정밀 뉴스 수집 엔진 (기업 성장 키워드 특화) ---
def fetch_biz_centric_news(query, lang, gl):
    # 2026년 2월 이후 + 비즈니스 확장 키워드 강제 결합
    biz_terms = '(investment OR "new plant" OR expansion OR "breaking ground" OR "capital increase" OR "official announcement")'
    date_filter = "after:2026-02-01"
    
    full_query = f'{query} {biz_terms} {date_filter}'
    encoded_query = urllib.parse.quote(full_query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    
    feed = feedparser.parse(url)
    verified = []
    
    # 노이즈 필터 (구금, 레이드, 사건 등 부정 키워드 제목에서 발견 시 즉시 제외)
    noise_words = ["arrest", "raid", "detain", "police", "investigation", "구금", "레이드", "수사"]
    
    for entry in feed.entries:
        title = entry.title.lower()
        if entry.get('published_parsed') and entry.published_parsed.tm_year == 2026:
            if not any(noise in title for noise in noise_words):
                verified.append(entry)
                
    return sorted(verified, key=lambda x: x.get('published_parsed'), reverse=True)

# --- 화면 구성: 공신력 있는 데이터 보드 ---
tab_us, tab_kr = st.tabs(["🇺🇸 미국 현지 오피셜 (Gov & Biz Media)", "🇰🇷 한국 언론 & 공시 (Domestic Press)"])

with tab_us:
    st.info("🏛️ 미국 주 정부(Official) 및 현지 경제지 발 '신규 투자/증설' 소식")
    for en_name, display_name in STATES.items():
        st.markdown(f"#### 📍 {display_name}")
        gov_col, biz_col = st.columns(2)
        
        with gov_col:
            st.caption("🏛️ 1. 주 정부 보도자료 (site:.gov)")
            # 주 정부 공식 프레스룸 및 경제개발국(GDEcD 등) 타겟팅
            q = f'site:.gov "{en_name}" ("South Korea" OR Korean) investment'
            items = fetch_biz_centric_news(q, "en-US", "US")
            if not items: st.write(":grey[신규 공식 발표 대기 중]")
            for e in items[:5]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]}")
        
        with biz_col:
            st.caption("📰 2. 현지 핵심 경제지 (Biz Journals, AJC 등)")
            # 'Journal', 'Chronicle' 등 로컬 경제 전문 매체 가중치
            q = f'"{en_name}" "South Korea" (Journal OR Chronicle OR News) investment'
            items = fetch_biz_centric_news(q, "en-US", "US")
            for e in items[:5]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")

with tab_kr:
    st.success("🗞️ 한국 주요 경제지 및 기업 공시 기반 투자 보도")
    for en_name, display_name in STATES.items():
        ko_name = display_name.split(" ")[0]
        st.markdown(f"#### 📍 {ko_name} ({en_name})")
        press_col, diaspora_col = st.columns(2)
        
        with press_col:
            st.caption("🗞️ 1. 한국 주요 언론 (투자/수주/증설)")
            # 사용자 요청 키워드 (출자, 증설, 변압기, 양산 등) 반영
            q = f'{ko_name} ("출자" OR "증설" OR "양산" OR "수주" OR "변압기")'
            items = fetch_biz_centric_news(q, "ko", "KR")
            for e in items[:6]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")
                    
        with diaspora_col:
            st.caption("🇺🇸 2. 미 현지 동포 경제 소식")
            q = f'{ko_name} (투자 OR 공장 OR 진출)'
            items = fetch_biz_centric_news(q, "ko", "US")
            for e in items[:6]:
                with st.container(border=True):
                    st.markdown(f"**[{e.title.split(' - ')[0]}]({e.link})**")
                    st.caption(f"📅 {e.published[:16]} | {e.source.title}")
