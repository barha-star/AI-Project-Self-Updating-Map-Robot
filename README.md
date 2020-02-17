# AI-Project-Self-Updating-Map-Robot

Overview
-------------------------------
* **Organization** : POSCO AI BIG DATA ACADEMY
* **Industry** :
* **Project Title** : 실내 정보를 자동으로 인식하고 바뀐 정보를 스스로 업데이트하는 인공지능 로봇 'P1'
* **Project Description** : 실내 지도의 최신성 유지를 위해 시간 간격을 두고 촬영한 매장 이미지를 비교하여 매장의 변화 여부를 판별하고, 변화가 발생했을 경우 지도를 업데이트하는 시스템
* **Author(s)** : [박규동](https://github.com/bgd0706), [공은비](https://github.com/barha-star), [김규리](https://github.com/KimGyuLee), [김송일](https://github.com/camelia13), [박병수](https://github.com/Hinterhalter), [이수진](https://github.com/sooooojinlee)
* **Date** : 19/11/18 ~ 19/12/20  


Related works
-------------------------------
 * **Logo and franchise detection (?)** : ???  
 * **Deep metric learning (?)** : ?? 


Hardware
-------------------------------


Dataset
-------------------------------
 * **Mall_space_image_data** : 제작한 세트에서 매장 사진을 수집한 데이터
 * **train_data** : 세트를 1회 주행하면서 수집한 데이터
 * **test_data** : 세트에서 매장 사진을 2개 변경하고 수집한 데이터


POI Change Detection
-------------------------------
 

Mapping
-------------------------------


Experimental Results
-------------------------------


Timeline
-------------------------------
|date|day|note|
|:-----:|:-----:|:------|
|19/11/04|mon|헬스케어 비즈니스 상황 분석, 추진배경 작성|
|19/11/05|tue|현황 및 개선기회 작성|
|19/11/06|wed|데이터 셋 확인, 웹 구현 시작|
|19/11/07|thur|도메인 지식, 변수 파악, 파생변수 생성, 태블로 시각화|
|19/11/08|fri|변수 파악 및 탐색적 분석, 추진배경 재작성, 구글 API 병원 위치 정보 지도 시각화, 태블로 시각화, 암 진단 모델링|
|19/11/09|sat|탐색적 분석 및 인사이트 도출|
|19/11/10|sum|탐색적 분석 후 분석 방향에 대한 고민, 데이터셋 통합 시도|
|19/11/11|mon|HRA 발견, 심뇌혈관질환 위험도 계산, 대사증후군 모델링, 암 모델링(LR, DT, RF, GB, XGB)|  
|19/11/12|tue|심뇌혈관질환 위험도 계산, 대사증후군 모델링, 암 모델링, 카이제곱 검정으로 지역별 의료인프라 차이 확인|
|19/11/13|wed|카이제곱검정, PPT 구성|
|19/11/14|thur|최종 PPT 완성|
|19/11/15|fri|최종 발표|  


Notebooks and Analysis
-------------------------------
The project includes the following notebooks (data manipulation and analysis):  

It is recommended to view the notebooks in the above order to avoid missing out on code explainations.

Tech
-------------------------------
The following technologies were used for this part of the project:

* Python 3
* iPython Notebooks: For interactive code development and result presentation.
* Pandas: Python package for data analysis.
* Matplotlib and Seaborn: Python 2D plotting library.
