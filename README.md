# 20170726TsukubaIoTHandson
2017/7/26,2017/11/12 つくばで行うIoTハンズオン用の資料です。

## タイムテーブル

### #0 イベント概要とAzureIoTHubの説明
#### [JupyterNoteBookについて](./JupyterNoteBook.md)

### [#1 RaspberryPiで入出力を行う](./1/README.md)
* LEDの点灯
* ボタン入力
* ボタンを押すとLEDを点灯、消灯させる

### [#2 Azure IoT Hubセットアップ](./2/README.md)
* 11/12参加の方々はこの章の手続きはこちらで行っています。当日の指示に従ってください。

### [#3 Azure IoT Hubにデータを送る](./3/README.md)
* ボタンを押してクラウドにデータを送る
* 送ったデータを別の端末などから確認する

### [#4 センサー値をIoT Hubに送信する](./4/README.md)
* 温度センサーとI2Cの説明
* センサーの値を読み出すプログラム(I2C)
* センサー値をサーバーに送る
* 時間がある人は加速度も読み出してみる

### [#5 クラウドからデバイスを制御](./5/README.md)
* 外部の端末からメッセージを受け取ってコンソールに出す
* コンソールに出す代わりにLEDを点滅させる
* 時間がある人はリレーを制御し外部機器を制御する

## ファイル構成
* 1/ ~ 5/:それぞれ#1~#5の内容を格納
* setup:ビルド済みのライブラリと環境構築の手順書
* JupyterNoteBook.md: JupyterNoteBookの簡単な使い方

[アンケートはこちら](https://1drv.ms/xs/s!AluBpRRYH8E_mll3bTqxKFd6ESWt)
