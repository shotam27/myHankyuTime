#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阪急総持寺駅 時刻表表示アプリ（Raspberry Pi用）
ブラウザ不要の軽量版
"""

import tkinter as tk
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 時刻表データ（平日・大阪梅田方面）
TIMETABLE_WEEKDAY = [
    "05:16", "05:35", "05:54", "06:12", "06:18", "06:22", "06:33", "06:43", "06:47", "06:57",
    "07:06", "07:17", "07:28", "07:45", "07:48", "08:03", "08:21", "08:32", "08:49",
    "09:09", "09:29", "09:50", "10:11", "10:31", "10:51", "11:11", "11:31", "11:51",
    "12:11", "12:31", "12:51", "13:11", "13:31", "13:51", "14:11", "14:31", "14:51",
    "15:11", "15:31", "15:50", "16:10", "16:30", "16:50",
    "17:13", "17:24", "17:33", "17:43", "17:53",
    "18:04", "18:14", "18:24", "18:34", "18:44", "18:54",
    "19:04", "19:15", "19:23", "19:33", "19:44", "19:54",
    "20:04", "20:08", "20:14", "20:24", "20:34", "20:45", "20:55",
    "21:04", "21:08", "21:19", "21:30", "21:43", "21:55",
    "22:08", "22:21", "22:31", "22:46",
    "23:00", "23:14", "23:29", "23:44"
]

# 時刻表データ（休日・大阪梅田方面）
TIMETABLE_HOLIDAY = [
    "05:16", "05:35", "05:53", "06:12", "06:22", "06:33", "06:40", "06:48",
    "07:03", "07:13", "07:23", "07:39",
    "08:11", "08:43",
    "09:07", "09:28", "09:48",
    "10:08", "10:28", "10:48",
    "11:08", "11:28", "11:48",
    "12:08", "12:28", "12:48",
    "13:08", "13:28", "13:48",
    "14:08", "14:28", "14:48",
    "15:08", "15:28", "15:48",
    "16:08", "16:28", "16:48",
    "17:09", "17:29", "17:50",
    "18:10", "18:30", "18:51",
    "19:12", "19:32", "19:52",
    "20:12", "20:32", "20:52",
    "21:03", "21:13", "21:23", "21:39", "21:44", "21:56",
    "22:13", "22:30", "22:46",
    "23:00", "23:14", "23:29", "23:44"
]

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("阪急総持寺駅 時刻表")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # ゴミの日表示（右上）
        self.garbage_label = tk.Label(
            root,
            text="",
            font=('Arial', 20, 'bold'),
            bg='green',
            fg='white',
            padx=20,
            pady=10
        )
        self.garbage_label.place(x=10, y=10)
        
        # アトランタ時間表示（左上）
        self.atlanta_frame = tk.Frame(root, bg='navy')
        self.atlanta_frame.place(x=10, y=80)
        
        tk.Label(
            self.atlanta_frame,
            text="🇺🇸 アトランタ",
            font=('Arial', 14),
            bg='navy',
            fg='gray',
            padx=10,
            pady=5
        ).pack()
        
        self.atlanta_time_label = tk.Label(
            self.atlanta_frame,
            text="--:--:--",
            font=('Arial', 20, 'bold'),
            bg='navy',
            fg='cyan',
            padx=10,
            pady=5
        )
        self.atlanta_time_label.pack()
        
        # タイトル
        self.title_label = tk.Label(
            root,
            text="阪急総持寺駅 → 大阪梅田",
            font=('Arial', 40, 'bold'),
            bg='black',
            fg='white'
        )
        self.title_label.pack(pady=20)
        
        # 現在時刻
        self.time_label = tk.Label(
            root,
            text="",
            font=('Arial', 30),
            bg='black',
            fg='cyan'
        )
        self.time_label.pack(pady=10)
        
        # ダイヤ種別
        self.day_type_label = tk.Label(
            root,
            text="",
            font=('Arial', 25),
            bg='black',
            fg='yellow'
        )
        self.day_type_label.pack(pady=10)
        
        # 次の電車
        self.train_label = tk.Label(
            root,
            text="",
            font=('Arial', 120, 'bold'),
            bg='black',
            fg='lime'
        )
        self.train_label.pack(pady=30)
        
        # あと何分
        self.until_label = tk.Label(
            root,
            text="",
            font=('Arial', 60, 'bold'),
            bg='black',
            fg='white'
        )
        self.until_label.pack(pady=20)
        
        # 最終更新時刻
        self.update_label = tk.Label(
            root,
            text="",
            font=('Arial', 15),
            bg='black',
            fg='gray'
        )
        self.update_label.pack(side='bottom', pady=10)
        
        # 更新開始
        self.update_display()
        self.update_current_time()
        
    def is_holiday(self):
        """休日判定"""
        day = datetime.now().weekday()
        return day >= 5  # 5=土曜, 6=日曜
    
    def get_week_of_month(self, date):
        """その曜日が月の中で第何回目かを計算"""
        return (date.day - 1) // 7 + 1
    
    def get_tomorrow_garbage(self):
        """明日のゴミの日を取得"""
        tomorrow = datetime.now() + timedelta(days=1)
        day = tomorrow.weekday()  # 0=月, 1=火, ..., 6=日
        week = self.get_week_of_month(tomorrow)
        
        garbage = []
        
        # 毎週のゴミ
        if day == 2:  # 水曜日
            garbage.append('普通ごみ')
        elif day == 5:  # 土曜日
            garbage.append('普通ごみ')
        
        # 第n週のゴミ
        if day == 4 and (week == 1 or week == 3):  # 第1・3金曜日
            garbage.append('ペットボトル')
        if day == 0 and week == 3:  # 第3月曜日
            garbage.append('古紙・古布')
        if day == 1 and week == 1:  # 第1火曜日
            garbage.append('小型粗大ごみ')
        if day == 1 and week == 3:  # 第3火曜日
            garbage.append('大型粗大ごみ')
        
        return '・'.join(garbage) if garbage else None
        
    def find_next_train(self):
        """次の電車を探す"""
        now = datetime.now()
        target = now + timedelta(minutes=4)
        target_minutes = target.hour * 60 + target.minute
        
        timetable = TIMETABLE_HOLIDAY if self.is_holiday() else TIMETABLE_WEEKDAY
        
        for time_str in timetable:
            h, m = map(int, time_str.split(':'))
            train_minutes = h * 60 + m
            if train_minutes >= target_minutes:
                return time_str
                
        # 翌日の始発
        return timetable[0]
        
    def get_time_until(self, train_time):
        """次の電車までの時間（分）"""
        now = datetime.now()
        h, m = map(int, train_time.split(':'))
        train_dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
        
        if train_dt < now:
            train_dt += timedelta(days=1)
            
        diff = (train_dt - now).total_seconds() / 60
        return int(diff)
        
    def update_display(self):
        """画面更新"""
        try:
            next_train = self.find_next_train()
            minutes_until = self.get_time_until(next_train)
            
            # 電車時刻
            self.train_label.config(text=f"普通 {next_train}")
            
            # あと何分
            self.until_label.config(text=f"あと {minutes_until} 分")
            
            # 色を変更（緊急度）
            if minutes_until <= 5:
                color = 'red'
            elif minutes_until <= 10:
                color = 'yellow'
            else:
                color = 'lime'
            self.train_label.config(fg=color)
            
            # ダイヤ種別
            day_type = "休日ダイヤ" if self.is_holiday() else "平日ダイヤ"
            self.day_type_label.config(text=day_type)
            
            # ゴミの日表示
            garbage = self.get_tomorrow_garbage()
            if garbage:
                self.garbage_label.config(
                    text=f"🗑️ 明日は {garbage} の日",
                    bg='orange'
                )
            else:
                self.garbage_label.config(text="", bg='black')
            
            # 最終更新
            now = datetime.now()
            self.update_label.config(
                text=f"最終更新: {now.strftime('%H:%M:%S')}"
            )
            
        except Exception as e:
            self.train_label.config(text=f"エラー: {e}", fg='red')
            
        # 30秒ごとに更新
        self.root.after(30000, self.update_display)
        
    def update_current_time(self):
        """現在時刻を更新"""
        now = datetime.now()
        self.time_label.config(text=f"現在時刻: {now.strftime('%H:%M:%S')}")
        
        # アトランタ時間を更新
        try:
            atlanta_now = datetime.now(ZoneInfo('America/New_York'))
            self.atlanta_time_label.config(text=atlanta_now.strftime('%H:%M:%S'))
        except:
            # Python 3.8以前の場合はpytzを使用
            from datetime import timezone
            atlanta_offset = timedelta(hours=-5)  # EST
            atlanta_now = datetime.now(timezone(atlanta_offset))
            self.atlanta_time_label.config(text=atlanta_now.strftime('%H:%M:%S'))
        
        # 1秒ごとに更新
        self.root.after(1000, self.update_current_time)

if __name__ == '__main__':
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
