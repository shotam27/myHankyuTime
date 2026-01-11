// 時刻表テキストをパースするスクリプト
const fs = require('fs');
const path = require('path');

function parseTimetableFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n').map(line => line.trim()).filter(line => line.length > 0);
    
    const timetables = {};
    let currentHour = null;
    let currentMinute = null;
    let currentDestination = null;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        // 時間の行（例: "5", "6", "7"など）+ "時"
        if (line === '時' && i > 0 && lines[i-1].match(/^\d+$/)) {
            currentHour = lines[i-1].padStart(2, '0');
            continue;
        }
        
        // 分の行（例: "16", "35"など）+ "分"
        if (line === '分' && i > 0 && lines[i-1].match(/^\d+$/)) {
            currentMinute = lines[i-1].padStart(2, '0');
            
            // 次の行から行き先を探す（行き先は［普通］の次）
            for (let j = i + 1; j < Math.min(i + 5, lines.length); j++) {
                const nextLine = lines[j];
                if (nextLine === '大阪梅田' || nextLine === '天下茶屋' || nextLine === '北千里' || 
                    nextLine === '高槻市' || nextLine === '淡路' || nextLine === '河原町' || 
                    nextLine === '嵐山' || nextLine === '桂' || nextLine === '豊津') {
                    currentDestination = nextLine;
                    break;
                }
            }
            
            if (currentHour && currentMinute && currentDestination) {
                const time = `${currentHour}:${currentMinute}`;
                if (!timetables[currentDestination]) {
                    timetables[currentDestination] = [];
                }
                timetables[currentDestination].push(time);
            }
            continue;
        }
    }
    
    return timetables;
}

// 平日時刻表をパース
const weekdayFile = path.join(__dirname, 'data', '平日時刻表.txt');
const holidayFile = path.join(__dirname, 'data', '休日時刻表.txt');

const weekdayTimetables = parseTimetableFile(weekdayFile);
const holidayTimetables = parseTimetableFile(holidayFile);

console.log('// 平日時刻表データ');
console.log('const TIMETABLE_WEEKDAY = {');
for (const [destination, times] of Object.entries(weekdayTimetables)) {
    console.log(`    "${destination}": [${times.map(t => `"${t}"`).join(', ')}],`);
}
console.log('};');
console.log('');

console.log('// 休日時刻表データ');
console.log('const TIMETABLE_HOLIDAY = {');
for (const [destination, times] of Object.entries(holidayTimetables)) {
    console.log(`    "${destination}": [${times.map(t => `"${t}"`).join(', ')}],`);
}
console.log('};');
