import re

def parse_timetable_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    all_times = []
    current_hour = None
    current_minute = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if re.match(r'^\d+$', line) and i + 1 < len(lines) and lines[i + 1] == '時':
            current_hour = line.zfill(2)
            i += 2
            continue
        
        if re.match(r'^\d+$', line) and i + 1 < len(lines) and lines[i + 1] == '分':
            current_minute = line.zfill(2)
            i += 2
            
            if current_hour and current_minute:
                time = f"{current_hour}:{current_minute}"
                all_times.append(time)
            continue
        
        i += 1
    
    return sorted(set(all_times))

# パース実行
weekday_data = parse_timetable_file('data/平日時刻表.txt')
holiday_data = parse_timetable_file('data/休日時刻表.txt')

# JavaScript形式で出力（全時刻統合版）
print('// 平日・休日を自動判別して時刻表を表示するバージョン（全方向統合）')
print()
print('// 時刻表データ（平日・全方向統合）')
print('const TIMETABLE_WEEKDAY = [')
times_str = ', '.join([f'"{t}"' for t in weekday_data])
print(f'    {times_str}')
print('];')
print()

print('// 時刻表データ（休日・全方向統合）')
print('const TIMETABLE_HOLIDAY = [')
times_str = ', '.join([f'"{t}"' for t in holiday_data])
print(f'    {times_str}')
print('];')
