# main.py

import requests
import time
from config import WEBHOOK_URL, ACCOUNTS

active_games = {}

def is_in_game(player):
    url = f"https://www.op.gg/api/v1.0/internal/bypass/summoner/{player['server']}/{player['encoded']}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"❌ Error {res.status_code} for {player['name']}")
            return None

        data = res.json()
        is_playing = data.get("data", {}).get("isInGame", False)
        game_mode = data.get("data", {}).get("currentGameInfo", {}).get("gameMode", "Unknown")

        return game_mode if is_playing else None
    except Exception as e:
        print(f"⚠️ Exception with {player['name']}: {e}")
        return None

def send_discord_notification(player, mode):
    message = (
        f"🔔 **{player['name']}** vừa bắt đầu một trận đấu!\n"
        f"🎮 Loại trận: `{mode}`\n"
        f"📅 Thời điểm: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🔗 https://www.op.gg/summoners/{player['server']}/{player['encoded']}/ingame"
    )
    requests.post(WEBHOOK_URL, json={"content": message})

def run():
    for player in ACCOUNTS:
        mode = is_in_game(player)
        key = player['name']

        if mode:
            if key not in active_games or active_games[key] != mode:
                send_discord_notification(player, mode)
                active_games[key] = mode
                print(f"✅ {key} đang chơi {mode}")
        else:
            if key in active_games:
                del active_games[key]

if __name__ == "__main__":
    run()
