// 平日・休日を自動判別して時刻表を表示するバージョン

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

// 時刻表データ（休日・大阪梅田方面）
const TIMETABLE_HOLIDAY = [
    "05:16", "05:35", "05:53", "06:12", "06:22", "06:33", "06:40", "06:48",
    "07:03", "07:13", "07:23", "07:39",
    "08:11", "08:43",
    "09:07", "09:28", "09:48",
    "10:08", "10:28", "10:48",
    "11:08", "11:28", "11:48",
    "12:08", "12:28", "12:48",
    "13:08", "13:28", "13:48",
    "14:08", "14:28", "14:48",
    "15:08", "15:28", "15:48",
    "16:08", "16:28", "16:48",
    "17:09", "17:29", "17:50",
    "18:10", "18:30", "18:51",
    "19:12", "19:32", "19:52",
    "20:12", "20:32", "20:52",
    "21:03", "21:13", "21:23", "21:39", "21:44", "21:56",
    "22:13", "22:30", "22:46",
    "23:00", "23:14", "23:29", "23:44"
];

// ゴミの日データ
const GARBAGE_SCHEDULE = {
    // 0: 日, 1: 月, 2: 火, 3: 水, 4: 木, 5: 金, 6: 土
    3: '普通ごみ',  // 水曜日
    6: '普通ごみ',  // 土曜日
};

// 第n週を計算
function getWeekOfMonth(date) {
    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
    const day = date.getDate();
    return Math.ceil((day + firstDay.getDay()) / 7);
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
        
        // ダイヤ種別を表示
        const dayType = isHoliday() ? '休日' : '平日';
        document.getElementById('dayType').innerText = `${dayType}ダイヤ`;
        
        // ゴミの日を表示
        const garbageElement = document.getElementById('garbageDay');
        const tomorrowGarbage = getTomorrowGarbage();
        if (tomorrowGarbage) {
            garbageElement.innerText = `🗑️ 明日は ${tomorrowGarbage} の日`;
            garbageElement.classList.add('today');
        } else {
            garbageElement.innerText = '';
            garbageElement.classList.remove('today');
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
    
    // アトランタ時間を更新
    const atlantaTime = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
    const atlantaStr = `${atlantaTime.getHours().toString().padStart(2, '0')}:${atlantaTime.getMinutes().toString().padStart(2, '0')}:${atlantaTime.getSeconds().toString().padStart(2, '0')}`;
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
