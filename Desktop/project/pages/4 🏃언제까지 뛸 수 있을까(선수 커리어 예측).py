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

# 모델 및 스케일러 로드
hitter_model = joblib.load("hitter_model.pkl")  # 타자 모델 파일
hitter_scaler = joblib.load("hitter_scaler.pkl")  # 타자 스케일러 파일
pitcher_model = joblib.load("pitcher_model.pkl")  # 투수 모델 파일
pitcher_scaler = joblib.load("pitcher_scaler.pkl")  # 투수 스케일러 파일

# Streamlit UI
st.title("🏃언제까지 뛸 수 있을까?: 선수 커리어 예측🏃")

# 페이지 열 나누기
left_col, right_col = st.columns(2)

# 왼쪽 열: 입력 및 예측 기능
with left_col:
    st.header("[선수 커리어 예측]")
    st.write("사용자가 입력한 정보를 기반으로 타자 또는 투수의 커리어를 예측합니다.")

    # 선수 유형 선택
    player_type = st.radio("선수 유형을 선택하세요:", ("타자", "투수"))

    if player_type == "타자":
        # 타자 입력 필드
        st.header("타자 정보 입력")
        games = st.number_input("통산 경기 (Career Games)", min_value=0, max_value=3000, value=1000)
        birth_year = st.number_input("출생 연도 (Birth Year)", min_value=1900, max_value=2025, value=1985)
        debut_age = st.number_input("데뷔 당시 나이 (Debut Age)", min_value=15, max_value=50, value=25)
        position_diversity = st.number_input("포지션 다양성 비율 (Position Diversity Ratio)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        year = st.number_input("연도 (Year)", min_value=1900, max_value=2025, value=2020)
        weight = st.number_input("몸무게 (Weight, kg)", min_value=40, max_value=150, value=80)
        last_game_days = st.number_input("마지막 경기 일수 (Days since last game)", min_value=0, max_value=10000, value=500)
        debut_days = st.number_input("데뷔 이후 경과 일수 (Days since debut)", min_value=0, max_value=20000, value=5000)
        height = st.number_input("키 (Height, cm)", min_value=140, max_value=220, value=180)
        last_game_month = st.number_input("마지막 경기 월 (Last Game Month)", min_value=1, max_value=12, value=6)

        # 사용자 입력값을 배열로 변환
        input_data = np.array([games, birth_year, debut_age, position_diversity, year,
                               weight, last_game_days, debut_days, height, last_game_month])

        # 모델이 요구하는 피처 수에 맞게 데이터 패딩
        hitter_features = 80  # 타자 모델이 요구하는 총 피처 수
        padded_data = np.zeros(hitter_features)  # 0으로 초기화된 배열 생성
        padded_data[:len(input_data)] = input_data  # 입력값으로 상위 데이터 채우기

        # 예측 버튼
        if st.button("🤖바랩! 예측해줘!"):
            # 결과 로딩 애니메이션
            progress_message = st.empty()
            for i in range(6):
                message = f"🤖바랩이 선수의 커리어를 예측 중이에요{'.' * i}"
                progress_message.text(message)
                time.sleep(1)

            # 입력 데이터를 스케일링
            scaled_data = hitter_scaler.transform([padded_data])
            # 모델 예측
            prediction = hitter_model.predict(scaled_data)

            # 결과 출력
            progress_message.text("🤖바랩이 커리어를 예측 했어요!")
            st.success(f"🤖바랩이 예측한 타자의 커리어 일수: {prediction[0]:.2f} 일")

    elif player_type == "투수":
        # 투수 입력 필드
        st.header("투수 정보 입력")
        innings_pitched = st.number_input("통산 투구 이닝 (Career Innings Pitched)", min_value=0.0, max_value=5000.0, value=1000.0)
        birth_year = st.number_input("출생 연도 (Birth Year)", min_value=1900, max_value=2025, value=1985)
        debut_age = st.number_input("데뷔 당시 나이 (Debut Age)", min_value=15, max_value=50, value=25)
        strikeouts = st.number_input("통산 삼진 개수 (Career Strikeouts)", min_value=0, max_value=5000, value=1000)
        wins = st.number_input("통산 승리 수 (Career Wins)", min_value=0, max_value=500, value=50)
        era = st.number_input("평균자책점 (ERA)", min_value=0.0, max_value=15.0, value=3.50, step=0.01)
        weight = st.number_input("몸무게 (Weight, kg)", min_value=40, max_value=150, value=80)
        last_game_days = st.number_input("마지막 경기 일수 (Days since last game)", min_value=0, max_value=10000, value=500)
        debut_days = st.number_input("데뷔 이후 경과 일수 (Days since debut)", min_value=0, max_value=20000, value=5000)
        height = st.number_input("키 (Height, cm)", min_value=140, max_value=220, value=180)

        # 사용자 입력값을 배열로 변환
        input_data = np.array([innings_pitched, birth_year, debut_age, strikeouts, wins,
                               era, weight, last_game_days, debut_days, height])

        # 모델이 요구하는 피처 수에 맞게 데이터 패딩
        pitcher_features = 67  # 투수 모델이 요구하는 총 피처 수
        padded_data = np.zeros(pitcher_features)  # 0으로 초기화된 배열 생성
        padded_data[:len(input_data)] = input_data  # 입력값으로 상위 데이터 채우기

        # 예측 버튼
        if st.button("🤖바랩! 예측해줘!"):
            # 결과 로딩 애니메이션
            progress_message = st.empty()
            for i in range(6):
                message = f"🤖바랩이 선수의 커리어를 예측 중이에요{'.' * i}"
                progress_message.text(message)
                time.sleep(1)

            # 입력 데이터를 스케일링
            scaled_data = pitcher_scaler.transform([padded_data])
            # 모델 예측
            prediction = pitcher_model.predict(scaled_data)

            # 결과 출력
            progress_message.text("🤖바랩이 선수의 커리어를 예측 했어요!")
            st.success(f"🤖바랩이 예측한 투수의 커리어 일수: {prediction[0]:.2f} 일")

# 오른쪽 열: 설명
with right_col:
    st.header("[모델 설명]")
    st.markdown("""
    ### 🏅 **선수 커리어 예측 모델이란?**
    이 모델은 선수의 주요 신체 및 경기 데이터를 기반으로, 타자 또는 투수의 전체 커리어 기간을 예측하는 머신러닝 기반 솔루션입니다.
    과거 데이터를 학습하여 선수의 잠재력을 수치화하고, 예상 커리어를 정량적으로 평가합니다.
    
    ### 📋 **사용된 주요 변수**
    - **통산 경기/투구 이닝:** 선수의 총 경기 및 투구 이닝 수.
    - **출생 연도:** 선수의 나이와 커리어의 상관관계를 평가합니다.
    - **데뷔 당시 나이:** 커리어 초기 환경과 연관된 변수입니다.
    - **포지션 다양성/투구 스타일:** 포지션 변경 및 역할의 다양성을 나타냅니다.
    - **신체 정보:** 키와 몸무게는 선수의 신체적 조건을 나타내며 커리어에 중요한 영향을 미칩니다.

    ### 🤖 **모델의 주요 특징**
    - **높은 예측 정확도:** 다양한 신체적 및 경기 데이터를 기반으로 신뢰성 높은 결과를 제공합니다.
    - **데이터 기반 통찰:** 입력된 데이터를 종합적으로 분석하여 선수의 강점과 약점을 평가합니다.
    - **맞춤형 피드백 제공:** 예측 결과와 함께 개선이 필요한 부분을 안내합니다.

    ### 🚀 **활용 가능성**
    이 모델은 특정 선수의 커리어 추적 외에도 팀 전체의 잠재력을 평가하거나 신인 드래프트에서 활용될 수 있는 혁신적인 도구입니다.
    """)
