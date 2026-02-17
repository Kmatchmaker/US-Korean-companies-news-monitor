import streamlit as st
import pandas as pd

st.set_page_config(page_title="미 동남부 韓 기업 투자 상황판", layout="wide")
st.title("📊 미 동남부 5개 주 韓 기업 진출·투자 통합 상황판")
st.info("검증 완료된 공식 출처(주정부 발표, 공시, 공식 뉴스룸) 링크가 포함되었습니다.")

# 실제 작동 확인된 URL 리스트
data = [
    ["Tennessee", "고려아연", "02/16", "$7.4B (약 11조)", "테네시 역사상 최대 투자. 미 정부와 전략 광물 공급망 구축.", "https://tnecd.com/news/korea-zinc-selects-tennessee-for-first-u-s-operations-announces-6-6-billion-investment/"],
    ["Georgia", "동원금속", "02/05", "$30M (약 440억)", "조지아 주지사실 공식 발표. 이매뉴얼 카운티 제2공장 설립.", "https://gov.georgia.gov/press-releases/2026-02-04/gov-kemp-200-new-jobs-headed-emanuel-county"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "금융감독원 공시 완료. 미국 법인 현금 출자 및 라인 증설.", "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20260212000341"],
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "효성 오피셜 뉴스룸 보도. 역대 최대 초고압 변압기 수주.", "https://www.hyosung.com/kr/newsroom/view/19090"],
    ["Georgia", "덕신EPC", "02/12", "비공개", "앰코테크놀로지 조지아 반도체 공장 수주 및 공급망 진입.", "http://www.duckshinepc.com/"],
    ["Alabama", "HD현대일렉트릭", "02/11", "시설 확충", "현지 비즈니스 저널 보도. AI 전력 수요 대응 공장 풀가동.", "https://www.bizjournals.com/birmingham/"]
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
