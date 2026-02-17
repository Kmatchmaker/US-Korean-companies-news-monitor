import streamlit as st
import feedparser
import urllib.parse  # 주소 오류 수정을 위해 추가되었습니다.

# 설정: 5개 주
STATES = ["Georgia", "Alabama", "Tennessee", "South Carolina", "Florida"]

st.set_page_config(page_title="미국 동남부 한국기업 뉴스 센터", layout="wide")
st.title("🇰🇷 미국 동남부 진출 한국 기업 실시간 모니터링")
st.sidebar.info("2026년 신규 진입 및 주요 기업 뉴스를 매일 업데이트합니다.")

def fetch_news(state):
    # 검색어 설정
    query = f"{state} South Korea investment factory"
    
    # [수정 포인트] 검색어 사이의 공백을 안전하게 변환합니다.
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(url)
    return feed.entries[:8]

# 대시보드 화면 구성
cols = st.columns(len(STATES))

for i, state in enumerate(STATES):
    with cols[i]:
        st.header(f"📍 {state}")
        try:
            news_items = fetch_news(state)
            if not news_items:
                st.write("새로운 소식이 없습니다.")
            for entry in news_items:
                with st.container():
                    st.markdown(f"**[{entry.source.title}]**")
                    st.write(f"[{entry.title}]({entry.link})")
                    st.caption(f"발행일: {entry.published[:16]}")
                    st.divider()
        except Exception as e:
            st.error(f"뉴스를 가져오는 중 오류가 발생했습니다.")
