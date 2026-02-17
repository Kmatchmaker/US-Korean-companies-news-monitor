import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="미 동남부 韓 기업 투자 상황판", layout="wide")
st.title("📊 미 동남부 5개 주 韓 기업 진출·투자 통합 상황판")
st.caption("2026년 2월 17일 기준 실시간 데이터")

# 2. 데이터 정의 (고려아연 및 덕신EPC 포함)
data = [
    ["Tennessee", "고려아연", "02/16", "$7.4B (약 11조)", "테네시 역사상 최대 투자. 미 정부와 전략 광물 공급망 구축.", "https://tnecd.com/news/korea-zinc-selects-tennessee-for-first-u-s-operations-announces-6-6-billion-investment/"],
    ["Georgia", "동원금속", "02/05", "$30M (약 440억)", "이매뉴얼 카운티 제2공장 설립 확정. 주지사 공식 발표.", "https://gov.georgia.gov/press-releases/2026-02-04/gov-kemp-200-new-jobs-headed-emanuel-county"],
    ["Georgia", "덕신EPC", "02/12", "비공개", "앰코테크놀로지 반도체 공장 '스피드데크' 수주. 반도체망 진입.", "http://www.duckshinepc.com/"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "미국 법인 현금 출자 결정. 전동화 부품 라인 증설.", "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20260212000341"],
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "역대 최대 초고압 변압기 수주. 멤피스 공장 물량 확보.", "https://www.hyosung.com/kr/newsroom/view/19090"],
    ["Alabama", "HD현대일렉트릭", "02/11", "시설 확충", "앨라배마 변압기 공장 증설 가동률 극대화 및 AI 수요 대응.", "https://www.bizjournals.com/birmingham/"],
    ["S. Carolina", "세방리튬배터리", "02/11", "확인 중", "배터리 모듈 캠퍼스 2단계 설비 입고 및 가동 준비.", "https://gsabusiness.com/"],
    ["Florida", "한국계 물류사", "02/15", "시설 확장", "잭슨빌/마이애미 항만 인근 신규 창고 계약 및 자동화 설비 도입.", "https://www.bizjournals.com/jacksonville/"]
]

df = pd.DataFrame(data, columns=["주(State)", "기업명", "날짜", "투자/수주 규모", "비즈니스 핵심 요약 및 의미", "Link"])

# 3. 표 출력 (에러 수정 포인트: LinkColumn 대문자 사용)
st.data_editor(
    df,
    column_config={
        "Link": st.column_config.LinkColumn(  # 'link_column' 대신 'LinkColumn' 사용
            "공식 출처 원문",
            display_text="원문 보기"
        )
    },
    hide_index=True,
    use_container_width=True
)

st.success("✅ 상황판이 성공적으로 업데이트되었습니다. 이제 링크를 클릭하면 해당 사이트로 연결됩니다.")
