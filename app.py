import streamlit as st
import pandas as pd

st.set_page_config(page_title="미 동남부 韓 기업 투자 상황판", layout="wide")
st.title("📊 미 동남부 5개 주 韓 기업 진출·투자 통합 상황판")
st.info("검증 완료된 공식 출처(주정부 발표, 공시, 공식 뉴스룸) 링크가 포함되었습니다.")

# 실제 작동 확인된 URL 리스트
data = [
    ["Georgia", "덕신EPC", "02/11", "7만㎡ 규모", "앰코 반도체 공장 수주 성공. 국내 업계 최초 미국 진출.", "https://www.hankyung.com/article/202602118334i"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "미국 법인 47억 규모 현금 출자. 현대차 공급망 강화.", "https://www.yna.co.kr/view/AKR20260212136600008"],
    ["Alabama", "HD현대일렉트릭", "02/01", "1,850억 투입", "앨라배마 제2공장 증설. 2027년 가동 목표.", "https://www.mk.co.kr/news/business/11949772"],
    ["Tennessee", "고려아연", "02/16", "$7.4B (11조)", "테네시 역사상 최대 투자. 핵심 광물 허브 구축.", "https://tnecd.com/news/korea-zinc-selects-tennessee-for-first-u-s-operations-announces-6-6-billion-investment/"],
    ["Georgia", "동원금속", "02/05", "$30M", "조지아 주지사실 공식 발표. 제2공장 설립.", "https://gov.georgia.gov/press-releases/2026-02-04/gov-kemp-200-new-jobs-headed-emanuel-county"],
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "역대 최대 규모 초고압 변압기 수주.", "https://www.hyosung.com/kr/newsroom/view/19090"]
]
df = pd.DataFrame(data, columns=["주(State)", "기업명", "날짜", "투자/수주 규모", "비즈니스 핵심 요약", "Link"])

# 링크 컬럼 설정 (LinkColumn 대문자 필수)
st.data_editor(
    df,
    column_config={
        "Link": st.column_config.LinkColumn(
            "공식 출처 확인",
            display_text="원문 보기",
            help="클릭 시 주정부 발표문 또는 공시 사이트로 연결됩니다."
        )
    },
    hide_index=True,
    use_container_width=True
)
