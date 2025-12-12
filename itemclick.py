# -*- coding: utf-8 -*-
# pip3 install pyautogui opencv-python pillow requests pyobjc
import pyautogui
import time
import requests
import os

try:
    from AppKit import NSScreen
except ImportError:
    NSScreen = None

# ==================== 設定區 ====================
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01  # 幾乎不延遲

BARK_KEY = ""   # 留空就不推播

# 支援最多三種物品圖片，沒有就留空字串或直接刪掉
ITEM_IMAGES = [
    "item1.png",   # 第一種物品（一定要有）
    "item2.png",   # 第二種（沒有就留空或刪掉這行）
    "item3.png",   # 第三種（沒有就留空或刪掉這行）
]

CONFIDENCE = 0.80                  # 0.75~0.85 之間調整
CLICK_COOLDOWN = 3.0               # 每次點擊後強制冷卻秒數
SCAN_INTERVAL = 0.3                # 掃描間隔（越小越快，但別低於 0.2）

# ==================== 自動偵測縮放比例 ====================
def get_scale_factor():
    if NSScreen:  # macOS
        try:
            return NSScreen.mainScreen().backingScaleFactor()
        except:
            pass
    # Windows DPI 偵測
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        dpi = ctypes.windll.user32.GetDpiForWindow(ctypes.windll.user32.GetForegroundWindow())
        return round(dpi / 96.0, 2)
    except:
        return 1.0

scale_factor = get_scale_factor()

# ==================== Bark 推播 ====================
def bark(msg):
    if BARK_KEY.strip():
        try:
            requests.get(f"https://api.day.app/{BARK_KEY}/{msg}", timeout=5)
        except:
            pass

# ==================== 主邏輯 ====================
last_click_time = 0

def try_click_any_item():
    global last_click_time

    # 冷卻中直接返回
    if time.time() - last_click_time < CLICK_COOLDOWN:
        remaining = CLICK_COOLDOWN - (time.time() - last_click_time)
        print(f"  冷卻中... 剩 {remaining:.1f}s", end="\r")
        return False

    # 依序檢查所有存在的圖片
    for img_path in ITEM_IMAGES:
        img_path = img_path.strip()
        if not img_path or not os.path.exists(img_path):
            continue

        try:
            locations = list(pyautogui.locateAllOnScreen(img_path, confidence=CONFIDENCE))
            if locations:
                box = locations[0]  # 只點第一個找到的
                cx = box.left + box.width // 2
                cy = box.top + box.height // 2
                real_x = cx / scale_factor
                real_y = cy / scale_factor

                print(f"{time.strftime('%H:%M:%S')} → 發現 {os.path.basename(img_path)}！瞬間點擊 ({int(real_x)}, {int(real_y)})")

                # 完全不甩鼠標，直接瞬移 + 點擊（最快）
                pyautogui.moveTo(real_x, real_y, duration=0)  # duration=0 就是瞬間移動
                pyautogui.click(real_x, real_y)

                last_click_time = time.time()
                bark(f"Cambria：撿到 {os.path.basename(img_path)} 啦～")
                print(f"已點擊，進入 {CLICK_COOLDOWN} 秒冷卻...")
                return True
        except Exception as e:
            # 偶爾會噴錯很正常，不影響
            pass

    return False

# ==================== 啟動 ====================
print("=== Cambria 極速自動撿物腳本（支援 1~3 種物品 + 無甩鼠標 + 瞬間點擊）===")
existing_items = [os.path.basename(p) for p in ITEM_IMAGES if p.strip() and os.path.exists(p.strip())]
print(f"目前啟用目標：{', '.join(existing_items) if existing_items else '無'}")
print(f"信心度：{CONFIDENCE} | 冷卻：{CLICK_COOLDOWN}秒 | 縮放修正：{scale_factor}x")
print("按 Ctrl+C 隨時停止\n")

try:
    while True:
        try_click_any_item()
        time.sleep(SCAN_INTERVAL)

except KeyboardInterrupt:
    print("\n\n已手動停止，88～")