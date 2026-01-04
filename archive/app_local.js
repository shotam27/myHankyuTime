// ローカルの時刻表データを使用するバージョン
// JSONファイルから時刻表を読み込んで表示

// 時刻表データ（平日・大阪梅田方面）
const TIMETABLE_WEEKDAY = [
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
];

// 時刻を「HH:MM」形式にパース（分単位に変換）
function parseTime(timeStr) {
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
}

// 現在時刻+4分を分単位で取得
function getTargetMinutes() {
    const now = new Date();
    const targetTime = new Date(now.getTime() + 4 * 60000);
    return targetTime.getHours() * 60 + targetTime.getMinutes();
}

// 次の電車を探す
function findNextTrain() {
    const targetMinutes = getTargetMinutes();
    
    // targetMinutes以降で最も近い電車を探す
    for (const timeStr of TIMETABLE_WEEKDAY) {
        const trainMinutes = parseTime(timeStr);
        if (trainMinutes >= targetMinutes) {
            return timeStr;
        }
    }
    
    // 翌日の始発を返す（深夜の場合）
    return TIMETABLE_WEEKDAY[0];
}

// 次の電車までの時間を計算
function getTimeUntil(trainTime) {
    const now = new Date();
    const [hours, minutes] = trainTime.split(':').map(Number);
    const trainDate = new Date(now);
    trainDate.setHours(hours, minutes, 0, 0);
    
    // 電車が過去の時刻の場合は翌日と判断
    if (trainDate < now) {
        trainDate.setDate(trainDate.getDate() + 1);
    }
    
    const diff = Math.floor((trainDate - now) / 1000 / 60);
    return diff;
}

// 画面を更新
function updateDisplay() {
    try {
        const nextTrainTime = findNextTrain();
        
        if (nextTrainTime) {
            document.getElementById('display').innerText = `普通 ${nextTrainTime}`;
            
            const minutesUntil = getTimeUntil(nextTrainTime);
            document.getElementById('timeUntil').innerText = `あと ${minutesUntil} 分`;
            
            // 緊急度によって色を変更
            const displayElement = document.querySelector('.next-train');
            if (minutesUntil <= 5) {
                displayElement.style.color = '#f00';
                displayElement.style.textShadow = '0 0 20px #f00';
            } else if (minutesUntil <= 10) {
                displayElement.style.color = '#ff0';
                displayElement.style.textShadow = '0 0 20px #ff0';
            } else {
                displayElement.style.color = '#0f0';
                displayElement.style.textShadow = '0 0 20px #0f0';
            }
        } else {
            document.getElementById('display').innerHTML = '<span class="error">本日の運行は終了しました</span>';
            document.getElementById('timeUntil').innerText = '';
        }
        
        // 最終更新時刻を表示
        const now = new Date();
        document.getElementById('lastUpdate').innerText = 
            `最終更新: ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
            
    } catch (error) {
        console.error('エラー:', error);
        document.getElementById('display').innerHTML = `<span class="error">エラー: ${error.message}</span>`;
        document.getElementById('timeUntil').innerText = '';
    }
}

// 現在時刻を更新
function updateCurrentTime() {
    const now = new Date();
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    document.getElementById('currentTime').innerText = timeStr;
}

// 初期化
window.addEventListener('DOMContentLoaded', () => {
    // 初回実行
    updateDisplay();
    updateCurrentTime();
    
    // 30秒ごとに更新
    setInterval(updateDisplay, 30000);
    
    // 1秒ごとに現在時刻を更新
    setInterval(updateCurrentTime, 1000);
});
