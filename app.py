import streamlit as st
import feedparser
import urllib.parse

# 설정: 주 이름 매핑 (한국어 검색용)
STATE_MAP = {
    "Georgia": "조지아",
    "Alabama": "앨라배마",
    "Tennessee": "테네시",
    "South Carolina": "사우스캐롤라이나",
    "Florida": "플로리다"
}

st.set_page_config(page_title="2026 미 동남부 기업 모니터", layout="wide")

# --- 뉴스 수집 함수 ---
def fetch_news(query, lang, gl):
    encoded_query = urllib.parse.quote(f"{query} when:30d")
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl={gl}&ceid={gl}:{lang}"
    feed = feedparser.parse(url)
    return sorted(feed.entries, key=lambda x: x.get('published_parsed', (0,0,0,0,0,0,0,0,0)), reverse=True)

# ==========================================================
# 🇺🇸 SECTION 1: 미국 현지 뉴스 보드 (US Official News)
# ==========================================================
st.title("🇺🇸 미국 현지 오피셜 보도")
st.markdown("##### 주 정부 및 현지 경제지에서 보도한 영문 기사")

cols_us = st.columns(len(STATE_MAP))
for i, (en_name, ko_name) in enumerate(STATE_MAP.items()):
    with cols_us[i]:
        st.info(f"📍 {en_name}")
        # 미국 뉴스는 영어로 검색
        query_us = f'"{en_name}" "South Korea" (investment OR factory OR plant)'
        items = fetch_news(query_us, "en-US", "US")
        
        if not items:
            st.write("최신 현지 뉴스가 없습니다.")
        for entry in items[:6]:
            with st.container(border=True):
                st.caption(f"📅 {entry.published[:16]}")
                st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                st.caption(f"출처: {entry.source.title}")

st.divider() # 보드 구분을 위한 굵은 선

# ==========================================================
# 🇰🇷 SECTION 2: 한국 언론 보도 보드 (Korean Media News)
# ==========================================================
st.title("🇰🇷 한국 언론 보도")
st.markdown("##### 국내 주요 일간지 및 경제지에서 보도한 진출 소식")

cols_kr = st.columns(len(STATE_MAP))
for i, (en_name, ko_name) in enumerate(STATE_MAP.items()):
    with cols_kr[i]:
        st.success(f"📍 {ko_name}")
        # [핵심 수정] 한국어 지명으로 검색하여 정확도 상향
        query_kr = f'{ko_name} "미국" (투자 OR 진출 OR 공장)'
        items = fetch_news(query_kr, "ko", "KR")
        
        if not items:
            st.write("관련 한국 보도가 없습니다.")
        for entry in items[:6]:
            with st.container(border=True):
                st.caption(f"📅 {entry.published[:16]}")
                st.markdown(f"**[{entry.title.split(' - ')[0]}]({entry.link})**")
                st.caption(f"출처: {entry.source.title}")
