from fastapi import FastAPI, Request
import logging
import uvicorn

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    # webhook 페이로드를 딕셔너리로 받기
    try:
        payload = await request.json()
        
        # 디버깅을 위한 로그 출력
        logger.debug("Received webhook payload:")
        logger.debug(f"Event type: {request.headers.get('X-GitHub-Event', 'No event type')}")
        logger.debug(f"Delivery ID: {request.headers.get('X-GitHub-Delivery', 'No delivery ID')}")
        logger.debug(f"Payload: {payload}")
        
        return {"status": "success", "message": "Webhook received"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 