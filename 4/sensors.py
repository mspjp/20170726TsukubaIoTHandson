# ライブラリの読み込み
import time #sleepを使うので追加でインポート
import iothub_client
from iothub_client import IoTHubClient, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubError
import smbus
import json


# Azure IoTHubに接続するためのプロトコル HTTPやMQTTなど MQTTのほうがセンサー値などを送るのには向いている
PROTOCOL = IoTHubTransportProvider.MQTT
# メッセージを送信する時のタイムアウト時間[ms]
MESSAGE_TIMEOUT = 10000
# Device Explorerで確認した接続文字列
CONNECTION_STRING = "<接続文字列>"

# 初期化関係の関数
# この関数を呼ぶと初期化済みのIoTHubのクライアントクラスのインスタンスを返す
def iothub_client_init():
    from iothub_client_cert import CERTIFICATES
    # 指定した接続文字列とプロトコルでクライアントを作成
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    # タイムアウト時間を指定
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    # 一部の環境では証明書情報が必要なので設定
    client.set_option("TrustedCerts", CERTIFICATES)
    # MQTTのログ機能を無効化
    client.set_option("logtrace", 0)
    return client

# 送信後に呼び出されるコールバック
def send_confirmation_callback(message, result, user_context):
    print(user_context)
    print("Result" + str(result))

# クライアントのインスタンスを作成
client = iothub_client_init()
# I2Cを読み書きするクラスの初期化 (デバイス1で初期化します RaspiはI2Cは1系統だけなので余り意味はありませんが)
bus = smbus.SMBus(1)
print("RUN")

try: # 例外処理
    while True:

        # アドレス0x40のデバイス（＝温湿度センサー）にコマンド0xF5(湿度計測要求)を送信
        bus.write_byte(0x40, 0xF5)

        # 計測が終わるまで少し待つ
        time.sleep(0.2)

        # アドレス0x40のデバイスから2バイト読み込みを要求する
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)
        # センサー値はMSB LSBの順で送られてくるので16bitのデータに構成し直す
        raw_value = (data0 << 8) | data1
        # 湿度に変換
        humidity = (125 * raw_value / 65536) - 6

        # 温度読み出し要求を送信
        bus.write_byte(0x40, 0xF3)

        time.sleep(0.2) #計測完了待ち

        # 2バイト読み出しとデータの構成
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)
        raw_value = (data0 << 8) | data1

        # 温度に変換
        temperature = (175.72 * raw_value / 65536) - 46.85

        # センサー値をKeyValueに
        data = {"humd": humidity, "temp": temperature}
        # KeyValueからjson文字列へ
        msg = json.dumps(data)
        message = IoTHubMessage(msg) # 文字列からIoTHubのメッセージを作成

        # 実際に送信 送信には時間がかかるのでコールバック関数をわたし結果を受け取る
        # 第三引数はコールバック関数のuser_contextに渡される
        client.send_event_async(message, send_confirmation_callback, msg)

        time.sleep(10) # 10秒待つ

except: # 例外が発生したら終了
    import traceback
    traceback.print_exc() #例外情報を出力
    print("EXIT")
