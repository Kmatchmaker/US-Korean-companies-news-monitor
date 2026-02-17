import streamlit as st
import feedparser
import urllib.parse

# 1. 5개 주 설정
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]

# 2. 뉴스에서 반드시 우선순위를 둘 핵심 기업 리스트 (예시)
CORE_COMPANIES = [
    "Hyundai", "Kia", "LG Energy", "SK On", "Samsung SDI", 
    "Hanwha Qcells", "Dongwon", "Ajin", "Seoyon E-Hwa", "Hanon Systems", 
    "Enchem", "NVH Korea", "Zincox", "Korea Zinc", "EcoPro"
]

st.set_page_config(page_title="2026 미 동남부 기업 투자 모니터", layout="wide")
st.title("🏭 한국 기업 진출 및 신규 투자 정밀 리포트")

def fetch_business_news(state):
    # [전략] 주 이름 + (한국 기업 리스트) + (투자 관련 핵심어) 조합
    # 고려아연(Korea Zinc), 동원(Dongwon) 등을 검색어에 직접 포함하여 정확도를 높임
    company_query = " OR ".join(CORE_COMPANIES[:10]) # 너무 길면 오류나므로 상위 10개 우선
    keywords = "(investment OR factory OR plant OR construction OR expansion OR groundbreaking)"
    
    query = f'{state} ("South Korea" OR {company_query}) {keywords} when:30d'
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(url)
    
    seen_titles = set()
    filtered_news = []
    
    for entry in feed.entries:
        pure_title = entry.title.split(' - ')[0]
        if pure_title not in seen_titles:
            # 제목에 한국 관련 혹은 산업 키워드가 있는지 최종 검증
            title_lower = entry.title.lower()
            if any(word.lower() in title_lower for word in CORE_COMPANIES + ["korea", "invest"]):
                filtered_news.append(entry)
                seen_titles.add(pure_title)
                
    return filtered_news[:6]

# 대시보드 화면 구성
cols = st.columns(len(STATES))

for i, state in enumerate(STATES):
    with cols[i]:
        st.subheader(f"📍 {state}")
        news_items = fetch_business_news(state)
        
        if not news_items:
            st.write("관련된 신규 투자 소식이 없습니다.")
        
        for entry in news_items:
            with st.container(border=True):
                # 출처 및 날짜
                st.caption(f"📅 {entry.published[:16]} | {entry.source.title}")
                
                # 제목 (클릭 시 원문)
                st.markdown(f"#### [{entry.title.split(' - ')[0]}]({entry.link})")
                
                # 본문 미리보기 (요약 대용)
                if 'summary' in entry:
                    # HTML 태그를 제거하고 실제 내용만 추출
                    clean_summary = entry.summary.split('<')[0]
                    if len(clean_summary) > 20:
                        st.write(f"🔍 {clean_summary[:180]}...")
                    else:
                        st.write("🔍 상세 내용은 기사 원문을 확인하세요.")
