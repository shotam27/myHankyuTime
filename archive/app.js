// config.jsから読み込み、なければデフォルトを使用
let API_KEY = 'YOUR_API_KEY_HERE';

// config.jsが存在する場合は読み込む
if (typeof CONFIG !== 'undefined' && CONFIG.API_KEY) {
    API_KEY = CONFIG.API_KEY;
}

// 駅すぱあとAPI設定
const STATION_CODE = '22630'; // 阪急総持寺駅の駅コード
const API_BASE_URL = 'https://api.ekispert.jp/v1/json';
const DIRECTION = '梅田'; // 行き先

// 時刻を「HH:MM」形式にパース
function parseTime(timeStr) {
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
}

// 現在時刻を「HH:MM」形式に変換
function getCurrentTimeString() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + 
           now.getMinutes().toString().padStart(2, '0');
}

// 現在時刻+4分を分単位で取得
function getTargetMinutes() {
    const now = new Date();
    const targetTime = new Date(now.getTime() + 4 * 60000);
    return targetTime.getHours() * 60 + targetTime.getMinutes();
}

// 日付をYYYYMMDD形式に変換
function getDateString() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    return `${year}${month}${day}`;
}

// 時刻をHHMM形式に変換
function getTimeString(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}${minutes}`;
}

// 駅すぱあとAPIから時刻表データを取得
async function fetchTimetable() {
    const date = getDateString();
    const targetTime = new Date(Date.now() + 4 * 60000); // 現在時刻+4分
    const time = getTimeString(targetTime);
    
    // 駅すぱあとAPIのstation/lightエンドポイントを使用
    const url = `${API_BASE_URL}/station/light?key=${API_KEY}&code=${STATION_CODE}&date=${date}&time=${time}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
        throw new Error(`APIエラー: ${response.status}`);
    }
    
    return await response.json();
}

// 次の電車情報を探す（駅すぱあとAPIのTimeLineから）
function findNextTrain(stationData) {
    // ResultSet.Information.Line を確認
    if (!stationData.ResultSet || !stationData.ResultSet.Information) {
        return null;
    }
    
    const lines = stationData.ResultSet.Information.Line;
    if (!lines || !Array.isArray(lines)) {
        return null;
    }
    
    const targetMinutes = getTargetMinutes();
    let nextTrain = null;
    let minDiff = Infinity;
    
    // 各路線を確認
    for (const line of lines) {
        const timeTable = line.TimeTable;
        if (!timeTable || !Array.isArray(timeTable)) continue;
        
        // 梅田方面の列車を探す
        for (const table of timeTable) {
            const direction = table.Direction;
            if (!direction || !direction.includes(DIRECTION)) {
                continue;
            }
            
            const times = table.Time;
            if (!times || !Array.isArray(times)) continue;
            
            // 時刻をチェック
            for (const timeEntry of times) {
                const departureTime = timeEntry.DepartureTime;
                if (!departureTime) continue;
                
                const trainMinutes = parseTime(departureTime);
                const diff = trainMinutes - targetMinutes;
                
                if (diff >= 0 && diff < minDiff) {
                    minDiff = diff;
                    nextTrain = {
                        time: departureTime,
                        destination: direction,
                        trainType: timeEntry.Type || ''
                    };
                }
            }
        }
    }
    
    return nextTrain;
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

// 電車種別を日本語に変換
function getTrainTypeName(trainType) {
    if (!trainType) return '';
    
    // 駅すぱあとAPIの種別名をそのまま使用（既に日本語の場合が多い）
    const typeMap = {
        'local': '普通',
        'express': '急行',
        'semi_express': '準急',
        'rapid_express': '快速急行',
        'limited_express': '特急',
        '普通': '普通',
        '急行': '急行',
        '準急': '準急',
        '快速急行': '快速急行',
        '特急': '特急'
    };
    
    return typeMap[trainType.toLowerCase()] || trainType;
}

// 画面を更新
async function updateDisplay() {
    try {
        const data = await fetchTimetable();
        const nextTrain = findNextTrain(data);
        
        if (nextTrain) {
            const trainType = getTrainTypeName(nextTrain.trainType);
            const displayText = trainType ? `${trainType} ${nextTrain.time}` : nextTrain.time;
            document.getElementById('display').innerText = displayText;
            
            const minutesUntil = getTimeUntil(nextTrain.time);
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
