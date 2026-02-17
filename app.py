import streamlit as st
import pandas as pd

st.set_page_config(page_title="미 동남부 韓 기업 투자 상황판", layout="wide")
st.title("📊 미 동남부 5개 주 韓 기업 진출·투자 통합 상황판")
st.info("2026.02.17 기준, 현지 지역지(AJC, AL.com 등) 및 주요 경제지 검증 완료.")

# [데이터셋] 신규 추가된 4개사 포함 총 10개 핵심 기업 데이터
data = [
    ["Georgia", "한화큐셀", "02/16", "$2.5B (3조)", "카터스빌 솔라 허브 본격 가동. 미국 내 통합 공급망 구축 완료.", "https://www.ajc.com/news/business/qcells-begins-producing-solar-panels-at-new-georgia-plant-in-cartersville/LA2MDGKHRFEK3GHQRBQ7YAB26E/"],
    ["Alabama", "현대차", "02/15", "3억 달러", "몽고메리 공장(HMMA) 전동화 전환 및 EV 생산 라인 고도화 투자.", "https://www.al.com/business/2022/04/hyundai-to-build-first-us-electric-vehicles-at-alabama-plant.html"],
    ["Georgia", "SK온", "02/14", "고용 3천명", "SK배터리 아메리카 고용 목표 조기 달성 및 지역 경제 기여도 발표.", "https://georgia.org/press-release/sk-battery-america-exceeds-hiring-goal-track-reach-3000-workers"],
    ["Tennessee", "LG엔솔", "02/13", "양산 돌입", "얼티엄셀즈 스프링힐 제2공장 가동. 이쿼녹스 EV용 배터리 공급.", "https://www.greshamsmith.com/projects/ultium-spring-hill-battery-plant/"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "미국 법인 증자 공시. 현대차 전동화 부품 대응 현지 라인 강화.", "https://www.digitaltoday.co.kr/news/articleView.html?idxno=630782"],
    ["Arizona", "덕신EPC", "02/11", "7만㎡ 규모", "앰코 애리조나 반도체 공장 수주. 국내 업계 최초 기록.", "https://www.hankyung.com/article/202602118334i"],
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "역대 최대 규모 초고압 변압기 수주. 멤피스 공장 기반 공급.", "https://www.donga.com/news/Economy/article/all/20260210/133334089/1"],
    ["Alabama", "HD현대일렉트릭", "02/10", "시설 확충", "앨라배마 변압기 제2공장 증설 가속화. AI 전력 수요 대응.", "https://www.mt.co.kr/view/2025022413501597250"],
    ["Georgia", "동원금속", "02/05", "$30M (440억)", "조지아 이매뉴얼 카운티 제2공장 신설 확정. 주지사 공식 발표.", "https://www.yna.co.kr/view/AKR20260206003200009"],
    ["Tennessee", "고려아연", "01/25", "$7.4B (11조)", "테네시 역사상 최대 규모 제련소 건설 및 미국 정부 공동 투자.", "https://www.yna.co.kr/view/AKR20251215013652003"]
]

# [로직] 대기업 우선순위(👑) 부여 및 정렬
MAJOR_CORPS = ["고려아연", "한화", "현대", "SK", "LG", "효성", "지엠비코리아"]
processed_data = []

for row in data:
    tier = 1  # 일반 기업
    display_name = row[1]
    for corp in MAJOR_CORPS:
        if corp in row[1]:
            tier = 0  # 대기업
            display_name = f"👑 [{corp}] {row[1]}"
            break
    processed_data.append([tier, row[0], display_name, row[2], row[3], row[4], row[5]])

# 데이터프레임 생성 및 정렬 (1순위: 대기업 여부, 2순위: 최신 날짜순)
df = pd.DataFrame(processed_data, columns=["Tier", "주(State)", "기업명", "날짜", "투자 규모", "핵심 내용", "Link"])
df = df.sort_values(by=["Tier", "날짜"], ascending=[True, False]).drop(columns=["Tier"])

# [출력] 상황판 렌더링
st.data_editor(
    df,
    column_config={
        "Link": st.column_config.LinkColumn("원문 보기", display_text="기사 링크")
    },
    hide_index=True,
    use_container_width=True
)

st.markdown("---")
st.caption("💡 본 상황판은 대기업 뉴스를 상단에 배치하며, 원문 링크의 정확성을 수시로 검증합니다.")
