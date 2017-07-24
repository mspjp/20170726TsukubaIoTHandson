# ライブラリの読み込み
import time
import iothub_client
from iothub_client import IoTHubClient, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubError
import RPi.GPIO as GPIO

PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
# Device Explorerで確認した接続文字列
CONNECTION_STRING = "<接続文字列>"

# 初期化関係の関数
def iothub_client_init():
    from iothub_client_cert import CERTIFICATES
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    client.set_option("TrustedCerts", CERTIFICATES)
    client.set_option("logtrace", 0)
    return client

def send_confirmation_callback(message, result, user_context):
    print(user_context)
    print("Result" + str(result))

counter = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# ボタンの状態を示す変数 押されている場合True
button_status = False
client = iothub_client_init()
print("RUN")
try:
    while True:
        time.sleep(0.1)
        if not button_status and  GPIO.input(5):
            msg = "count:" + str(counter)
            message = IoTHubMessage(msg)
            client.send_event_async(message, send_confirmation_callback, msg)
            counter += 1

        button_status = GPIO.input(5)

except: # 例外が発生したら終了
    import traceback
    traceback.print_exc() #例外情報を出力
    print("EXIT")
