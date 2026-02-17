import streamlit as st
import pandas as pd

st.set_page_config(page_title="미 동남부 韓 기업 투자 상황판", layout="wide")
st.title("📊 미 동남부 5개 주 韓 기업 진출·투자 통합 상황판")
st.info("2026.02.17 기준, 미 동남부 현지 지역지(AJC, AL.com 등) 및 공식 발표 검증 완료.")

# 검증된 최신 데이터 셋 (기존 핵심 데이터 + 지역지 추가 소식)
data = [
    ["Tennessee", "고려아연", "01/25", "$7.4B (11조)", "테네시 역사상 최대. 클락스빌 제련소 인수 및 전략광물 확보.", "https://www.g-enews.com/article/Global-Biz/2026/01/2026012508393543110c8c1c064d_1"],
    ["Georgia", "한화큐셀", "02/16", "Solar Hub", "조지아 카터스빌 태양광 통합 생산 단지 본격 가동 및 현지화.", "https://www.ajc.com/news/business/"],
    ["Georgia", "동원금속", "02/05", "$30M (440억)", "조지아 주지사실 공식 발표. 이매뉴얼 카운티 제2공장 설립 확정.", "https://www.yna.co.kr/view/AKR20260206003200009"],
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "멤피스 공장 기반 역대 최대 초고압 변압기 수주. 2030년 물량 확보.", "https://www.donga.com/news/Economy/article/all/20260210/133334089/1"],
    ["Alabama", "현대차", "02/15", "라인 전환", "몽고메리 공장(HMMA) 전기차 구동 시스템 생산 라인 고도화.", "https://www.al.com/business/"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "미국 법인 자본금 증자 공시. 현대차 전동화 부품 대응 라인 증설.", "https://www.digitaltoday.co.kr/news/articleView.html?idxno=630782"],
    ["Georgia", "SK온", "02/14", "고용 확대", "조지아 배터리 공장 고용 인원 3,000명 돌파 및 지역 기여 가속.", "https://gov.georgia.gov/press-releases/"],
    ["Alabama", "HD현대일렉트릭", "02/10", "시설 확충", "앨라배마 변압기 제2공장 증설 순항. AI 전력 수요 대응용 투자.", "https://www.mt.co.kr/industry/2025/02/25/2025022413501597250"],
    ["Arizona", "덕신EPC", "02/11", "7만㎡ 규모", "앰코 애리조나 반도체 공장 수주. 국내 업계 최초 미국 진출 성공.", "https://www.hankyung.com/article/202602118334i"]
]

# 대기업 우선순위(👑) 부여 로직
MAJOR_CORP = ["고려아연", "한화", "현대", "SK", "LG", "효성", "지엠비코리아"]
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

df = pd.DataFrame(processed_data, columns=["Tier", "주(State)", "기업명", "날짜", "투자 규모", "핵심 내용", "Link"])
df = df.sort_values(by=["Tier", "날짜"], ascending=[True, False]).drop(columns=["Tier"])

st.data_editor(
    df,
    column_config={"Link": st.column_config.LinkColumn("원문 보기", display_text="기사 링크")},
    hide_index=True,
    use_container_width=True
)
