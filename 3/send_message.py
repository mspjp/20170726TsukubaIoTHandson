# ライブラリの読み込み
import time #sleepを使うので追加でインポート
import iothub_client
from iothub_client import IoTHubClient, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubError

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

# 送信した回数を保持するカウンター
counter = 0
# クライアントのインスタンスを作成
client = iothub_client_init()
try: # 例外処理
    while True:
        msg = "count:" + str(counter) # カウンターを文字列に変換して文字列と結合しメッセージの中身を作る
        message = IoTHubMessage(msg) # 文字列からIoTHubのメッセージを作成

        # 実際に送信 送信には時間がかかるのでコールバック関数をわたし結果を受け取る
        # 第三引数はコールバック関数のuser_contextに渡される
        client.send_event_async(message, send_confirmation_callback, msg)

        counter += 1 # カウンターインクリメント
        time.sleep(10) # 10秒待つ

except: # 例外が発生したら終了
    import traceback
    traceback.print_exc() #例外情報を出力
    print("EXIT")
