<div align="center">

  # Wanted Backend Pre Onboarding Project 004
    
![3076738490_20220125121000_7714646312](https://user-images.githubusercontent.com/86827063/169651848-18c03bdb-7f33-43cf-85cb-43369546df89.jpg)
</div>

## 목차
- [D팀 멤버 소개](#-team-d-member)  
- [개발 기간](#--개발-기간--) 
- [프로젝트 설명 분석](#-프로젝트-설명--분석)
- [프로젝트 개발 조건](#-개발-조건)
- [프로젝트 요구 조건](#-요구-조건)  
- [기술 스택](#-사용된-기술-스택)
- [구현 기능](#-구현-기능)  
- [API 명세서](#-api-명세서)  
- [DFD](#dfd)
- [Test cases ](#-test-case) 
- [프로젝트 후기](#-프로젝트-후기)

<div align="center">  

## 👨‍👨‍👦‍👦 Team "D" member  
  
  |권상현|김석재|류성훈|정미정|  
  |:------:|:------:|:------:|:------:|  
  |<img src="https://avatars.githubusercontent.com/u/39396492?v=4" width="200"/> | <img src="https://avatars.githubusercontent.com/u/86823305?v=4" width="200"/> | <img src="https://avatars.githubusercontent.com/u/72593394?v=4" width="200"/> |<img src="https://avatars.githubusercontent.com/u/86827063?v=4" width="200"/> |      
  |[Github](https://github.com/gshduet)|[Github](https://github.com/Cloudblack)|[Github](https://github.com/rsh1994)|[Github](https://github.com/nxxxtyetdecided)|  
  
  <br>


  
|<img height="200" width="380" src="https://retaintechnologies.com/wp-content/uploads/2020/04/Project-Management-Mantenimiento-1.jpg">|<img height="200" width="330" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGElLjafMUhHglmqwh9lRh_sVzOCQyBiPNfQ&usqp=CAU">|
|:------:|:------:|
|💻 [**Team work**](https://mature-citron-a04.notion.site/Wanted_Pre_Onboarding-6af013e2bb3b43739cebc641de4ff558)  | 📒 [**Project page**](https://www.notion.so/4-e89b2e9ef1fe48bab285411c446fecc2)|
|공지사항, 컨벤션 공유 등<br> 우리 팀을 위한 룰 |요구사항 분석, 정보 공유 및<br> 원할한 프로젝트를 위해 사용|

  </div> 

  <h2> ⌛ 개발 기간  </h2> 
  2022/05/16  ~ 2022/05/21 
  
  <img src = "https://user-images.githubusercontent.com/86827063/169651914-9d4b8629-62d4-4b76-9288-5bc7571d4b07.png" width="40%">
  
# 💻 Project
  ### 💭 프로젝트 설명 & 분석
  - DAG 알고리즘을 사용한 json 파일 처리 API 설계
  - Pandas를 활용하여 csv 파일의 데이터 가공

  ### 🛠 개발 조건
  - a.csv 파일은 있는 것으로 전제, 컬럼과 데이터는 자유롭게 생성
  - flask 활용한 개발
  - REST API 각 기능에 대한 Unit test를 수행
  - read : a.csv 파일을 읽어 Pandas DataFrame 반환
  - drop : 지정한 컬럼을 제거한 후 DataFrame 반환
  - write : 지정된 파일 경로로 csv 파일 저장

 ### 📰 요구 조건
     REST API 기능
  - job 저장 : 전달받은 job 정보를 json 파일에 저장
  - job 삭제 : 전달 받은 job id를 job.json 파일에서 찾아 삭제 후 저장
  - job 수정 : 전달 받은 job id를 job.json 파일에서 찾아 수정 후 저장
  - job 실행: 전달 받은 Job id를 job.json 파일에서 찾아 task들을 실행
    * 예시: read(a.csv) -> drop(date) -> write(b.csv) 


### 🧹 사용된 기술 스택

> - Back-End :  <img src="https://img.shields.io/badge/Python 3.10-3776AB?style=flat&logo=Python&logoColor=white"/>&nbsp;<img src ="https://img.shields.io/badge/flask-%23000.svg?style=flat-badge&logo=flask&logoColor=white">&nbsp;<img alt="Python" src ="https://img.shields.io/badge/pandas-3776AB.svg?&style=flat-badage&logo=pandas&logoColor=white"/>
> 
> - ETC　　　  <img src="https://img.shields.io/badge/Git-F05032?style=flat-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=flat-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Swagger-FF6C37?style=flat-badge&logo=Swagger&logoColor=white"/>&nbsp;


 ### 🧨 구현 기능 
 - [x] job 저장
 - [x] job 삭제
 - [x] job 수정
 - [x] job 실행
 - [x] API 명세서
 - [x] DFD, Sequence Diagram
 - [x] REST API 각 기능의 Unit Test

<br>

### 📃 API 명세서
|           URL            | Method |      Description       |
|:------------------------:|:------:|:----------------------:|
|      " "                 |  GET   |   json 파일의 전체 리스트 읽기   |
 |           " "            |  POST  | json 값을 받아 json 파일에 저장 |
 |    "/<string:job_id>"    |  GET   |    입력받은 job_id로 검색     |
|    "/<string:job_id>"    |  PUT   |      입력받은 job 수정       |
 |    "/<string:job_id>"    | DELETE |      입력받은 job 삭제       | 
 | "/<string:job_id>/start" | GET    |   입력받은 job의 task 수행    |

<br>

### DFD
![image](https://user-images.githubusercontent.com/86823305/169633875-21d79f12-eb2f-4362-9cad-96d777138c2b.png)

<br>

### 📑 TEST CASE
- 11 개의 테스트 작성

<br>

### 🎭 프로젝트 후기

구현한 방법과 이유, 느낀점 간략하게 서술

<details>
<summary>권상현</summary>
<div markdown="1">

>구현한 기능
- 요구사항 분석
- REST API 설계
- API 리팩토링
> 느낀점
-
      
</div>
</details>

<details>
<summary>김석재</summary>
<div markdown="1">

> 구현한 기능

- 요구사항 분석
- DAG (Directed Acyclic Graph) 활용해 Task 순서를 정하는 알고리즘 구현
- DFD (Data Flow Diagram)

> 느낀점

- 다시 한다면 각자 API구현하기보다는 의견만을 교환하거나 바로 사용 할 수 있게 라이브러리화 할 것입니다.
이번 프로젝트는 각자의 관점으로 API를 구현해보고 다양한 시각을 통합하면서 프로젝트를 더욱 견고하게 만들 수 있었습니다. 
공부를 전제하에 두었기때문에 시도한 방법이었지만 완성된 API 코드들을 하나로 합치는 과정은 일을 한번 더 하게되어 시간 대비 효율이 많이 떨어집니다.
- 알고리즘은 매력적이다
프로젝트 요구사항이었던 DAG를 활용하기위해 개념 설명을 듣고 그걸 코드로 바꿔 적용했습니다. 백준에서 문제집 풀던 느낌과 다르게 프로젝트에 필요한걸 만든다는 느낌이 시간이 오래걸렸지만 시간가는줄 모르고 즐겁게 구현했습니다.
- 전체적인 이해를 위해 필요한 DFD
DFD를 처음으로 만들어 보았는데 다 만들고 나니까 이전에 복잡하게 생각했던 프로세스가 정말 단순하게 보였다.  DFD를 마지막에 만들지만 시작할때의 의견을 종합해 먼저 만들고 끝나고 한번 더 만든다면 팀원들과 같은 이해를 하는데 도움이 될 것 이다.

</div>
</details>

<details>
<summary>류성훈</summary>
<div markdown="1">

>구현한 기능
    - 요구사항 분석
    - REST API 설계
    - API명세서(Swagger) 작성
    - pytest 사용하여 Unit Test 작성
> 느낀점
- 팀원들과 같은 문서를 읽고 분석하면서 받아들이는 요구사항의 관점의 차이가 있다는 것을 느꼈습니다. 
      다양한 관점에서 문제를 해석한 후에 괜찮은 해결점에 도달했다는 점이 인상깊었습니다.
- 마이크로 프레임워크인 Flask를 사용하여 API를 만드는 것은 자유도가 높지만, 그만큼 꼼꼼함이 필요하다는 것을 느꼈습니다.
- 몇 개의 Swagger 데코레이터를 붙여서 API명세서를 작성할 수 있다는 점이 좋았고 편리했습니다.
- 유닛테스트를 통하여 코드의 신뢰를 얻는 만큼 정확하고, 빠지는부분이 없어야만 한다는 것을 느꼈습니다.

</div>
</details>

<details>
<summary>정미정</summary>
<div markdown="1">

>구현한 기능
- 요구사항 분석
- REST API 설계
- READ.md, Notion 작성 (문서화)
> 느낀점
  
- 하나의 요구사항에서도 여러 의견이 나와 놓칠 수 있는 부분들을 챙길 수 있었다는 점에서 서로의 피드백을 받아 들이면 견고한 프로젝트가 될 수 있다는 것을 느꼈습니다.
- 3일간 각자 작성해본 REST API는 [저의 코드](https://github.com/wanted-pre-onboarding-2nd-BE-Team-D/004_Moa_Data/tree/nxxxtyetdecided)는 클래스화를 통해서 깔끔해졌지만 에러처리에서 부족함이 있었습니다. 팀원들의 코드를 통해서 어떤 식의 에러처리가 좋은 지 배울 수 있었습니다.
- 코드를 깔끔하게 하는 것도 좋지만 기한을 맞추지 못한다면 아무 의미가 없는 것을 느꼈습니다. 기능 개발을 해놓고 이후에 고도화하는 것이 좋은 프로세스임을 느껴 적용하도록 노력     했습니다.
- 코드를 잘 짜는 것도 좋지만, 좋은 커뮤니케이션을 위해 읽는 사람에게읽기 쉬운 문서화를 작성하는 것도 중요하다는 것을 배웠습니다.
      
</div>
</details>
