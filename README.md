# 치지직 도구모음

## Dependencies 설치
pip install -r requirements.txt

## 환경 변수 설정

이 프로젝트를 실행하려면, 프로젝트 루트 디렉토리의 `env` 폴더에 `.env` 파일을 생성하고, 아래 예시와 같이 환경 변수를 입력해주세요.

- **NID_AUT**와 **NID_SES**: 치지직에 로그인 후 브라우저의 개발자 도구에서 `Application -> Cookies` 항목에서 치지직 탭을 통해 확인할 수 있습니다.
- **OBS 변수들**: OBS에서 `도구 -> 플러그인 설정 -> WebSocket 서버 사용`을 체크한 후, `서버 설정 -> 서버정보 표시`에서 확인할 수 있습니다.

### .env 파일 예시

```env
CHANNEL_ID=your_channel_id_here 
NID_AUT=your_nid_aut_here
NID_SES=your_nid_ses_here
OBS_HOST=localhost
OBS_PORT=4455
OBS_PASSWORD=your_obs_password_here
```

