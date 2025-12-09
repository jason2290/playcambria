# pip install pyautogui pynput

import pyautogui
import time
from pynput import mouse

# 讓 pyautogui 不要太慢
pyautogui.FAILSAFE = False 
pyautogui.MINIMUM_DURATION = 0.1
pyautogui.PAUSE = 0.05

# 全域變數儲存起始點
origin = None

def on_click(x, y, button, pressed):
    global origin
    if pressed and button == mouse.Button.left:      # 只接受左鍵按下
        origin = (x, y)
        print(f"\n已記錄起始位置：{origin}")
        print("開始執行週期動作（每7秒一次），按 Ctrl+C 停止\n")
        return False    # 停止監聽

print("請在任意地方用「滑鼠左鍵」點一下螢幕來設定原點位置...")
print("（點擊後會立刻開始週期動作）")

# 監聽一次左鍵點擊
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

if origin is None:
    print("沒有偵測到點擊，腳本結束")
    exit()

ox, oy = origin

# 進入主要循環
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
        
        # 5. 等待下一個週期（總週期約 7 秒）
        time.sleep(7 - 1 - 0.3)    # 扣掉前面已經花的時間，確保整體約 5 秒一次

except KeyboardInterrupt:
    print("\n腳本已手動停止，拜拜！")
