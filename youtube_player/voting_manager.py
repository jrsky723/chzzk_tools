# voting_manager.py
import threading
import constants.youtube_player_const as YoutubeConst

class VotingManager:
    def __init__(self, youtube_player):
        self.youtube_player = youtube_player
        self.votes_skip = 0
        self.votes_keep = 0
        self.vote_lock = threading.Lock()
        self.skip_timer = None
        self.user_vote_cnt = {} # 유저별 투표 횟수

    def handle_vote(self, nickname, vote):
        with self.vote_lock:
            if vote == "skip":
                self.votes_skip += 1
            elif vote == "keep":
                self.votes_keep += 1
            self.check_votes()

    def check_votes(self):
        if self.votes_skip > self.votes_keep:
            if self.skip_timer is None:
                self.start_skip_timer()
        else:
            self.cancel_skip_timer()

    def start_skip_timer(self):
        self.skip_timer = threading.Timer(YoutubeConst.SKIP_WAIT_TIME, self.execute_skip)
        self.skip_timer.start()

    def cancel_skip_timer(self):
        if self.skip_timer is not None:
            self.skip_timer.cancel()
            self.skip_timer = None

    def execute_skip(self):
        with self.vote_lock:
            if self.votes_skip > self.votes_keep:
                self.youtube_player.skip_video()

    def reset_votes(self):
        self.votes_skip = 0
        self.votes_keep = 0
        self.skip_timer = None
