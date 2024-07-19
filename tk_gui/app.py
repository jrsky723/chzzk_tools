import tkinter as tk
from tkinter import messagebox
import constants.tk_gui as gui_const
from obs.nico_chat import NicoChat
from youtube_player.player import YoutubePlayer
from chzzkpy.chat import ChatClient as BaseChatClient

class App:
    def __init__(self, root: tk.Tk, nico_chat: NicoChat, youtube_player: YoutubePlayer, chzzk_cl: BaseChatClient, variables: dict):
        self.root = root
        self.root.title("OBS and YouTube Control")
        self.root.geometry("600x500") 
        self.nico_chat: NicoChat = nico_chat
        self.youtube_player: YoutubePlayer = youtube_player
        self.chzzk_cl: BaseChatClient = chzzk_cl
        self.variables: dict = variables

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
        
        # NicoChat 기능 토글
        self.nico_chat_checkbox = tk.Checkbutton(self.root, text=gui_const.GuiCommand.NICO_CHAT_TOGGLE, variable=self.variables['nico_chat_var'])
        self.nico_chat_checkbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # 명령어 별 기능 토글
        row = 1
        for command, var in self.variables['command_vars'].items():
            cb = tk.Checkbutton(self.root, text=f"{command} ON/OFF", variable=var)
            cb.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            row += 1

        self.create_button = tk.Button(self.root, text=gui_const.GuiCommand.CREATE_BROWSER, command=self.create_browser_source)
        self.create_button.grid(row=row, column=0, padx=10, pady=10, sticky="ew")

        # OBS 브라우저 소스 새로고침 버튼
        self.refresh_button = tk.Button(self.root, text=gui_const.GuiCommand.REFRESH_BROWSER, command=self.refresh_browser_source)
        self.refresh_button.grid(row=row, column=1, padx=10, pady=10, sticky="ew")

        # OBS 브라우저 소스 삭제 버튼
        self.delete_browser_button = tk.Button(self.root, text=gui_const.GuiCommand.DELETE_BROWSER, command=self.delete_browser_source)
        self.delete_browser_button.grid(row=row, column=2, padx=10, pady=10, sticky="ew")

        # 현재 동영상 정보와 남은 시간 표시
        row += 1
        self.current_video_label = tk.Label(self.root, text="현재 재생 중인 동영상: 0/0")
        self.current_video_label.grid(row=row, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        row += 1
        self.current_video_info_label = tk.Label(self.root, text="제목: 없음, 채널: 없음")
        self.current_video_info_label.grid(row=row, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

        row += 1
        self.remaining_time_label = tk.Label(self.root, text="남은 시간: 0:00:00")
        self.remaining_time_label.grid(row=row, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # 동영상 리스트 업데이트 버튼
        row += 1
        self.update_video_list_button = tk.Button(self.root, text="동영상 리스트 업데이트", command=self.update_video_list)
        self.update_video_list_button.grid(row=row, column=1, columnspan=1, padx=10, pady=10, sticky="ew")

        # 동영상 리스트 표시
        row += 1
        listbox_frame = tk.Frame(self.root)
        listbox_frame.grid(row=row, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.video_listbox = tk.Listbox(listbox_frame, height=7)
        self.video_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.video_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.video_listbox.yview)
        
        # 동영상 스킵 버튼
        row += 1
        self.skip_video_button = tk.Button(self.root, text="동영상 스킵", command=self.skip_video)
        self.skip_video_button.grid(row=row, column=0, padx=10, pady=10, sticky="ew")

        # 동영상 재생 버튼
        self.play_video_button = tk.Button(self.root, text="동영상 재생", command=self.play_selected_video)
        self.play_video_button.grid(row=row, column=1, padx=10, pady=10, sticky="ew")

        # 동영상 제거 버튼
        self.remove_video_button = tk.Button(self.root, text="동영상 제거", command=self.remove_selected_video)
        self.remove_video_button.grid(row=row, column=2, 
        padx=10, pady=10, sticky="ew")

      

    def skip_video(self):
        try:
            self.youtube_player.skip_video()
            self.update_current_video_info()
            self.update_video_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to skip the current video: {e}")

    def refresh_browser_source(self):
        try:
            self.youtube_player.refresh_browser_source()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh browser source: {e}")

    def delete_browser_source(self):
        try:
            self.youtube_player.delete_browser_source()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete browser source: {e}")

    def create_browser_source(self):
        try:
            self.youtube_player.create_browser_source()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create browser source: {e}")

    def update_remaining_time(self):
        remaining_time = self.youtube_player.get_remaining_time()
        self.remaining_time_label.config(text=f"남은 시간: {remaining_time}")
        self.root.after(1000, self.update_remaining_time)  # 1초마다 갱신

    def update_video_list(self):
        scroll_position = self.video_listbox.yview()
        selected_index = self.video_listbox.curselection()
        self.video_listbox.delete(0, tk.END)
        for idx, video in enumerate(self.youtube_player.video_list):
            display_text = f"{video['channel']} - {video['title']}"
            self.video_listbox.insert(tk.END, display_text)
            if idx == self.youtube_player.current_video_index:
                self.video_listbox.itemconfig(idx, {'bg': 'lightblue'})
        self.video_listbox.yview_moveto(scroll_position[0])
        if selected_index:
            self.video_listbox.selection_set(selected_index)
        
        self.updat_current_video_index()
    
    def updat_current_video_index(self):
        self.current_video_label.config(text=f"현재 재생 중인 동영상: {self.youtube_player.current_video_index + 1}/{len(self.youtube_player.video_list)}")

    def update_current_video_info(self):
        if self.youtube_player.current_video_index != -1:
            current_video = self.youtube_player.video_list[self.youtube_player.current_video_index]
            self.current_video_info_label.config(text=f"제목: {current_video['title']}, 채널: {current_video['channel']}")
        else:
            self.current_video_info_label.config(text="제목: 없음, 채널: 없음")

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
        self.root.destroy()