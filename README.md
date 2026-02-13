## 🎬 Demo Video

> Django 기반 계좌 중심 가계부 웹 애플리케이션 시연 영상  
> (회원가입 → 계좌 생성 → 거래 등록 → 대시보드 확인)

[![Mini Ledger Demo](https://img.youtube.com/vi/AjXKGRciI0Y/maxresdefault.jpg)](https://youtu.be/AjXKGRciI0Y)

# 💰 Mini Ledger - Django 가계부 프로젝트

Django 기반의 계좌 중심 가계부 웹 애플리케이션입니다.
수입/지출 관리, 계좌 관리, 대시보드 시각화를 포함한 MVP 프로젝트입니다.

---

## 📌 프로젝트 개요

본 프로젝트는 다음을 목표로 제작되었습니다:

* Django 기반 CRUD 구조 이해
* 도메인 모델 설계 (User → Account → Transaction)
* 대시보드 집계 및 시각화 구현
* JavaScript 없이 CSS 기반 그래프 구현
* URL 구조 및 앱 분리 설계

---

## 🏗 도메인 구조

```
User
 └── Account (여러 개)
       └── Expense(Transaction) (여러 개)
```

### 핵심 관계

* 한 사용자는 여러 개의 계좌(Account)를 가질 수 있다.
* 각 계좌에는 여러 개의 거래(Expense)가 속한다.
* 거래는 수입(IN) 또는 지출(OUT)로 구분된다.

---

## ✨ 주요 기능

### 🔐 인증

* 회원가입
* 로그인 / 로그아웃

### 💳 계좌 관리 (Account CRUD)

* 계좌 생성 / 수정 / 삭제
* 사용자별 계좌 분리

### 💸 거래 관리 (Expense CRUD)

* 카테고리 선택 (음식/교통/기타 등)
* 수입/지출 구분 (tx_type)
* 계좌 선택 (ForeignKey 연결)
* 필터 및 검색 기능

### 📊 대시보드

* 월별 KPI

  * 총 수입
  * 총 지출
  * 순합
  * 거래 건수
* 카테고리별 지출 비율 그래프
* 최근 6개월 지출 추이
* 일별 지출 추이
* 그래프는 JS 없이 CSS로 구현
* 차트 금액은 만원 단위 표시

---

## 🛠 기술 스택

* Python 3.x
* Django 4.x
* SQLite (개발 환경)
* HTML5 / CSS3
* Django Template Engine
* django.contrib.humanize (숫자 포맷)

---

## 📁 프로젝트 구조

```
mini-ledger/
│
├── accounts/      # 인증 관련 앱
├── banking/       # 계좌(Account) 관리 앱
├── expenses/      # 거래(Expense) 관리 및 대시보드
├── config/        # 프로젝트 설정
├── templates/
├── static/
└── db.sqlite3
```

---

## 🚀 실행 방법

### 1️⃣ 가상환경 생성

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

### 2️⃣ 패키지 설치

```bash
pip install django
```

### 3️⃣ 마이그레이션

```bash
python manage.py migrate
```

### 4️⃣ 서버 실행

```bash
python manage.py runserver
```

브라우저 접속:

```
http://127.0.0.1:8000/
```

---

# 📄 기술 설계 문서

## 1. 아키텍처 설계

본 프로젝트는 Django MVT(Model-View-Template) 구조를 따른다.

### 앱 분리 전략

| 앱        | 역할        |
| -------- | --------- |
| accounts | 인증 처리     |
| banking  | 계좌 도메인    |
| expenses | 거래 및 대시보드 |

도메인 단위로 앱을 분리하여 확장성을 확보하였다.

---

## 2. 데이터 모델 설계

### Account

* user (ForeignKey)
* name
* created_at

### Expense

* user (ForeignKey)
* account (ForeignKey)
* category
* tx_type (IN / OUT)
* amount
* memo
* spent_at

---

## 3. 집계 로직

### 월별 KPI 계산

```
총수입 = SUM(IN)
총지출 = SUM(OUT)
순합 = 총수입 - 총지출
```

### 최근 6개월 집계

* Python에서 월 단위 shift 계산
* DB에서 범위 조회
* 퍼센트 계산 후 템플릿 전달

---

## 4. 그래프 구현 방식

* JavaScript 사용하지 않음
* CSS flex 기반 세로 막대 구현
* 퍼센트 height 계산
* 금액은 만원 단위 반올림 처리

---

## 5. 보안

* login_required 적용
* 사용자별 데이터 분리 (user=request.user 필터)
* CSRF 보호 활성화

---

## 6. URL 설계

```
/               → Dashboard
/accounts/      → 인증
/banking/       → 계좌
/expenses/      → 거래
```

서비스 메인 = 대시보드

---