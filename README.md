# 阪急 梅田方面 時刻表アプリ

Google Nest Hubに常時表示する、阪急総持寺駅から梅田方面への次の電車を大きく表示するWebアプリです。

## 📁 ディレクトリ構成

```
260104_myHankyuTime/
├── index.html              # メインアプリ（平日・休日自動判別）
├── app.js                  # メインJavaScript
├── config.example.js       # APIキー設定サンプル
├── README.md               # このファイル
├── .gitignore
│
├── data/                   # 時刻表データ
│   ├── timetable_weekday.json      # 平日時刻表（81本）
│   ├── timetable_weekday.csv
│   ├── timetable_holiday.json      # 休日時刻表（63本）
│   ├── timetable_holiday.csv
│   └── 時刻.txt                    # 元データ
│
├── scripts/                # データ生成スクリプト
│   ├── create_timetable.py         # 平日データ生成
│   └── create_timetable_holiday.py # 休日データ生成
│
├── docs/                   # ドキュメント
│   ├── 手順.txt                    # セットアップ手順
│   └── 時刻表データ_README.md      # データ説明
│
└── archive/                # 旧バージョン
    ├── index.html          # API使用版
    ├── app.js              # API使用版JS
    ├── index_local.html    # 平日のみ版
    └── app_local.js        # 平日のみ版JS
```

## 🚀 クイックスタート

### すぐに使う（推奨）

1. **[index.html](index.html)** をブラウザで開く
2. 自動的に平日・休日を判別して次の電車を表示

**特徴:**
- ✅ APIキー不要
- ✅ 平日・休日を自動判別
- ✅ ブラウザで開くだけで動作
- ✅ Nest Hub向けの大画面デザイン

## 📊 データについて

| ファイル | 形式 | 内容 | 本数 |
|---------|------|------|------|
| [data/timetable_weekday.json](data/timetable_weekday.json) | JSON | 平日ダイヤ | 81本 |
| [data/timetable_weekday.csv](data/timetable_weekday.csv) | CSV | 平日ダイヤ | 81本 |
| [data/timetable_holiday.json](data/timetable_holiday.json) | JSON | 休日ダイヤ | 63本 |
| [data/timetable_holiday.csv](data/timetable_holiday.csv) | CSV | 休日ダイヤ | 63本 |

詳細は [docs/時刻表データ_README.md](docs/時刻表データ_README.md) を参照

## ⚙️ 機能

- **自動ダイヤ判別**: 土日は休日ダイヤ、平日は平日ダイヤを自動選択
- **4分後表示**: 現在時刻+4分以降の次の電車を表示
- **色分け表示**: 
  - 🔴 5分以内 → 赤色（急いで！）
  - 🟡 10分以内 → 黄色（そろそろ）
  - 🟢 それ以上 → 緑色（余裕あり）
- **自動更新**: 30秒ごとに時刻表を更新

## 🖥️ Nest Hubへの表示

### 方法A: catt を使う（推奨）

```bash
# cattのインストール
pip install catt

# URLをキャスト
catt -d "Nest Hub のデバイス名" cast_site "https://your-app-url.com"

# デバイス名を確認
catt scan
```

### 方法B: 定期的な再キャスト（常時表示）

**Windows (タスクスケジューラ)**
1. `cast_to_nest.bat` を作成
2. タスクスケジューラで10分ごとに実行

**Linux/Raspberry Pi (cron)**
```bash
# 10分ごとに実行
*/10 * * * * /usr/local/bin/catt -d "デバイス名" cast_site "https://your-app-url.com"
```

## 🌐 Webアプリの公開

### GitHub Pagesを使う場合

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/ユーザー名/リポジトリ名.git
git push -u origin main
```

リポジトリの Settings > Pages で "main branch" を選択

### Firebase Hostingを使う場合

```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

## 🔧 カスタマイズ

### 駅を変更する場合

`app.js` 内の時刻表データを書き換えるか、`scripts/create_timetable.py` を編集してデータを再生成

### 表示時間のオフセットを変更

`app.js` の `getTargetMinutes()` 関数を編集:
```javascript
const targetTime = new Date(now.getTime() + 4 * 60000);  // 4分 → 任意の値
```

### デザイン変更

`index.html` の `<style>` タグ内を編集

## 📝 データ更新方法

時刻表が変更された場合:

```bash
# Python環境のアクティベート
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 平日ダイヤの更新
cd scripts
python create_timetable.py

# 休日ダイヤの更新
python create_timetable_holiday.py
```

## 🗂️ 旧バージョン

[archive/](archive/) フォルダに以下のバージョンを保管:
- **API使用版**: 駅すぱあとAPIを使うバージョン（APIキー必要）
- **平日のみ版**: 平日ダイヤのみのシンプル版

## ⚠️ 注意事項

- 祝日は自動判定できません（土日のみ休日扱い）
- ダイヤ改正時には `scripts/` のデータを更新する必要があります
- 大阪梅田方面のみ対応（天下茶屋方面は未対応）

## 📄 ライセンス

MIT License

## 🙏 データ提供元

時刻表データは阪急電鉄の公式サイトを参考にしています
