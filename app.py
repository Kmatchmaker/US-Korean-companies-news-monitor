import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 설정
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]

st.set_page_config(page_title="2026 미 동남부 기업 뉴스", layout="wide")
st.title("🚀 2026년 미 동남부 한국 기업 진출 실시간 리포트")

def fetch_latest_news(state):
    # [전략] 검색어 뒤에 강제로 '2026'과 'when:30d'를 붙여 과거 기사 차단
    # 한국어 뉴스용 쿼리와 영어 뉴스용 쿼리를 각각 생성
    
    # 1. 한국어 쿼리 (한글 뉴스 타겟)
    query_ko = f'{state} "한국 기업" 투자 2026 when:30d'
    # 2. 영어 쿼리 (현지 보도 타겟)
    query_en = f'{state} "South Korea" (factory OR investment OR plant) 2026 when:30d'
    
    combined_entries = []
    
    # 한국어/영어 뉴스 각각 수집
    for q, lang, gl in [(query_ko, "ko", "KR"), (query_en, "en", "US")]:
        encoded_q = urllib.parse.quote(q)
        url = f"https://news.google.com/rss/search?q={encoded_q}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
        feed = feedparser.parse(url)
        combined_entries.extend(feed.entries)
    
    # 중복 제거 및 2026년 확인 로직
    seen_titles = set()
    final_news = []
    
    # 최신순 정렬 (발행일 기준)
    combined_entries.sort(key=lambda x: x.get('published_parsed', 0), reverse=True)
    
    for entry in combined_entries:
        pure_title = entry.title.split(' - ')[0]
        if pure_title not in seen_titles:
            # 제목이나 날짜에 2024, 2023이 포함된 경우 한번 더 걸러냄
            if "2024" not in entry.title and "2023" not in entry.title:
                final_news.append(entry)
                seen_titles.add(pure_title)
                
    return final_news[:8] # 주별 최신 뉴스 8개

# 대시보드 화면 구성
cols = st.columns(len(STATES))

for i, state in enumerate(STATES):
    with cols[i]:
        st.subheader(f"📍 {state}")
        news_items = fetch_latest_news(state)
        
        if not news_items:
            st.write("최근 30일 내 업데이트된 소식이 없습니다.")
        
        for entry in news_items:
            with st.container(border=True):
                # 뉴스 출처 및 날짜 강조
                st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
                st.markdown(f"#### [{entry.title.split(' - ')[0]}]({entry.link})")
                
                # 요약 미리보기
                if 'summary' in entry:
                    summary = entry.summary.split('<')[0]
                    st.write(f"📝 {summary[:150]}...")
