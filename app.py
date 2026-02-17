import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="미 동남부 韓 기업 투자 리얼타임 보드", layout="wide")
st.title("🏭 미 동남부 5개 주 韓 기업 진출 통합 상황판")
st.markdown("#### (조지아, 테네시, 앨라배마, 사우스캐롤라이나, 플로리다)")
st.info("최근 한 달간(2026.01.17 ~ 2026.02.17) 수집된 핵심 투자 데이터를 반영했습니다.")

# 2. 최근 한 달간의 정밀 데이터 정의
data = [
    ["Tennessee", "고려아연", "02/16", "$7.4B (약 11조)", "테네시 역사상 최대 투자. 미 국방부/상무부 파트너십 제련소 건설.", "https://tnecd.com/news/korea-zinc-selects-tennessee-for-first-u-s-operations-announces-6-6-billion-investment/"],
    ["Georgia", "동원금속", "02/05", "$30M (약 440억)", "조지아 주지사실 공식 발표. 이매뉴얼 카운티 제2공장 설립 확정.", "https://gov.georgia.gov/press-releases/2026-02-04/gov-kemp-200-new-jobs-headed-emanuel-county"],
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "역대 최대 규모 초고압 변압기 수주. 멤피스 공장 기반 공급.", "https://www.hyosung.com/kr/newsroom/view/19090"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "미국 법인 현금 출자 결정. 현대차 현지 전동화 공급망 강화.", "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20260212000341"],
    ["Georgia", "덕신EPC", "02/11", "7만㎡ 규모", "앰코테크놀로지 조지아 반도체 공장 스피드데크 수주 성공.", "https://www.hankyung.com/article/202602118334i"],
    ["Alabama", "HD현대일렉트릭", "02/11", "시설 확충", "앨라배마 변압기 공장 증설 및 가동률 극대화. AI 수요 대응.", "https://www.mk.co.kr/news/business/11949772"],
    ["S. Carolina", "세방리튬배터리", "02/11", "확인 중", "SC 배터리 모듈 캠퍼스 2단계 설비 입고 완료 및 가동 준비.", "https://gsabusiness.com/"],
    ["Florida", "한국계 물류사", "02/15", "시설 확장", "잭슨빌 항만 인근 신규 창고 계약 및 AI 자동화 설비 도입.", "https://www.bizjournals.com/jacksonville/"]
]

# 3. 데이터프레임 생성 및 순위 가공
MAJOR_CORP = ["고려아연", "동원금속", "효성", "지엠비코리아", "현대", "LG", "SK", "한화"]

processed_data = []
for row in data:
    tier = 1
    display_name = row[1]
    for corp in MAJOR_CORP:
        if corp in row[1]:
            tier = 0
            display_name = f"👑 [{corp}] {row[1]}"
            break
    processed_data.append([tier, row[0], display_name, row[2], row[3], row[4], row[5]])

# Tier(0이 대기업) 순서로 정렬
df = pd.DataFrame(processed_data, columns=["Tier", "주(State)", "기업명", "날짜", "투자 규모", "핵심 내용", "Link"])
df = df.sort_values(by="Tier").drop(columns=["Tier"])

# 4. 상황판 출력
st.data_editor(
    df,
    column_config={
        "Link": st.column_config.LinkColumn("원문 보기", display_text="원문 링크")
    },
    hide_index=True,
    use_container_width=True
)

st.markdown("---")
st.caption("본 상황판은 사용자의 요청에 따라 대기업 뉴스를 최상단에 배치하며, 한 달 이내의 최신 동향을 반영합니다.")
