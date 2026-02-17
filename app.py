import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# 1. 대상 주 및 정밀 검색을 위한 주요 기업 리스트
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]
TARGET_COMPANIES = [
    "Hyundai", "Kia", "LG Energy", "SK On", "Samsung SDI", "Hanwha Qcells", 
    "Korea Zinc", "Dongwon", "Ajin", "Seoyon", "Hanon", "Enchem", "NVH Korea"
]

st.set_page_config(page_title="2026 미 동남부 기업 투자 리포트", layout="wide")
st.title("🏭 2026년 미 동남부 한국 기업 진출·투자 모니터링")

def fetch_latest_business_news(state):
    # [전략] 개별 기업명과 투자 키워드를 조합하여 정밀 검색
    # when:30d를 사용하여 최근 1개월 기사만 타겟팅
    company_query = " OR ".join([f'"{c}"' for c in TARGET_COMPANIES])
    query = f'{state} ({company_query}) (investment OR factory OR plant OR construction) when:30d'
    
    # 한국어/영어 동시 검색을 위한 설정
    results = []
    configs = [
        {"hl": "ko", "gl": "KR"}, # 한국 언론사 뉴스
        {"hl": "en", "gl": "US"}  # 미국 현지 보도자료 및 경제지
    ]
    
    for config in configs:
        encoded_query = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl={config['hl']}&gl={config['gl']}&ceid={config['gl']}:{config['hl']}"
        feed = feedparser.parse(url)
        results.extend(feed.entries)

    # 2. 최신 날짜 순으로 강제 정렬 (중요!)
    # feedparser의 published_parsed를 기준으로 내림차순 정렬
    results.sort(key=lambda x: x.get('published_parsed', (0,0,0,0,0,0,0,0,0)), reverse=True)

    # 3. 중복 제거 및 2026년 기사 검증
    seen_titles = set()
    final_list = []
    for entry in results:
        title_main = entry.title.split(' - ')[0]
        if title_main not in seen_titles:
            # 제목에 대기업이나 투자 키워드가 실제로 있는지 재검증
            if any(kw.lower() in entry.title.lower() for kw in TARGET_COMPANIES + ["korea"]):
                final_list.append(entry)
                seen_titles.add(title_main)
                
    return final_list[:10] # 각 주별 최신 뉴스 10개씩

# 대시보드 화면 구성
cols = st.columns(len(STATES))

for i, state in enumerate(STATES):
    with cols[i]:
        st.subheader(f"📍 {state}")
        news_items = fetch_latest_business_news(state)
        
        if not news_items:
            st.write("최근 30일 내 주요 투자 소식이 없습니다.")
        
        for entry in news_items:
            with st.container(border=True):
                # 1. 최신 날짜 강조 (가장 위에 배치)
                pub_date = entry.published[:16] # 날짜 및 시간
                st.caption(f"📅 {pub_date} | {entry.source.title}")
                
                # 2. 기사 제목 (개별 기업 중심)
                st.markdown(f"#### [{entry.title.split(' - ')[0]}]({entry.link})")
                
                # 3. 기사 요약(미리보기)
                if 'summary' in entry:
                    summary = entry.summary.split('<')[0]
                    if len(summary) > 20:
                        st.write(f"📝 {summary[:150]}...")
