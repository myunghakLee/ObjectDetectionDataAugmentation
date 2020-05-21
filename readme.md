# SinGAN을 이용한 DataAugmentation

해상 이미지의 경우 보통 위성 이미지를 사용하는데 위성 이미지는 구하기 힘든 탓에 신경망을 훈련하기위한 데이터셋 부족 현상을 겪는다.    
따라서 SinGAN을 이용하여 DataAugmentation에 도전해보고자 한다.

## Method 1 
* 원래 배가 있는 이미지에 SinGAN을 이용하여 dataset을 확대해보자, 방법은 다음과 같다.    
    1. 아래 그림의 왼쪽 이미지를 가지고 SinGAN을 학습시킨다.
    2. 학습된 신경망을 이용하여 원본 이미지를 확대하여 많은 배들을 생성한다.
    3. 생성된 그림을 가지고 사람이 직접 레이블링을한다.    

![image](https://user-images.githubusercontent.com/12128784/82555247-66355580-9ba2-11ea-9e75-b610d69c8f1e.png)


* 하지만 위와 같은 방법은 사람이 직접 레이블링을 해야한다는 단점과 아래 그림과 같이 생성된 이미지가 실제하고는 다소 차이가 있다는 단점이 존재한다. 따라서 다른 방법을 시도해볼 것이다.

![image](https://user-images.githubusercontent.com/12128784/82555292-7b11e900-9ba2-11ea-83af-5ea20b77398e.png)


## Method 2
* Method2는 SinGAN을 이용하여 data augmentation을 할 때 배가 없는 부분만 하는 것이다. 그리고 Augmentate된 이미지에 boat들을 붙여넣는 방식을 사용할 것이다. 여타 다른 데이터셋에서는 그다지 효율적인 방법이라고 생각되지는 않지만 해상 데이터셋에서는 문제없이 작동할 것이라고 예상한다.

* 방법은 다음과 같다.    
    1. 우선 원본 이미지를 잘게 조각낸다.
    ![image](https://user-images.githubusercontent.com/12128784/82555521-e491f780-9ba2-11ea-8dee-0bccd5366dd7.png)
    2. 조각낸 데이터중 한 조각을 가지고와 SinGAN을 통하여 확대한다.
    ![image](https://user-images.githubusercontent.com/12128784/82555613-068b7a00-9ba3-11ea-89f8-6913616be495.png)
    3. 그리고 이번에는 원본 이미지에서 배 부분만 따로 잘라온다.
    ![image](https://user-images.githubusercontent.com/12128784/82555660-23c04880-9ba3-11ea-91d3-d05be0a4028e.png)
    4. 이렇게 잘라온 배를 2번에서 생성한 배경에 붙여넣는다. 그리고 이러한 작업을 반복하여 약 8000여장의 데이터셋을 만든다.
    ![image](https://user-images.githubusercontent.com/12128784/82555721-45213480-9ba3-11ea-85d9-b164de930b19.png)
    5. 그리고 이렇게 생성된 데이터셋을 원본 데이터에 추가하여 신경망의 성능이 높아지는지 확인한다.


## 진행 상황

현재 Method1,2를 모두 완료하였으며 신경망의 성능이 높아지는지 비교를 위하여 Rotated Fastr R-CNN을 이용하여 신경망을 학습하였으며 현재 Fine tuning중에 있다.

## Reference
SinGAN : http://openaccess.thecvf.com/content_ICCV_2019/papers/Shaham_SinGAN_Learning_a_Generative_Model_From_a_Single_Natural_Image_ICCV_2019_paper.pdf 

DataSet : https://dacon.io/competitions/official/235492/overview/

