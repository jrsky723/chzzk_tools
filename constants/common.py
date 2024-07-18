class Path:
    DOTENV_PATH = "env/.env"

class Screen:
    WIDTH = 1920
    HEIGHT = 1080

UNDEFINED = "UNDEFINED"

class Prefix:
    COMMAND_PREFIX = "!"
    RESPONSE_PREFIX = "응답:"

class Command:
    HELLO = f"{Prefix.COMMAND_PREFIX}안녕"
    LIST = f"{Prefix.COMMAND_PREFIX}명령어"
    SONG_REQUEST = f"{Prefix.COMMAND_PREFIX}신청곡"

class Message:
        HELLO = f"{Prefix.RESPONSE_PREFIX} 안녕하세요! {{}}님, 반가워요!"
        RESPONSE = f"{Prefix.RESPONSE_PREFIX} {{}}"
        INVALID_COMMAND = f"{Prefix.RESPONSE_PREFIX} 잘못된 명령어 형식입니다: {{}} (으)로 입력해주세요."
        DONATION_THANKS = f"{Prefix.RESPONSE_PREFIX} {{}}님, {{}}원 후원 감사합니다."