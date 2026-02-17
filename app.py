import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="미 동남부 5개 주 韓 기업 투자 보드", layout="wide")
st.title("🏭 미 동남부 5개 주 韓 대기업 진출 실시간 상황판")
st.markdown("#### (조지아, 테네시, 앨라배마, 사우스캐롤라이나, 플로리다)")
st.caption(f"기준일: {datetime.now().strftime('%Y-%m-%d')} | 대기업(현대차, LG, SK, 고려아연, 한화 등) 뉴스 상단 고정")

# 2. 고정된 타겟 주 및 대기업 키워드 설정
TARGET_STATES = ["조지아", "테네시", "앨라배마", "사우스캐롤라이나", "플로리다"]
MAJOR_CORP = ["현대차", "현대자동차", "LG", "SK", "고려아연", "한화", "삼성", "효성"]
BIZ_KEYWORDS = "('투자' OR '수주' OR '공장' OR '신설' OR '진출' OR '증설')"

def fetch_tiered_news():
    all_news = []
    for state in TARGET_STATES:
        # 구글 뉴스 검색 (주 + 비즈니스 키워드 조합)
        query = f"{state} {BIZ_KEYWORDS} when:7d"
        encoded_query = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
        
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:5]: # 각 주별 최신 뉴스 5개씩 수집
            title = entry.title
            source = entry.source.title
            date = entry.published[:16]
            link = entry.link
            
            # 티어(Tier) 판별 로직
            tier = 1 # 일반 기업 (기본값)
            for corp in MAJOR_CORP:
                if corp in title:
                    tier = 0 # 대기업 (최상단)
                    title = f"👑 [{corp}] {title}" # 제목 앞에 왕관 및 기업명 강조
                    break
            
            all_news.append([tier, state, title, date, source, link])
    
    # Tier(0이 대기업) 오름차순 정렬 후 날짜 내림차순 정렬
    sorted_news = sorted(all_news, key=lambda x: (x[0], x[3]), reverse=False)
    # 데이터프레임용으로 tier 열은 제거
    return [row[1:] for row in sorted_news]

# 3. 데이터 처리 및 대시보드 출력
with st.spinner('실시간 투자 데이터를 수집 중입니다...'):
    processed_data = fetch_tiered_news()
    df = pd.DataFrame(processed_data, columns=["주(State)", "뉴스 제목", "날짜", "출처", "Link"])

if not df.empty:
    # 대기업 소식 강조 알림
    major_hits = df[df['뉴스 제목'].str.contains("👑")].shape[0]
    if major_hits > 0:
        st.success(f"🔥 총 {major_hits}건의 주요 대기업 최신 동향이 감지되었습니다.")
    
    # 상황판 표 출력
    st.data_editor(
        df,
        column_config={
            "Link": st.column_config.LinkColumn(
                "원문 보기", 
                display_text="기사 링크",
                help="클릭 시 해당 뉴스의 원문 페이지로 이동합니다."
            )
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.warning("최근 7일간 5개 주에서 업데이트된 한국 기업 뉴스가 없습니다.")

st.markdown("---")
st.info("💡 이 상황판은 매일 자동으로 조지아, 테네시, 앨라배마, 사우스캐롤라이나, 플로리다 지역의 한국 대기업 투자를 우선 감지하여 업데이트합니다.")
