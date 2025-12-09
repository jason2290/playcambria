import pyautogui
import time
from pynput import mouse
import requests  # 新增，用來發送 Bark 通知

pyautogui.FAILSAFE = False        # 關閉失敗安全
pyautogui.MINIMUM_DURATION = 0.1
pyautogui.PAUSE = 0.05

# Bark 相關設定（請替換成你的 Bark key）
BARK_KEY = '你的Bark_Key_在這裡'  # 例如：'https://api.day.app/你的key/' 或直接用 key
BARK_MESSAGE = 'Cambria背包已滿！'

# 圖片檔案名稱（與腳本同一資料夾）
IMAGE_PATH = 'full.jpg'

origin = None

def on_click(x, y, button, pressed):
    global origin
    if pressed and button == mouse.Button.left:
        origin = (x, y)
        print(f"\n已記錄起始位置：{origin}")
        print("開始執行週期動作（每7秒一次），按 Ctrl+C 停止\n")
        return False

print("請在任意地方用「左鍵點一下」來設定原點位置...")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

if origin is None:
    print("沒有偵測到點擊，腳本結束")
    exit()

ox, oy = origin

# 追蹤點擊次數
click_count = 0

try:
    while True:
        # 1. 移到右上 100,100
        pyautogui.moveTo(ox + 100, oy - 100, duration=0.15)
        
        # 2. 立刻移回原位
        pyautogui.moveTo(ox, oy, duration=0.15)
        
        # 3. 移回後等 1 秒
        time.sleep(1)
        
        # 4. 在原位置點一下左鍵
        pyautogui.click()          # 預設點當前位置
        print(f"{time.strftime('%H:%M:%S')} → 已點擊原位置 {origin}")
        
        # 更新點擊次數
        click_count += 1
        
        # 每 50 次點擊檢查一次螢幕是否有 full.jpg
        if click_count % 50 == 0:
            print(f"{time.strftime('%H:%M:%S')} → 檢查螢幕中是否有 {IMAGE_PATH}...")
            if pyautogui.locateOnScreen(IMAGE_PATH, confidence=0.9) is not None:  # confidence=0.9 提高匹配準確度
                print(f"{time.strftime('%H:%M:%S')} → 偵測到 {IMAGE_PATH}！發送 Bark 通知...")
                # 發送 Bark 通知
                try:
                    response = requests.get(f"https://api.day.app/{BARK_KEY}/{BARK_MESSAGE}")
                    if response.status_code == 200:
                        print(f"{time.strftime('%H:%M:%S')} → Bark 通知發送成功！")
                    else:
                        print(f"{time.strftime('%H:%M:%S')} → Bark 通知發送失敗：{response.text}")
                except Exception as e:
                    print(f"{time.strftime('%H:%M:%S')} → Bark 通知發送錯誤：{e}")
            else:
                print(f"{time.strftime('%H:%M:%S')} → 未偵測到 {IMAGE_PATH}。")
        
        # 5. 等待下一個週期（總週期約 7 秒）
        time.sleep(7 - 1 - 0.3)    # 扣掉前面已經花的時間，確保整體約 5 秒一次

except KeyboardInterrupt:
    print("\n腳本已手動停止，拜拜！")