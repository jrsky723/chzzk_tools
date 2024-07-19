import os
import requests
from jinja2 import Environment, FileSystemLoader
import obsws_python as obs
from constants.youtube_player import BANNED_CHANNEL_TITLE, BANNED_KEYWORDS
from constants.youtube_player import Status, Source, Message
from obs.obs_utils import get_current_scene_name, scene_item_exists
import threading
from datetime import timedelta, datetime
from urllib.parse import urlparse, parse_qs

class YoutubePlayer:
    def __init__(self, obs_client: obs.ReqClient, api_key: str):
        self.obs_client = obs_client
        self.api_key = api_key
        self.video_list = []
        self.current_video_index = -1
        self.current_video_start_time = None
        self.current_video_duration = None
        self.is_running = True
        self.playback_thread = None
        self.is_browser_source_created = False
        self.clear_html()
        self.setup_browser_source()
        

    def execute_video_request(self, video_url: str) -> str:
        video_id = self.extract_video_id(video_url)
        if not video_id:
            return Message.INVALID_URL
        
        status, video_title, channel_title, duration_str = self.get_video_info(video_id)
        if status == Status.ERROR:
                return Message.SEARCH_ERROR
        if status == Status.NOT_FOUND:
                return Message.NOT_FOUND.format()
            
        if channel_title in BANNED_CHANNEL_TITLE:
            return Message.REQUEST_BANNED_CHANNEL.format(channel_title)
        
        if any(keyword in video_title for keyword in BANNED_KEYWORDS):
            return Message.REQUEST_BANNED_KEYWORD.format(video_title)
        
        duration = self.parse_duration(duration_str)

        self.add_video_to_list(video_id, video_title, channel_title, duration)
     
        return Message.REQUEST_SUCCESS.format(
            f"{video_title} - {channel_title} ({duration})"
        )

    def extract_video_id(self, url: str) -> str | None:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query).get('v', [None])[0]
            if parsed_url.path.startswith('/embed/'):
                return parsed_url.path.split('/')[2]
            if parsed_url.path.startswith('/v/'):
                return parsed_url.path.split('/')[2]
            if parsed_url.path.startswith('/shorts/'):
                return parsed_url.path.split('/')[2]
        elif parsed_url.hostname in ['youtu.be']:
            return parsed_url.path[1:]
        return None

    def get_video_info(self, video_id: str):
        url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                video_title = data['items'][0]['snippet']['title']
                channel_title = data['items'][0]['snippet']['channelTitle']
                duration_str = data['items'][0]['contentDetails']['duration']
                return Status.SUCCESS, video_title, channel_title, duration_str 
            return Status.NOT_FOUND, "", "", ""
        return Status.ERROR, "", "", ""

    def parse_duration(self, duration_str):
        duration_str = duration_str.replace('PT', '')
        hours = 0
        minutes = 0
        seconds = 0
        if 'H' in duration_str:
            hours, duration_str = duration_str.split('H')
        if 'M' in duration_str:
            minutes, duration_str = duration_str.split('M')
        if 'S' in duration_str:
            seconds = duration_str.split('S')[0]
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    def add_video_to_list(self, video_id: str, title: str, channel: str, duration: timedelta):
        self.video_list.append({
            "video_id": video_id,
            "title": title,
            "channel": channel,
            "duration": duration,
        })
        if self.current_video_index == -1:
            self.play_video(0)

    def play_video(self, index: int):
        if 0 <= index < len(self.video_list):
            self.current_video_index = index
            video = self.video_list[self.current_video_index]
            self.update_html(video["video_id"], video["title"], video["channel"])
            self.refresh_browser_source()
            self.current_video_start_time = datetime.now()
            self.current_video_duration = video["duration"]
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
            del self.video_list[index]
            if index <= self.current_video_index and self.current_video_index > 0:
                self.current_video_index -= 1

    def skip_video(self):
        if self.current_video_index < len(self.video_list) - 1:
            self.current_video_index += 1
            self.play_video(self.current_video_index)
        else:
           self.play_video(-1)

    def check_next_video(self):
        while self.is_running:
            if self.current_video_start_time and self.current_video_duration:
                elapsed_time = datetime.now() - self.current_video_start_time
                if elapsed_time >= self.current_video_duration:
                    self.current_video_index += 1
                    if self.current_video_index < len(self.video_list):
                        self.play_video(self.current_video_index)
                    else:
                        self.play_video(-1)
                    break
            threading.Event().wait(1)
        
    def get_remaining_time(self) -> str:
        if self.current_video_start_time and self.current_video_duration:
            elapsed_time = datetime.now() - self.current_video_start_time
            remaining_time = self.current_video_duration - elapsed_time
            if remaining_time.total_seconds() > 0:
                return str(remaining_time).split('.')[0]  # Return as H:MM:SS
        return "0:00:00"
    
    def update_html(self, video_id: str, title: str, channel: str):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, 'templates')
        file_loader = FileSystemLoader(templates_dir)
        env = Environment(loader=file_loader)
        
        template = env.get_template(Source.TEMPLATE)

        data = {
            'video_id': video_id,
            'title': title,
            'channel': channel,
        }
        
        output = template.render(data)
        output_path = os.path.join(current_dir, Source.OUTPUT)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(output)

    def clear_html(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(current_dir, Source.OUTPUT)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("")

    def setup_browser_source(self):
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
                    "is_local_file": True
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