from constants.common import Prefix, CommandName

class Source:
        NAME = "youtube_player"
        WIDTH = 1280
        HEIGHT = 880
        OUTPUT = "output.html"
        TEMPLATE = "template.html"

class Message:
        SEARCH_ERROR = f"{Prefix.RESPONSE_PREFIX} 유튜브 검색 중 오류가 발생했습니다"
        DURATION_ERROR = f"{Prefix.RESPONSE_PREFIX} 영상의 길이를 가져오는 중 오류가 발생했습니다"
        NOT_FOUND = f"{Prefix.RESPONSE_PREFIX} 영상을 찾을 수 없습니다: {{}}"
        REQUEST_SUCCESS = f"{Prefix.RESPONSE_PREFIX} {{}} 추가되었습니다"
        REQUEST_BANNED_KEYWORD = f"{Prefix.RESPONSE_PREFIX} 영상 제목에 금지어가 포함되어 있습니다: {{}}"
        REQUEST_BANNED_CHANNEL = f"{Prefix.RESPONSE_PREFIX} 유튜브 채널명이 금지되어 있습니다: {{}}"
        REQUEST_ERROR = f"{Prefix.RESPONSE_PREFIX} 요청 중 오류가 발생했습니다"
        INVALID_URL = f"{Prefix.RESPONSE_PREFIX} 유효하지 않은 URL입니다: {{}}"
        

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
}


BANNED_KEYWORDS = {
        "욕설",
        "예수",
        "대깨문",
        "종북",
        "종자",
}