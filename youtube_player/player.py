import os
import requests
import threading
from datetime import timedelta, datetime

import obsws_python as obs
from jinja2 import Environment, FileSystemLoader
from urllib.parse import urlparse, parse_qs

from youtube_player.models.video import Video
from youtube_player.voting_manager import VotingManager
from constants.youtube_player_const import *
from obs.obs_utils import get_current_scene_name, scene_item_exists


class YoutubePlayer:
    def __init__(self, obs_client: obs.ReqClient, api_key: str):
        self.obs_client = obs_client
        self.api_key = api_key
        self.video_list: list[Video] = []
        self.current_video_index = -1
        self.current_video_start_time = None
        self.current_video_duration = None
        self.is_running = True
        self.playback_thread = None
        self.is_browser_source_created = False
        self.refresh_ui_callback = None
        self.user_request_cnt = {}  # 유저별 신청곡 제한을 위한 딕셔너리
        self.voting_manager = VotingManager(self)  # 스킵, 유지 투표 관리자
        self.clear_html()
        self.setup_browser_source()

    def set_refresh_ui_callback(self, callback):
        self.refresh_ui_callback = callback

    def execute_video_request(
        self,
        video_url: str,
        start_time: timedelta | None,
        end_time: timedelta | None,
        nickname: str,
        keyword: str | None,
    ) -> str:
        try:

            # 사용자 신청 횟수 확인
            if nickname in self.user_request_cnt:
                if self.user_request_cnt[nickname] >= MAX_REQUESTS:
                    return Message.REQUEST_LIMIT_REACHED.format(nickname, MAX_REQUESTS)
            else:
                self.user_request_cnt[nickname] = 0

            video_id = self.extract_video_id(video_url)

            if not video_id:
                return Message.INVALID_URL.format(video_url)

            status, video_title, channel_title, duration_str = self.get_video_info(
                video_id
            )
            if status == Status.ERROR:
                return Message.SEARCH_ERROR
            if status == Status.NOT_FOUND:
                return Message.NOT_FOUND.format(video_url)

            if channel_title in BANNED_CHANNEL_TITLE:
                return Message.REQUEST_BANNED_CHANNEL.format(video_url)

            if any(keyword in video_title for keyword in BANNED_KEYWORDS):
                return Message.REQUEST_BANNED_KEYWORD.format(video_title)

            # 키워드가 None이 아니면, 특정 키워드가 포함된 영상만 신청 가능
            if keyword is not None and keyword not in video_title:
                return Message.NO_KEYWORD.format(keyword)

            s_t = timedelta(0)
            duration = self.parse_duration(duration_str)
            min_time = timedelta(seconds=10)
            if start_time is not None:
                s_t = start_time
                if end_time is not None:
                    e_t = end_time
                    d_t = e_t - s_t
                    if d_t.total_seconds() < min_time.total_seconds():
                        return Message.INVALID_TIME.format(
                            "영상 길이가 너무 짧습니다. (최소 10초)"
                        )
                    if d_t.total_seconds() > duration.total_seconds():
                        return Message.INVALID_TIME.format(
                            "종료시간이 영상 길이보다 큽니다"
                        )
                    duration = d_t
                else:
                    if s_t.total_seconds() >= duration.total_seconds():
                        return Message.INVALID_TIME.format(
                            "시작시간이 영상 길이보다 큽니다."
                        )
                    duration = duration - s_t

            video = Video(
                video_id,
                video_title,
                channel_title,
                s_t,
                duration,
                nickname,
                video_url,
            )
            self.add_video_to_list(video)

            # video_title의 길이 제한
            if len(video_title) > MAX_TITLE_LENGTH:
                video_title = video_title[:MAX_TITLE_LENGTH] + "..."

            return Message.REQUEST_SUCCESS.format(
                f"{video_title} | {channel_title} ({duration})",
                self.user_request_cnt[nickname],
                MAX_REQUESTS,
            )
        except Exception as e:
            print(f"Error in execute_video_request: {e}")
            return Message.REQUEST_ERROR

    def extract_video_id(self, url: str) -> str | None:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query).get("v", [None])[0]
            if parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            if parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]
            if parsed_url.path.startswith("/shorts/"):
                return parsed_url.path.split("/")[2]
        elif parsed_url.hostname in ["youtu.be"]:
            return parsed_url.path[1:]
        return None

    def get_video_info(self, video_id: str):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "items" in data and len(data["items"]) > 0:
                video_title = data["items"][0]["snippet"]["title"]
                channel_title = data["items"][0]["snippet"]["channelTitle"]
                duration_str = data["items"][0]["contentDetails"]["duration"]
                return Status.SUCCESS, video_title, channel_title, duration_str
            return Status.NOT_FOUND, "", "", ""
        return Status.ERROR, "", "", ""

    def parse_duration(self, duration_str):
        duration_str = duration_str.replace("PT", "")
        hours = 0
        minutes = 0
        seconds = 0
        if "H" in duration_str:
            hours, duration_str = duration_str.split("H")
        if "M" in duration_str:
            minutes, duration_str = duration_str.split("M")
        if "S" in duration_str:
            seconds = duration_str.split("S")[0]
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    def add_video_to_list(
        self,
        video: Video,
    ):
        self.video_list.append(video)
        self.user_request_cnt[video.nickname] += 1
        if self.current_video_index == -1:
            self.play_video(len(self.video_list) - 1)
        if self.refresh_ui_callback:
            self.refresh_ui_callback()

    def play_video(self, index: int):
        if 0 <= index < len(self.video_list):
            self.handle_fisrt_play(index)
            self.voting_manager.reset_votes()
            self.current_video_index = index
            video = self.video_list[self.current_video_index]
            self.update_html(video)
            self.refresh_browser_source()
            self.current_video_start_time = datetime.now()
            self.current_video_duration = video.duration
            self.playback_thread = threading.Thread(target=self.check_next_video)
            self.playback_thread.start()
        else:
            self.current_video_index = -1
            self.current_video_start_time = None
            self.current_video_duration = None
            self.clear_html()
            self.refresh_browser_source()

    def remove_video_from_list(self, index: int):
        if 0 <= index < len(self.video_list):
            self.handle_fisrt_play(index)
            del self.video_list[index]
            if index <= self.current_video_index and self.current_video_index > 0:
                self.current_video_index -= 1

    def skip_video(self):
        if self.current_video_index < len(self.video_list) - 1:
            self.current_video_index += 1
            self.play_video(self.current_video_index)
        else:
            self.play_video(-1)

    def handle_fisrt_play(self, index: int):
        # 처음 재생된 영상인지 확인
        played = self.video_list[index].played
        if not played:
            # 처음 재생된 영상일 경우, 사용자 신청 횟수 감소
            self.video_list[index].played = True
            nickname = self.video_list[index].nickname
            self.user_request_cnt[nickname] -= 1

    def check_next_video(self):
        while self.is_running:
            if self.current_video_start_time and self.current_video_duration:
                elapsed_time = datetime.now() - self.current_video_start_time
                if elapsed_time >= self.current_video_duration:
                    # 재생 완료 처리
                    self.current_video_index += 1
                    if self.current_video_index < len(self.video_list):
                        self.play_video(self.current_video_index)
                    else:
                        self.play_video(-1)
                    if self.refresh_ui_callback:
                        self.refresh_ui_callback()
                    break
            threading.Event().wait(1)

    def get_remaining_time(self) -> str:
        if self.current_video_start_time and self.current_video_duration:
            elapsed_time = datetime.now() - self.current_video_start_time
            remaining_time = self.current_video_duration - elapsed_time
            if remaining_time.total_seconds() > 0:
                return str(remaining_time).split(".")[0]  # Return as H:MM:SS
        return "0:00:00"

    def update_html(self, video: Video):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, "templates")
        file_loader = FileSystemLoader(templates_dir)
        env = Environment(loader=file_loader)

        template = env.get_template(Source.TEMPLATE)

        data = {
            "video_id": video.video_id,
            "title": video.title,
            "channel": video.channel,
            "start_time": video.start_time.total_seconds(),
            "nickname": video.nickname,
        }

        output = template.render(data)
        output_path = os.path.join(current_dir, Source.OUTPUT)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(output)

    def clear_html(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, Source.OUTPUT)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write("")

    def setup_browser_source(self):
        self.is_browser_source_created = scene_item_exists(
            self.obs_client, get_current_scene_name(self.obs_client), Source.NAME
        )
        self.create_browser_source()
        self.refresh_browser_source()

    def create_browser_source(self):
        if self.is_browser_source_created:
            return
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, Source.OUTPUT)
        try:
            self.obs_client.create_input(
                sceneName=get_current_scene_name(self.obs_client),
                inputName=Source.NAME,
                inputKind="browser_source",
                inputSettings={
                    "local_file": file_path,
                    "width": Source.WIDTH,
                    "height": Source.HEIGHT,
                    "is_local_file": True,
                },
                sceneItemEnabled=True,
            )
            self.is_browser_source_created = True
        except Exception as e:
            raise e

    def refresh_browser_source(self):
        if not self.is_browser_source_created:
            return
        try:
            self.obs_client.press_input_properties_button(Source.NAME, "refreshnocache")
        except Exception as e:
            raise e

    def delete_browser_source(self):
        if not self.is_browser_source_created:
            return
        try:
            self.obs_client.remove_input(Source.NAME)
            self.is_browser_source_created = False
        except Exception as e:
            raise e

    def stop(self):
        self.is_running = False
        self.clear_html()
        scene_name = get_current_scene_name(self.obs_client)
        if scene_item_exists(self.obs_client, scene_name, Source.NAME):
            self.delete_browser_source()
        if self.playback_thread:
            self.playback_thread.join()

    def handle_skip(self, nickname: str, is_skip: bool, is_vote: bool) -> str:
        # 스킵, 유지 투표 및 시청자 자기 자신의 음악 바로 스킵 처리

        # 현재 재생 중인 영상이 없을 경우
        if self.current_video_index == -1:
            return Message.NO_VIDEO_PLAYING

        # 스킵 투표 기능이 켜져 있을 경우
        if is_vote:
            self.voting_manager.handle_vote(nickname, "skip" if is_skip else "keep")
            current_skip = self.voting_manager.votes_skip
            current_keep = self.voting_manager.votes_keep
            if is_skip:
                # 스킵 투표로 인해 스킵 횟수가 유지 횟수보다 1 더 클 경우
                if current_skip == current_keep + 1:
                    return Message.SKIP_COUNT_START.format(
                        nickname,
                        current_skip,
                        current_keep,
                    )
            else:
                # 유지 투표로 인해 스킵 횟수와 유지 횟수가 같을 경우
                if current_keep == current_skip:
                    return Message.KEEP_VIDEO.format(
                        nickname,
                        current_skip,
                        current_keep,
                    )

            return Message.VOTE_SUCCESS.format(
                nickname,
                current_skip,
                current_keep,
            )

        else:  # 스킵 투표 기능이 아닐 경우
            current_video = self.video_list[self.current_video_index]

            # 시청자 자신의 음악일 경우 바로 스킵
            if current_video.nickname == nickname:
                self.skip_video()
                return Message.SKIP_OWN_VIDEO.format(nickname)
            else:
                return Message.IS_NOT_OWN_VIDEO.format(current_video.nickname)
