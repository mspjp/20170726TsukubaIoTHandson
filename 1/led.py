import RPi.GPIO as GPIO # ライブラリの読み込み
import time             # sleepを呼ぶためtimeライブラリを読み込み

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 状態を示す変数 Falseで消灯、Trueで点灯
led_status = False
# ボタンの状態を示す変数 押されている場合True
button_status = False

print("start")
try:
    while True:
        time.sleep(0.1)
        if not button_status and  GPIO.input(5):
            led_status = not led_status
            GPIO.output(2, led_status)
        button_status = GPIO.input(5)
finally:
    print("end")
    GPIO.cleanup()
