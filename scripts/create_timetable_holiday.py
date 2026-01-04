#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
時刻表データ（休日）を手動で整形してCSV/JSON形式に変換
"""

import json
import csv

# 時刻表データ（大阪梅田方面のみ・休日）
timetable_data = [
    ("05:16", "普通", "大阪梅田"),
    ("05:35", "普通", "大阪梅田"),
    ("05:53", "普通", "大阪梅田"),
    ("06:12", "普通", "大阪梅田"),
    ("06:22", "普通", "大阪梅田"),
    ("06:33", "普通", "大阪梅田"),
    ("06:40", "普通", "大阪梅田"),
    ("06:48", "普通", "大阪梅田"),
    ("07:03", "普通", "大阪梅田"),
    ("07:13", "普通", "大阪梅田"),
    ("07:23", "普通", "大阪梅田"),
    ("07:39", "普通", "大阪梅田"),
    ("08:11", "普通", "大阪梅田"),
    ("08:43", "普通", "大阪梅田"),
    ("09:07", "普通", "大阪梅田"),
    ("09:28", "普通", "大阪梅田"),
    ("09:48", "普通", "大阪梅田"),
    ("10:08", "普通", "大阪梅田"),
    ("10:28", "普通", "大阪梅田"),
    ("10:48", "普通", "大阪梅田"),
    ("11:08", "普通", "大阪梅田"),
    ("11:28", "普通", "大阪梅田"),
    ("11:48", "普通", "大阪梅田"),
    ("12:08", "普通", "大阪梅田"),
    ("12:28", "普通", "大阪梅田"),
    ("12:48", "普通", "大阪梅田"),
    ("13:08", "普通", "大阪梅田"),
    ("13:28", "普通", "大阪梅田"),
    ("13:48", "普通", "大阪梅田"),
    ("14:08", "普通", "大阪梅田"),
    ("14:28", "普通", "大阪梅田"),
    ("14:48", "普通", "大阪梅田"),
    ("15:08", "普通", "大阪梅田"),
    ("15:28", "普通", "大阪梅田"),
    ("15:48", "普通", "大阪梅田"),
    ("16:08", "普通", "大阪梅田"),
    ("16:28", "普通", "大阪梅田"),
    ("16:48", "普通", "大阪梅田"),
    ("17:09", "普通", "大阪梅田"),
    ("17:29", "普通", "大阪梅田"),
    ("17:50", "普通", "大阪梅田"),
    ("18:10", "普通", "大阪梅田"),
    ("18:30", "普通", "大阪梅田"),
    ("18:51", "普通", "大阪梅田"),
    ("19:12", "普通", "大阪梅田"),
    ("19:32", "普通", "大阪梅田"),
    ("19:52", "普通", "大阪梅田"),
    ("20:12", "普通", "大阪梅田"),
    ("20:32", "普通", "大阪梅田"),
    ("20:52", "普通", "大阪梅田"),
    ("21:03", "普通", "大阪梅田"),
    ("21:13", "普通", "大阪梅田"),
    ("21:23", "普通", "大阪梅田"),
    ("21:39", "普通", "大阪梅田"),
    ("21:44", "普通", "大阪梅田"),
    ("21:56", "普通", "大阪梅田"),
    ("22:13", "普通", "大阪梅田"),
    ("22:30", "普通", "大阪梅田"),
    ("22:46", "普通", "大阪梅田"),
    ("23:00", "普通", "大阪梅田"),
    ("23:14", "普通", "大阪梅田"),
    ("23:29", "普通", "大阪梅田"),
    ("23:44", "普通", "大阪梅田"),
]

def main():
    # JSONデータ作成
    trains = []
    for time_str, train_type, destination in timetable_data:
        hour, minute = time_str.split(':')
        trains.append({
            'time': time_str,
            'hour': hour,
            'minute': minute,
            'type': train_type,
            'destination': destination
        })
    
    json_output = {
        'station': '総持寺',
        'direction': '大阪梅田',
        'day_type': '休日',
        'total_trains': len(trains),
        'trains': trains
    }
    
    # JSON保存
    with open('timetable_holiday.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    
    print(f'✓ JSON保存完了: timetable_holiday.json ({len(trains)}本)')
    
    # CSV保存
    with open('timetable_holiday.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['時刻', '種別', '行き先'])
        for time_str, train_type, destination in timetable_data:
            writer.writerow([time_str, train_type, destination])
    
    print(f'✓ CSV保存完了: timetable_holiday.csv ({len(timetable_data)}本)')
    
    # サンプル表示
    print('\n【最初の5本】')
    for time_str, train_type, destination in timetable_data[:5]:
        print(f"  {time_str} [{train_type}] {destination}")
    
    print('\n【最後の5本】')
    for time_str, train_type, destination in timetable_data[-5:]:
        print(f"  {time_str} [{train_type}] {destination}")
    
    print(f'\n合計: {len(timetable_data)}本の電車（大阪梅田方面・休日）')

if __name__ == '__main__':
    main()
