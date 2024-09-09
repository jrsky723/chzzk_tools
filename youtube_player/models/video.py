from datetime import timedelta


class Video:
    def __init__(
        self,
        video_id: str,
        title: str,
        channel: str,
        start_time: timedelta,
        duration: timedelta,
        nickname: str,
        video_url: str,
    ):
        self.video_id = video_id
        self.title = title
        self.channel = channel
        self.start_time = start_time
        self.duration = duration
        self.nickname = nickname
        self.video_url = video_url
        self.played = False

    def __str__(self):
        return f"Video({self.video_id}, {self.title}, {self.channel}, {self.start_time}, {self.duration}, {self.nickname}, {self.video_url}, {self.played})"

    def __repr__(self):
        return self.__str__()
