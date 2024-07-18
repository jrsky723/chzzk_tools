class Path:
    DOTENV_PATH = "env/.env"

class Screen:
    WIDTH = 1920
    HEIGHT = 1080

class Prefix:
    COMMAND_PREFIX = "!"
    RESPONSE_PREFIX = "응답:"

class Message:
        RESPONSE = f"{Prefix.RESPONSE_PREFIX} {{}}"
        INVALID_COMMAND = f"{Prefix.RESPONSE_PREFIX} 잘못된 명령어 형식입니다: {{}} (으)로 입력해주세요."
        DONATION_THANKS = f"{Prefix.RESPONSE_PREFIX} {{}}님, {{}}원 후원 감사합니다."
