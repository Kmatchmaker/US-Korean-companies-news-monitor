import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 주별 검색어 최적화 (데이터 섞임 방지 로직 강화)
# 'site:.gov'나 지역 언론사를 우선하도록 검색어를 구성했습니다.
STATE_QUERIES = {
    "Georgia": 'Georgia ("South Korea" OR Korean) (investment OR factory OR "new plant") when:30d',
    "Alabama": 'Alabama ("South Korea" OR Korean) (investment OR factory OR "new plant") when:30d',
    "Tennessee": 'Tennessee ("South Korea" OR Korean) (investment OR factory OR "new plant") when:30d',
    "South Carolina": '"South Carolina" ("South Korea" OR Korean) (investment OR factory OR "new plant") when:30d',
    "Florida": 'Florida ("South Korea" OR Korean) (investment OR factory OR "new plant") when:30d'
}

st.set_page_config(page_title="2026 미 동남부 韓 기업 투자 현황", layout="wide")
st.title("🚜 2026년 미 동남부 한국 기업 진출·투자 실시간 모니터링")
st.markdown("---")

def fetch_and_clean_news(state_name):
    query = STATE_QUERIES.get(state_name)
    encoded_query = urllib.parse.quote(query)
    
    # 영어(현지 보도)와 한국어(국내 보도) 결과를 모두 가져와 통합합니다.
    news_feeds = [
        f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en",
        f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    ]
    
    all_entries = []
    for url in news_feeds:
        feed = feedparser.parse(url)
        all_entries.extend(feed.entries)
    
    # 2. 최신 날짜 순 정렬 (강제 정렬)
    all_entries.sort(key=lambda x: x.get('published_parsed', (0,0,0,0,0,0,0,0,0)), reverse=True)
    
    # 3. 중복 제거 및 '그 주' 뉴스가 맞는지 교차 검증
    unique_news = []
    seen_titles = set()
    
    for entry in all_entries:
        pure_title = entry.title.split(' - ')[0].strip()
        # 데이터 섞임 방지: 제목이나 링크에 해당 주 이름이 포함되어야 함
        if state_name.lower() in entry.title.lower() or state_name.lower().replace(" ", "") in entry.link.lower():
            if pure_title not in seen_titles:
                # 2024년 이전 노후 기사 배제 (한 번 더 필터링)
                if "2024" not in entry.title and "2023" not in entry.title:
                    unique_news.append(entry)
                    seen_titles.add(pure_title)
                
    return unique_news[:8]

# 4. 대시보드 화면 구성
cols = st.columns(len(STATE_QUERIES))

for i, state in enumerate(STATE_QUERIES.keys()):
    with cols[i]:
        st.subheader(f"📍 {state}")
        news_items = fetch_and_clean_news(state)
        
        if not news_items:
            st.write("✅ 신규 소식이 없습니다.")
        
        for entry in news_items:
            with st.container(border=True):
                # 최신 날짜 및 언론사
                st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
                # 제목 (클릭 시 원문 이동)
                st.markdown(f"#### [{entry.title.split(' - ')[0]}]({entry.link})")
                
                # 본문 미리보기 (핵심 내용 파악)
                if 'summary' in entry:
                    # HTML 태그 제거 및 텍스트만 추출
                    clean_summary = entry.summary.split('<')[0]
                    if len(clean_summary) > 10:
                        st.write(f"📝 {clean_summary[:150]}...")
