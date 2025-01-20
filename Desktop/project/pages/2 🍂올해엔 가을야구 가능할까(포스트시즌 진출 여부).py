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

# 현재 파일의 디렉토리 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))

# 모델 파일 경로 설정 (루트 디렉토리 기준으로 변경)
model_path = os.path.join(base_dir, "../rf_model.pkl")

 # 모델 로드
    with open(model_path, "rb") as file:
        model = pickle.load(file)

# 학습에 사용된 모든 feature 확인
all_features = model.feature_names_in_

# 사용자에게 입력받을 주요 변수와 기본값 설정
important_features_defaults = {
    '승률': 0.48,
    '승리횟수': 80.0,         # 시즌 승리 평균
    '세이브_횟수': 29.0,      # 시즌 평균 세이브 횟수
    '총_실점수': 800.0,       # 평균 실점
    '홈런횟수': 180.0,        # 시즌 평균 홈런
    '2루타횟수': 300.0,       # 시즌 평균 2루타
    '타자_삼진횟수': 1300.0   # 타자 삼진 평균
}

# Streamlit UI
st.title("🍂올해엔 가을야구 가능할까? : 포스트시즌 진출 여부 예측🍂")

# 열 나누기: 왼쪽과 오른쪽
left_col, right_col = st.columns(2)

# 왼쪽 열: 예측 기능
with left_col:
    st.header("[포스트시즌 진출 여부 예측]")
    inputs = {}
    for feature, default_value in important_features_defaults.items():
        inputs[feature] = st.number_input(f"{feature} 입력", min_value=0.0, value=default_value)

    if st.button("🤖바랩! 예측해줘!"):
        try:
            # 모든 feature를 0으로 초기화
            input_data = {feature: 0 for feature in all_features}

            # 입력받은 feature만 사용자 입력값으로 업데이트
            for feature, value in important_features_defaults.items():
                input_data[feature] = inputs[feature]

            # DataFrame 생성
            input_data_df = pd.DataFrame([input_data])

            # 동적 문구 컨테이너 생성
            progress_message = st.empty()

            # 로딩 메시지 업데이트
            for i in range(5):
                message = f"🤖바랩이 가을야구를 할 수 있을지 예측 중이에요{'.' * (i + 1)}"
                progress_message.text(message)  # 메시지 업데이트
                time.sleep(1)  # 1초 대기

            # 예측 수행
            prediction = model.predict(input_data_df)
            prob = model.predict_proba(input_data_df)[0][1]

            # 로딩 메시지 완료 문구로 교체
            progress_message.text("🤖바랩이 가을야구를 할 수 있을지 예측했어요!")

            # 결과 출력
            result = "🙆🏻‍♀️올해엔 포스트 시즌 진출 가능성이 높습니다!🙆🏻‍♂️" if prediction[0] == 1 else "🤦🏻‍♀️올해엔 포스트 시즌 진출 가능성이 낮습니다🤦🏻‍♂️"
            st.subheader(f"바랩이 예측한 결과는?: {result}")
            st.write(f"바랩이 예측한 진출 확률은 {prob*100:.2f}% 입니다!")

            # 간단한 분석
            st.subheader("📜바랩이 알려주는 포스트 시즌 진출이 어려운 이유 간단분석!📜:")
            if input_data['승률'] < 0.5:
                st.write("⚠️ 승률이 낮습니다. 더 많은 승리가 필요합니다.")
            if input_data['총_실점수'] > 700:
                st.write("⚠️ 총 실점수가 많습니다. 투수력 강화가 필요합니다.")
            if input_data['세이브_횟수'] < 30:
                st.write("⚠️ 세이브 횟수가 적습니다. 마무리 투수의 안정이 필요합니다.")
        except Exception as e:
            st.error(f"예측 중 오류 발생: {e}")



# 오른쪽 열: 설명
with right_col:
    st.header("[모델 설명]")
    st.markdown("""
    ### 🏆 **포스트시즌 진출 예측 모델이란?**
    이 모델은 팀의 주요 경기 데이터를 바탕으로 포스트시즌 진출 가능성을 예측하는 머신러닝 모델을 구현한 기능입니다. 
    승률, 승리 횟수, 홈런, 세이브 등 다양한 주요 지표를 입력하면 결과를 직관적으로 확인할 수 있습니다.

    ### 📊 **사용된 주요 데이터와 지표**
    - **승률:** 팀의 승리 비율을 나타냅니다. 경기 성과를 평가하는 핵심 지표입니다.
    - **홈런 수:** 공격력을 상징하는 대표적인 지표입니다.
    - **세이브 횟수:** 마무리 투수의 경기 마감 능력을 평가합니다.
    - **타자 생산력 지수:** 선수들의 전체적인 득점 기여도를 반영합니다.  
    이 외에도 다양한 팀 성과 데이터를 모델에 활용하여 정확도를 높였습니다.

    ### 🤖 **머신러닝 모델의 강점**
    - **예측 정확도:** 70% 이상의 데이터를 기반으로 훈련되어 높은 신뢰성을 제공합니다.
    - **팀 맞춤 분석:** 입력된 데이터를 기반으로 팀의 강점과 약점을 한눈에 분석할 수 있습니다.
    - **빠른 결과 도출:** 실시간으로 예측 결과를 확인할 수 있어 경기 전략에 즉시 반영 가능합니다.

    ### 🚀 **미래 활용 가능성**
    이 모델은 향후 팀의 연간 성적을 예측하거나 특정 선수의 성과를 추적하는 데 확장될 수 있습니다. 
    MLB 구단뿐만 아니라 다양한 스포츠 팀에서도 활용 가능한 데이터 기반 솔루션입니다.
    """)
