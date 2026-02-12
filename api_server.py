#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡易APIサーバー - YouTube Music再生履歴とキャスト機能
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import re
from urllib.parse import parse_qs, urlparse
import sys

# ログ出力用
def log(message):
    print(f"[API] {message}", file=sys.stderr, flush=True)

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # CORS設定
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if parsed_path.path == '/api/last_played':
            # ログから最後に再生されたYouTube Musicの情報を取得
            try:
                with open('/tmp/auto_cast.log', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # 最新のYouTube Music情報を検索
                for line in reversed(lines):
                    if 'SONG:' in line and 'CONTENT_ID:' in line:
                        # [日時] APP: YouTube Music, STATE: PLAYING, SONG: 曲名 - アーティスト, CONTENT_ID: xxx
                        song_match = re.search(r'SONG: (.+?) - (.+?), CONTENT_ID:', line)
                        content_match = re.search(r'CONTENT_ID: (\S+)', line)
                        
                        if song_match and content_match:
                            title = song_match.group(1).strip()
                            artist = song_match.group(2).strip()
                            content_id = content_match.group(1).strip()
                            
                            response = {
                                'title': title,
                                'artist': artist,
                                'content_id': content_id,
                                'url': f'https://music.youtube.com/watch?v={content_id}'
                            }
                            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                            return
                
                self.wfile.write(json.dumps({'error': 'No recent music found'}).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        
        elif parsed_path.path == '/api/cast_music':
            # YouTube MusicをNest Hubにキャスト
            params = parse_qs(parsed_path.query)
            title = params.get('title', [None])[0]
            artist = params.get('artist', [None])[0]
            
            log(f"Cast music request: title={title}, artist={artist}")
            
            if title and artist:
                # 先にレスポンスを返す
                self.wfile.write(json.dumps({'status': 'processing', 'title': title, 'artist': artist}).encode('utf-8'))
                
                try:
                    import time
                    import threading
                    
                    def cast_async():
                        try:
                            # まず現在のキャストを停止
                            log("Stopping current cast...")
                            stop_result = subprocess.run(
                                ['/home/pi/.local/bin/catt', '-d', 'キッチン', 'stop'],
                                check=False,
                                capture_output=True,
                                timeout=10,
                                text=True
                            )
                            log(f"Stop result: returncode={stop_result.returncode}")
                            
                            # 短めに待機
                            time.sleep(2)
                            
                            # yt-dlpでYouTube検索して最初の動画URLを取得
                            search_query = f"ytsearch1:{title} {artist}"
                            log(f"Searching with yt-dlp: {search_query}")
                            
                            # yt-dlpで動画URLを取得
                            result = subprocess.run(
                                ['yt-dlp', '--get-id', '--no-playlist', search_query],
                                capture_output=True,
                                text=True,
                                timeout=30
                            )
                            
                            log(f"yt-dlp result: returncode={result.returncode}, video_id={result.stdout.strip()[:50]}")
                            
                            if result.returncode == 0 and result.stdout.strip():
                                video_id = result.stdout.strip()
                                video_url = f"https://www.youtube.com/watch?v={video_id}"
                                
                                log(f"Casting video: {video_url}")
                                
                                # 取得したURLをキャスト
                                cast_result = subprocess.run(
                                    ['/home/pi/.local/bin/catt', '-d', 'キッチン', 'cast', video_url],
                                    capture_output=True,
                                    text=True,
                                    timeout=30
                                )
                                
                                log(f"Cast result: returncode={cast_result.returncode}")
                                
                                # キャスト成功後、YouTubeが確実に起動するまで待機
                                if cast_result.returncode == 0:
                                    time.sleep(20)
                                    log("Cast completed and waited for YouTube to start")
                            else:
                                log(f"Video search failed: {result.stderr[:200]}")
                        except Exception as e:
                            log(f"Exception in cast_async: {e}")
                    
                    # 別スレッドで実行
                    thread = threading.Thread(target=cast_async)
                    thread.start()
                    
                except Exception as e:
                    log(f"Exception: {e}")
            else:
                self.wfile.write(json.dumps({'error': 'Title or artist missing'}).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({'error': 'Unknown endpoint'}).encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8081), APIHandler)
    print('API Server running on port 8081...')
    server.serve_forever()
