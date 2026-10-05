import time
import tm1637
from datetime import datetime

# 依據函式庫要求，這裡填寫 BCM 腳位編號
CLK = 23  # 對應實體第 16 腳
DIO = 24  # 對應實體第 18 腳

# 初始化顯示器物件
display = tm1637.TM1637(clk=CLK, dio=DIO)
display.brightness(2)  # 設定亮度 (範圍 0~7)

try:
    print("啟動時鐘... (按 Ctrl+C 停止)")
    
    while True:
        # 取得現在的系統時間
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        
        # 判斷當前秒數是單數還是雙數 (用來控制冒號閃爍)
        # 單數秒時為 True (亮起)，雙數秒時為 False (熄滅)
        show_colon = (now.second % 2 == 0)
        
        # 將時間顯示到七段顯示器上
        # 參數依序為：小時、分鐘、是否顯示中間冒號
        display.numbers(hour, minute, colon=show_colon)
        
        # 暫停 0.5 秒再更新一次，以確保能精準捕捉到每一秒的變化
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n時鐘已停止")
finally:
    # 離開程式時清除螢幕，避免殘留數字
    display.write([0, 0, 0, 0])