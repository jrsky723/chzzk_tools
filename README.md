# 치지직 도구모음

python version: 3.10.7

## 가상환경 설치

```sh
python -m venv .venv
.venv\Scripts\activate
```

## Dependencies 설치

```sh
pip install -r requirements.txt
```

## 환경 변수 설정

프로젝트를 실행하려면, 프로젝트 루트 디렉토리의 `env` 폴더에 `.env` 파일을 생성하고, 아래 예시와 같이 환경 변수를 입력해주세요.

- **NID_AUT**와 **NID_SES**: 치지직에 로그인 후 브라우저의 개발자 도구에서 `Application -> Cookies` 항목에서 치지직 탭을 통해 확인할 수 있습니다.
- **OBS 변수들**: OBS에서 `도구 -> 플러그인 설정 -> WebSocket 서버 사용`을 체크한 후, `서버 설정 -> 서버정보 표시`에서 확인할 수 있습니다.

### .env 파일 예시

```env
CHANNEL_ID="your_channel_id_here"
NID_AUT="your_nid_aut_here"
NID_SES="your_nid_ses_here"
OBS_HOST="localhost"
OBS_PORT="4455"
OBS_PASSWORD="your_obs_password_here"
YOUTUBE_DATA_API_KEY="your_youtube_data_api_key"
```

# 프로젝트 설명

## 1. 기능

- 니코동 감성 채팅
- 유튜브 신청곡 기능
  - 스킵 투표 기능

### 1.1. 니코동 감성 채팅

- 채팅 입력시, 화면 우측에서 좌측으로 이동하는 애니메이션이 적용되는 기능

### 1.2. 유튜브 신청곡 기능

- 사용자가 유튜브 링크를 입력하면, 해당 링크의 영상과 설명이, OBS의 브라우저 소스에 자동으로 추가되는 기능

### 1.2.1. 스킵 투표 기능

- 신청곡의 스킵을 투표 할 수 있음 (다른 사용자 까지)
  - 스킵 | 유지 중, 스킵이 과반수를 넘으면 스킵 시간(10초) 후 스킵됨
  - 문제점:
    - 사용자간의 분쟁이 발생할 수 있음...
    - 아직 얀모 채널이 너무 작아서, 기능의 사용법과 의도를 시청자들이 알기 어렵다...
    - 대체 방안: 시청자가 자기 자신의 신청곡만 스킵 할 수 있도록
