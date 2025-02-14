# 👕 Cody Now
> AI를 활용한 코디 추천 서비스
<img src="static/images/readme/introduce-001.png" alt="소개">

실시간 날씨 정보를 확인할 수 있어요.<br>
사용자 정보를 입력하고, 사진을 업로드하면<br> 
AI가 맞춤형 코디 추천을 해줘요.

<br>

## 💻 Developers
* 프로젝트 기간 : 2025.01 - 2025.02

|                                                                         FE                                                                         |                                                                         FE                                                                          |
| :------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------: |
| <a href="https://github.com/yeeeww"><img src="https://avatars.githubusercontent.com/yeeeww?v=4" alt="profile" width="140" height="140"></a> | <a href="https://github.com/Imggaggu"><img src="https://avatars.githubusercontent.com/Imggaggu?v=4" alt="profile" width="140" height="140"></a> |
|                                                       [김예원](https://github.com/yeeeww)                                                       |                                                       [박서정](https://github.com/Imggaggu)                                                       |

|                                                                        BE                                                                        |                                                                         BE                                                                         |
| :----------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------: |
| <a href="https://github.com/junhkchoi"><img src="https://avatars.githubusercontent.com/junhkchoi?v=4" alt="profile" width="140" height="140"></a> | <a href="https://github.com/eunkyoung529"><img src="https://avatars.githubusercontent.com/eunkyoung529?v=4" alt="profile" width="140" height="140"></a> |
|                                                       [최준혁](https://github.com/junhkchoi)                                                       |                                                       [김은경](https://github.com/eunkyoung529)                                                       |

|                                                                        PM                                                                        |
| :----------------------------------------------------------------------------------------------------------------------------------------------: |
| <a href="https://github.com/RRT3333"><img src="https://avatars.githubusercontent.com/RRT3333?v=4" alt="profile" width="140" height="140"></a> |
|                                                       [홍다오](https://github.com/RRT3333)                                                       |

<br>

## ✨ Feature

### 💁🏻‍♀️ 온보딩

<br>

### 🤖 코디 추천

<br>

### 🚪 나만의 옷장

<br>

## 🚀 Deploy 
<img src="static/images/readme/deploy.png" alt="배포">

<br>

## 🔀 Service Flow
<img src="static/images/readme/serviceflow.png" alt="서비스 플로우">

<br>

## 🛠️ Tech Stack
<img src="static/images/readme/techstack-001.png" alt="기술 스택">

<br>

## 의존성 목록 정리
```
의존성 목록
pip install django
pip install social-auth-app-django
pip install django-environ
pip install psycopg2-binary

pip install python-dotenv // 보안 이슈: 1월 29일에 추가
pip install django-allauth // 소셜 로그인 구현: 1월 29일에 추가

pip install Pillow // 이미지 저장 관련: 1월 29일에 추가
pip install google-generativeai requests pillow

pip install google-generativeai // 6번 기능 관련: 1월 29일에 추가
pip install google.ai.generativelanguage 

pip install google-genai

pip install six // 토큰 유효성 검사 관련: 1월 30일에 추가

pip install django-debug-toolbar

pip install Pillow pillow-heif //IOS 파일 처리: 2월 2일에 추가

pip install requests//커스텀 검색결과 (2/3)
pip install beautifulsoup4
pip install markdown2
```