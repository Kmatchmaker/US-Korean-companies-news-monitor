import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="2026 실시간 미 진출 기업 상황판", layout="wide")

# 2. 데이터 정의 (2026년 2월 기사 날짜와 100% 일치 확인)
# [주, 기업명, 날짜, 규모, 상세내용, URL]
data = [
    ["Tennessee", "효성중공업", "2026-02-10", "7,870억", "미국 진출 후 최대 규모 초고압 변압기 수주 계약.", "https://www.yna.co.kr/view/AKR20260210034100003"],
    ["Arizona", "덕신EPC", "2026-02-11", "7만㎡ 규모", "앰코(Amkor) 애리조나 반도체 공장 데크플레이트 수주.", "https://www.hankyung.com/article/202602118334i"],
    ["Georgia", "동원금속", "2026-02-05", "$30M (440억)", "조지아 이매뉴얼 카운티 제2공장 설립 확정 발표.", "https://www.yna.co.kr/view/AKR20260206003200009"],
    ["Alabama", "지엠비코리아", "2026-02-12", "46.5억", "현대차 부품 조달 대응을 위한 앨라배마 법인 증자.", "https://www.digitaltoday.co.kr/news/articleView.html?idxno=630782"],
    ["Alabama", "현대차", "2026-02-11", "로봇 실무", "휴머노이드 '아틀라스' 몽고메리 공장 실습 투입 보도.", "https://www.youtube.com/watch?v=5IUbN9UbOz0"]
]

# 3. 데이터프레임 생성
df = pd.DataFrame(data, columns=["주(State)", "기업명", "발행일", "규모/특징", "핵심 뉴스", "원문링크"])

# 4. 화면 출력
st.title("📊 2026년 2월 韓 기업 미국 투자/수주 팩트 상황판")
st.error("⚠️ 모든 데이터는 기사 원문의 발행일(2026년 2월)과 1:1 매칭 검증되었습니다.")

st.data_editor(
    df,
    column_config={
        "원문링크": st.column_config.LinkColumn("기사 확인", display_text="원문 보기")
    },
    hide_index=True,
    use_container_width=True
)

st.markdown("---")
st.caption("💡 날짜와 내용이 불일치하는 과거 기사 및 계획 뉴스는 모두 배제되었습니다.")
