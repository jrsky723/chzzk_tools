from chzzkpy.chat import ChatClient as BaseChatClient, ChatMessage, DonationMessage
from obs.nico_chat import NicoChat
from youtube_player.youtube_player import YoutubePlayer
import constants.common as const
import constants.youtube_player as youtubeConst

class ChatClient(BaseChatClient):
    def __init__(self, channel_id, nico_chat: NicoChat, youtube_player: YoutubePlayer):
        super().__init__(channel_id)
        self.nico_chat = nico_chat
        self.youtube_player = youtube_player
        self.setup_event_handlers()

    def setup_event_handlers(self):
        @self.event
        async def on_chat(message: ChatMessage):
            color = 0xFFFFFF # white
            content = message.content
            profile = message.profile
            nickname = profile.nickname if profile is not None else const.UNDEFINED
            if content.startswith(const.Prefix.COMMAND_PREFIX):
                if content.startswith(const.Command.SONG_REQUEST):
                    await self.handle_song_request(message)
                elif content.startswith(const.Command.HELLO):
                    await message.send(const.Message.HELLO.format(nickname))
                
            elif content.startswith(const.Prefix.RESPONSE_PREFIX):
                return
            else:
                await self.nico_chat.splash_chat(message.content, nickname, color)

        @self.event
        async def on_donation(message: DonationMessage):
            profile = message.profile
            extras = message.extras
            nickname = profile.nickname if profile is not None else const.UNDEFINED
            pay_amount = extras.pay_amount if extras is not None else 0
            await self.send_chat(const.Message.DONATION_THANKS.format(nickname, pay_amount))
            # todo: donation alert

    async def handle_song_request(self, message: ChatMessage):
        try:
            parts = message.content.split(" ", 1)
            if len(parts) < 2:
                await self.send_chat(const.Message.INVALID_COMMAND.format(youtubeConst.Message.COMMAND_FORMAT))
                return
            
            song_info = parts[1].split("-", 1)
            if len(song_info) < 2:
                await self.send_chat(const.Message.INVALID_COMMAND.format(youtubeConst.Message.COMMAND_FORMAT))
                return

            artist = song_info[0].strip()
            title = song_info[1].strip()
            
            status, video_id, video_title = self.youtube_player.search_youtube(artist, title)

            

            if await self.handle_status(status, video_title):
                return

            self.youtube_player.update_html(video_id, video_title)
            self.youtube_player.refresh_browser_source(youtubeConst.SOURCE_NAME) 

            await self.send_chat(youtubeConst.Message.REQUEST_SUCCESS.format(video_title))
        except Exception as e:
            await self.send_chat(youtubeConst.Message.REQUEST_ERROR.format(e))
            print(f"Error in handle_song_request: {e}")
        
    async def handle_status(self, status, video_title) -> bool:
        if status == youtubeConst.Status.BANNED_CHANNEL:
            await self.send_chat(youtubeConst.Message.REQUEST_BANNED_CHANNEL.format(video_title))
            return True
        elif status == youtubeConst.Status.BANNED_KEYWORD:
            await self.send_chat(youtubeConst.Message.REQUEST_BANNED_KEYWORD.format(video_title))
            return True
        elif status == youtubeConst.Status.ERROR:
            await self.send_chat(youtubeConst.Message.REQUEST_ERROR.format(video_title))
            return True
        elif status == youtubeConst.Status.NOT_FOUND:
            await self.send_chat(youtubeConst.Message.NOT_FOUND.format(video_title))
            return True
        return False

    @staticmethod
    def hash_to_color(hash_str):
        hex_color = hash_str[2:8]
        return int(hex_color, 16)
