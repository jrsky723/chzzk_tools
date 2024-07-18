from chzzkpy.chat import ChatClient as BaseChatClient, ChatMessage, DonationMessage
from obs.nico_chat import NicoChat
from youtube_player.youtube_player import YoutubePlayer
import constants as const

class ChatClient(BaseChatClient):
    def __init__(self, channel_id, nico_chat: NicoChat, youtube_player: YoutubePlayer):
        super().__init__(channel_id)
        self.nico_chat = nico_chat
        self.youtube_player = youtube_player
        self.setup_event_handlers()

    def setup_event_handlers(self):
        @self.event
        async def on_chat(message: ChatMessage):
            if message.content.startswith(const.COMMAND_PREFIX):
                if message.content.startswith(f"{const.COMMAND_PREFIX}신청곡"):
                    await self.handle_song_request(message)
            elif message.content.startswith(const.RESPONSE_PREFIX):
                return
            else:
                color = 0xFFFFFF # white
                profile = message.profile
                nickname = profile.nickname if profile is not None else "Unknown"
                await self.nico_chat.splash_chat(message.content, nickname, color)

        @self.event
        async def on_donation(message: DonationMessage):
            profile = message.profile
            extras = message.extras
            nickname = profile.nickname if profile is not None else "Unknown"
            pay_amount = extras.pay_amount if extras is not None else 0
            await self.send_chat(f"{const.RESPONSE_PREFIX} {nickname}님, {pay_amount}원 후원 감사합니다.")
            # todo: donation alert

    async def handle_song_request(self, message: ChatMessage):
        try:
            parts = message.content.split(" ", 1)
            if len(parts) < 2:
                await self.send_chat(f"{const.RESPONSE_PREFIX} 잘못된 명령어 형식입니다. {const.COMMAND_PREFIX}신청곡 아티스트명 - 곡제목 으로 입력해주세요.")
                return
            
            song_info = parts[1].split("-", 1)
            if len(song_info) < 2:
                await self.send_chat(f"{const.RESPONSE_PREFIX} 잘못된 명령어 형식입니다. {const.COMMAND_PREFIX}신청곡 아티스트명 - 곡제목 으로 입력해주세요.")
                return

            artist = song_info[0].strip()
            title = song_info[1].strip()
            
            video_id, video_title = self.youtube_player.search_youtube(artist, title)
            if video_id is None:
                await self.send_chat(f"{const.RESPONSE_PREFIX} 신청곡을 찾을 수 없습니다: {video_title}")
                return
            self.youtube_player.update_html(video_id, video_title)
            self.youtube_player.refresh_browser_source("youtube_player") 

            await self.send_chat(f"{const.RESPONSE_PREFIX} 신청곡: {video_title}")
        except Exception as e:
            await self.send_chat(f"{const.RESPONSE_PREFIX} 신청곡 처리 중 오류가 발생했습니다: {e}")

    @staticmethod
    def hash_to_color(hash_str):
        hex_color = hash_str[2:8]
        return int(hex_color, 16)
