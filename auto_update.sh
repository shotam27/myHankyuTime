#!/bin/bash
cd ~/myHankyuTime

while true; do
  git fetch origin main
  LOCAL=$(git rev-parse HEAD)
  REMOTE=$(git rev-parse origin/main)
  
  if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date): 更新検出、プル開始"
    git pull origin main
    
    # Webサーバー再起動
    pkill -f "python3 -m http.server" || true
    sleep 1
    nohup python3 -m http.server 8080 > /dev/null 2>&1 &
    
    # Nest Hub再キャスト
    sleep 2
    ~/.local/bin/catt -d "キッチン" cast_site http://192.168.11.21:8080/
  fi
  
  sleep 60
done
