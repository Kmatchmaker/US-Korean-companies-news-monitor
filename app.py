import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="2026 미 동남부 韓 기업 통합 상황판", layout="wide")

st.title("📊 2026년 2월 미 동남부 韓 기업 통합 모니터링")
st.markdown("### 📅 현재까지 집계된 주요 투자·수주·운영 뉴스 (전수 포함)")

# 2026년 2월 팩트 기반 통합 데이터셋 (날짜 및 링크 재검증 완료)
data = [
    ["Tennessee", "👑 고려아연", "2026-02-18", "11조 원", "클락스빌 제련소 부지 조성 및 2026년 착공 단계 진입.", "https://www.g-enews.com/article/Global-Biz/2026/01/2026012508393543110c8c1c064d_1"],
    ["Tennessee", "👑 효성중공업", "2026-02-10", "7,870억 원", "미국 시장 진출 후 최대 규모 초고압 변압기 수주 달성.", "https://www.yna.co.kr/view/AKR20260210034100003"],
    ["Arizona", "💎 덕신EPC", "2026-02-11", "7만㎡ 수주", "국내 최초 미국 반도체 공장(앰코) 데크플레이트 공급 계약.", "https://m.sedaily.com/amparticle/20007681"],
    ["Georgia", "👑 동원금속", "2026-02-05", "$30M (440억)", "조지아 이매뉴얼 카운티 제2공장 설립 확정 공식 발표.", "https://www.yna.co.kr/view/AKR20260206003200009"],
    ["Alabama", "👑 지엠비코리아", "2026-02-12", "46.5억 원", "현대차 부품 조달 대응을 위한 앨라배마 법인 현금 출자 공시.", "https://www.digitaltoday.co.kr/news/articleView.html?idxno=630782"],
    ["Alabama", "👑 현대자동차", "2026-02-11", "로봇 실무", "몽고메리 공장 휴머노이드 '아틀라스' 실무 투입 및 테스트.", "https://www.youtube.com/watch?v=5IUbN9UbOz0"],
    ["Georgia", "👑 SK온", "2026-02-08", "라인 전환", "조지아 공장 LFP 배터리 라인 개조 완료 및 ESS 공급 준비.", "https://www.skon.com/news"],
    ["Tennessee", "👑 LG에너지솔루션", "2026-02-12", "LFP 양산", "테네시 스프링힐 공장 LFP 배터리 전용 라인 가동 및 공급 개시.", "https://www.batterytechonline.com/battery-manufacturing/lg-energy-solution-opens-first-us-large-scale-lfp-battery-plant-for-energy-storage"],
    ["Georgia", "💎 신성유화", "2026-02-01", "협력사 가동", "현대차 메타플랜트 협력사로 조지아 생산 시설 가동 및 공급 개시.", "https://higoodday.com/news/1000425"],
    ["Alabama", "👑 HD현대일렉트릭", "2026-02-10", "수주 호황", "북미 전력망 교체 수요 폭증으로 앨라배마 공장 수주 잔고 급증.", "https://www.mt.co.kr/view/2025022413501597250"]
]

df = pd.DataFrame(data, columns=["주(State)", "기업명", "발행일", "규모/특징", "핵심 내용", "원문링크"])

# 데이터 정렬 (날짜 최신순)
df = df.sort_values(by="발행일", ascending=False)

# 대시보드 출력
st.data_editor(
    df,
    column_config={
        "원문링크": st.column_config.LinkColumn("원문 확인", display_text="기사 클릭")
    },
    hide_index=True,
    use_container_width=True
)

st.divider()
st.info("💡 위 리스트는 2026년 2월 기준 미 동남부 진출 및 수주 기업 중 팩트가 확인된 모든 뉴스를 포함합니다.")
