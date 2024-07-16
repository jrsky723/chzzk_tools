import logging
# 로그 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat.log'),  # 로그를 파일에 기록
        logging.StreamHandler()  # 로그를 콘솔에 출력
    ]
)

logger = logging.getLogger(__name__)
