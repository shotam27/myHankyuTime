#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
時刻表テキストファイルをJSON形式に変換するスクリプト
"""

import json
import re

def parse_timetable(filename):
    """時刻表テキストファイルを解析してJSON形式に変換"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]  # 空行を除外
    
    timetable = []
    current_hour = None
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # デバッグ用
        if i < 20:  # 最初の20行だけ表示
            print(f"Line {i}: '{line}'")
        
        # 時間の行を検出
        if line.isdigit() and i + 1 < len(lines) and lines[i + 1] == '時':
            current_hour = line.zfill(2)
            i += 2
            continue
        
        # 分の行を検出
        if i + 1 < len(lines) and lines[i + 1] == '分':
            minute = line.zfill(2)
            i += 2
            
            # 種別を取得（次の行が［...］形式）
            train_type = '普通'
            if i < len(lines) and lines[i].startswith('［') and lines[i].endswith('］'):
                train_type = lines[i].strip('［］')
                i += 1
            
            # 行き先を取得
            destination = ''
            if i < len(lines) and lines[i] and lines[i] != 'ポップアップウィンドウで開く':
                destination = lines[i]
                i += 1
            
            # 「ポップアップウィンドウで開く」をスキップ
            while i < len(lines) and lines[i] == 'ポップアップウィンドウで開く':
                i += 1
            
            # データを追加
            if current_hour is not None:
                timetable.append({
                    'time': f'{current_hour}:{minute}',
                    'hour': current_hour,
                    'minute': minute,
                    'type': train_type,
                    'destination': destination
                })
            continue
        
        i += 1
    
    return timetable

def main():
    # 時刻表ファイルを解析
    timetable = parse_timetable('時刻.txt')
    
    # 大阪梅田方面のみをフィルタリング
    umeda_trains = [
        train for train in timetable 
        if '大阪梅田' in train['destination']
    ]
    
    # 結果をJSONファイルに保存
    output = {
        'station': '総持寺',
        'direction': '大阪梅田',
        'day_type': '平日',
        'trains': umeda_trains
    }
    
    with open('timetable_weekday.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f'✓ 時刻表を解析しました: {len(umeda_trains)}本の電車（大阪梅田方面）')
    print(f'✓ timetable_weekday.json に保存しました')
    
    # 全データも保存（参考用）
    output_all = {
        'station': '総持寺',
        'day_type': '平日',
        'trains': timetable
    }
    
    with open('timetable_weekday_all.json', 'w', encoding='utf-8') as f:
        json.dump(output_all, f, ensure_ascii=False, indent=2)
    
    print(f'✓ 全データ（{len(timetable)}本）も timetable_weekday_all.json に保存しました')
    
    # サンプル表示
    print('\n【最初の5本】')
    for train in umeda_trains[:5]:
        print(f"  {train['time']} [{train['type']}] {train['destination']}")
    
    print('\n【最後の5本】')
    for train in umeda_trains[-5:]:
        print(f"  {train['time']} [{train['type']}] {train['destination']}")

if __name__ == '__main__':
    main()
