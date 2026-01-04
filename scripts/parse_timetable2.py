#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VS Code APIを使って時刻.txtファイルから時刻表データを抽出してCSV/JSON形式に変換
"""

import re
import json
import csv

# 時刻.txtの内容を直接記述して解析
# VS Codeで読み込めるがPythonで読み込めない場合の対処

def parse_from_lines(lines):
    """行のリストから時刻表を解析"""
    timetable = []
    current_hour = None
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:  # 空行はスキップ
            i += 1
            continue
        
        # 時間の行を検出
        if line.isdigit() and i + 1 < len(lines) and lines[i + 1].strip() == '時':
            current_hour = line.zfill(2)
            i += 2
            continue
        
        # 分の行を検出
        if i + 1 < len(lines) and lines[i + 1].strip() == '分':
            try:
                minute = line.zfill(2)
            except:
                i += 1
                continue
                
            i += 2
            
            # 種別を取得
            train_type = '普通'
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('［') and next_line.endswith('］'):
                    train_type = next_line.strip('［］')
                    i += 1
            
            # 行き先を取得
            destination = ''
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line and next_line != 'ポップアップウィンドウで開く':
                    destination = next_line
                    i += 1
            
            # 「ポップアップウィンドウで開く」をスキップ
            while i < len(lines) and lines[i].strip() == 'ポップアップウィンドウで開く':
                i += 1
            
            # データを追加
            if current_hour is not None and destination:
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

# サンプルデータで手動テスト
sample_data = """5
時
16
分

［普通］

大阪梅田

ポップアップウィンドウで開く
35
分

［普通］

大阪梅田

ポップアップウィンドウで開く"""

if __name__ == '__main__':
    # まずサンプルでテスト
    print("=== サンプルデータでテスト ===")
    lines = sample_data.split('\n')
    result = parse_from_lines(lines)
    for item in result:
        print(f"  {item['time']} [{item['type']}] {item['destination']}")
    
    print(f"\n{len(result)}件のデータを抽出しました")
    
    # 実際のファイルを試行
    print("\n=== 実際のファイルから読み込み ===")
    try:
        with open('時刻.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"ファイル読み込み成功: {len(lines)}行")
            
            timetable = parse_from_lines(lines)
            print(f"解析結果: {len(timetable)}件")
            
            if len(timetable) > 0:
                # 大阪梅田方面のみをフィルタリング
                umeda_trains = [t for t in timetable if '大阪梅田' in t['destination']]
                
                # CSV形式で保存
                with open('timetable_weekday.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['時刻', '種別', '行き先'])
                    for train in umeda_trains:
                        writer.writerow([train['time'], train['type'], train['destination']])
                
                print(f"✓ CSV保存完了: timetable_weekday.csv ({len(umeda_trains)}件)")
                
                # JSON形式で保存
                output = {
                    'station': '総持寺',
                    'direction': '大阪梅田',
                    'day_type': '平日',
                    'total_trains': len(umeda_trains),
                    'trains': umeda_trains
                }
                
                with open('timetable_weekday.json', 'w', encoding='utf-8') as jsonfile:
                    json.dump(output, jsonfile, ensure_ascii=False, indent=2)
                
                print(f"✓ JSON保存完了: timetable_weekday.json")
                
                # 最初と最後を表示
                print(f"\n【最初の5本】")
                for train in umeda_trains[:5]:
                    print(f"  {train['time']} [{train['type']}] {train['destination']}")
                
                print(f"\n【最後の5本】")
                for train in umeda_trains[-5:]:
                    print(f"  {train['time']} [{train['type']}] {train['destination']}")
            else:
                print("⚠ データを抽出できませんでした")
                
    except FileNotFoundError:
        print("⚠ ファイルが見つかりません")
    except Exception as e:
        print(f"⚠ エラー: {e}")
