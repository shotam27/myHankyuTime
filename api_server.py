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
            url = params.get('url', [None])[0]
            
            if url:
                try:
                    subprocess.run(
                        ['/home/pi/.local/bin/catt', '-d', 'キッチン', 'cast', url],
                        check=True
                    )
                    self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
                except Exception as e:
                    self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({'error': 'No URL provided'}).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({'error': 'Unknown endpoint'}).encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8081), APIHandler)
    print('API Server running on port 8081...')
    server.serve_forever()
