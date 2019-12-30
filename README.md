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

* #### [Data Preprocessing](https://nbviewer.jupyter.org/gist/KimGyuLee/30aca84f405bb5ddc81a522b6fda84df)
* #### [Data Exploration](https://nbviewer.jupyter.org/gist/KimGyuLee/c370b6d1c85167bcd1cda85789603f05)
* #### [Modeling & Evaluating model performance (1)-대사증후군](https://nbviewer.jupyter.org/gist/KimGyuLee/6f8dbdd37f4b845f22272a6732236644)
* #### [Modeling & Evaluating model performance (2)-심혈관질환](https://nbviewer.jupyter.org/gist/KimGyuLee/325028ce0612728111bdb7641596e04b)
* #### [Modeling & Evaluating model performance (3)-암](https://nbviewer.jupyter.org/gist/KimGyuLee/c4b3a29ff479431cf69f809db372046e)
* #### [Web]()
* #### [Project Portfolio](https://nbviewer.jupyter.org/github/KimGyuLee/Health-Care-Big-Data-Project/blob/master/healthcare_project.pdf)

It is recommended to view the notebooks in the above order to avoid missing out on code explainations.

Tech
-------------------------------
The following technologies were used for this part of the project:

* Python 3
* iPython Notebooks: For interactive code development and result presentation.
* Pandas: Python package for data analysis.
* Matplotlib and Seaborn: Python 2D plotting library.

References
----------------------------------------------
|#|title|source|note|
|:----:|:-----|:-------|:------|
|1|[국가건강검진 건강위험평가 개선](#국가건강검진-건강위험평가-개선-참고-페이지)|질병관리본부|health_data 변수 전처리 참고, 심뇌혈관질환 위험도 계산|
|2|국가중점개방데이터 사용자 매뉴얼(ver4.0)|국민건강보험공단 빅데이터운영실|health_data 변수 파악|
|3|[대한진단검사학회](https://labtestsonline.kr/)|대한검사의학회|각 질병 진단 기준을 파악하여 파생변수 생성|
|4|[라이프시맨틱스](https://lifesemantics.kr/intro/company)|라이프시맨틱스|데이터 분석 후 개선안 수립 시 참조|
|5|[메트라이프](http://insu.greenpio.com/MetLife360health/)|메트라이프|데이터 분석 후 개선안 수립 시 참조|
|6|직장에서의 뇌·심혈관계질환 예방을 위한 발병위험도 평가 및 사후관리지침|한국산업안전보건공단|심뇌혈관질환 예측 모델을 만들기 위해 참고|
|7|[일반적으로 잘 알려져 있는 심혈관질환의 위험인자](https://www.circulation.or.kr:4443/bbs/index.php?code=int&category=&gubun=&page=1&number=6896&mode=view&keyfield=all&key=)|대한심장학회|중증질환의 주요 위험인자인 대사증후군 진단 기준 참고|  


Appendix
----------------------------------------------
#### 참고한 코드 출처
**adambielski** https://github.com/adambielski/siamese-triplet 
**krasserm** https://github.com/krasserm/face-recognition 
**p.100** 생활습관 요인 정의  
**p.109** 수검여부에 따른 건강위험요인 변화여부 비교    
**p.127** (p.144, p.221) HRA 로직 수정 및 시범 적용  
**p.204** 서비스 예시  
**p.216** 결론 및 발전방향  
**p.219** 스마트 헬스케어 분야 활용  
**p.222** 변수 재정리  
**p.231** 건강위험요인 알아보기 평가기준  
**p.233** 로직계산 예시  
