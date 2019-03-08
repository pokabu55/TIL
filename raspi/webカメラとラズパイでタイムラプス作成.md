### 1. モチベーション
* ラズパイとwebカメラを使ってタイムラプス動画を作りたい
* 当初は、Pythonによる画像取得を考えていたが、せっかくなのでCRONでやってみた
* とりあえず、窓に向かってwebカメラを固定し、空を撮影
* 流れ行く雲を撮ってみたかった…できれば夕焼けとか

### 2. 準備物
* ラズパイ3b：[OpenCV3.1](https://qiita.com/mt08/items/e8e8e728cf106ac83218)を予めインストール
* webカメラ [logicool C270](https://www.amazon.co.jp/LOGICOOL-%E3%82%A6%E3%82%A7%E3%83%96%E3%82%AB%E3%83%A0-HD%E7%94%BB%E8%B3%AA-120%E4%B8%87%E7%94%BB%E7%B4%A0-C270/dp/B003YUB660)

### 3. 仕様
* ラズパイに接続されたwebカメラで定期的に画像を保存
* 定期的な撮影はcronを使って実施
* 適当に撮影時間を決め、後から撮りためた画像を動画としてつなげる

### 4. webカメラによる定期的な撮影
#### 4.1 cronの設定
* 定期的な撮影はcronを使って実施した
* cronの解説とか設定法は[こちら](http://www.tapun.net/raspi/raspberry-pi-cron-settings)を参照。滅茶詳しいです!!
* 定期的撮影の設定の概要
  * 何時から何時まで、何分おきにに撮影するって具合にcron設定を書く
  * 「撮影する」は、webカメラの画像をJpeg保存するっていう、シェルスクリプトで実施する
* cronの書き方
  * `$ crontab -e`とコマンドを打つとnanoエディタでのcronの設定が開く
  * 設定項目は左から「分」「時」「日」「月」「曜日」「実行内容」とする。
  * ここでは、指定の時間（４〜１９時）を1分おきに撮影したかったので、下記のように書いた
  ```
  */1 4-19 * * * /home/pi/camera.sh
  ```
* webカメラでjpeg保存するシェル
  * ファイル名は、上記のcronで設定した `camera.sh` とする
  * [この記事](https://qiita.com/ikemura23/items/4f949d47489e6c5ff6a2)を参考に以下のように書いた
  ```
  fswebcam -D 2 -r 1280x960 --jpeg 60 /home/pi/work/picture/`date +%Y%m%d%H%M%S`.jpg
  ```
  * fswebcamについては、[ここ](http://seesaawiki.jp/w/renkin3q/d/Linux/fswebcam)を参考にした
    * `-D, --delay <number>         Sets the pre-capture delay time. (seconds)`
    * `-r, --resolution <size>      Sets the capture resolution.`
    * `--jpeg <factor>              Outputs a JPEG image. (-1, 0 - 95)`
  * `--jpeg 60` のパラメータの検討。jpegの圧縮率?画質？
    * 数字を小さくするとファイルサイズが小さくなってるのを確認した。30とか、劣化がやば過ぎ
    * 値を入れ替え試して検証して、サイズ1280x960で、ファイルサイズが50kB位になるように調整した結果が、60です。
    * 画質が高すぎると、ファイルサイズが大きくなり、また保存に時間がかかってフレーム落ちが出たので調整した
   
#### 4.2 いざ撮影
* webカメラを窓の外に向けて固定
* 前日の夜のうちにラズパイを起動させ、後はカメラが動かないことを祈るのみ
* もちろん、明るい時にカメラの方向などの確認をお忘れなく

### 5. タイムラプス動画の作成
* ラズパイに保存されたjpeg画像をPython＋OpenCVで動画に変換した
* 下記にサンプルコードを示す
* 仕上がりがfpsは雲の流れ方や、ファイルサイズが変わるので、適宜調整して決めればよい

### 6. タイムラプス動画のサンプル
* [サンプル１](https://twitter.com/okakim55/status/1039124760242704384?s=20)
* [サンプル２](https://twitter.com/okakim55/status/1038781525955829760?s=20)
* [月の移動から夜明け](https://twitter.com/okakim55/status/1033863759540801537?s=20)
* [途中から雨](https://twitter.com/okakim55/status/1039124760242704384?s=20)

<pre class=“prettyprint linenums:”>
# -*- coding: utf-8 -*-
# 所定のディレクトリの画像から、動画を作るサンプルコード

import cv2
import glob

# 保存先のディレクトリからファイル名を取得
fileName = glob.glob("./picture/*.jpg")
# 念の為、ソート
fileName.sort()

#print(fileName)

# コーデックの種類
codecs = 'H264'
# fps、雲の流れる速度が変わるので、そこそこ重要かも
fps = 15
# 動画のサイズ
imgW = 1280
imgH = 960

fourcc = cv2.VideoWriter_fourcc(*codecs)
# 保存ファイル名とパラメータの指定
video = cv2.VideoWriter('timeLapseSky_20fps_full.mp4', fourcc, fps, (imgW, imgH))

for fn in fileName:
	print(fn)
	img = cv2.imread(fn)
	img = cv2.resize(img, (imgW, imgH))
	video.write(img)

video.release()
</pre>
