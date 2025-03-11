from fastapi import FastAPI, Request
import logging
import uvicorn
import json

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

def clean_json_string(json_str: str) -> str:
    """JSON 문자열을 정제하고 이스케이프 문자를 처리합니다."""
    # 제어 문자 제거
    import re
    json_str = re.sub(r'[\x00-\x1F\x7F]', '', json_str)
    return json_str

@app.post("/webhook")
async def github_webhook(request: Request):
    try:
        # 원본 요청 데이터 로깅
        body = await request.body()
        raw_data = body.decode('utf-8')
        logger.debug("Raw request body: %s", raw_data)
        
        # 헤더 정보 로깅
        logger.debug("Request headers:")
        for name, value in request.headers.items():
            logger.debug(f"{name}: {value}")

        # JSON 문자열 정제
        cleaned_data = clean_json_string(raw_data)
        logger.debug("Cleaned JSON data: %s", cleaned_data)

        # JSON 파싱
        try:
            payload = json.loads(cleaned_data)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Error position: line {e.lineno}, column {e.colno}")
            # 문제가 발생한 위치의 전후 컨텍스트 출력
            error_context = cleaned_data[max(0, e.pos-50):min(len(cleaned_data), e.pos+50)]
            logger.error(f"Context around error: ...{error_context}...")
            return {"status": "error", "message": f"Invalid JSON format: {str(e)}"}
        
        # 웹훅 이벤트 타입 확인
        event_type = request.headers.get("X-GitHub-Event", "no-event")
        logger.info(f"Received {event_type} event")
        
        # 페이로드 처리
        if event_type == "push":
            logger.info(f"Push to {payload.get('ref')} by {payload.get('pusher', {}).get('name')}")
            if 'commits' in payload:
                for commit in payload['commits']:
                    logger.info(f"Commit: {commit.get('message', 'No message')} ({commit.get('id', 'No ID')})")
        
        return {"status": "success", "message": "Webhook received and processed"}
        
    except Exception as e:
        logger.exception("Error processing webhook")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 