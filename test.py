import tkinter as tk
from tkinter import ttk
import keyboard
import time
import playsound
import os
import threading

class KeyBot:
    def __init__(self, root):
        self.root = root
        self.repeat_f9 = False
        self.voice_enabled = True
        self.interval = 0.7  # 设置默认按键间隔时间

        self.voice_on_path = "./to/on_voice.mp3"
        self.voice_off_path = "./to/off_voice.mp3"

        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)

        self.voice_button = ttk.Button(root, text="语音提示开关", command=self.toggle_voice)
        self.voice_button.pack(pady=10)

        self.test_button = ttk.Button(root, text="测试开关", command=self.toggle_test)
        self.test_button.pack(pady=10)

        keyboard.on_press(self.toggle_repeat_f9)

    def toggle_repeat_f9(self, event):
        if event.name == "~":
            self.repeat_f9 = not self.repeat_f9
            if self.repeat_f9:
                self.update_status("开始重复按F9")
                if self.voice_enabled:
                    self.play_voice(self.voice_on_path)
                self.start_simulate_f9()
            else:
                self.update_status("停止重复按F9")
                if self.voice_enabled:
                    self.play_voice(self.voice_off_path)
                keyboard.unhook_all_hotkeys()

    def start_simulate_f9(self):
        self.simulate_f9_thread = threading.Thread(target=self.simulate_f9)
        self.simulate_f9_thread.start()

    def stop_simulate_f9(self):
        self.repeat_f9 = False

    def simulate_f9(self):
        while self.repeat_f9:
            keyboard.send("f9")
            time.sleep(self.interval)

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        self.update_status(f"语音提示已 {'开启' if self.voice_enabled else '关闭'}")

    def play_voice(self, path):
        if os.path.exists(path) and self.voice_enabled:
            try:
                playsound.playsound(path)
            except Exception as e:
                self.update_status(f"播放语音失败: {e}")

    def update_status(self, message):
        self.status_label.config(text=message)

    def toggle_test(self):
        if self.simulate_f9_thread is None or not self.simulate_f9_thread.is_alive():
            self.start_simulate_f9()
        else:
            self.stop_simulate_f9()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("按键精灵")

    key_bot = KeyBot(root)

    root.mainloop()