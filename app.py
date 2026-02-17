import streamlit as st
import feedparser
import urllib.parse

st.set_page_config(page_title="2026 韓 기업 미국 투자 보드", layout="wide")
st.title("🏭 2026년 2월 韓 기업 미국 진출·수주 실시간 상황판")

# 수집할 핵심 타겟과 검색어 정의
CORE_NEWS = [
    {"title": "조지아 동원금속 3천만불 투자 (주정부 발표)", "query": "site:.gov 'Dongwon Autopart' Georgia"},
    {"title": "효성중공업 7870억 역대급 수주 (테네시)", "query": "Hyosung Heavy Industries 787 billion transformer"},
    {"title": "지엠비코리아 앨라배마 자회사 출자 (공시)", "query": "지엠비코리아 'GMB USA ALABAMA' 출자"}
]

def fetch_top_priority_news(q):
    encoded_q = urllib.parse.quote(f"{q} after:2026-01-01")
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)
    return feed.entries[:3]

# 대시보드 출력
for biz in CORE_NEWS:
    with st.container(border=True):
        st.subheader(f"✅ {biz['title']}")
        items = fetch_top_priority_news(biz['query'])
        if items:
            for e in items:
                st.markdown(f"**[{e.title}]({e.link})**")
                st.caption(f"📅 {e.published}")
        else:
            st.write("관련 공식 보도자료를 수집 중입니다.")
