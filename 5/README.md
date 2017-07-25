#5 クラウドからデバイスを制御
この章ではAzureIoTHub側からメッセージを受け取りデバイス側でLEDを光らせます。

## Azure IoTHubからメッセージを受け取る
クラウドから送信されたメッセージを受信するには受信用のコールバック関数を用意し、AzureIoTHubクライアントのインスタンスに登録します。

以下にコールバック関数と修正したiothub_client_init関数を示します。

```python
# 追加でライブラリ読み込み
from iothub_client import IoTHubMessageDispositionResult

# メッセージを受信したときに呼び出されるコールバック関数
def receive_message_callback(message, user_context):
    # 受信したメッセージを文字列に変換
    message_text = message.get_bytearray().decode('utf-8')

    # 受信したメッセージに応じて何か処理をする
    # ここではお試しに標準出力にメッセージを出力する
    print(message_text)

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

```

また、今回はメッセージを受信して処理を行うため送信処理は削除します。
```python
client = iothub_client_init()
try: # 例外処理
    while True:
        time.sleep(10) # 10秒待つ
except: # 例外が発生したら終了
    import traceback
    traceback.print_exc() #例外情報を出力
    print("EXIT")
```

この受信したメッセージを表示するサンプルプログラムはreceive.pyで添付します。

このプログラムを実行したあと、iothub-explorerで

```
iothub-explorer send <ここにデバイスのIDを入れてください> <ここにメッセージを入れてください> --login "<ここにサービス用の接続文字列を入れてください>"
```
のようにメッセージを送信するとコールバック関数が呼び出され、Jupyter上の出力に送信したメッセージが表示されると思います。

## [演習]メッセージを受け取ってLEDを光らせる
1章を参考にONというメッセージを受け取ったらLEDを光らせ、OFFというメッセージを受け取ったらLEDを消すプログラムを作成してみてください。

GPIO2にLEDを接続した場合で実装したコードはled_onoff.pyです。
