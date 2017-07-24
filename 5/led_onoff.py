# ライブラリの読み込み
import iothub_client
import time
from iothub_client import IoTHubClient, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubError
from iothub_client import IoTHubMessageDispositionResult
import RPi.GPIO as GPIO

# Azure IoTHubに接続するためのプロトコル HTTPやMQTTなど MQTTのほうがセンサー値などを送るのには向いている
PROTOCOL = IoTHubTransportProvider.MQTT
# メッセージを送信する時のタイムアウト時間[ms]
MESSAGE_TIMEOUT = 10000
# Device Explorerで確認した接続文字列
CONNECTION_STRING = "<接続文字列>"

# メッセージを受信したときに呼び出されるコールバック関数
def receive_message_callback(message, user_context):
    # 受信したメッセージを文字列に変換
    message_text = message.get_bytearray().decode('utf-8')

    # LEDの点灯、消灯処理
    # ON, OFF以外は無視する
    if message_text == "ON":
        GPIO.output(2, 1)
    elif message_text == "OFF":
        GPIO.output(2, 0)

    # 処理した場合はACCEPTEDを返す
    return IoTHubMessageDispositionResult.ACCEPTED

# 初期化関係の関数
def iothub_client_init():
    from iothub_client_cert import CERTIFICATES
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    client.set_option("TrustedCerts", CERTIFICATES)
    client.set_option("logtrace", 0)
    # メッセージを受信したときにの処理を登録
    # 第二引数はコールバック関数のuser_contextに渡される
    client.set_message_callback(receive_message_callback, 0)
    return client

# GPIO初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
# 初期状態はLEDOFF
GPIO.output(2, 0)

client = iothub_client_init()
print("RUN")
try: # 例外処理
    while True:
        time.sleep(10) # 10秒待つ
except: # 例外が発生したら終了
    import traceback
    traceback.print_exc() #例外情報を出力
    print("EXIT")
