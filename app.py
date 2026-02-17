import streamlit as st
import feedparser
import urllib.parse

# 5개 주 설정
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]

st.set_page_config(page_title="2026 미 동남부 기업 모니터", layout="wide")
st.title("📑 한국 기업 진출 및 투자 정밀 모니터링")

def fetch_precise_news(state):
    # 정밀 쿼리: South Korea와 산업 키워드 결합
    query = f'{state} "South Korea" (factory OR plant OR investment OR EV OR battery) when:30d'
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(url)
    
    seen_titles = set()
    unique_news = []
    
    for entry in feed.entries:
        # 제목에서 언론사명 제거 후 중복 체크
        pure_title = entry.title.split(' - ')[0]
        if pure_title not in seen_titles:
            # 주요 키워드가 포함된 경우만 수집
            keywords = ["korea", "hyundai", "lg", "sk", "samsung", "hanwha", "battery", "ev", "automotive"]
            if any(kw in entry.title.lower() for kw in keywords):
                unique_news.append(entry)
                seen_titles.add(pure_title)
                
    return unique_news[:5] # 주당 5개씩만 노출

# 대시보드 화면 구성
cols = st.columns(len(STATES))

for i, state in enumerate(STATES):
    with cols[i]:
        st.subheader(f"📍 {state}")
        news_items = fetch_precise_news(state)
        
        if not news_items:
            st.write("새로운 기업 소식이 없습니다.")
        
        for entry in news_items:
            with st.container(border=True):
                # 제목 클릭 시 원문 이동
                st.markdown(f"**[{entry.source.title}]**")
                st.markdown(f"#### [{entry.title.split(' - ')[0]}]({entry.link})")
                
                # 기사 요약(미리보기) 부분
                # RSS에서 제공하는 summary/description을 활용합니다.
                if 'summary' in entry:
                    # HTML 태그 제거 및 간단한 요약 노출
                    summary_text = entry.summary.split('<')[0] # 단순 텍스트만 추출
                    if len(summary_text) > 10:
                        st.write(f"📝 {summary_text[:150]}...")
                    else:
                        st.write("📝 본문 요약 내용은 원문을 참조하세요.")
                
                st.caption(f"📅 {entry.published[:16]}")
