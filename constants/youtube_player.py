from constants.common import Prefix, CommandName

# 한번에 할 수 있는 최대 요청 횟수
MAX_REQUESTS = 3

# 출력 시의 영상 제목 최대 길이
MAX_TITLE_LENGTH = 30

# 동영상 스킵 대기 시간 (초)
SKIP_WAIT_TIME = 10

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
        REQUEST_SUCCESS = f"{Prefix.RESPONSE_PREFIX} {{}} 추가되었습니다 (신청: {{}}/{{}}회)"
        REQUEST_BANNED_KEYWORD = f"{Prefix.RESPONSE_PREFIX} 영상 제목에 금지어가 포함되어 있습니다: {{}}"
        REQUEST_BANNED_CHANNEL = f"{Prefix.RESPONSE_PREFIX} 유튜브 채널명이 금지되어 있습니다: {{}}"
        REQUEST_ERROR = f"{Prefix.RESPONSE_PREFIX} 요청 중 오류가 발생했습니다"
        INVALID_URL = f"{Prefix.RESPONSE_PREFIX} 유효하지 않은 URL입니다: {{}}"

        # 시간
        INVALID_TIME_FORMAT = f"{Prefix.RESPONSE_PREFIX} 잘못된 시간 형식입니다: {{}} (Ex: 3:40, 10:30, 1:30:00)"
        INVALID_TIME = f"{Prefix.RESPONSE_PREFIX} 잘못된 시간입니다: {{}}"

        # 신청 횟수
        REQUEST_LIMIT_REACHED = f"{Prefix.RESPONSE_PREFIX} {{}}님의 신청 횟수가 초과되었습니다 (최대 {{}}회)"

        # 투표
        VOTE_ERROR = f"{Prefix.RESPONSE_PREFIX} 투표 중 오류가 발생했습니다"
        VOTE_SUCCESS = f"{Prefix.RESPONSE_PREFIX} {{}} 투표 완료! (스킵:{{}} | 유지:{{}})"
        NO_VIDEO_PLAYING = f"{Prefix.RESPONSE_PREFIX} 현재 재생 중인 영상이 없습니다"
        SKIP_COUNT_START = f"{Prefix.RESPONSE_PREFIX} {{}}로 인해 {SKIP_WAIT_TIME}초 후 영상을 스킵합니다 (스킵:{{}} | 유지:{{}})"
        KEEP_VIDEO = f"{Prefix.RESPONSE_PREFIX} {{}}로 인해 영상을 유지합니다 (스킵:{{}} | 유지:{{}})"


class Status:
        SUCCESS = "SUCCESS"
        ERROR = "ERROR"
        NOT_FOUND = "NOT_FOUND"
        BANNED_CHANNEL = "BANNED_CHANNEL"
        BANNED_KEYWORD = "BANNED_KEYWORDS"

# 밴하는 채널 리스트를 추가
BANNED_CHANNEL_TITLE = {

}


BANNED_KEYWORDS = {}