#  💵 USD 팀

## 1. 👏 소개
- 프로젝트명 : **Na-Dle** (나랑 들을래?)
  - 'Na-Dle'은 사용자의 취향을 반영하여 취향에 맞는 음악을 추천해주고, 취향이 비슷한 다른 사용자의 플레이리스트를 보여주는 추천서비스 입니다.

<br>

## 2. ⏱︎ 개발기간
- 2022.11.02 ~ 2022.11.08

<br>

## 3. 🦕 역할분담

- 🖥 Frontend
  - 팀원 전체

- ⚙ Backend 
  - 박수인 : 평점, 리뷰
  
  - 이동영 : 유저기능
  
  - 이현지 : 추천시스템
  
  - 정현주 : 평점, 리뷰
  
  - 최해민 : 추천시스템

## 4. 🌌 시작하기

1. 패키지 설치
    - `pip install -r requirements.txt`

2. 음원 데이터 DB저장
    - `python manage.py loaddata data/music_data_for_db.json`

3. 더미 유저 100명 생성
    - `python manage.py create-users --number 100`

4. 더미 선호도 데이터 생성
    - `musics/dummy.py`에서 `save_grades_data_csv()` 함수 호출하고, -> `dummy.py 실행`
    - **꼭 dummy.py 실행 후 호출코드 삭제해주세요!!**

## 5. 📂 기능 명세서

![](https://velog.velcdn.com/images/haeminchoi2/post/3477fd26-c395-4050-b9b9-8426b49ee16d/image.png)


<br>

## 6. 📗 DB설계

![](https://velog.velcdn.com/images/haeminchoi2/post/49400507-c337-4c45-9a06-dd2e6e825d9b/image.png)

## 7. 📕 API명세서

| 구분 | NAME | method | URL | request | response |
| --- | --- | --- | --- | --- | --- |
| 회원가입 | 회원가입HTML | GET | /users/signup/ |  | 회원가입 html |
|  | 회원가입 | POST | /users/signup/ | { ”fullname”:fullname, ”username”:username, ”password”:password } | redirect(”users/signin.html/”) |
| 로그인 | 로그인HTML | GET | /users/signin/ |  | 로그인 html |
|  | 로그인 | POST | /users/signin/ | { ”username”:username, “password”:password } | redirect(”users/first_like.html/”) |
| 로그아웃 | 로그아웃 | POST | /users/logout/ |  | redirect(”users/first_like.html/”) |
| 팔로우 | 팔로우 | POST | /users/follow/<int:user_id>/ | { “follow” } |  |
| 프로필페이지 | 프로필조회 | GET | /users/<str:username>/ |  | { ”id”:id, “my_reviews”:[review Object, music Object], “follower”:[follower Object], “follow”:[follow Object], “last_login”: last_login, “username”:username, “password”:password, “fullname”:fullname, “email”:email, “profile_image”:profile_image, “is_active”:is_active, “is_admin”: is_admin } |
|  | 프로필편집 | GET | /users/profile/ | 로그인 유저 | { ”username”:username, “password”:password,”profile_image”:profile_image,”email”:email, ”fullname”:fullname } |
|  | 프로필수정 | PUT | /users/profile/ | { ”username”:username, “password”:password,”profile_image”:profile_image,”email”:email, ”fullname”:fullname } |  |
| 첫로그인 판단 | 첫로그인 판단 | PATCH | /users/first/<int:user_id>/ | { “is_admin” } |  |
| 메인 | 추천시스템 결과 | GET | /musics/recommend/ |  | { "musics": [music Object] ,"recommend_musics": [music Object],"recommend_users": [User Object] } |
| 음원 | 전체음원목록 | GET | /musics/ |  | {"id": id, "avg_grade": avg_grade, "title": title, "image": image, "artist": artist," album": album, "track_id": track_id } |
|  | 랜덤음원목록 | GET | /musics/random/ | {”limit”: limit} | {"id": id, "avg_grade": avg_grade, "title": title, "image": image, "artist": artist," album": album, "track_id": track_id } |
|  | 음원생성 | POST | /musics/ | {”title”:title, ”image”:image, ”artist”:artist, ”album”:album } |  |
|  | 음원상세조회
리뷰목록 | GET | /musics/<int:music_id>/ |  | {"id": id, "avg_grade": avg_grade, "title": title, "image": image, "artist": artist," album": album, "track_id": track_id, “reviews”:[Review Object] } |
|  | 음원수정 | PUT | /musics/<int:music_id>/ | {”title”:title, ”image”:image, ”artist”:artist, ”album”:album } |  |
|  | 음원삭제 | DELETE | /musics/<int:music_id>/ |  |  |
| 리뷰 | 유저리뷰목록 | GET | /reviews/<int:user_id>/ |  | {"id": id, "user": username, "music": [music Object],"content": content, "created_at":created_at, "updated_at": updated_at, "grade": grade } |
|  | 리뷰생성 | POST | /musics/<int:music_id>/reviews/ | { ”content”:content, ”grade”:grade } | {"id": id, "user": user, "user_id": user_id "content": content, "created_at": created_at, "updated_at": updated_at, "grade": grade "music": music_id} |
|  | 리뷰수정 | PUT | /musics/reviews/<int:review_id>/ | { ”content”:content, ”grade”:grade } | {"content": content,"grade": grade} |
|  | 리뷰삭제 | DELETE | /musics/reviews/<int:review_id>/ |  |  |

## 8. 🍺 이렇게 문제 해결했어요.
### <a href="https://github.com/sparta-USD/Na-dle/wiki/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85">상세보기 이동!</a>
