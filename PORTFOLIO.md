# Coffee Log

> 좋아하는 커피를 기록하고 서로의 취향을 발견하는 Django 기반 커피 커뮤니티

[GitHub 저장소](https://github.com/ionjk2879-eng/python-Django-)

![Coffee Log 대표 이미지](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/board/static/img/coffee-log-community-og.png)

## 1. 프로젝트 소개

Coffee Log는 원두, 커피 장비, 추출 레시피, 시음 노트와 카페 탐방 경험을 기록하고 공유하는 커뮤니티 서비스입니다. 단순 게시판 구현을 넘어 회원별 활동 관리, 다중 이미지 업로드, 좋아요와 북마크, 조건별 검색, 비동기 댓글 수정 등 실제 커뮤니티에 필요한 흐름을 Django의 인증·ORM·클래스 기반 뷰로 구현했습니다.

- 개발 형태: 개인 프로젝트
- 개발 목적: Django 서버 사이드 렌더링과 관계형 데이터 모델링 실습
- 주요 사용자: 홈카페 입문자, 커피 애호가, 추출 레시피를 공유하는 사용자
- UI 방향: 커피 브라운과 내추럴 톤을 활용한 반응형 커뮤니티

## 2. 핵심 기능

### 커뮤니티 게시판

- 게시글 작성, 조회, 수정, 삭제
- 원두 이야기, 커피 장비, 추출 레시피, 시음 노트, 카페 탐방 카테고리
- 제목·내용·작성자·태그 통합 검색 및 검색 범위 선택
- 최신순 목록과 페이지당 10개 페이지네이션
- 게시글별 최대 5개 이미지 업로드 및 기존 이미지 선택 삭제
- 레시피용 원두량, 물의 양, 물 온도, 추출 시간, 추출 도구 기록

### 사용자와 상호작용

- Google OAuth 소셜 로그인(django-allauth) 및 세션 인증
- 작성자만 게시글과 댓글을 수정·삭제할 수 있는 권한 제어
- 댓글 작성·수정·삭제를 페이지 이동 없이 그 자리에서 처리 (Fetch API로 DRF 댓글 API 호출)
- 게시글 좋아요 및 북마크 토글
- 마이페이지에서 프로필, 작성 글, 댓글 수, 북마크 현황 확인
- 프로필 이미지, 소개, 활동 지역, 이메일 수정 (파일 선택 시 이미지 미리보기)

### REST API (Django REST Framework)

- `/api/posts/` — 목록 조회(제목·내용·작성자·태그 검색, 카테고리 필터), 상세 조회, 생성·수정·삭제
- `/api/posts/{id}/recommendations/` — 같은 카테고리 내 좋아요순 추천
- `/api/posts/{id}/like/`, `/api/posts/{id}/bookmark/` — 로그인 사용자 전용 토글 액션
- `/api/comments/` — 댓글 생성·수정·삭제
- 세션 인증 재사용으로 별도 토큰 체계 없이 기존 로그인과 통합, 작성자 본인만 쓰기 가능하도록 객체 단위 권한(`IsAuthorOrReadOnly`) 적용

### 공유와 사용자 경험

- Tailwind CSS CDN 기반 반응형 UI
- htmx 기반 사이트 전역 부분 페이지 전환(PJAX): 전체 새로고침 없이 링크·폼 탐색, View Transitions API로 자연스러운 전환 효과
- Open Graph 및 Twitter Card 메타 태그
- 카카오톡 공유 미리보기를 위한 1200×630 대표 이미지
- JPEG, PNG, WebP 파일 형식과 파일당 5MB 제한 검증

## 3. 화면 구성

### 홈

브랜드 메시지와 카테고리 진입점을 먼저 제시하고 최근 커피 이야기를 이어서 탐색할 수 있도록 구성했습니다.

![홈 화면](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/01-home.jpg)

### 게시글 목록 (커뮤니티)

검색어와 카테고리, 검색 범위를 조합해 필요한 콘텐츠를 빠르게 찾을 수 있습니다.

![게시글 목록 화면](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/02-community.jpg)

### 게시글 상세

본문과 레시피 정보를 구조화해 보여주며 조회수, 좋아요, 북마크, 댓글을 한 화면에서 사용할 수 있습니다. 좋아요·북마크가 활성화된 상태입니다.

![게시글 상세 화면](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/03-post-detail.jpg)

### 게시글 작성

카테고리를 "추출 레시피"로 선택하면 원두량·물양·물 온도·추출 시간·추출 도구 등 레시피 전용 입력 필드가 나타납니다.

![게시글 작성 화면](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/04-write.jpg)

### 마이페이지

사용자 프로필과 활동 통계, 작성 글 및 저장한 게시글을 한곳에서 확인할 수 있습니다.

![마이페이지](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/05-mypage.jpg)

### 로그인

Google OAuth 소셜 로그인만 지원하는 인증 화면입니다.

![로그인 화면](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/06-login.jpg)

### REST API (DRF Browsable API)

`/api/posts/`를 브라우저로 직접 열면 DRF의 브라우저블 API로 응답을 확인할 수 있습니다.

![DRF API 화면](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/07-api.jpg)

### 댓글 인라인 수정

수정 버튼을 누르면 페이지 이동 없이 그 자리에서 바로 댓글을 편집할 수 있습니다.

![댓글 인라인 수정 화면](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/08-comment-edit.jpg)

### 프로필 편집

아바타, 이메일, 소개, 활동 지역을 수정할 수 있고 이미지 선택 시 바로 미리보기가 표시됩니다.

![프로필 편집 화면](https://raw.githubusercontent.com/ionjk2879-eng/python-Django-/main/portfolio/screenshots/09-profile-edit.jpg)

## 4. 기술 스택

| 구분 | 기술 |
|---|---|
| Backend | Python 3.13, Django 6.0, Django REST Framework |
| Database | PostgreSQL 16 (Docker Compose), Django ORM |
| Frontend | Django Templates, Tailwind CSS CDN, htmx, Vanilla JavaScript |
| Authentication | django-allauth (Google OAuth), Session |
| Forms | Django Forms, django-widget-tweaks |
| Infra | Docker Compose, python-dotenv (환경 변수 기반 비밀정보 관리) |
| Version Control | Git, GitHub |

## 5. 시스템 구조

```text
Browser
  │ HTTP request / form / Fetch API
  ▼
Django URL Router
  ├── accounts: Google OAuth 인증(allauth), 프로필, 마이페이지
  ├── board: 게시글, 이미지, 댓글, 좋아요, 북마크 (서버 렌더링)
  └── api: DRF ViewSet 기반 게시글·댓글 REST API
       │
       ▼
Class-Based Views + Forms  /  DRF Serializers + Permissions
       │
       ▼
Django ORM
       │
       ▼
PostgreSQL (Docker)
```

### 데이터 관계

```text
User 1 ─── 1 Profile
User 1 ─── N Post
User 1 ─── N Comment
Post 1 ─── N PostImage
Post 1 ─── N Comment
User N ─── M Post (liked_by)
User N ─── M Post (bookmarked_by)
```

## 6. 주요 기술적 구현

### 동시 요청에도 안전한 조회수 증가

게시글 객체의 기존 값을 Python에서 읽어 더하는 대신 `F()` 표현식으로 데이터베이스에서 직접 증가시켰습니다. 여러 요청이 동시에 들어왔을 때 증가 값이 유실될 가능성을 줄였습니다.

```python
Post.objects.filter(pk=obj.pk).update(view_count=F('view_count') + 1)
obj.refresh_from_db(fields=['view_count'])
```

### 검색 조건의 동적 결합

`Q` 객체를 사용해 제목, 내용, 작성자, 태그 조건을 통합하고 사용자가 선택한 검색 범위에 따라 조건을 분기했습니다. 카테고리 필터와 검색어 조건도 하나의 QuerySet 안에서 조합합니다.

### N+1 쿼리 완화

게시글 목록과 상세 화면에서 작성자·프로필은 `select_related()`, 이미지·좋아요·북마크는 `prefetch_related()`로 함께 조회합니다. 댓글 수와 좋아요 수는 `Count()`로 주석 처리해 템플릿에서 반복 쿼리가 발생하지 않도록 구성했습니다.

### 다중 이미지 업로드의 정합성

- 허용 확장자와 MIME 타입을 함께 검사
- 파일당 최대 5MB, 게시글당 최대 5개 제한
- 수정 시 선택한 기존 이미지를 삭제한 후 최종 이미지 수 재검증
- 게시글 저장과 이미지 처리를 `transaction.atomic`으로 묶어 일부만 저장되는 상황 방지

### 객체 단위 권한 제어

`LoginRequiredMixin`과 `UserPassesTestMixin`을 조합해 인증 여부와 작성자 일치 여부를 뷰 계층에서 검사합니다. 화면에서 버튼을 감추는 수준이 아니라 서버에서 수정·삭제 권한을 강제합니다.

### 점진적 비동기 처리와 PJAX 네비게이션

React 같은 SPA 프레임워크로 전면 전환하는 대신, 서버 렌더링(Django 템플릿) 구조는 그대로 두고 htmx의 `hx-boost`로 링크·폼 탐색을 가로채 페이지의 `<body>`만 교체하는 PJAX 방식을 전역에 적용했습니다. 브라우저 View Transitions API를 연결해 전환 시 짧은 크로스페이드 효과를 주고, 미지원 브라우저에서는 자동으로 일반 전환으로 폴백됩니다.

댓글 작성·수정·삭제처럼 상호작용이 더 잦은 부분은 htmx 전역 처리와 별도로 자체 Fetch 코드를 작성해 DRF 댓글 API를 직접 호출하고 해당 댓글 DOM만 교체합니다. 이 둘을 같은 페이지에 함께 적용하면서 **htmx가 모든 폼을 자동으로 가로채 기존 Fetch 코드와 동시에 같은 댓글을 두 번 생성하는 버그**를 발견했고, 댓글 폼에 `hx-boost="false"`를 지정해 htmx 처리 대상에서 제외하는 방식으로 해결했습니다. 여러 비동기 처리 계층이 겹칠 때 이벤트 핸들러 간 충돌을 식별하고 범위를 명확히 분리하는 경험이었습니다.

## 7. 프로젝트 구조

```text
accounts/                  Google OAuth 인증, 프로필, 마이페이지
board/                     게시글, 이미지, 댓글, 반응 기능
  api/                     DRF serializers, permissions, viewsets
  management/commands/     포트폴리오 데모 데이터 생성 명령
  static/img/              브랜드·카테고리·Open Graph 이미지
config/                    Django 프로젝트 설정과 루트 URL
templates/                 공통 레이아웃과 인증 템플릿
portfolio/screenshots/     포트폴리오 화면 캡처
docker-compose.yml         로컬 PostgreSQL 컨테이너
manage.py
requirements.txt
```

## 8. 테스트 및 검증

Django 테스트 데이터베이스에서 인증과 게시판의 핵심 동작을 검증했습니다.

- 테스트 5개 통과
- Django system check 이상 없음
- 프로필 수정, 카테고리·태그 검색, 게시글 이미지 업로드, 좋아요·북마크 토글, 프로필이 없는 작성자의 상세 화면 렌더링 검증

```text
Ran 5 tests
OK
System check identified no issues (0 silenced).
```

## 9. 로컬 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# .env에 DB_NAME, DB_USER, DB_PASSWORD, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET 설정 후
docker compose up -d          # PostgreSQL 컨테이너 기동
python manage.py migrate
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/`으로 접속합니다. Google 로그인을 쓰려면 Google Cloud Console에서 OAuth 클라이언트를 발급받아 `.env`에 등록하고, 승인된 리디렉션 URI에 `http://localhost:8000/accounts/google/login/callback/`을 추가해야 합니다.

포트폴리오용 데모 데이터를 생성하려면 다음 명령을 실행합니다.

```powershell
python manage.py seed_portfolio
```

## 10. 회고와 확장 계획

이 프로젝트를 통해 Django의 인증, ORM 관계 모델, 클래스 기반 뷰, 폼 검증과 서버 사이드 렌더링을 하나의 사용자 흐름으로 연결했습니다. 특히 기능 구현에 그치지 않고 쿼리 효율, 객체 단위 권한, 동시성, 업로드 정합성을 고려하면서 커뮤니티 서비스의 기본 구조를 설계했습니다.

이후 SQLite에서 PostgreSQL(Docker Compose)로 전환하고, 비밀정보를 `.env`로 분리했습니다. 검색·추천·상세 조회 기능은 처음에 별도 FastAPI 서비스로 구현했다가, Django 세션 인증을 그대로 재사용할 수 있고 서버를 하나로 유지할 수 있다는 이유로 Django REST Framework로 통합하는 방향으로 재설계했습니다. 인증도 자체 회원가입 대신 Google OAuth(django-allauth)로 전환해 비밀번호 관리 부담을 없앴습니다. 이 과정에서 두 프레임워크의 트레이드오프(프로세스 분리 여부, 인증 재사용성, 운영 복잡도)를 직접 비교하고 프로젝트 규모에 맞는 선택을 하는 경험을 했습니다.

이어서 페이지 전환 시 화면이 매번 새로고침되는 문제를 htmx 기반 PJAX 방식으로 개선했습니다. React로 전면 SPA화하는 대신 기존 Django 템플릿 구조를 유지하면서 필요한 부분만 부분 교체하는 절충안을 택했고, 그 과정에서 기존 Fetch 기반 댓글 처리와 htmx의 자동 폼 처리가 충돌해 댓글이 중복 생성되는 버그를 겪고 원인을 추적해 수정했습니다.

향후에는 클라우드 이미지 스토리지, 알림 기능, 자동화 테스트 확대, CI/CD 및 운영 서버 배포를 적용해 프로덕션 수준으로 확장할 계획입니다.
