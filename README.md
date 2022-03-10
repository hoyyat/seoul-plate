# 프로젝트 이름 : 서울 플레이트(3.7~3.10)
## 간단소개
서울에 위치한 맛집을 손쉽게 검색해 보세요.

## 와이어 프레임


로그인 페이지

![레아아웃1](https://user-images.githubusercontent.com/86460176/157622672-7b44ed4f-34e8-4ab9-bdef-1bc40f3b6028.png)

회원가입 페이지

![2](https://user-images.githubusercontent.com/86460176/157622718-1352e41e-c39c-4ce7-b6ad-93f4c414176e.png)

메인페이지

![3](https://user-images.githubusercontent.com/86460176/157622742-3e2e29f3-8927-42bc-a4f0-f345b224df14.png)


## 사용 기술
* framewrk : Flask
* Database : MongoDB
* server : AWS EC2
* front-end : JQuery, AJAX

## 핵심 기능
* 로그인/회원가입
  - 아이디 중복화인 및 입력요소 유효성 검사

* 검색기능
  - 키워드 검색만으로 검색가능하게 구현

* 댓글등록
  - 각 상세페이지 마다 리뷰를 남길 수 있게 만듦
  - 댓글 개수를 메인페이지 이미지에 보이게 만듦

## trouble shooting
1) 로그인이 작동이 안하는 문제 발생 
   -> impprot certifi
      ca = certifi.where()
   파이몽고 주소뒤에 tlsCAFile=ca 적고 해결하였습니다.
   
2) 검색기능 구현시 디비에 저장되어 있는 지역의 이름 그리고 특수문자까지 정확히 일치하지 않으면 안되는 문제가 발생하였습니다
   -> plates = list(db.plates.find({str(select): {'$regex':keyword}}, {'_id': False}))
      select 값 (palce와 title) 의 문자열이 키워드에 속해있으면 찾아오게 만들었습니다.
