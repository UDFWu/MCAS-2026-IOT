
import serial
import time

# 設定 UART 連接埠與參數
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

# 傳送資料
def send_data(data):
    if ser.is_open:
        ser.write(data.encode('utf-8'))
        print(f"已傳送：{data.strip()}")

# 接收資料
def receive_data():
    if ser.is_open:
        incoming = ser.readline().decode('utf-8').strip()
        if incoming:
            print(f"收到資料：{incoming}")
        return incoming

# 主程式
try:
    print("UART 自傳自收測試開始")
    print("按 Ctrl+C 可以停止程式")

    while True:
        data = input("請輸入數字或字元：")

        send_data(data + "\n")

        time.sleep(0.1)

        receive_data()

        time.sleep(1)

except KeyboardInterrupt:
    print("\n程式中斷")

finally:
    if ser.is_open:
        ser.close()
        print("串列埠已關閉")
