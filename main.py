from dotenv import load_dotenv
import os
import constants as const
import obsws_python as obs
from chzzkpy.chat import ChatClient, ChatMessage, DonationMessage
from obs.nico_chat import NicoChat

load_dotenv(dotenv_path=const.DOTENV_PATH)

# get environment variables
CHANNEL_ID = os.getenv("CHANNEL_ID")
NID_AUT = os.getenv("NID_AUT")
NID_SES = os.getenv("NID_SES")
OBS_HOST = os.getenv('OBS_HOST')
OBS_PORT = int(os.getenv('OBS_PORT'))
OBS_PASSWORD = os.getenv('OBS_PASSWORD')

# create clients
chzzk_cl = ChatClient(CHANNEL_ID)

nico_chat = NicoChat(OBS_HOST, OBS_PORT, OBS_PASSWORD)


def hash_to_color(hash_str):
    # 해시값의 앞 6자리를 이용해 RGB 값 생성
    hex_color = hash_str[2:8]
    # 16진수 값을 10진수 RGB 값으로 변환
    return int(hex_color, 16)


@chzzk_cl.event
async def on_chat(message: ChatMessage):
    color = hash_to_color(message.profile.user_id_hash)
    print(color)
    await nico_chat.splash_chat(message.content, message.profile.nickname, color)
    # if message.content == "!안녕":
    #     await chzzk_cl.send_chat("%s님, 안녕하세요!" % message.profile.nickname)
    # if message.content == "!신청곡":
    #     await chzzk_cl.send_chat("%s님, 신청곡은 현재 받지 않고 있습니다." % message.profile.nickname)

@chzzk_cl.event
async def on_donation(message: DonationMessage):
    await chzzk_cl.send_chat("%s님, %d원 후원 감사합니다." % (message.profile.nickname, message.extras.pay_amount))


chzzk_cl.run(NID_AUT, NID_SES)