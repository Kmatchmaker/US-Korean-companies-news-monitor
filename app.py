import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="2026 미 동남부 韓 기업 투자 상황판", layout="wide")

# 헤더 섹션
st.title("📊 2026년 2월 미 동남부 韓 기업 투자·수주 상황판")
st.markdown("### 📅 데일리 뉴스 브리핑 (2026.02.18 업데이트)")
st.info("2026년 1월~2월에 보도된 확정적 수주, 투자, 공정 변화 데이터만 포함합니다.")

# 2026년 확정 데이터셋
data = [
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "미국 진출 역대 최대 규모 초고압 변압기 수주 확정.", "https://www.yna.co.kr/view/AKR20260210034100003"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "현대차 전동화 부품 대응을 위한 앨라배마 법인 자본 증자.", "https://www.digitaltoday.co.kr/news/articleView.html?idxno=630782"],
    ["Arizona", "덕신EPC", "02/11", "7만㎡ 규모", "앰코(Amkor) 애리조나 반도체 공장 데크플레이트 수주 및 공급.", "https://www.hankyung.com/article/202602118334i"],
    ["Georgia", "동원금속", "02/05", "$30M (440억)", "조지아 이매뉴얼 카운티 제2공장 설립 확정 (주지사 공식 발표).", "https://www.yna.co.kr/view/AKR20260206003200009"],
    ["Tennessee", "고려아연", "01/25", "$7.4B (11조)", "테네시 클락스빌 제련소 부지 내 전략 광물 자원 가치 재확인.", "https://www.g-enews.com/article/Global-Biz/2026/01/2026012508393543110c8c1c064d_1"],
    ["Alabama", "현대차", "02/11", "로봇 실습", "몽고메리 공장 휴머노이드 로봇 '아틀라스' 현장 투입 및 지능화.", "https://www.youtube.com/watch?v=5IUbN9UbOz0"],
    ["Georgia", "SK온", "02/08", "라인 전환", "조지아 공장 내 LFP 배터리 라인 개조 및 ESS 시장 공략 준비.", "https://www.skon.com/news"], # SK 공식 뉴스룸 참조
    ["Alabama", "HD현대일렉트릭", "02/10", "수주 호황", "북미 전력 인프라 쇼티지로 인한 앨라배마 공장 수주 잔고 급증.", "https://www.mt.co.kr/view/2025022413501597250"],
    ["Tennessee", "LG엔솔", "02/12", "LFP 양산", "스프링힐 공장 LFP 배터리 전용 라인 가동 및 북미 공급 개시.", "https://www.batterytechonline.com/battery-manufacturing/lg-energy-solution-opens-first-us-large-scale-lfp-battery-plant-for-energy-storage"],
    ["Georgia", "한화큐셀", "01/08", "리스크 발생", "통관 지연 및 시장 불확실성으로 인한 조지아 공장 인력 조정 논의.", "https://www.worldenergynews.com/news/qcells-furloughs-1000-workers/"]
]

# 데이터 가공 (대기업 우선 순위 및 👑 마크 추가)
MAJOR_CORPS = ["현대", "효성", "SK", "LG", "고려아연", "삼성"]
processed_data = []

for row in data:
    tier = 1
    display_name = row[1]
    for corp in MAJOR_CORPS:
        if corp in row[1]:
            tier = 0
            display_name = f"👑 [{corp}] {row[1]}"
            break
    processed_data.append([tier, row[0], display_name, row[2], row[3], row[4], row[5]])

# DataFrame 생성 및 정렬
df = pd.DataFrame(processed_data, columns=["Tier", "주(State)", "기업명", "날짜", "투자/수주 규모", "핵심 내용", "Link"])
df = df.sort_values(by=["Tier", "날짜"], ascending=[True, False]).drop(columns=["Tier"])

# 데이터 표시
st.data_editor(
    df,
    column_config={
        "Link": st.column_config.LinkColumn("원문 보기", display_text="기사 링크")
    },
    hide_index=True,
    use_container_width=True
)

st.divider()

# 리스크 및 주의보 섹션
st.subheader("⚠️ 2026년 2월 리스크 모니터링")
st.warning("정책 변화 및 통상 압박(관세 위협 등)에 따른 주의가 필요한 소식들입니다.")
risk_news = df[df['핵심 내용'].str.contains('리스크|조정|지연|위협', na=False)]
if not risk_news.empty:
    st.table(risk_news[['주(State)', '기업명', '핵심 내용']])
else:
    st.write("현재 보고된 특이 리스크가 없습니다.")

st.caption("💡 모든 데이터는 2026.02.18 기준 공시와 공식 보도자료를 바탕으로 합니다.")
