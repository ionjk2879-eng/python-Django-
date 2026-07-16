# Django 게시판 프로젝트

Python과 Django로 구현한 서버 사이드 렌더링 게시판입니다. 원래 Java 21 + Spring Boot로 만들었던 게시판([java21-spring-web-mybatis-mariaDB-jpa-lombok-thymeleaf-aws-light-sail-](https://github.com/ionjk2879-eng/java21-spring-web-mybatis-mariaDB-jpa-lombok-thymeleaf-aws-light-sail-))과 동일한 기능(회원, 게시글, 댓글, 검색)을 Django 스택으로 다시 구현한 학습용 프로젝트이며, 실제 배포 없이 로컬 개발 서버 확인을 목표로 합니다.

## 핵심 기술 스택

**백엔드**: Python 3.13, Django 6.0, Django ORM, django-widget-tweaks
**프론트엔드**: Django Templates(서버 사이드 렌더링), Bootstrap 5.3, Pretendard 폰트, 바닐라 JavaScript(Fetch API)
**데이터베이스**: SQLite (개발 전용)
**인증**: Django 내장 auth 시스템 (세션 기반)

## 로컬 실행 방법

1. Python 3.10 이상 준비
2. 가상환경 생성 및 활성화
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. 의존성 설치
   ```
   pip install -r requirements.txt
   ```
4. DB 마이그레이션
   ```
   python manage.py migrate
   ```
5. (선택) 관리자 계정 생성 후 개발 서버 실행
   ```
   python manage.py createsuperuser
   python manage.py runserver
   ```
   `http://127.0.0.1:8000` 접속

## 주요 기능

- **회원**: 회원가입, 로그인/로그아웃, 마이페이지(내가 쓴 글 목록)
- **게시글**: CRUD, 조회수 증가(`F()` 표현식으로 동시성 안전 처리), 작성자 본인만 수정/삭제 가능
- **댓글**: 작성/수정/삭제, 본인 댓글은 페이지 새로고침 없이 Fetch API로 그 자리에서 수정
- **검색**: 제목/내용/작성자 기준, Django ORM `Q` 객체 기반 동적 쿼리
- **페이지네이션**: 게시글 목록 10개 단위

## 화면 구성

| URL | 설명 |
|---|---|
| `/` | 게시글 목록 (검색, 페이지네이션) |
| `/create/` | 게시글 작성 |
| `/<id>/` | 게시글 상세 + 댓글 목록/작성 |
| `/<id>/update/` | 게시글 수정 |
| `/<id>/delete/` | 게시글 삭제 확인 |
| `/accounts/signup/` | 회원가입 |
| `/accounts/login/` | 로그인 |
| `/accounts/mypage/` | 마이페이지 |
| `/admin/` | Django 관리자 페이지 |

## ERD

```
User (Django 기본)
 ├─< Post (author FK)
 └─< Comment (author FK)

Post
 └─< Comment (post FK)
```

## 프로젝트 구조

```
config/          # 프로젝트 설정 (settings, urls)
accounts/        # 회원가입/로그인/로그아웃/마이페이지
board/           # 게시글·댓글 모델/뷰/템플릿
templates/       # 공통 템플릿(base.html, 로그인)
manage.py
requirements.txt
```

## 기술적 의사결정

- 원본 프로젝트의 "CRUD는 JPA, 동적 검색은 MyBatis" 이원화 대신, Django ORM 하나로 CRUD와 `Q` 객체 기반 동적 검색을 모두 처리했습니다.
- 조회수 증가는 원본의 JPQL 단일 UPDATE 최적화와 동일한 목적으로, `Post.objects.filter(pk=pk).update(view_count=F('view_count') + 1)`을 사용해 읽기-수정-쓰기 경합 없이 처리했습니다.
- 댓글 수정에만 Fetch API를 적용하고 나머지 화면은 전통적인 서버 렌더링 폼 제출 방식을 유지했습니다. 전체를 SPA화하지 않고, 새로고침 없는 UX가 실제로 필요한 지점에만 최소한으로 JS를 더했습니다.
- `LoginRequiredMixin`(로그인 여부)과 `UserPassesTestMixin`(작성자 본인 여부)을 조합해 게시글·댓글의 수정/삭제 권한을 뷰 단에서 체크합니다.

## 참고

실제 배포(AWS 등)는 진행하지 않았고, `python manage.py runserver`로 로컬 개발 서버 동작 확인까지만 검증했습니다.
