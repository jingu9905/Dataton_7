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

# 사이드바: 팀 1 선택
with st.sidebar:
    st.header("첫 번째 팀 선택")
    # 팀 1 기본값 설정
    default_year_1 = 1982
    default_league_1 = "AL"
    default_team_1 = "Boston Red Sox"

    # 첫 번째 팀 선택 옵션
    selected_year_1 = st.selectbox("년도", options=sorted(data['year'].unique()), index=sorted(data['year'].unique()).index(default_year_1), key="year_1")
    selected_league_1 = st.selectbox("리그", options=data['league_id'].unique(), index=list(data['league_id'].unique()).index(default_league_1), key="league_1")
    available_teams_1 = data[(data['year'] == selected_year_1) & (data['league_id'] == selected_league_1)]['team_id'].unique()
    selected_team_1 = st.selectbox("팀", options=available_teams_1, index=list(available_teams_1).index(default_team_1), key="team_1")

# 사이드바: 팀 2 선택
with st.sidebar:
    st.header("두 번째 팀 선택")
    # 팀 2 기본값 설정
    default_year_2 = 1983
    default_league_2 = "AL"
    default_team_2 = "Boston Red Sox"

    # 두 번째 팀 선택 옵션
    year_range = list(range(default_year_1 - 5, default_year_1 + 6))
    available_years_2 = [year for year in year_range if year in data['year'].unique()]
    selected_year_2 = st.selectbox("년도", options=sorted(available_years_2), index=sorted(available_years_2).index(default_year_2), key="year_2")
    selected_league_2 = st.selectbox("리그", options=data['league_id'].unique(), index=list(data['league_id'].unique()).index(default_league_2), key="league_2")
    available_teams_2 = data[(data['year'] == selected_year_2) & (data['league_id'] == selected_league_2)]['team_id'].unique()
    selected_team_2 = st.selectbox("팀", options=available_teams_2, index=list(available_teams_2).index(default_team_2), key="team_2")

# 데이터 필터링
filtered_data_1 = data[(data['year'] == selected_year_1) &
                       (data['league_id'] == selected_league_1) &
                       (data['team_id'] == selected_team_1)]

filtered_data_2 = data[(data['year'] == selected_year_2) &
                       (data['league_id'] == selected_league_2) &
                       (data['team_id'] == selected_team_2)]

# 그래프 데이터 설정
series_data = []
if not filtered_data_1.empty:
    values_1 = [round(val, 3) for val in filtered_data_1[[col + '_diff' for col in columns_for_spider]].iloc[0].values.tolist()]
    series_data.append({
        "value": values_1,
        "name": f"{selected_team_1} ({selected_year_1})",
        "itemStyle": {"color": "#FF5733"},
        "lineStyle": {"color": "#FF5733"},
        "areaStyle": {"opacity": 0.2, "color": "#FF5733"}
    })

if not filtered_data_2.empty:
    values_2 = [round(val, 3) for val in filtered_data_2[[col + '_diff' for col in columns_for_spider]].iloc[0].values.tolist()]
    series_data.append({
        "value": values_2,
        "name": f"{selected_team_2} ({selected_year_2})",
        "itemStyle": {"color": "#3375FF"},
        "lineStyle": {"color": "#3375FF"},
        "areaStyle": {"opacity": 0.2, "color": "#3375FF"}
    })

# Echarts 옵션 설정
team1_label = f"{selected_team_1} ({selected_year_1})" if not filtered_data_1.empty else "팀1"
team2_label = f"{selected_team_2} ({selected_year_2})" if not filtered_data_2.empty else "팀2"

option = {
    "title": {
        "text": f"{team1_label} 성과지표 vs {team2_label} 성과지표",
        "left": "center",
        "textStyle": {"fontSize": 18, "fontWeight": "bold"}
    },
    "tooltip": {},  # 툴팁 추가
    "legend": {
        "data": [team1_label, team2_label],  # 범례에 팀 이름 추가
        "bottom": "0%",  # 범례 위치 (그래프 하단)
        "textStyle": {
            "fontSize": 14,
            "fontWeight": "bold"
        },
        "orient": "horizontal"  # 범례를 수평으로 표시
    },
    "radar": {
        "indicator": [{"name": col, "max": 1, "min": -1} for col in columns_for_spider]
    },
    "series": [
        {
            "name": "Team Comparison",
            "type": "radar",
            "data": series_data
        }
    ]
}


# Streamlit UI
st.title("🤔우리 팀의 부족한 점은 무엇일까?: 팀 성과 지표 비교평가🤔")

# 페이지 레이아웃
left_col, right_col = st.columns(2)

# 왼쪽 열: 레이더 차트 표시
with left_col:
    st.header("[MLB 팀 성과 비교 모델]")
    st_echarts(options=option, height="500px")

# 오른쪽 열: 모델 설명
with right_col:
    st.header("[모델 설명]")
    st.markdown("""
    ### 📊 MLB 팀 성과 비교 모델이란?
    이 모델은 MLB 팀의 성과 데이터를 바탕으로 **두 팀 간의 성과를 비교**할 수 있도록 설계되었습니다. 주요 성과 지표를 기반으로 팀 간의 강점과 약점을 시각적으로 파악할 수 있습니다.

    #### 🔑 주요 기능
    - **팀 간 비교**: 두 팀의 성과를 동일한 기준에서 분석 및 시각화.
    - **레이더 차트**: 주요 성과 지표(SLG, OPS, ERA 등)를 직관적으로 비교.
    - **유연한 필터링**: 연도, 리그, 팀을 독립적으로 선택 가능.

    #### 📋 주요 지표
    - **SLG (Slugging Percentage)**: 타격 생산성을 측정.
    - **OPS (On-base Plus Slugging)**: 출루율과 장타율의 합.
    - **ERA (Earned Run Average)**: 투수의 평균자책점.
    - **WP (Winning Percentage)**: 승률.
    - **PAR/PARA**: 특정 상황에서 선수의 기여도.
    - **BA (Batting Average)**: 타율.
    - **OBP (On-Base Percentage)**: 출루율.

    #### 🚀 활용 가능성
    - **팀 전략 수립**: 강점 및 약점 분석.
    - **상대 팀 비교**: 경기 전 상대 성과 파악.
    - **성과 평가**: 과거 데이터를 기반으로 개선 방향 제시.
    """)

