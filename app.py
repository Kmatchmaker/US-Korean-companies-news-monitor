import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 주별 최적화된 정밀 쿼리 (노이즈 제거 강화)
# 특히 AL, SC, FL은 산업 키워드를 필수 포함(+)하도록 수정했습니다.
STATE_QUERIES = {
    "Georgia": 'Georgia ("South Korea" OR Korean) (investment OR factory OR Dongwon) when:30d',
    "Alabama": 'Alabama ("South Korea" OR Korean) (Hyundai OR factory OR investment OR automotive) when:30d',
    "Tennessee": 'Tennessee ("South Korea" OR Korean) (LG OR SK OR investment OR factory) when:30d',
    "South Carolina": '"South Carolina" ("South Korea" OR Korean) (Samsung OR factory OR investment OR manufacturing) when:30d',
    "Florida": 'Florida ("South Korea" OR Korean) (investment OR "new office" OR energy OR technology) when:30d'
}

st.set_page_config(page_title="2026 미 동남부 기업 모니터", layout="wide")
st.title("🚜 2026년 미 동남부 韓 기업 진출 정밀 리포트")

def fetch_and_clean_news(state_name):
    query = STATE_QUERIES.get(state_name)
    encoded_query = urllib.parse.quote(query)
    
    # 글로벌(US) 뉴스를 메인으로 하되, 한국어 검색 결과를 보조로 합칩니다.
    news_feeds = [
        f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en",
        f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    ]
    
    all_entries = []
    for url in news_feeds:
        feed = feedparser.parse(url)
        all_entries.extend(feed.entries)
    
    # 시간순 정렬
    all_entries.sort(key=lambda x: x.get('published_parsed', (0,0,0,0,0,0,0,0,0)), reverse=True)
    
    unique_news = []
    seen_titles = set()
    
    # 2단계 필터: 수집된 뉴스 중 '투자/공장/기업' 관련 단어가 제목에 있는 것만 승인
    biz_keywords = ["invest", "factory", "plant", "company", "jobs", "new", "open", "korean", "korea", "venture", "partnership"]

    for entry in all_entries:
        title_lower = entry.title.lower()
        pure_title = entry.title.split(' - ')[0].strip()
        
        # 주 이름 검증 + 비즈니스 키워드 검증
        if state_name.lower() in title_lower:
            if any(kb in title_lower for kb in biz_keywords):
                if pure_title not in seen_titles:
                    # 2024년 이전 구형 뉴스 강제 배제
                    if "2024" not in entry.title and "2023" not in entry.title:
                        unique_news.append(entry)
                        seen_titles.add(pure_title)
                
    return unique_news[:8]

# 대시보드 화면 구성
cols = st.columns(len(STATE_QUERIES))

for i, state in enumerate(STATE_QUERIES.keys()):
    with cols[i]:
        st.subheader(f"📍 {state}")
        news_items = fetch_and_clean_news(state)
        
        if not news_items:
            st.info("현재 관련 비즈니스 소식이 없습니다.")
        
        for entry in news_items:
            with st.container(border=True):
                st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
                st.markdown(f"#### [{entry.title.split(' - ')[0]}]({entry.link})")
                
                if 'summary' in entry:
                    clean_summary = entry.summary.split('<')[0]
                    if len(clean_summary) > 10:
                        st.write(f"📝 {clean_summary[:140]}...")
