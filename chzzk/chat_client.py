from chzzkpy.chat import ChatClient as BaseChatClient, ChatMessage, DonationMessage
from obs.nico_chat import NicoChat
from youtube_player.player import YoutubePlayer
import constants.common as const
import constants.youtube_player as youtubeConst
from utils import parse_time, is_valid_url


class ChatClient(BaseChatClient):
    def __init__(self, channel_id, nico_chat: NicoChat, youtube_player: YoutubePlayer, tk_vars):
        super().__init__(channel_id)
        self.nico_chat = nico_chat
        self.youtube_player = youtube_player
        self.tk_vars = tk_vars
        self.setup_event_handlers()

    def setup_event_handlers(self):
        @self.event
        async def on_chat(message: ChatMessage):
            color = 0xFFFFFF # white
            content = message.content
            profile = message.profile
            nickname = profile.nickname if profile is not None else const.UNDEFINED
            if content.startswith(const.Prefix.COMMAND_PREFIX):
                if content.startswith(const.CommandPrefix.YOUTUBE) and self.tk_vars['command_vars'][const.CommandName.YOUTUBE].get():
                    await self.handle_video_request(message)
                elif content.startswith(const.CommandPrefix.HELLO) and self.tk_vars['command_vars'][const.CommandName.HELLO].get():
                    await self.send_chat(const.Message.HELLO.format(nickname))
                
            elif content.startswith(const.Prefix.RESPONSE_PREFIX):
                return
            else:
                if self.tk_vars['nico_chat_var'].get():
                    await self.nico_chat.splash_chat(message.content, color)

        @self.event
        async def on_donation(message: DonationMessage):
            profile = message.profile
            extras = message.extras
            nickname = profile.nickname if profile is not None else const.UNDEFINED
            pay_amount = extras.pay_amount if extras is not None else 0
            await self.send_chat(const.Message.DONATION_THANKS.format(nickname, pay_amount))
            # todo: donation alert

    async def handle_video_request(self, message: ChatMessage):
        try:    #!유튜브 <동영상 링크> (시작시간) (종료시간)
            parts = message.content.split(" ", 2)
            if len(parts) < 2:
                await self.send_chat(const.Message.INVALID_COMMAND.format(const.CommandFormat.YOUTUBE))
                return
            
            video_url = parts[1].strip()
            # 유효한 URL인지 확인
            if not is_valid_url(video_url):
                await self.send_chat(youtubeConst.Message.INVALID_URL.format(video_url))
                return

            start_time = None
            end_time = None
            # 시작 시간과 종료 시간이 주어졌는지 확인
            if len(parts) > 2:
                times = parts[2].split(" ")
                if len(times) > 0:
                    start_time = parse_time(times[0])
                if len(times) > 1:
                    end_time = parse_time(times[1])
                    

            result:str = self.youtube_player.execute_video_request(video_url, start_time, end_time)
            await self.send_chat(result)
        except ValueError as ve:
            await self.send_chat(youtubeConst.Message.INVALID_TIME_FORMAT.format(ve))
        except Exception as e:
            await self.send_chat(youtubeConst.Message.REQUEST_ERROR)
            print(f"Error in handle_video_request: {e}")

    @staticmethod
    def hash_to_color(hash_str):
        hex_color = hash_str[2:8]
        return int(hex_color, 16)
