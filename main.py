from dotenv import load_dotenv
import os
import constants as const
import obsws_python as obs
from chzzk.chat_client import ChatClient
from obs.nico_chat import NicoChat
from youtube_player.youtube_player import YoutubePlayer

def main():
    load_dotenv(dotenv_path=const.DOTENV_PATH)

    # 환경 변수 로드
    CHANNEL_ID = str(os.getenv("CHANNEL_ID"))
    NID_AUT = str(os.getenv("NID_AUT"))
    NID_SES = str(os.getenv("NID_SES"))
    OBS_HOST = str(os.getenv('OBS_HOST'))
    
    OBS_PORT = int(str(os.getenv('OBS_PORT')))
    OBS_PASSWORD = str(os.getenv('OBS_PASSWORD'))
    YOUTUBE_DATA_API_KEY = str(os.getenv('YOUTUBE_DATA_API_KEY'))

    # 클라이언트 생성
    obs_cl = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)
    nico_chat = NicoChat(obs_cl)
    youtube_player = YoutubePlayer(obs_cl, YOUTUBE_DATA_API_KEY)
    chzzk_cl = ChatClient(CHANNEL_ID, nico_chat, youtube_player)

    # 클라이언트 실행
    chzzk_cl.run(NID_AUT, NID_SES)

if __name__ == "__main__":
    main()