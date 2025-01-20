# 필수 라이브러리 정리
import streamlit as st  # Streamlit 웹 애플리케이션 프레임워크
import pandas as pd  # 데이터 처리 및 분석을 위한 라이브러리
import numpy as np  # 수치 연산 및 배열 계산을 위한 라이브러리
import time  # 시간 제어 및 지연을 위한 기본 라이브러리
import pickle  # 머신러닝 모델 저장 및 로드를 위한 라이브러리
import joblib  # 머신러닝 모델 저장 및 로드 (Pickle의 대안)
import plotly.express as px  # 대화형 데이터 시각화를 위한 라이브러리
from streamlit_echarts import st_echarts  # Echarts 기반의 데이터 시각화 지원
import os  # 운영 체제 작업 (파일 경로, 디렉토리 작업 등)
import base64  # 데이터 인코딩 및 디코딩 (파일 다운로드 링크 생성 등에 사용)
import streamlit.components.v1 as components  # HTML/CSS/JS를 삽입하여 Streamlit 확장

# 페이지 설정
st.set_page_config(
    page_title="데이터톤 프로젝트",
    page_icon="⚾",  # 원하는 아이콘
    layout="wide"
)

# 사이드바 상단에 제목 추가
with st.sidebar:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"]::before {
            content: "⚾ 7조 데이터톤 프로젝트";
            font-size: 20px;
            font-weight: bold;
            margin-left: 10px;
            margin-top: 10px;
            display: block;
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# 팀 이름 매핑
team_name_mapping = {
    "CHN": "Chicago Cubs",
    "PHI": "Philadelphia Phillies",
    "PIT": "Pittsburgh Pirates",
    "CIN": "Cincinnati Reds",
    "SLN": "St. Louis Cardinals",
    "WAS": "Washington Nationals",
    "BOS": "Boston Red Sox",
    "CHA": "Chicago White Sox",
    "CLE": "Cleveland Indians",
    "DET": "Detroit Tigers",
    "NYA": "New York Yankees",
    "BAL": "Baltimore Orioles",
    "LAN": "Los Angeles Dodgers",
    "SFN": "San Francisco Giants",
    "LAA": "Los Angeles Angels",
    "MIN": "Minnesota Twins",
    "HOU": "Houston Astros",
    "NYN": "New York Mets",
    "ATL": "Atlanta Braves",
    "OAK": "Oakland Athletics",
    "KCA": "Kansas City Royals",
    "SDN": "San Diego Padres",
    "TEX": "Texas Rangers",
    "SEA": "Seattle Mariners",
    "TOR": "Toronto Blue Jays",
    "COL": "Colorado Rockies",
    "ARI": "Arizona Diamondbacks",
    "MIL": "Milwaukee Brewers",
    "TBA": "Tampa Bay Rays",
    "MIA": "Miami Marlins"
}

# 데이터 로드
data_path = '팀_성과_지표_시각화.csv'  # Replace with your file path
data = pd.read_csv(data_path)

# 팀 이름 매핑 적용
data['team_id'] = data['team_id'].map(team_name_mapping)

# 레이더 차트에 필요한 열 정의
columns_for_spider = ['SLG', 'OPS', 'era', 'WP', 'PAR', 'PARA', 'BA', 'OBP']

# 사이드바에서 팀 정보 선택
with st.sidebar:
    st.header("팀 선택")
    selected_year = st.selectbox("년도", options=sorted(data['year'].unique()), index=sorted(data['year'].unique()).index(1982), key="year")
    selected_league = st.selectbox("리그", options=data['league_id'].unique(), index=list(data['league_id'].unique()).index("AL"), key="league")
    available_teams = data[(data['year'] == selected_year) & (data['league_id'] == selected_league)]['team_id'].unique()
    selected_team = st.selectbox("팀", options=available_teams, index=0, key="team")

# 데이터 필터링
filtered_data = data[(data['year'] == selected_year) &
                     (data['league_id'] == selected_league) &
                     (data['team_id'] == selected_team)]

series_data = []

if not filtered_data.empty:
    values = [round(val, 3) for val in filtered_data[[col + '_diff' for col in columns_for_spider]].iloc[0].values.tolist()]
    series_data.append({
        "value": values,
        "name": f"{selected_team} ({selected_year})",
        "itemStyle": {"color": "#FF5733"},
        "lineStyle": {"color": "#FF5733"},
        "areaStyle": {"opacity": 0.2, "color": "#FF5733"}
    })

# Streamlit UI
st.title("🤔우리 팀의 부족한 점은 무엇일까?: 팀 성과지표 평가🤔")

# 두 열로 나누기
left_col, right_col = st.columns(2)



# 왼쪽 열: 레이더 차트
with left_col:
    st.header("[MLB 팀 성과 현황 지표]")
    # Echarts 옵션 설정
    option = {
        "title": {
            "text": f"{selected_team} ({selected_year}) 성과 지표",
        },
        "tooltip": {},
        "radar": {
            "indicator": [
                {"name": col, "max": 1, "min": -1} for col in columns_for_spider
            ]
        },
        "series": [
            {
                "name": "Team Performance",
                "type": "radar",
                "data": series_data
            }
        ]
    }

    # Streamlit에 그래프 표시
    st_echarts(options=option, height="500px")

    # "바랩! 분석해줘!" 버튼 추가
    if st.button("🤖바랩! 분석해줘!"):
        # 동적 문구 컨테이너 생성
        status_message = st.empty()

        # 분석 중 문구 표시
        status_message.markdown("**🤖바랩이 해당 팀의 성과지표를 분석중입니다...**")

        # 로딩바 구현
        progress_bar = st.progress(0)  # 진행률 초기화
        for percent in range(1, 101):  # 1%부터 100%까지
            time.sleep(0.05)  # 진행률 업데이트 간격 (0.05초)
            progress_bar.progress(percent)  # 진행률 업데이트

        # 로딩바 제거
        progress_bar.empty()

        # 분석 완료 문구 업데이트
        status_message.markdown("**🤖바랩이 해당 팀의 성과지표를 분석했어요!**")

        # 분석 결과 출력
        st.markdown("""
        ### 📋 전반적 제안
        1. **공격력 강화**: 
           - 장타력(SLG)과 출루율(OBP)을 동시에 개선하는 전략이 필요합니다.
           - 타자들의 훈련 프로그램 강화, 특히 선구안과 파워 향상에 초점을 맞추세요.

        2. **투수력 개선**:
           - ERA를 안정적으로 낮출 수 있는 불펜 및 선발 로테이션 강화가 필요합니다.
           - 경기 후반을 책임질 불펜 투수의 보강을 고려하세요.

        3. **전술적 개선**:
           - 클러치 상황에서 타격력을 높이고, 경기 전략을 더 세밀하게 구성하여 승률(WP)을 높이는 방안을 고려하세요.

        4. **선수 보강**:
           - 조정된 대체 가치(PARA)가 낮으므로 약점이 되는 포지션을 보강하거나 팀 내 균형을 맞추는 것이 중요합니다.
        """)


# 오른쪽 열: 설명
with right_col:
    st.header("[모델 설명]")
    st.markdown("""
    ### 📊 MLB 팀 성과 현황 지표 모델이란?
    이 모델은 MLB 팀의 성과 데이터를 바탕으로 팀 간의 주요 성과 지표를 시각적으로 비교할 수 있도록 설계되었습니다. 특히, 팀의 특정 연도 성과를 중심으로 **레이더 차트**를 통해 직관적인 비교를 제공합니다.

    #### 🔑 주요 기능
    1. 팀 간 성과 비교
    2. 시각적 이해 제공 (SLG, OPS, ERA 등 주요 지표 포함)
    3. 필터링 기능 (연도, 리그, 팀 이름으로 선택)

    #### 📋 주요 지표
    - **SLG (Slugging Percentage):** 타격 생산성을 측정하는 지표.
    - **OPS (On-base Plus Slugging):** 출루율과 장타율의 합.
    - **ERA (Earned Run Average):** 투수의 평균자책점.
    - **WP (Winning Percentage):** 승률.
    - **PAR/PARA:** 특정 상황에서 선수의 기여도.
    - **BA (Batting Average):** 타율.
    - **OBP (On-Base Percentage):** 출루율.

    #### 🚀 활용 가능성
    1. 특정 연도 팀의 강점과 약점을 분석하여 전략 수립.
    2. 상대 팀 비교를 통해 특정 지표에서의 상대적 우위 파악.
    3. 과거 데이터를 기반으로 팀 성과를 평가 및 개선 방향 도출.
    """)
