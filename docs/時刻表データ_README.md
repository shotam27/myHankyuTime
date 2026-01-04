# 時刻表データについて

このフォルダには阪急総持寺駅から大阪梅田方面への平日時刻表データが含まれています。

## ファイル一覧

### 扱いやすい形式のファイル

#### 平日ダイヤ（81本）
1. **[timetable_weekday.json](timetable_weekday.json)** - JSON形式の時刻表（平日）
2. **[timetable_weekday.csv](timetable_weekday.csv)** - CSV形式の時刻表（平日）

#### 休日ダイヤ（63本）
3. **[timetable_holiday.json](timetable_holiday.json)** - JSON形式の時刻表（休日）
4. **[timetable_holiday.csv](timetable_holiday.csv)** - CSV形式の時刻表（休日）

#### Webアプリ（APIキー不要）
5. **[index_auto.html](index_auto.html)** + **[app_auto.js](app_auto.js)** 【推奨】
   - 平日・休日を自動判別
   - ブラウザで開くだけで動作

6. **[index_local.html](index_local.html)** + **[app_local.js](app_local.js)**
   - 平日ダイヤのみ固定表示
   - シンプルなバージョン

### 元のファイル

- **[時刻.txt](時刻.txt)** - 元の時刻表データ（テキスト形式）
  - Webサイトからコピーしたデータ
  - 扱いにくい形式なので、上記のJSON/CSV版を使用することを推奨

### 変換スクリプト

- **[create_timetable.py](create_timetable.py)** - 平日時刻表を生成
- **[create_timetable_holiday.py](create_timetable_holiday.py)** - 休日時刻表を生成

## 使用方法

### すぐに試したい場合（API不要・推奨）

1. **[index_auto.html](index_auto.html)** をブラウザで開く
2. 平日・休日が自動判別され、次の電車が表示されます

または

1. **[index_local.html](index_local.html)** をブラウザで開く（平日のみ固定）

### データを活用する場合

**プログラムで使う（JavaScript）:**
```javascript
// JSONファイルを読み込む
fetch('timetable_weekday.json')
  .then(response => response.json())
  .then(data => {
    console.log(`駅: ${data.station}`);
    console.log(`方面: ${data.direction}`);
    console.log(`本数: ${data.total_trains}本`);
    data.trains.forEach(train => {
      console.log(`${train.time} [${train.type}] ${train.destination}`);
    });
  });
```

**Pythonで使う:**
```python
import json

with open('timetable_weekday.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
print(f"駅: {data['station']}")
print(f"方面: {data['direction']}")
print(f"本数: {data['total_trains']}本")

for train in data['trains']:
    print(f"{train['time']} [{train['type']}] {train['destination']}")
```

**Excelで使う:**
1. [timetable_weekday.csv](timetable_weekday.csv) を開く
2. データを編集・分析

## データ構造

### JSON形式
```json
{
  "station": "総持寺",
  "direction": "大阪梅田",
  "day_type": "平日",
  "total_trains": 81,
  "trains": [
    {
      "time": "05:16",
      "hour": "05",
      "minute": "16",
      "type": "普通",
      "destination": "大阪梅田"
    },
    ...
  ]
}
```

### CSV形式
```csv
時刻,種別,行き先
05:16,普通,大阪梅田
05:35,普通,大阪梅田
...
```

## データ更新

時刻表データを更新する場合：

**平日ダイヤの更新:**
1. [create_timetable.py](create_timetable.py) の `timetable_data` を編集
2. スクリプトを実行: `python create_timetable.py`
3. JSON/CSVファイルが自動生成されます

**休日ダイヤの更新:**
1. [create_timetable_holiday.py](create_timetable_holiday.py) の `timetable_data` を編集
2. スクリプトを実行: `python create_timetable_holiday.py`
3. JSON/CSVファイルが自動生成されます

## 注意事項

- **平日ダイヤ**: 81本の電車（月〜金曜日）
- **休日ダイヤ**: 63本の電車（土日祝日）
- ダイヤ改正時には更新が必要です
- 大阪梅田方面のみが含まれています（天下茶屋方面は除外）
- 祝日の判定は含まれていません（土日のみ休日扱い）
