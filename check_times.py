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

weekday = parse_timetable_file('data/平日時刻表.txt')
holiday = parse_timetable_file('data/休日時刻表.txt')

print(f"平日: {len(weekday)}本")
print(f"休日: {len(holiday)}本")
print(f"\n平日: {', '.join(weekday[:15])}")
print(f"\n休日: {', '.join(holiday[:15])}")
