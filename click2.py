# pip install pyautogui pynput requests

# -*- coding: utf-8 -*-
import pyautogui
import time
from pynput import mouse
import requests
import os

# ==================== 設定區 ====================
pyautogui.FAILSAFE = False      # 關閉左上角緊急停止
pyautogui.PAUSE = 0.05

# ←←←←← 請改這裡！你的 Bark key ←←←←←
BARK_KEY = "oj9qzw8D7BFe5ZXuXy7nvM"   # 例如：abcd1234abcd1234abcd1234

# 圖片必須和此腳本放在同一資料夾
FULL_IMAGE = "full.jpg"         # 150% + 背包的完整截圖

# 每點幾下檢查一次
CHECK_EVERY = 1

# ==================== 全域變數 ====================
origin = None
click_count = 0

# ==================== 工具函式 ====================
def bark(message: str):
    """發送 Bark 通知"""
    if not BARK_KEY or BARK_KEY.startswith("請"):
        print(f"[Bark] 未設定 key，忽略：{message}")
        return
    try:
        url = f"https://api.day.app/{BARK_KEY}/{message}"
        requests.get(url, timeout=8)
        print(f"{time.strftime('%H:%M:%S')} → Bark 已推播：{message}")
    except Exception as e:
        print(f"{time.strftime('%H:%M:%S')} → Bark 推播失敗：{e}")

def has_full_image():
    """安全檢查 full.jpg 是否出現在螢幕上"""
    if not os.path.exists(FULL_IMAGE):
        print("警告：找不到 full.jpg 檔案！")
        return False
    try:
        # confidence 設 0.9 比較嚴格，避免誤判；可自行調成 0.85~0.95
        return pyautogui.locateOnScreen(FULL_IMAGE, confidence=0.7) is not None
    except Exception:
        return False

# ==================== 設定點擊位置 ====================
def on_click(x, y, button, pressed):
    global origin
    if pressed and button == mouse.Button.left:
        origin = (x, y)
        print(f"\n已記錄點擊位置：{origin}")
        print("開始自動點擊＋監控，按 Ctrl+C 停止\n")
        return False

print("請用滑鼠左鍵點一下你要狂點的位置...")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

if origin is None:
    print("沒點到，腳本結束")
    exit()

ox, oy = origin

# ==================== 主迴圈 ====================
try:
    while True:
        # 你原本的甩鼠標動作
        pyautogui.moveTo(ox + 100, oy - 100, duration=0.15)
        pyautogui.moveTo(ox, oy, duration=0.15)
        time.sleep(1)

        # 點擊
        pyautogui.click()
        click_count += 1
        print(f"{time.strftime('%H:%M:%S')} → 第 {click_count:4d} 次點擊")

        # 每 50 次檢查一次是否背包滿了
        if click_count % CHECK_EVERY == 0:
            print(f"{time.strftime('%H:%M:%S')} → 檢查背包是否已滿...")
            if has_full_image():
                bark("Cambria背包已滿！")
                print("偵測到 full.jpg → 已發送通知！")
            else:
                print("尚未滿，繼續點～")

        # 週期控制（整體約 5 秒一次）
        time.sleep(5.7)

except KeyboardInterrupt:
    print("\n\n手動停止，腳本結束，拜拜～")
