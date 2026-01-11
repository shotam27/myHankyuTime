// 平日・休日を自動判別して時刻表を表示するバージョン（全方向統合）

// 時刻表データ（平日・全方向統合）
const TIMETABLE_WEEKDAY = [
    "00:06", "00:27", "05:16", "05:35", "05:54", "06:12", "06:18", "06:22", "06:33", "06:43", "06:47", "06:57", "07:06", "07:17", "07:28", "07:39", "07:45", "07:48", "07:57", "08:03", "08:14", "08:21", "08:32", "08:39", "08:49", "08:58", "09:09", "09:19", "09:29", "09:39", "09:50", "10:01", "10:11", "10:21", "10:31", "10:41", "10:51", "11:01", "11:11", "11:21", "11:31", "11:41", "11:51", "12:01", "12:11", "12:21", "12:31", "12:41", "12:51", "13:01", "13:11", "13:21", "13:31", "13:41", "13:51", "14:01", "14:11", "14:21", "14:31", "14:41", "14:51", "15:01", "15:11", "15:21", "15:31", "15:40", "15:50", "16:00", "16:10", "16:20", "16:30", "16:40", "16:50", "17:00", "17:08", "17:13", "17:24", "17:27", "17:33", "17:43", "17:47", "17:53", "18:04", "18:08", "18:14", "18:24", "18:29", "18:34", "18:44", "18:54", "19:04", "19:09", "19:15", "19:23", "19:33", "19:44", "19:54", "20:04", "20:08", "20:14", "20:24", "20:27", "20:34", "20:45", "20:55", "21:04", "21:08", "21:16", "21:19", "21:26", "21:30", "21:40", "21:43", "21:51", "21:55", "22:08", "22:21", "22:31", "22:46", "23:00", "23:14", "23:29", "23:44", "23:56"
];

// 時刻表データ（休日・全方向統合）
const TIMETABLE_HOLIDAY = [
    "00:06", "00:27", "05:16", "05:35", "05:53", "06:12", "06:22", "06:33", "06:40", "06:48", "07:03", "07:13", "07:23", "07:33", "07:39", "07:49", "07:59", "08:11", "08:22", "08:32", "08:43", "08:56", "09:07", "09:18", "09:28", "09:38", "09:48", "09:58", "10:08", "10:18", "10:28", "10:38", "10:48", "10:58", "11:09", "11:19", "11:28", "11:38", "11:48", "11:58", "12:08", "12:18", "12:28", "12:38", "12:48", "12:58", "13:09", "13:19", "13:28", "13:38", "13:48", "13:58", "14:08", "14:18", "14:28", "14:38", "14:48", "14:58", "15:08", "15:19", "15:28", "15:38", "15:48", "15:58", "16:08", "16:18", "16:28", "16:38", "16:48", "16:58", "17:08", "17:19", "17:28", "17:38", "17:48", "17:58", "18:08", "18:18", "18:28", "18:38", "18:48", "18:58", "19:08", "19:18", "19:28", "19:38", "19:48", "19:56", "20:07", "20:14", "20:27", "20:33", "20:35", "20:40", "20:51", "21:00", "21:03", "21:13", "21:23", "21:28", "21:39", "21:44", "21:56", "22:13", "22:30", "22:46", "23:00", "23:14", "23:29", "23:44"
];

// ゴミの日データ
const GARBAGE_SCHEDULE = {
    // 0: 日, 1: 月, 2: 火, 3: 水, 4: 木, 5: 金, 6: 土
    3: '普通ごみ',  // 水曜日
    6: '普通ごみ',  // 土曜日
};

// 第n週を計算
function getWeekOfMonth(date) {
    // その曜日が月の中で第何回目かを計算
    return Math.floor((date.getDate() - 1) / 7) + 1;
}

// 明日のゴミの日を取得
function getTomorrowGarbage() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const day = tomorrow.getDay(); // 0-6
    const week = getWeekOfMonth(tomorrow);
    
    const garbage = [];
    
    // 毎週のゴミ
    if (GARBAGE_SCHEDULE[day]) {
        garbage.push(GARBAGE_SCHEDULE[day]);
    }
    
    // 第n週のゴミ
    if (day === 5 && (week === 1 || week === 3)) { // 第1・3金曜日
        garbage.push('ペットボトル');
    }
    if (day === 1 && week === 3) { // 第3月曜日
        garbage.push('古紙・古布');
    }
    if (day === 2 && week === 1) { // 第1火曜日
        garbage.push('小型粗大ごみ');
    }
    if (day === 2 && week === 3) { // 第3火曜日
        garbage.push('大型粗大ごみ');
    }
    
    return garbage.length > 0 ? garbage.join('・') : null;
}

// 曜日を判定（平日 or 休日）
function isHoliday() {
    const now = new Date();
    const day = now.getDay();
    // 0: 日曜, 6: 土曜
    return (day === 0 || day === 6);
}

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
    const timetable = isHoliday() ? TIMETABLE_HOLIDAY : TIMETABLE_WEEKDAY;
    
    // targetMinutes以降で最も近い電車を探す
    for (const timeStr of timetable) {
        const trainMinutes = parseTime(timeStr);
        if (trainMinutes >= targetMinutes) {
            return timeStr;
        }
    }
    
    // 翌日の始発を返す（深夜の場合）
    return timetable[0];
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
            document.getElementById('display').innerText = `${nextTrainTime}`;
            
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
        
        // ダイヤ種別を表示
        const dayType = isHoliday() ? '休日' : '平日';
        document.getElementById('dayType').innerText = `${dayType}ダイヤ`;
        
        // ゴミの日を表示
        const garbageElement = document.getElementById('garbageDay');
        const tomorrowGarbage = getTomorrowGarbage();
        if (tomorrowGarbage) {
            garbageElement.innerText = `🗑️ 明日は\n${tomorrowGarbage}\nの日`;
            garbageElement.classList.add('today');
        } else {
            garbageElement.innerText = '明日は\nごみ回収なし';
            garbageElement.classList.remove('today');
        }
        garbageElement.style.display = 'flex';
        
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
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    document.getElementById('currentTime').innerText = timeStr;
    
    // アトランタ時間を更新
    const atlantaTime = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
    const atlantaStr = `${atlantaTime.getHours().toString().padStart(2, '0')}:${atlantaTime.getMinutes().toString().padStart(2, '0')}`;
    document.getElementById('atlantaTimeValue').innerText = atlantaStr;
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
