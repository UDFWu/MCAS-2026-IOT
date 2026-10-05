import RPi.GPIO as GPIO
import time

# --- 腳位設定 (請依據您的實際接線修改) ---
BUZZER_PIN = 12  # 蜂鳴器接實體第 12 腳
LED_PIN = 11     # LED 燈接實體第 11 腳 (新增這行)

freq = 523       # 蜂鳴器發聲頻率

# 初始化 GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)  # 設定 LED 腳位為輸出模式

# 建立 PWM 物件控制蜂鳴器
voice = GPIO.PWM(BUZZER_PIN, freq)

# --- 摩斯密碼時間設定 (單位：秒) ---
DOT_TIME = 0.2          # 短音/短亮 (滴)
DASH_TIME = 0.6         # 長音/長亮 (答)
SYMBOL_SPACE = 0.2      # 符號間的停頓 (靜音/暗)
LETTER_SPACE = 0.6      # 字母間的停頓
WORD_SPACE = 2.0        # 一組 SOS 打完後的停頓

def signal(duration):
    """同時控制蜂鳴器發聲與 LED 亮起指定時間"""
    voice.start(50)                    # 蜂鳴器發聲
    GPIO.output(LED_PIN, GPIO.HIGH)    # LED 亮起 (HIGH 代表通電)
    
    time.sleep(duration)               # 持續維持動作
    
    voice.stop()                       # 蜂鳴器停止
    GPIO.output(LED_PIN, GPIO.LOW)     # LED 熄滅 (LOW 代表斷電)
    
    time.sleep(SYMBOL_SPACE)           # 符號間的停頓

try:
    print("開始發送 SOS 訊號... (按 Ctrl+C 停止)")
    
    # 確保一開始燈是暗的
    GPIO.output(LED_PIN, GPIO.LOW)

    while True:
        # --- S: 3 短 ---
        for _ in range(3):
            signal(DOT_TIME)
        time.sleep(LETTER_SPACE - SYMBOL_SPACE)

        # --- O: 3 長 ---
        for _ in range(3):
            signal(DASH_TIME)
        time.sleep(LETTER_SPACE - SYMBOL_SPACE)

        # --- S: 3 短 ---
        for _ in range(3):
            signal(DOT_TIME)
        
        # 完整 SOS 結束，等待 2 秒後重複
        time.sleep(WORD_SPACE)

except KeyboardInterrupt:
    print("\n程式已手動停止")
finally:
    # 程式結束時的安全清理
    voice.stop()
    GPIO.output(LED_PIN, GPIO.LOW)  # 確保離開程式時燈泡不會一直亮著
    GPIO.cleanup()