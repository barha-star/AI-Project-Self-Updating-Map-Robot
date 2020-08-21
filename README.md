# AI-Project-Self-Updating-Map-Robot

Overview
-------------------------------
* **Organization** : POSCO AI BIG DATA ACADEMY
* **Industry** :
* **Project Title** : 실내 정보를 자동으로 인식하고 바뀐 정보를 스스로 업데이트하는 인공지능 로봇 'P1'
* **Project Description** : 실내 지도의 최신성 유지를 위해 시간 간격을 두고 촬영한 매장 이미지를 비교하여 매장의 변화 여부를 판별하고, 변화가 발생했을 경우 지도를 업데이트하는 시스템
* **Author(s)** : [박규동](https://github.com/bgd0706), [공은비](https://github.com/barha-star), [김규리](https://github.com/KimGyuLee), [김송일](https://github.com/camelia13), [박병수](https://github.com/Hinterhalter), [이수진](https://github.com/sooooojinlee)
* **Date** : 19/09/26 ~ 19/12/20  


### Project Overview
#### 개요
* 현재의 매장이 과거와 비교했을 때 변화가 있는지를 판별한 후, 변화가 있을 경우 지도를 업데이트하는 시스템을 구현하기 위한 구체적인 절차는 다음과 같다.  
  1. 로봇이 쇼핑몰을 주행하며 매장 영상을 촬영하는 동시에 LiDAR 센서를 통해 맵을 생성한다.  
  2. 촬영한 매장 영상을 통해 얻은 매장 정보와 LiDAR로 생성한 맵을 결합하여 실내 매장 지도를 만든다.  
  3. 시간이 흘러 몇 개의 매장이 바뀐 후 로봇이 동일한 공간을 다시 촬영한다.  
  4. 현재 매장이 과거의 매장과 비교하여 변화가 있는 지를 판별하기 위해 기준 매장 이미지로부터 바뀐 매장 이미지가 들어오면 두 이미지 간의 거리가 좁아지도록 학습시킨다.  
  5. 학습시킨 모델로 과거와 현재 매장 이미지 페어를 비교하여 매장의 변화 여부, 즉 POI 변화 여부를 판별한다.  
  6. 변화가 검출된 경우 변화된 매장 정보를 기존 지도에 업데이트 한다.  



#### 전체 구조도
<div>
<img src="https://user-images.githubusercontent.com/51358226/76726498-a3d9c480-6794-11ea-984f-4e0b0d521d5f.png">
</div>
  
  



Dataset
-------------------------------
 * **Mall_space_image_data** : 제작한 세트에서 매장 사진을 수집한 데이터
 * **train_data** : 세트를 1회 주행하면서 수집한 데이터
 * **test_data** : 세트에서 매장 사진을 2개 변경하고 수집한 데이터


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



  
###
<details>
 <summary> References </summary>
<div markdown="1">
  
[1] Naver Labs, “Did it change? Learning to Detect Point-of-Interest Changes for Proactive Map Updates”, CVPR, 2019.  
[2] A. Gordo, J. Almazan, J. Revaud, and D. Larlus. “Deep image retrieval: Learning global representations for image search.” In ECCV, 2016.  
[3] E. Ustinova and V. Lempitsky. “Learning deep embeddings with histogram loss.” In NIPS, 2016.  
[3] Deeplearning.ai. "C4W4L04 Triplet loss." Online video. Youtube, 2017.11.7. Web. 
(https://www.youtube.com/watch?v=d2XB5-tuCWU)  
[4] Naver Labs, “Indoor Map Self-Update using CV: Learning to Detect Changes in POI” 
(https://www.slideshare.net/deview/242pcd-public)  
[5] Naver Labs, "컴퓨터 비전을 이용한 실내 지도 자동 업데이트 방법: 딥러닝을 통한 POI 변화 탐지" 
(https://tv.naver.com/v/4580314)  
[6] “Understanding Ranking Loss, Contrastive Loss, Margin Loss, Triplet Loss, Hinge Loss and all those confusing names”, 2019.8.3. Web. 
(https://gombru.github.io/2019/04/03/ranking_loss/)  
[7] Florian Schroff, Dmitry Kalenichenko, James Philbin, “FaceNet: A Unified Embedding for Face Recognition and Clustering”, 2015.  
[8] Jérome Revaud, “Making maps evergreen with deep learning, robots and computer vision”, 2019. Web. 
(https://europe.naverlabs.com/blog/making-maps-evergreen/)  
[9] Shibsankar Das, “Image similarity using Triplet Loss”, 2019.7.17. Web. 
(https://towardsdatascience.com/image-similarity-using-triplet-loss-3744c0f67973)  
[10] https://www.coursera.org/learn/convolutional-neural-networks?specialization=deep-learning  
[11] https://www.youtube.com/watch?v=PjCwRK2i2yo  
[12] https://github.com/krasserm/face-recognition  
[13] Boosting Standard Classification Architectures Through a Ranking Regularizer 
60 (https://arxiv.org/pdf/1901.08616.pdf)  
[14] Beyond triplet loss: a deep quadruplet network for person re-identification 
(https://arxiv.org/pdf/1704.01719.pdf)  
[15] https://www.youtube.com/watch?v=mUueSPmcOBc  
[16] https://www.youtube.com/watch?v=38hn-FpRaJs&t=1s  
[17] https://www.youtube.com/watch?v=3vnMY-BlwmU  
[18] https://www.biz-gis.com/index.php?document_srl=47813&mid=GISFAQ  
[19] https://www.youtube.com/watch?v=mUueSPmcOBc  
[20] https://www.youtube.com/watch?v=38hn-FpRaJs&t=1s  
[21] https://www.youtube.com/watch?v=3vnMY-BlwmU  
[22] https://www.biz-gis.com/index.php?document_srl=47813&mid=GISFAQ  
[23] https://www.youtube.com/watch?v=mUueSPmcOBc  
[24] https://www.youtube.com/watch?v=38hn-FpRaJs&t=1s  
[25] https://www.youtube.com/watch?v=3vnMY-BlwmU  
[26] https://www.biz-gis.com/index.php?document_srl=47813&mid=GISFAQ  
[27] https://keras.io/preprocessing/image/  
[28] https://towardsdatascience.com/when-conventional-wisdom-fails-revisiting-dataaugmentation-for-self-driving-cars-4831998c5509  
[29] Elad Hoffer, Nir Ailon, "DEEP METRIC LEARNING USING TRIPLET NETWORK"  
[30] Shibsankar Das, "Image similarity using Triplet Loss"  (https://github.com/sanku-lib/image_triplet_loss)  
  
</div>
</details>
