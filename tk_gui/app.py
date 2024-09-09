import tkinter as tk
from tkinter import messagebox
import constants.tk_gui_const as gui_const
from obs.nico_chat import NicoChat
from youtube_player.player import YoutubePlayer
from chzzkpy.chat import ChatClient as BaseChatClient
import webbrowser


class App:
    def __init__(
        self,
        root: tk.Tk,
        nico_chat: NicoChat,
        youtube_player: YoutubePlayer,
        chzzk_cl: BaseChatClient,
        tk_vars: dict,
    ):
        self.root = root
        self.root.title("OBS and YouTube Control")
        self.root.geometry("600x550")
        self.nico_chat: NicoChat = nico_chat
        self.youtube_player: YoutubePlayer = youtube_player
        self.chzzk_cl: BaseChatClient = chzzk_cl
        self.tk_vars: dict = tk_vars

        # 윈도우 닫기 이벤트 핸들러 설정
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # GUI 요소 생성
        self.create_widgets()
        self.update_remaining_time()
        self.update_video_list()

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        row = 0

        # 명령어 별 기능 토글
        # 니코동 채팅, 유튜브, 인사말, 스킵 투표
        for name, var in self.tk_vars.items():
            self.create_checkbutton(row, 1, 1, f"{name} ON/OFF", var)
            row += 1

        # 브라우저 소스 관련 버튼들
        self.create_action_button(
            row, 0, gui_const.GuiLabel.CREATE_BROWSER, self.create_browser_source
        )
        self.create_action_button(
            row, 1, gui_const.GuiLabel.REFRESH_BROWSER, self.refresh_browser_source
        )
        self.create_action_button(
            row, 2, gui_const.GuiLabel.DELETE_BROWSER, self.delete_browser_source
        )

        # 현재 동영상 정보와 남은 시간 표시
        row += 1
        self.current_video_label = self.create_label(
            row, 0, 3, gui_const.GuiLabel.CURRENT_VIDEO_INFO.format(0, 0)
        )
        row += 1
        self.current_video_info_label = self.create_label(
            row, 0, 3, gui_const.GuiLabel.VIDEO_INFO_NONE
        )
        row += 1
        self.remaining_time_label = self.create_label(
            row, 0, 3, gui_const.GuiLabel.REMAINING_TIME.format("0:00:00")
        )

        # 동영상 리스트 업데이트 버튼
        row += 1
        self.create_action_button(
            row, 1, gui_const.GuiLabel.UPDATE_VIDEO_LIST, self.update_video_list
        )

        # 동영상 리스트 표시
        row += 1
        self.create_video_listbox(row)

        # 동영상 관련 버튼들
        row += 1
        self.create_action_button(
            row, 0, gui_const.GuiLabel.SKIP_VIDEO, self.skip_video
        )
        self.create_action_button(
            row, 1, gui_const.GuiLabel.PLAY_VIDEO, self.play_selected_video
        )
        self.create_action_button(
            row, 2, gui_const.GuiLabel.DELETE_VIDEO, self.remove_selected_video
        )

    def create_action_button(self, row, column, text, command):
        button = tk.Button(self.root, text=text, command=command)
        button.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
        return button

    def create_checkbutton(self, row, column, colspan, text, variable):
        checkbutton = tk.Checkbutton(self.root, text=text, variable=variable)
        checkbutton.grid(
            row=row, column=column, columnspan=colspan, padx=10, pady=10, sticky="ew"
        )
        return checkbutton

    def create_label(self, row, column, colspan, text):
        label = tk.Label(self.root, text=text)
        label.grid(
            row=row, column=column, columnspan=colspan, padx=10, pady=5, sticky="ew"
        )
        return label

    def create_video_listbox(self, row):
        listbox_frame = tk.Frame(self.root)
        listbox_frame.grid(
            row=row, column=0, columnspan=3, padx=10, pady=10, sticky="ew"
        )

        self.video_listbox = tk.Listbox(listbox_frame, height=7)
        self.video_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.video_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.video_listbox.yview)

        # 더블클릭 이벤트 바인딩
        self.video_listbox.bind("<Double-Button-1>", self.open_video_url)

    def handle_action(self, action, success_message, error_message):
        try:
            action()
            self.update_current_video_info()
            self.update_video_list()
        except Exception as e:
            messagebox.showerror("Error", error_message.format(e))

    def skip_video(self):
        self.handle_action(
            self.youtube_player.skip_video, None, gui_const.GuiLabel.ERROR_SKIP_VIDEO
        )

    def refresh_browser_source(self):
        self.handle_action(
            self.youtube_player.refresh_browser_source,
            None,
            gui_const.GuiLabel.ERROR_REFRESH_BROWSER,
        )

    def delete_browser_source(self):
        self.handle_action(
            self.youtube_player.delete_browser_source,
            None,
            gui_const.GuiLabel.ERROR_DELETE_BROWSER,
        )

    def create_browser_source(self):
        self.handle_action(
            self.youtube_player.create_browser_source,
            None,
            gui_const.GuiLabel.ERROR_CREATE_BROWSER,
        )

    def update_remaining_time(self):
        remaining_time = self.youtube_player.get_remaining_time()
        self.remaining_time_label.config(
            text=gui_const.GuiLabel.REMAINING_TIME.format(remaining_time)
        )
        self.root.after(1000, self.update_remaining_time)  # 1초마다 갱신

    def update_video_list(self):
        scroll_position = self.video_listbox.yview()
        selected_index = self.video_listbox.curselection()

        # 리스트 초기화
        self.video_listbox.delete(0, tk.END)

        # 리스트 업데이트 (제목 | 채널 | 신청자) 하나씩 추가
        for idx, video in enumerate(self.youtube_player.video_list):
            display_text = f"{video.title} | {video.channel} | {video.nickname}"
            self.video_listbox.insert(tk.END, display_text)
            if idx == self.youtube_player.current_video_index:
                self.video_listbox.itemconfig(idx, {"bg": "lightblue"})

        self.video_listbox.yview_moveto(scroll_position[0])
        if selected_index:
            self.video_listbox.selection_set(selected_index)

        self.update_current_video_index()

    def update_current_video_index(self):
        self.current_video_label.config(
            text=gui_const.GuiLabel.CURRENT_VIDEO_INFO.format(
                self.youtube_player.current_video_index + 1,
                len(self.youtube_player.video_list),
            )
        )

    def update_current_video_info(self):
        if self.youtube_player.current_video_index != -1:
            current_video = self.youtube_player.video_list[
                self.youtube_player.current_video_index
            ]
            self.current_video_info_label.config(
                text=f"제목: {current_video.title}, 채널: {current_video.channel}"
            )
        else:
            self.current_video_info_label.config(
                text=gui_const.GuiLabel.VIDEO_INFO_NONE
            )

    def remove_selected_video(self):
        selected_index = self.video_listbox.curselection()
        if selected_index:
            self.youtube_player.remove_video_from_list(selected_index[0])
            self.update_video_list()

    def play_selected_video(self):
        selected_index = self.video_listbox.curselection()
        if selected_index:
            self.youtube_player.play_video(selected_index[0])
            self.update_current_video_info()
            self.update_video_list()

    def on_closing(self):
        self.youtube_player.stop()
        self.nico_chat.remove_existing_mytext_sources()
        self.root.destroy()

    def open_video_url(self, event):
        selected_index = self.video_listbox.curselection()
        if selected_index:
            video_url = self.youtube_player.video_list[selected_index[0]].video_url
            if video_url:
                webbrowser.open(video_url)
