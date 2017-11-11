# 環境構築用
このフォルダーはハンズオン用に環境構築を行った手順及びコンパイル済みのライブラリなどを配置しています。

## 環境構築手順
RaspbianをダウンロードしSDカードに展開する

SSHを利用できるようにブートパーティションにsshという名前のからファイルを作成する

RaspberruPiを起動しSSHで接続する(ユーザー:pi パスワード:raspberry)

ホスト名変更
```
sudo raspi-config
```
から変更できる

パッケージをインストール
```
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudp apt-get update
sudo apt-get install python3 python3-pip git libboost-python-dev nodejs
sudo pip3 install --upgrade pip
sudo pip3 install jupyter rpi.gpio
sudo npm install -g iothub-explorer
```

I2Cの設定
sudo raspi-config
からInterface->I2CでEnableにする
再起動後
```
sudo apt-get install python3-smbus
```


Jupyter Notebookの初期設定
```
sudo python3 -m IPython kernelspec install-self
jupyter notebook --generate-config
```

パスワード生成
パスワードはmspjpにしてください
```
python3 -c 'from notebook.auth import passwd;print(passwd())'
```

出力されたshaをメモしてください。

表示されたコンフィグファイルを以下のように編集する
```
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.password = 'sha1:56531de49faa:bc140dd230ba1913ce5768371acece59d190d3dc'

```

jupyter 自動起動スクリプト
[参考](http://qiita.com/taka4sato/items/2c3397ff34c440044978)

```
sudo touch /start_jupyter.sh
sudo chmod 777 /start_jupyter.sh
sudo cat "/usr/local/bin/jupyter notebook" > /start_jupyter.sh
```

/etc/rc.local
```
su - pi /start_jupyter.sh &
exit 0
```

再起動後jupyter notebookにアクセスできることを確認してください。
最後にライブラリなどをホームに展開したら完了です。


# ビルド済みSDK及びライブラリファイルについて
Microsoft Azure IoT SDKs
Copyright (c) Microsoft Corporation
All rights reserved.
MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the ""Software""), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
