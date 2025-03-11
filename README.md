# GitHub Webhook Listener

GitHub webhook 요청을 받아서 디버그 로그를 출력하는 FastAPI 애플리케이션입니다.

## 설치 방법

```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
python main.py
```

서버는 `http://localhost:8000/webhook`에서 GitHub webhook 요청을 수신합니다.

## GitHub Webhook 설정 방법

1. GitHub 리포지토리의 Settings > Webhooks로 이동
2. "Add webhook" 클릭
3. Payload URL에 `http://your-server:8000/webhook` 입력
4. Content type을 `application/json`으로 설정
5. 원하는 이벤트 선택
6. "Add webhook" 클릭하여 저장 
"# test" 
"# test" 
