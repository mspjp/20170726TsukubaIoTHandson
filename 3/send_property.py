
# ライブラリの読み込み
import json
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

# プロパティー送信後に呼ばれるコールバック
def send_reported_state_callback(status_code, user_context):
    print("status code:" + str(status_code))

# クライアントのインスタンスを作成
client = iothub_client_init()
print("RUN")

# 現在の状態をマップで用意
status_map = {"statsu":"OK", "temp":12.3}
# マップからjsonという形式に変換
json_str = json.dumps(status_map)
# 送信する（最後に引数はコールバックのuser_contextに渡される)
client.send_reported_state(json_str, len(json_str), send_reported_state_callback, 0)
