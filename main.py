from dotenv import load_dotenv
import os
import obsws_python as obs
from chzzk.chat_client import ChatClient
from obs.nico_chat import NicoChat
from youtube_player.player import YoutubePlayer
from constants.common_const import Path as CommonPath, FunctionName
from tk_gui.app import App
import tkinter as tk
import threading


def init_clients(tk_vars):
    load_dotenv(dotenv_path=CommonPath.DOTENV_PATH)

    # 환경 변수 로드
    CHANNEL_ID = str(os.getenv("CHANNEL_ID"))
    NID_AUT = str(os.getenv("NID_AUT"))
    NID_SES = str(os.getenv("NID_SES"))
    OBS_HOST = str(os.getenv("OBS_HOST"))
    OBS_PORT = int(str(os.getenv("OBS_PORT")))
    OBS_PASSWORD = str(os.getenv("OBS_PASSWORD"))
    YOUTUBE_DATA_API_KEY = str(os.getenv("YOUTUBE_DATA_API_KEY"))

    # 클라이언트 생성
    obs_cl = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)
    nico_chat = NicoChat(obs_cl)
    youtube_player = YoutubePlayer(obs_cl, YOUTUBE_DATA_API_KEY)
    chzzk_cl = ChatClient(CHANNEL_ID, nico_chat, youtube_player, tk_vars)

    # 클라이언트 실행을 별도의 스레드에서 실행
    threading.Thread(target=chzzk_cl.run, args=(NID_AUT, NID_SES), daemon=True).start()

    return nico_chat, youtube_player, chzzk_cl


def main():
    root = tk.Tk()
    # GUI 변수 초기화
    tk_vars = {
        FunctionName.NICO_CHAT: tk.BooleanVar(value=True),
        FunctionName.YOUTUBE: tk.BooleanVar(value=True),
        FunctionName.HELLO: tk.BooleanVar(value=True),
        FunctionName.SKIP_VOTE: tk.BooleanVar(value=True),
    }
    nico_chat, youtube_player, chzzk_cl = init_clients(tk_vars)

    app = App(root, nico_chat, youtube_player, chzzk_cl, tk_vars)

    youtube_player.set_refresh_ui_callback(app.update_video_list)

    root.mainloop()


if __name__ == "__main__":
    main()
