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

# 각 컬럼의 평균값 (임의 데이터로 설정)
hitter_avg_values = np.full(80, 100.0)  # 타자: 모델이 요구하는 80개의 피처 평균값
pitcher_avg_values = np.full(67, 50.0)  # 투수: 모델이 요구하는 67개의 피처 평균값

# Streamlit UI
st.title("💰올해는 얼마나 받을 수 있을까?: 야구선수 연봉 예측💰")

if "연봉 예측":
    # 열 나누기
    left_col, right_col = st.columns(2)

    # 왼쪽 열: 입력 및 예측 기능
    with left_col:
        st.header("[선수 연봉 예측 앱]")
        st.write("사용자가 입력한 정보를 기반으로 타자 또는 투수의 연봉을 예측합니다.")

        # 선수 유형 선택
        player_type = st.radio("선수 유형을 선택하세요:", ("타자", "투수"))

        if player_type == "타자":
            # 타자 입력 필드
            st.header("타자 정보 입력")
            hits = st.number_input("볼넷 횟수 (Walks)", min_value=0.0, max_value=500.0, value=50.0)
            strikeouts = st.number_input("삼진 횟수 (Strikeouts)", min_value=0.0, max_value=500.0, value=50.0)
            homeruns = st.number_input("홈런 (Home Runs)", min_value=0.0, max_value=100.0, value=10.0)
            stolen_bases = st.number_input("도루 성공 횟수 (Stolen Bases)", min_value=0.0, max_value=100.0, value=20.0)
            caught_stealing = st.number_input("도루 실패 횟수 (Caught Stealing)", min_value=0.0, max_value=100.0, value=5.0)
            games = st.number_input("경기수 (Games)", min_value=0.0, max_value=300.0, value=50.0)
            at_bats = st.number_input("타석수 (At Bats)", min_value=0.0, max_value=300.0, value=50.0)
            slugging = st.number_input("장타율 (Slugging Percentage)", min_value=0.0, max_value=1.0, value=0.5)
            avg = st.number_input("타율 (Batting Average)", min_value=0.0, max_value=1.0, value=0.3)
            on_base = st.number_input("출루율 (On Base Percentage)", min_value=0.0, max_value=1.0, value=0.4)

            # 사용자 입력값을 배열로 변환
            input_data = hitter_avg_values.copy()  # 평균값으로 초기화
            input_data[:10] = [hits, strikeouts, homeruns, stolen_bases, caught_stealing, games, at_bats, slugging, avg, on_base]

            # 예측 버튼
            if st.button("🤖바랩! 예측해줘!", key="hitter_predict"):
                # 결과 로딩 애니메이션
                progress_message = st.empty()
                for i in range(5):
                    message = f"🤖바랩이 연봉을 얼마나 받을 수 있을지 예측 중이에요{'.' * (i + 1)}"
                    progress_message.text(message)
                    time.sleep(1)

                # 입력 데이터를 스케일링
                scaled_data = hitter_scaler.transform([input_data])

                # 모델 예측
                prediction = hitter_model.predict(scaled_data)

                # 최종 메시지 및 결과 출력
                progress_message.text("🤖바랩이 연봉을 얼마나 받을 수 있을지 예측 했어요!")
                st.success(f"🤖바랩이 예측한 타자의 연봉은: ${int(prediction[0]):,},000")

        elif player_type == "투수":
            # 투수 입력 필드
            st.header("투수 정보 입력")
            era = st.number_input("평균자책점 (ERA)", min_value=0.0, max_value=10.0, value=2.30)
            whip = st.number_input("WHIP (Walks + Hits per Inning Pitched)", min_value=0.0, max_value=2.0, value=0.95)
            k_bb = st.number_input("삼진/볼넷 비율 (K/BB)", min_value=0.0, max_value=10.0, value=5.00)
            innings = st.number_input("투구 이닝 (Innings Pitched)", min_value=0.0, max_value=300.0, value=220.0)
            saves = st.number_input("세이브 (Saves)", min_value=0.0, max_value=50.0, value=20.0)
            strikeouts = st.number_input("삼진 (Strikeouts)", min_value=0.0, max_value=300.0, value=210.0)

            # 사용자 입력값을 배열로 변환
            input_data = pitcher_avg_values.copy()  # 평균값으로 초기화
            input_data[:6] = [era, whip, k_bb, innings, saves, strikeouts]

            # 예측 버튼
            if st.button("🤖바랩! 예측해줘!", key="pitcher_predict"):
                # 결과 로딩 애니메이션
                progress_message = st.empty()
                for i in range(5):
                    message = f"🤖바랩이 연봉을 얼마나 받을 수 있을지 예측 중이에요{'.' * (i + 1)}"
                    progress_message.text(message)
                    time.sleep(1)

                # 입력 데이터를 스케일링
                scaled_data = pitcher_scaler.transform([input_data])

                # 모델 예측
                prediction = pitcher_model.predict(scaled_data)

                # 최종 메시지 및 결과 출력
                progress_message.text("🤖바랩이 연봉을 얼마나 받을 수 있을지 예측 했어요!")
                st.success(f"🤖바랩이 예측한 투수의 연봉은: ${int(prediction[0]):,},000")

# 오른쪽 열: 설명
with right_col:
    st.header("[모델 설명]")
    st.markdown(
        """
        ### 📊 MLB 팀 성과 비교 모델이란?
        이 모델은 타자 또는 투수의 주요 성과 데이터를 입력받아 선수의 연봉을 예측하는 머신러닝 기반 애플리케이션입니다.
        사용자가 제공한 성과 지표를 분석하여 해당 선수의 가치(예상 연봉)를 추정하며, 데이터 분석과 시각화를 통해 추가적인 통찰을 제공합니다.

        #### 🔑 주요 기능
        - **선수 유형 선택**: 타자 또는 투수를 선택할 수 있으며, 해당 포지션에 적합한 입력 필드가 제공됩니다.
        - **연봉 예측**: 사용자가 입력한 성과 데이터를 기반으로 머신러닝 모델이 연봉을 예측하며, 결과는 실시간으로 표시됩니다.
        - **성과 지표 분석**: 선수의 주요 지표(예: 홈런, 타율, 삼진 등)를 기반으로 강점과 약점을 분석하여 연봉에 미친 영향을 제공합니다.
        - **결과 시각화 및 비교**: 입력 데이터를 시각화하거나 다른 선수와 비교하는 추가적인 기능을 제공합니다.

        #### 📋 입력 필드
        - **타자**: 볼넷, 삼진, 홈런, 도루 성공/실패, 경기수, 타석수, 장타율, 타율, 출루율.
        - **투수**: 평균자책점, WHIP, 삼진/볼넷 비율, 투구 이닝, 세이브, 삼진.

        #### 🚀 활용 가능성
        - **스카우팅 및 계약 협상**: 선수의 성과 데이터를 기반으로 연봉 추정치를 제공하여 공정한 계약 협상을 돕습니다.
        - **팀 전략 수립**: 팀 내에서 각 선수의 가치를 정량적으로 평가하여 자원 배분에 대한 통찰을 제공합니다.
        - **데이터 기반 분석**: 선수의 강점과 약점을 명확히 파악하여 훈련 방향을 설정하는 데 기여합니다.
        """
    )
