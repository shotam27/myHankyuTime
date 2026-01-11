import re
import json

def parse_timetable_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    timetables = {}
    current_hour = None
    current_minute = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 時間パターン: 数字 + "時"
        if re.match(r'^\d+$', line) and i + 1 < len(lines) and lines[i + 1] == '時':
            current_hour = line.zfill(2)
            i += 2
            continue
        
        # 分パターン: 数字 + "分"
        if re.match(r'^\d+$', line) and i + 1 < len(lines) and lines[i + 1] == '分':
            current_minute = line.zfill(2)
            i += 2
            
            # 次の行から行き先を探す
            destination = None
            for j in range(i, min(i + 5, len(lines))):
                if lines[j] in ['大阪梅田', '天下茶屋', '北千里', '高槻市', '淡路', '河原町', '嵐山', '桂', '豊津']:
                    destination = lines[j]
                    break
            
            if current_hour and current_minute and destination:
                time = f"{current_hour}:{current_minute}"
                if destination not in timetables:
                    timetables[destination] = []
                timetables[destination].append(time)
            continue
        
        i += 1
    
    return timetables

# パース実行
weekday_data = parse_timetable_file('data/平日時刻表.txt')
holiday_data = parse_timetable_file('data/休日時刻表.txt')

# JavaScript形式で出力
print('// 平日時刻表データ')
print('const TIMETABLE_WEEKDAY = {')
for destination, times in weekday_data.items():
    times_str = ', '.join([f'"{t}"' for t in times])
    print(f'    "{destination}": [{times_str}],')
print('};')
print()

print('// 休日時刻表データ')
print('const TIMETABLE_HOLIDAY = {')
for destination, times in holiday_data.items():
    times_str = ', '.join([f'"{t}"' for t in times])
    print(f'    "{destination}": [{times_str}],')
print('};')
