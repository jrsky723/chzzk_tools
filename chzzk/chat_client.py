from chzzkpy.chat import ChatClient as BaseChatClient, ChatMessage, DonationMessage
from obs.nico_chat import NicoChat
from youtube_player.player import YoutubePlayer
import constants.common_const as const
import constants.youtube_player_const as youtubeConst
from utils import parse_time, is_valid_url
import re


class ChatClient(BaseChatClient):
    def __init__(
        self, channel_id, nico_chat: NicoChat, youtube_player: YoutubePlayer, tk_vars
    ):
        super().__init__(channel_id)
        self.nico_chat = nico_chat
        self.youtube_player = youtube_player
        self.tk_vars = tk_vars
        self.setup_event_handlers()

    def setup_event_handlers(self):
        @self.event
        async def on_chat(message: ChatMessage):
            content = message.content
            profile = message.profile
            nickname = profile.nickname if profile is not None else const.UNDEFINED
            if content.startswith(const.Prefix.COMMAND_PREFIX):

                # 유튜브 기능 on
                if self.tk_vars[const.FunctionName.YOUTUBE].get():
                    # 유튜브 신청곡 기능
                    if content.startswith(const.CommandPrefix.YOUTUBE):
                        await self.handle_video_request(message)

                    # 스킵
                    if content == const.CommandPrefix.SKIP:
                        await self.handle_skip(nickname, is_skip=True)

                    # 유지
                    if content == const.CommandPrefix.KEEP:
                        await self.handle_skip(nickname, is_skip=False)

                # 인사말 기능
                elif (
                    content.startswith(const.CommandPrefix.HELLO)
                    and self.tk_vars[const.FunctionName.HELLO].get()
                ):
                    await self.handle_hello(message, nickname)

            elif content.startswith(const.Prefix.RESPONSE_PREFIX):
                return
            else:
                if self.tk_vars[const.FunctionName.NICO_CHAT].get():
                    # {} 안에 있는 내용은 무시 (이모티콘)
                    await self.handle_nico_chat(content)

        @self.event
        async def on_donation(message: DonationMessage):
            profile = message.profile
            extras = message.extras
            nickname = profile.nickname if profile is not None else const.UNDEFINED
            pay_amount = extras.pay_amount if extras is not None else 0
            await self.send_chat(
                const.Message.DONATION_THANKS.format(nickname, pay_amount)
            )
            # todo: donation alert

    async def handle_hello(self, message: ChatMessage, nickname: str):
        await self.send_chat(const.Message.HELLO.format(nickname))

    async def handle_nico_chat(self, content: str):
        # {}, 와 {} 안에 있는 내용은 무시 (이모티콘)
        cleaned_content = re.sub(r"\{.*?\}", "", content)
        if cleaned_content == "":
            return
        color = 0xFFFFFF  # white
        await self.nico_chat.splash_chat(cleaned_content, color)

    async def handle_video_request(self, message: ChatMessage):
        try:
            # 신청곡 제한을 위한 닉네임 확인
            nickname = (
                message.profile.nickname
                if message.profile is not None
                else const.UNDEFINED
            )

            #!유튜브 <동영상 링크> (시작시간) (종료시간)
            # \xa0 -> 공백으로 변환 (소보로빠아앙님의 경우 공백이 이상하게 들어가는 경우가 있음)
            parts = message.content.replace("\xa0", " ").split(" ", 2)

            if len(parts) < 2:
                await self.send_chat(
                    const.Message.INVALID_COMMAND.format(const.CommandFormat.YOUTUBE)
                )
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

            # 특정 아티스트의 곡을 받기 위한 키워드
            is_keyword = self.tk_vars[const.FunctionName.KEYWORD].get()
            keyword = self.tk_vars["keyword"].get() if is_keyword else None

            result: str = self.youtube_player.execute_video_request(
                video_url,
                start_time,
                end_time,
                nickname,
                keyword,
            )
            await self.send_chat(result)
        except ValueError as ve:
            await self.send_chat(youtubeConst.Message.INVALID_TIME_FORMAT.format(ve))
        except Exception as e:
            await self.send_chat(youtubeConst.Message.REQUEST_ERROR)
            print(f"Error in handle_video_request: {e}")

    async def handle_skip(self, nickname: str, is_skip: bool):
        # 유지(Keep) 이면서, 스킵 투표가 꺼져 있는 경우
        if not is_skip and not self.tk_vars[const.FunctionName.SKIP_VOTE].get():
            await self.send_chat(youtubeConst.Message.SKIP_VOTE_OFF)
            return

        result = self.youtube_player.handle_skip(
            nickname,
            is_skip,
            is_vote=self.tk_vars[const.FunctionName.SKIP_VOTE].get(),
        )
        await self.send_chat(result)
