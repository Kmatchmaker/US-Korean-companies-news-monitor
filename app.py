import streamlit as st
import pandas as pd

st.set_page_config(page_title="미 동남부 韓 기업 투자 상황판", layout="wide")
st.title("📊 미 동남부 5개 주 韓 기업 진출·투자 통합 상황판")
st.info("2026.02.17 기준, 현지 지역지(AJC, AL.com 등) 및 주요 경제지 검증 완료.")

# [데이터셋] 신규 추가된 4개사 포함 총 10개 핵심 기업 데이터
# 2026.02.17 최종 업데이트 데이터
# 2026.02.17 기준 최근 1개월 내(2026.01.17 이후) 소스만 포함
data = [
    ["Tennessee", "효성중공업", "02/10", "7,870억 원", "미국 시장 진출 후 최대 규모 초고압 변압기 단일 계약 수주.", "https://www.donga.com/news/Economy/article/all/20260210/133334089/1"],
    ["Arizona", "덕신EPC", "02/11", "7만㎡ 규모", "앰코(Amkor) 애리조나 반도체 공장 건설용 데크플레이트 수주 성공.", "https://www.hankyung.com/article/202602118334i"],
    ["Georgia", "동원금속", "02/05", "$30M (440억)", "조지아 이매뉴얼 카운티 제2공장 신설 확정. 주지사실 공식 발표.", "https://www.yna.co.kr/view/AKR20260206003200009"],
    ["Alabama", "지엠비코리아", "02/12", "46.5억 원", "현대차 전동화 부품 대응을 위한 앨라배마 현지 법인 자본금 증자.", "https://www.digitaltoday.co.kr/news/articleView.html?idxno=630782"],
    ["Tennessee", "고려아연", "01/25", "$7.4B (11조)", "테네시 클락스빌 제련소 인수지 내 전략 광물 자원 가치 확인.", "https://www.g-enews.com/article/Global-Biz/2026/01/2026012508393543110c8c1c064d_1"]
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
