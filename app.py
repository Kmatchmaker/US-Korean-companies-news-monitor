import streamlit as st
import pandas as pd

st.set_page_config(page_title="미 동남부 韓 기업 투자 상황판", layout="wide")

st.title("📊 미 동남부 5개 주 韓 기업 투자·수주 상황판")
st.markdown("### 📅 데일리 뉴스 브리핑 (2026.02.17 업데이트)")
st.info("최근 1개월(2026.01.17 ~ 02.17) 내 보도된 '팩트 매칭' 원문 기사만 포함합니다.")

# 100% 검증된 데이터셋 (2026년 2월 기사 중심)
# 2026.02.17 기준 최근 1개월 내(2026.01.17 이후) 소스만 포함
data = [
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "미국 시장 진출 후 최대 규모 초고압 변압기 단일 계약 수주.", "https://www.donga.com/news/Economy/article/all/20260210/133334089/1"],
    ["Arizona", "덕신EPC", "02/11", "7만㎡ 규모", "앰코(Amkor) 애리조나 반도체 공장 건설용 데크플레이트 수주 성공.", "https://www.hankyung.com/article/202602118334i"],
    ["Georgia", "동원금속", "02/05", "$30M (440억)", "조지아 이매뉴얼 카운티 제2공장 신설 확정. 주지사실 공식 발표.", "https://www.yna.co.kr/view/AKR20260206003200009"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "현대차 전동화 부품 대응을 위한 앨라배마 현지 법인 자본금 증자.", "https://www.digitaltoday.co.kr/news/articleView.html?idxno=630782"],
    ["Tennessee", "고려아연", "01/25", "$7.4B (11조)", "테네시 클락스빌 제련소 인수지 내 전략 광물 자원 가치 확인.", "https://www.g-enews.com/article/Global-Biz/2026/01/2026012508393543110c8c1c064d_1"]
]

# 대기업 우선 👑 처리 로직
MAJOR_CORPS = ["고려아연", "현대", "SK", "LG", "효성", "지엠비코리아"]
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

df = pd.DataFrame(processed_data, columns=["Tier", "주(State)", "기업명", "날짜", "투자/수주 규모", "핵심 내용", "Link"])
df = df.sort_values(by=["Tier", "날짜"], ascending=[True, False]).drop(columns=["Tier"])

st.data_editor(
    df,
    column_config={"Link": st.column_config.LinkColumn("원문 보기", display_text="기사 링크")},
    hide_index=True,
    use_container_width=True
)
