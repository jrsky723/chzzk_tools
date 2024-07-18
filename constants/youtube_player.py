from constants.common import Prefix

SOURCE_NAME = "youtube_player"

class Message:
        COMMAND_FORMAT = f"{Prefix.COMMAND_PREFIX}신청곡 아티스트명 - 곡제목"
        NOT_FOUND = f"{Prefix.RESPONSE_PREFIX} 신청곡을 찾을 수 없습니다: {{}}"
        REQUEST_SUCCESS = f"{Prefix.RESPONSE_PREFIX} 신청곡: {{}}"
        REQUEST_ERROR = f"{Prefix.RESPONSE_PREFIX} 신청곡 처리 중 오류가 발생했습니다: {{}}"
        REQUEST_BANNED_KEYWORD = f"{Prefix.RESPONSE_PREFIX} 신청곡이 금지어로 등록되어 있습니다: {{}}"
        REQUEST_BANNED_CHANNEL = f"{Prefix.RESPONSE_PREFIX} 신청곡의 채널이 금지어로 등록되어 있습니다: {{}}"
        


class Status:
        SUCCESS = "SUCCESS"
        ERROR = "ERROR"
        NOT_FOUND = "NOT_FOUND"
        BANNED_CHANNEL = "BANNED_CHANNEL"
        BANNED_KEYWORD = "BANNED_KEYWORDS"

# 밴하는 채널 리스트를 추가
BANNED_CHANNEL_TITLE = {
        "얀모",
        "뮤직모",
        "겜모",
        "개형",
}


BANNED_KEYWORDS = {
        "욕설",
        "예수",
        "대깨문",
        "종북",
        "종자",
}