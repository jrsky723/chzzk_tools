from constants.common import Prefix

class Message:
        COMMAND = f"{Prefix.COMMAND_PREFIX}신청곡"
        COMMAND_FORMAT = f"{Prefix.COMMAND_PREFIX}신청곡 아티스트명 - 곡제목"
        SONG_NOT_FOUND = f"{Prefix.RESPONSE_PREFIX} 신청곡을 찾을 수 없습니다: {{}}"
        SONG_REQUEST_SUCCESS = f"{Prefix.RESPONSE_PREFIX} 신청곡: {{}}"
        SONG_REQUEST_ERROR = f"{Prefix.RESPONSE_PREFIX} 신청곡 처리 중 오류가 발생했습니다: {{}}"
        