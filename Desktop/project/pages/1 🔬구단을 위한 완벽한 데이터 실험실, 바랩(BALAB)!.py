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


# 사이드바 네비게이션
st.sidebar.title("📄 기획서 목차")
menu = st.sidebar.radio(
    "궁금한 부분을 선택해 주세요😉:",
    ["바랩(BALAB)", "프로젝트 개요", "대상", "분석 목적", "목표 및 기대 효과", "데이터 수집 및 전처리", "모델 개발 및 성능 평가", "프로젝트 일정", "결론", "팀원 소개 및 역할"]
)

# 각 섹션별 내용 표시
if menu == "바랩(BALAB)":
    

    # Base64로 이미지 변환 함수
    def image_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    
    # 이미지 파일 경로 설정
    # 현재 파일 기준 디렉토리 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # images 폴더 경로 설정
    image_folder = os.path.join(base_dir, "../images")

    image_files = [
        "001.png",  # 첫 번째 이미지
        "002.png",  # 두 번째 이미지
        "003.png",  # 세 번째 이미지
        
    ]
    image_files = [os.path.join(image_folder, f) for f in image_files]
    
    # HTML로 이미지 슬라이더 생성
    slider_html = f"""
    <div style="display: flex; align-items: center; justify-content: center; padding: 100px;">
      <div style="max-width: 891px; max-height: 1260px; border: 2px solid #ddd; border-radius: 10px; overflow: hidden;">
        <div class="slideshow-container">
            {''.join(f'''
            <div class="mySlides fade">
                <img src="data:image/png;base64,{image_to_base64(img)}" style="width: 100%; height: auto; object-fit: contain;">
                <div class="caption">{caption}</div>
            </div>
            ''' for img, caption in zip(image_files, ['"연봉?그거_어떻게_아는건데_바랩(BALAB)_포스터"', '"이_선수_계속_뛸_수_있을까?_바랩(BALAB)_포스터"', '"올해_안엔_가을야구_가능할까?_바랩(BALAB)_포스터"', "네 번째 이미지 캡션"]))}
        </div>
      </div>
    </div>

    <style>
    .slideshow-container {{
      position: relative;
      max-width: 700px; /* 컨테이너 너비를 제한 */
      margin: auto;
    }}

    .mySlides {{
      display: none;
      text-align: center; /* 캡션을 중앙 정렬 */
    }}

    .fade {{
      -webkit-animation-name: fade;
      -webkit-animation-duration: 1.5s;
      animation-name: fade;
      animation-duration: 1.5s;
    }}

    @-webkit-keyframes fade {{
      from {{opacity: .4}} 
      to {{opacity: 1}}
    }}

    @keyframes fade {{
      from {{opacity: .4}} 
      to {{opacity: 1}}
    }}

    .slideshow-container img {{
      border-radius: 10px;
    }}

    .caption {{
      background-color: rgba(0, 0, 0, 0.5); /* 반투명한 검정 배경 */
      color: white; /* 텍스트 색상 */
      padding: 10px;
      font-size: 16px;
      position: absolute;
      bottom: 0; /* 이미지 하단에 배치 */
      width: 100%; /* 캡션 너비를 이미지에 맞춤 */
      text-align: center; /* 중앙 정렬 */
      box-sizing: border-box; /* 패딩 포함 크기 계산 */
    }}
    </style>

    <script>
    var slideIndex = 0;
    showSlides();

    function showSlides() {{
      var i;
      var slides = document.getElementsByClassName("mySlides");
      for (i = 0; i < slides.length; i++) {{
        slides[i].style.display = "none";
      }}
      slideIndex++;
      if (slideIndex > slides.length) {{slideIndex = 1}}
      slides[slideIndex-1].style.display = "block";
      setTimeout(showSlides, 5000); // Change image every 5 seconds
    }}
    </script>
    """

    
    # 레이아웃 구성
    st.title("⚾구단을 위한 완벽한 데이터 실험실, 바랩(BALAB)!⚾")
    
    # 두 열로 나누기
    col1, col2 = st.columns([1, 1.3])
    
    # 첫 번째 열: 이미지 슬라이더
    with col1:
        components.html(slider_html, height=1260, width=891)  # 슬라이더 컨테이너 크기
    
    # 두 번째 열: 본문 내용
    with col2:
        # 상단 공백 추가
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """

            ### 🖥️구단을 위한 단 하나의 통합 서비스 플랫폼, 바랩(BALAB)!  
            **BALAB**은 **Baseball LAB**의 약자로, 구단의 모든 데이터를 분석하고 예측하는 완벽한 실험실 같은 플랫폼입니다.  
            저희 바랩(BALAB)이 추구하는 미션에는 저희만의 유쾌한 바람이 담겨 있습니다:
    
            - **연봉 협상, 잘 되기를 "바랩"**: 
              데이터를 통해 공정하고 신뢰할 수 있는 연봉 협상을 지원합니다.  
    
            - **올해도 우리 팀에 있기를 "바랩"**: 
              선수와 구단의 상호 신뢰를 데이터 기반으로 강화하여 장기적인 팀 구성을 돕습니다.  
    
            - **오래오래 뛸 수 있기를 "바랩"**:
              선수의 커리어를 데이터로 관리하여 지속 가능한 성장을 지원합니다.
            """
        ) 
        
        st.markdown(
            """      
            ### ⚙️바랩(BALAB)이 제공하는 주요 기능
            - **선수 연봉 예측**: 성과 데이터를 기반으로 공정한 연봉 책정을 제안.  
            - **포스트 시즌 진출 가능성 분석**: 팀의 성과를 다각도로 분석하여 시즌 전략 수립.  
            - **커리어 기간 예측**: 선수의 커리어 지속 가능성을 정량적으로 평가.  
            - **구단 운영 최적화**: 데이터 기반으로 팀 성과와 재정적 효율성 극대화.
    
            ### ⚾바랩(BALAB)과 함께 데이터로 구단의 미래를 만들어보세요!
            """
        )

       # 첫 번째 그림 삽입 (크기 줄이기)
        st.markdown(
            """      
            ##### 🙋🏻‍♂️참고로 바랩(BALAB)은 로고도 귀엽답니다!🙋🏻‍♀️
            """
        )

        st.image(
        "images/005.png",  # 이미지 경로
        caption="구단을 위한 완벽한 데이터 실험실, BALAB!",  # 이미지 캡션
        width=700,  # 이미지 너비 설정
        use_container_width=False  # 컨테이너 너비 사용 여부
        )        
        
        

else:
    # Streamlit 메인 화면 제목
    st.title("⚾ MLB 데이터 분석 프로젝트")

    if menu == "프로젝트 개요":
        st.title("📌 프로젝트 개요")

    # MLB 리그의 성장과 문제점
        st.markdown("#### **MLB 리그의 성장과 그에 따른 문제점**")
        st.markdown(
        """
        MLB(메이저리그 베이스볼)는 매년 전 세계적으로 수억 명 이상의 팬을 보유하며, 경기의 질 향상과 글로벌 시장 확장을 목표로 막대한 자원을 투자하고 있는 글로벌 스포츠 리그입니다.  
        하지만 리그의 성장과 함께 몇 가지 주요 문제가 대두되고 있습니다:

        1. **선수 계약 규모의 증가와 재정적 부담**  
            - MLB 구단들은 선수 계약 규모가 지속적으로 증가하면서 예측 가능한 데이터를 활용한 공정한 연봉 책정 및 팀 구성의 중요성이 점점 더 부각되고 있습니다.  
            - 특히, 고액 연봉을 받는 선수들이 기대 이하의 성과를 보이는 경우(일명 **‘먹튀 논란’**)에는 팀의 재정적 손실뿐 아니라 팬들과의 신뢰 관계에도 부정적인 영향을 미치고 있습니다.

        2. **경쟁 구단 간 격차 심화**  
            - 리그 내에서 구단 간 성적 및 재정적 격차가 심화되면서, 경쟁력 있는 팀 구성과 장기적인 성과 유지가 더욱 어려운 상황입니다.  
            - 이러한 문제는 데이터 분석 기술을 활용해 선수 스카우트, 트레이드, 경기 전략 등 구단 운영의 다양한 측면에서 해결할 수 있습니다.
        """
    )

    # 데이터 분석 기술의 필요성
        st.markdown("#### **데이터 분석 기술의 필요성**")
        st.markdown(
        """
        MLB는 매 시즌 방대한 경기 데이터를 생성하며, 이를 효과적으로 분석하고 활용하는 것은 리그와 구단의 경쟁력 향상을 위한 필수적인 요소로 자리 잡았습니다.  
        다음은 데이터 분석 기술의 주요 필요성을 설명합니다:

        1. **정량적 의사결정 도구로서의 데이터 분석**  
            - 데이터 기반의 예측은 감각적이고 주관적인 판단 대신, 과학적이고 신뢰도 높은 의사결정을 가능하게 합니다.  
            - 경기 전략 수립뿐 아니라 선수 계약 협상, 트레이드, 훈련 계획 설정 등 구단 운영 전반에서 활용도가 높습니다.

        2. **성과 최적화를 위한 데이터 활용**  
            - 팀별 전력 분석을 통해 효율적인 시즌 운영 전략을 설계할 수 있으며, 포스트 시즌 진출 가능성을 예측함으로써 리그 내 경쟁력을 높이는 데 기여합니다.  
            - 데이터는 선수 개개인의 커리어 관리뿐 아니라, 구단 전체의 장기적인 성과 최적화에도 중요한 역할을 합니다.

        3. **리스크 관리 및 재정적 안정성 확보**  
            - 데이터 분석을 활용해 고액 연봉 계약에 따른 리스크를 최소화하고, 공정한 연봉 책정 기준을 마련할 수 있습니다.  
            - 이를 통해 구단은 재정적 안정성을 확보하고 장기적인 성장을 도모할 수 있습니다.
        """
    )

    elif menu == "대상":
        # 페이지 제목
        st.title("🙋 대상")

        # MLB 구단 운영진
        st.markdown("#### **MLB 팀 및 구단 운영진**")
        st.markdown(
            """
            MLB 구단은 본 프로젝트의 주요 대상으로, 데이터 기반 의사결정을 통해 팀 성과를 극대화하고 재정적 효율성을 높일 수 있습니다.

            - **데이터 기반 전략 수립**: 팀의 경기력 분석 및 예측 데이터를 활용하여 시즌 전략을 최적화.  
            - **선수 계약 협상**: 선수 성과 데이터를 기반으로 공정한 연봉 책정과 계약 협상 지원.  
            - **효율적인 팀 구성**: 선수 스카우트 및 트레이드 전략에 데이터를 반영해 경쟁력 있는 팀 구성 가능.  
            - **포스트 시즌 진출 가능성 평가**: 팀의 중간 성적 분석을 통해 포스트 시즌 진출 가능성을 예측하고, 이에 따른 운영 전략 수립.  
            - **리스크 관리**: 고액 연봉 선수 계약 시 재정적 리스크를 최소화하며, 장기적인 팀 운영의 안정성을 확보.
            """
        )

        # 선수 에이전트 및 개인 선수
        st.markdown("#### **선수 에이전트 및 개인 선수**")
        st.markdown(
            """
            선수 에이전트와 개인 선수는 데이터 분석 결과를 활용해 시장 가치를 평가하고 커리어 개발 계획을 수립할 수 있습니다.

            - **시장 가치 분석**: 선수의 주요 성과 데이터를 기반으로 시장에서의 가치를 평가하여 에이전트가 협상 전략 수립 가능.  
            - **커리어 개발**: 장기적인 커리어 지속 가능성을 분석하여 훈련 및 경기 계획에 반영.  
            - **트레이드 및 팀 선택 전략**: 데이터를 활용해 자신에게 가장 적합한 팀 또는 리그 선택 지원.
            """
        )


    elif menu == "분석 목적":
        st.title("📊 분석 목적")

        st.markdown(
        """
        1. **팀별 주요 지표 현황 분석 및 객관적 전력 평가**  
           - 팀의 타격, 투수력, 수비 등 주요 퍼포먼스 지표를 다각적으로 분석하여 객관적인 전력 평가 지표를 제공합니다.  
           - 이를 통해 팀의 강점과 약점을 명확히 파악하여 시즌 전략을 최적화할 수 있습니다.

        2. **포스트 시즌 진출 가능성 평가 및 운영 전략 수립**  
           - 팀의 시즌 중반 데이터 및 성적을 기반으로 포스트 시즌 진출 가능성을 예측합니다.  
           - 구단 운영진이 데이터를 활용해 시즌 후반 경기 운영 전략을 개선하고 목표를 달성할 수 있도록 지원합니다.

        3. **선수 커리어 관리 및 성장 가능성 분석**  
           - 선수의 성과 지표를 분석하여 장기적인 커리어 성장 가능성과 잠재력을 평가합니다.  
           - 선수 훈련 계획과 관리 방안을 데이터에 기반하여 최적화함으로써 팀 내 선수 육성 체계를 강화합니다.

        4. **공정한 연봉 책정을 위한 가치 평가**  
           - 선수의 퍼포먼스 데이터를 기반으로 시장 가치를 정량적으로 분석하여 적정 연봉을 산출합니다.  
           - 이는 구단과 선수 간 신뢰를 강화하고, 재정적 리스크를 최소화하는 데 기여합니다.
        """
    )

    elif menu == "목표 및 기대 효과":
        st.title("🧾 목표 및 기대 효과")
        st.markdown(
            """
            ### **비즈니스 가치**
            1. **MLB 구단의 경쟁력 강화**  
                - 데이터 기반 의사결정을 통해 경기력 향상 및 운영 효율성 극대화  
                - 적절한 연봉 책정과 전략적 선수 영입으로 비용 절감 및 팀 성과 최적화  
            2. **구단의 수익 증대**  
                - 포스트 시즌 진출 가능성 예측을 통해 경기 운영 전략을 개선하고 팬 만족도 증대  
                - 공정한 선수 계약으로 팀 내 신뢰 강화 및 장기적인 성과 증대  
            3. **비즈니스 모델로서의 활용 가능성**  
                - 본 예측 모델은 구단 운영진과 선수 에이전트를 대상으로 판매할 수 있는 **데이터 솔루션**  
                - MLB 데이터를 활용한 분석 결과를 바탕으로 구단의 의사결정 과정을 혁신적으로 개선  

            ### **목적성**
            - **정확한 예측 모델 제공**  
                팀 및 선수 성과를 분석하여 효율적인 팀 구성 및 연봉 협상 지원  
            - **사용자 친화적 데이터 도구 개발**  
                Streamlit 기반의 시각화 및 대시보드 제공으로 데이터를 쉽게 활용 가능  
            - **시장 경쟁력 확보**  
                MLB 구단과 협력 관계를 구축하고, 데이터를 활용한 의사결정 도구로 구단의 성과를 개선하는 솔루션 제공
            """
        )

    elif menu == "데이터 수집 및 전처리":
        # 페이지 제목
        st.title("📂 데이터 수집 및 전처리")

        # 데이터 출처
        st.markdown("### 데이터 출처")
        st.markdown(
            """
            - **[Kaggle - History of Baseball](https://www.kaggle.com/datasets/seanlahman/the-history-of-baseball?select=all_star.csv)**  
              (이 데이터는 MLB의 선수 기록, 경기 결과, 수상 내역 등 방대한 역사적 데이터를 포함합니다.)  

            - **[MLB 공식 데이터베이스](https://www.mlb.com/)**  
              (MLB 리그의 최신 경기 데이터, 선수 성적, 팀 성적 등 실시간 정보를 제공합니다.)  
            """
        )


        # 결측값 및 이상치 처리
        st.markdown("### 1. 결측값 및 이상치 처리")
        st.markdown(
            """
            - **연봉 예측**  
              - 결측값: 연봉 데이터에 비어 있는 값은 선수의 이전 시즌 평균 연봉으로 대체.  
              - 이상치: 비정상적으로 높은 연봉 데이터는 퍼포먼스 지표(타율, 방어율 등)와 비교하여 유효성 검토 후 제거.  

            - **포스트 시즌 진출 예측**  
              - 결측값: 경기 성적 데이터의 결측값은 시즌 평균으로 대체.  
              - 이상치: 한 팀이 특정 지표에서 극단적인 값을 보이는 경우(예: 득점이 0인 경기) 데이터의 신뢰도를 확인.  

            - **선수 커리어 기간 예측**  
              - 결측값: 선수의 생애 데이터(데뷔 연도, 경기 수 등)의 결측값은 연도별 평균값으로 대체.  
              - 이상치: 극도로 적은 경기 수로 은퇴한 사례는 특별한 주석으로 처리.  

            - **기타 분석 모델**  
              - 모든 데이터에서 결측값은 통계적 방법(중앙값 또는 평균값)으로 대체하고 이상치는 도메인 전문가의 검토를 통해 처리.  
            """
        )

        # 변수 변환 및 인코딩
        st.markdown("### 2. 변수 변환 및 인코딩")
        st.markdown(
            """
            - **연봉 예측**  
              - 범주형 데이터(포지션, 리그 등)는 원-핫 인코딩 적용.  
              - 연속형 데이터(타율, 홈런, 방어율 등)는 로그 변환을 통해 스케일 조정.  

            - **포스트 시즌 진출 예측**  
              - 팀 이름, 소속 리그와 같은 범주형 데이터는 라벨 인코딩을 사용하여 수치형 데이터로 변환.  
              - 승률과 같은 비율 데이터는 Min-Max 스케일링으로 정규화.  

            - **선수 커리어 기간 예측**  
              - 포지션(투수, 타자 등)은 원-핫 인코딩으로 변환.  
              - 나이와 같은 연속형 변수는 이진화(나이를 구간화)하여 새 변수를 생성.  

            - **기타 분석 모델**  
              - 모든 모델에서 범주형 변수는 적절히 인코딩하며, 연속형 변수는 필요에 따라 표준화(정규 분포화) 또는 정규화(Min-Max 스케일링)를 적용.  
            """
        )

        # 특성 선택 및 생성
        st.markdown("### 3. 특성 선택 및 생성")
        st.markdown(
            """
            - **연봉 예측**  
              - 주요 성과 지표(타율, 출루율, OPS, 방어율 등)와 연봉 간의 상관관계를 분석하여 중요한 변수만 선택.  
              - 팀 성적, 선수 나이, 계약 연수 등 새로운 파생 변수 생성.  

            - **포스트 시즌 진출 예측**  
              - 팀별 주요 성과 지표(득점, 실점, 승률 등) 중 포스트 시즌 진출과 높은 상관성을 보이는 변수 선택.  
              - 시즌 중반 데이터를 기준으로 팀 성적 변화율을 파생 변수로 생성.  

            - **선수 커리어 기간 예측**  
              - 선수의 연도별 경기 수, 평균 타율 또는 방어율, 부상 기록 등 주요 변수를 선택.  
              - 데뷔 나이와 같은 변수에서 구간화된 변수를 추가로 생성.  

            - **기타 분석 모델**  
              - 모델링에 따라 PCA(주성분 분석)를 활용해 변수의 차원을 축소하거나, 주요 변수의 상호작용 효과를 분석해 새로운 파생 변수를 생성.  
            """
        )


    elif menu == "모델 개발 및 성능 평가":
        # 페이지 제목
        st.title("📈 모델 개발 및 성능 평가")

        # 연봉 예측 모델
        st.markdown("### 1. 연봉 예측")
        st.markdown(
            """
            - **모델**: Scikit-learn (회귀 모델)  
            - **평가 지표**: RMSE (Root Mean Square Error)  
                - 실제 정답 값과 예측 값의 차이를 제곱한 후 평균을 구하여 도출 가능한 평균 오차값에 제곱근을 씌워서 구함.  
            - **특징 및 세부 내용**:
                - 주요 입력 변수: 타격 성과(OPS, 타율 등), 수비 성과, 출루율, 나이, 계약 기간, 포지션 등.
                - 이상치 제거와 결측값 대체를 통해 데이터 정제.
                - 로그 변환으로 데이터 분포 조정 및 극단값 처리.
            """
        )

        # 포스트 시즌 진출 여부 예측 모델
        st.markdown("### 2. 포스트 시즌 진출 여부")
        st.markdown(
            """
            - **모델**: Scikit-learn (Random Forest Regression)  
            - **평가 지표**: RMSE, R² (결정 계수)  
                - RMSE: 예측 값과 실제 값의 평균 오차를 제곱근으로 나타냄.  
                - R²: 모델이 데이터를 얼마나 잘 설명하는지를 나타내며, 1에 가까울수록 성능이 좋음.
            - **특징 및 세부 내용**:
                - 주요 입력 변수: 팀 성적(득점, 실점, 타율, 방어율 등), 시즌 중반 이후 경기 흐름 변화율, 상대팀 성적.
                - 샘플 불균형 문제 해결을 위해 Oversampling 또는 SMOTE 적용.
                - PCA(주성분 분석)으로 상관 관계가 높은 변수 처리.
            """
        )

        # 커리어 잔여 기간 예측 모델
        st.markdown("### 3. 커리어 잔여 기간 예측")
        st.markdown(
            """
            - **모델**: Scikit-learn (회귀 모델)  
            - **평가 지표**: RMSE (Root Mean Square Error)  
                - 실제 커리어 잔여 기간과 예측 값의 차이를 제곱한 후 평균을 구해 도출.  
            - **특징 및 세부 내용**:
                - 주요 입력 변수: 경기 수, 평균 타율, 방어율, 시즌별 주요 기록, 부상 기록, 나이, 데뷔 연도.
                - 나이를 구간화하여 비선형성을 보완.
                - 이상치로부터 생기는 값의 왜곡에 민감하게 반응하도록 로그 변환 적용.
            """
        )


    elif menu == "프로젝트 일정":
        st.title("📅 프로젝트 일정")

        # 데이터프레임 생성
        data = {
            "단계": ["기획 및 데이터 수집", "데이터 전처리", "모델 개발 및 검증", "검토 및 발표 준비"],
            "주요 작업 내용": [
                "주제 기획, 데이터 수집",
                "EDA, 특성 공학, 결측값 처리",
                "모델링, 하이퍼파라미터 튜닝, 성능 평가",
                "Streamlit 구현, PPT 제작"
            ],
            "시작일": ["2024-12-23", "2025-01-02", "2025-01-06", "2025-01-15"],
            "종료일": ["2025-01-04", "2025-01-10", "2025-01-18", "2025-01-22"],
        }

        df = pd.DataFrame(data)

        # Gantt 차트 생성
        fig = px.timeline(
            df,
            x_start="시작일",
            x_end="종료일",
            y="단계",
            color="단계",
            title="프로젝트 일정 스케줄",
            labels={"단계": "Project Phase"},
            text="주요 작업 내용",
        )

        fig.update_yaxes(categoryorder="total ascending")  # 단계 순서 정렬
        fig.update_layout(showlegend=False)  # 범례 숨김

        # 스타일 조정
        fig.update_traces(
            marker=dict(line=dict(width=0.5, color="black")),  # 막대 테두리 얇게
            opacity=1.0,  # 막대 불투명도
            textfont=dict(size=10, color="black")  # 텍스트 스타일
        )

        # 차트 레이아웃 조정
        fig.update_layout(
            title=dict(text="프로젝트 일정", font=dict(size=20, family="Arial")),  # 제목 크기 및 글꼴
            xaxis_title=None,  # X축 제목 제거
            yaxis_title=None,  # Y축 제목 제거
            font=dict(family="Arial", size=12, color="black"),  # 전체 글꼴 스타일
            plot_bgcolor="white",  # 배경 색상 (흰색)
            margin=dict(l=50, r=50, t=50, b=50),  # 여백 조정
        )

        # 축 설정
        fig.update_yaxes(
            categoryorder="total ascending",  # Y축 순서 정렬
            title=None,  # Y축 제목 제거
            ticksuffix=" ",  # 불필요한 틱 제거
        )
        fig.update_xaxes(
            showgrid=False,  # X축 그리드 제거
            title=None  # X축 제목 제거
        )

        # Streamlit에서 렌더링
        st.write("아래는 프로젝트의 각 단계와 주요 작업 내용을 나타낸 일정 스케줄러입니다.")
        st.plotly_chart(fig)

        # 데이터프레임 표도 함께 표시
        st.write("### 📋 상세 일정")
        st.dataframe(df)


    elif menu == "결론":
        st.title("📌 결론")
        st.markdown(
        """
        ### **결론**
        MLB 데이터를 기반으로 개발된 예측 모델은 다음과 같은 핵심적인 **인사이트**와 **비즈니스적 가치**를 제공합니다:

        1. **선수 및 팀 성과 분석 도구**  
            - 본 프로젝트의 예측 모델은 선수의 연봉 책정, 팀 전력 분석, 포스트 시즌 진출 가능성 평가 등 다양한 데이터 기반 의사결정을 지원합니다.  
            - 이를 통해 구단 운영진은 과거 경험에 의존하는 감각적인 판단 대신, 정량적인 데이터를 바탕으로 전략을 최적화할 수 있습니다.  

        2. **구단 운영 효율성 및 리스크 관리 강화**  
            - 데이터에 기반한 연봉 예측은 고액 연봉 선수를 계약하는 과정에서 발생할 수 있는 재정적 리스크를 줄이고, **공정한 계약 구조**를 제시합니다.  
            - 또한, 포스트 시즌 진출 가능성을 미리 예측함으로써 중반 이후 시즌 운영 전략을 더욱 구체화할 수 있습니다.

        3. **선수 커리어 관리와 구단 장기적 경쟁력 확보**  
            - 선수의 커리어 기간을 예측함으로써 장기적인 관리 및 훈련 계획 수립이 가능하며, 이는 구단의 인재 관리 시스템을 강화합니다.  
            - 신인 선수 스카우트와 트레이드 결정 시에도 데이터를 활용해 더욱 효과적인 의사결정을 내릴 수 있습니다.

        4. **비즈니스 모델로서의 확장 가능성**  
            - 본 프로젝트에서 개발한 데이터 분석 및 시각화 도구는 MLB 구단뿐 아니라, 선수 에이전트, 개인 선수, 팬 커뮤니티 등 다양한 이해관계자들에게도 유용한 도구로 활용될 수 있습니다.  
            - 특히, 예측 결과와 시각화된 데이터를 통해 구단 운영의 투명성을 증대시키고, 구단-선수 간 신뢰를 강화할 수 있습니다.

        ### **기대 효과**
        - **데이터 기반 리그 운영 혁신**: 본 프로젝트는 MLB 리그가 더 많은 데이터를 효과적으로 활용하도록 돕고, 구단의 전략적 의사결정을 지원하여 리그 전반의 운영 효율성을 증대시킵니다.  
        - **공정성과 신뢰성 확보**: 연봉 책정 및 선수 관리에서의 공정성을 증대하여 구단과 선수 간의 신뢰를 강화할 수 있습니다.  
        - **지속 가능한 성장 지원**: 장기적인 데이터를 활용하여 구단의 지속 가능한 성장을 지원하고, 팬들에게 더욱 흥미로운 경기를 제공할 수 있는 기회를 만듭니다.  
        """,
        unsafe_allow_html=True
    )

    elif menu == "팀원 소개 및 역할":
        st.title("🙋 팀원 소개 및 역할")
        st.markdown(
            """
            - **임종경** - 팀장 (프로젝트 관리 및 전반적 기획)  
            - **이정훈** - 데이터 수집 및 전처리 담당  
            - **전진구** - 모델 개발 및 성능 평가 담당  
            - **정지훈** - Streamlit 구현 및 발표 자료 제작  
            """
        )
