# OpenCVのビルド法
## 1. 動機
* 今のPCで C++でOpenCVを使いたくなった
  * Python環境では、最新の4.1を使ってます。（pipによるバージョン管理もできて楽だなぁ）
    * ちょっとしたことを試すなら、Pythonでも良いかと。
  * やりたいことがあって、パフォーマンスを要するのと、書き慣れたC++で素早く書きたくなったため。
* インストール手順を残したい
  * 現状、開発マシンにはC++版は2.4.11 が入ってるが、どうやって入れたのかは不明。
  * 手順を残しておけば…。手順を残すのも動機の1つ。
* 4.1がリリースされた今、2.系を使い続けるのもね。
* ということで、バージョンアップに踏み切る決心を付けました。
* 結果を先に言うと、4.1狙ったがビルドできず、3.4.6を入れました。

## 2. 開発環境
* OS:Ubuntu 18.04 LTS

## 3. 手順
### 3.1 概要
* 現状の2.4.11のアンインストール
* 最新版ソースをgitから落とす
* ビルド、インストール
* 最後は動作確認で閉める
* 参考サイト
  * [1][OpenCVの本当に動くインストール手順](https://qiita.com/usk81/items/98e54e2463e9d8a11415)
  * [2][OpenCVの入れ直し](http://ssr-yuki.hatenablog.com/entry/2018/05/14/022802)
  * [3][OpenCV (安定版)を入れてみた](http://ssr-yuki.hatenablog.com/entry/2018/04/30/041414)
  * [2]と[3]は同じ人のブログで、[3]をやった後に入れ直しの記録を[2]として残しているもよう。

### 3.2 古いバージョンの削除
* 正直、正しいやり方がわからない…。
* [2]を参考に、手作業でファイルを消していった。
* 最初に調査として、ライブラリ等がどこに入っているかを調べた

|ディレクトリ|ファイル|説明|
|--|--|--|
|/usr/lib|libopencv_**.so|ライブラリファイル|
|/usr/include/opencv, /opencv2|*.h, *.hpp|ヘッダファイル|
|/usr/lib/pkg-config|opencv.pc|pkg-config|

* OpenCV関連のファイルをrmコマンドを使って、とことん消した。
* cmakeとかmakeをしたopencv/build/の中で、下記コマンドでもいいらしい
```
$ sudo make uninstall
```
* が、いかんせん今のバージョンのビルドの記憶がないので…。
* このあたりは[3]を参考にしました。

### 3.4 ビルドに必要なパッケージの準備
* [1]の方だと、以下が必要となってた。
```
apt-get -y install build-essential checkinstall cmake unzip pkg-config yasm
apt-get -y install git gfortran python3-dev
apt-get -y install libjpeg8-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libxine2-dev libv4l-dev
apt-get -y install libjpeg-dev libpng-dev libtiff-dev libtbb-dev
apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libatlas-base-dev libxvidcore-dev libx264-dev libgtk-3-dev
```
* [2]の方では、下記のみ。
```
$ sudo apt-get install build-essential
$ sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
```
* だいたい、[2]を包含している[1]を実行した。ちなみに[1]は先に、`sudo su -` してます。
* ただし、libjasper-dev が見つからないと言ってきた。JPEG2000のRead/Writeに必要らしいが、使わないので無視した。
* また、libpng12-dev これも見つからないと言ってきた。`sudo apt-get install libpng-dev` とすればインストールできるかもだが、やってません。

### 3.3 ダウンロード
* [OpenCVのReleaseページ](https://opencv.org/releases/)にアクセス、ダウンロード
* Github ボタンを押せば、githubサイトに飛びます。
  * git clone でもいいんだけど、タグの設定方が分からぬ。タブを指定して、zipで落としました。
  * opencvは[ここ](https://github.com/opencv/opencv/tree/4.1.0)
  * opencv_contribは[ここ](https://github.com/opencv/opencv_contrib/tree/4.1.0)
* ダウンロード先
  * [1]だと、`/usr/local/src` に置くように言っていますが、決まりはないようです。
  * 実際、ここにダウンロードしたが、ビルドすると5GB程度に膨れ上がり、自分のPCでは、ストレージ残量の問題でビルド中断となった…
  * なので、自分はSDカード（/media）に置きました

### 3.4 インストール
* 解凍
  * unzipで
* cmake の準備
  * 解凍した `/opencv` に移動し`mkdir build`で、ビルド用のディレクトリを作り、そこに移動します。`cd build`
* cmake
  * `/build` 内で下記コマンドを打つ
  * `cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_V4L=OFF ..`
  * 上記で`/usr/local`にビルド生成物が作られます
  * 今回は、[1][2]でも書いてあるような、contribのビルドはパスしました。
  * 詳しくはここの[issue](https://github.com/opencv/opencv/issues/6262)が参考になります。
  * そういえば、`sys/videoio.h not found` って出たので、[ここ](https://qiita.com/_-_-_-_-_/items/8131b1b2ddaef6b0d18d)も参考にしてた。
* make
  * `/build`のままで、`make -j4`でmakeします。そこそこに時間がかかったような。
  * オプションの意味は[こちら](https://linuxjm.osdn.jp/html/GNU_make/man1/make.1.html)
  * 同時に実行できる jobs (コマンド) の数を指定する。 -j オプションが複数個指定された場合は、最後の指定が有効になる。引き数無しで -j オプションが与えられた場合、 make は同時に実行できるジョブの数を制限しない。
* インストール
  * `sudo make install`で実行。
  * 意味合いとしては、makeしたファイル群をディレクトリにコピーするってことです。
* configファイルの設定
  * この作業、よく分かってないが…[1]に書いてあった。
```
echo /usr/local/lib > /etc/ld.so.conf.d/opencv.conf
ldconfig -v
```

### 3.5 動作確認
* バージョン確認
  * `opencv_version` と打つと `3.4.6` って出たよ。
  * これ、`which opencv_version` とすると、`/usr/local/bin/opencv_version` と出てっきた。インストールされてたのね。
  * `$ pkg-config --modversion opencv`これでも確認できます。
* サンプルコードで確認
  * そういえば、[2]では、~/.bashrcでPATHを通すように書いてあったがやってないな
  * [pkg-configを使ってOpenCVをコンパイルしてみる](https://blog.monophile.net/posts/20131106_pkgconfig.html)という記事を参考にして作ったMakefileが以下のリンクになります。
  * [自分のTIL](https://github.com/pokabu55/TIL/blob/master/make/OpenCV%E3%81%AEMakefile.md)
  * Makefileは[こちら](https://github.com/pokabu55/TIL/blob/master/make/Makefile)

## 4. おわりに
* 以上で終わりです。
* まだ、修正必要な部分があるかもだが、一旦閉じます。

## 5. 再ビルド
### 動機
* OpenCVでWebカメラが使えないため
* 調べてみると、ビルド時にV4LをONにしなかったため？
* 現象としては
  * isopened関数で毎度falseを返す
  * PYTHONコードではカメラを認識する
  * ということで、ハード的な問題もなく、C++環境に問題ありと判断
  ### アンインストール
  * 3.2章に倣い、uninstall をやってみる
  * 自分のPCだと、SDのopencv ディレクトリのbuild に行って、
  * `sudo make uninstall` を実行
  * これで、so とか hpp が消された模様
  * 後は残党を消す
  * OpenCVは、/usr/locl/lib, /usr/locl/include に配置されたっぽい
  * 上記 uninstall 後に、soは消えたが、inlucdeの方に /opencv, /opencv2 が残っていたので、まるっと rm した
  
  ### ビルド
  * SDカードの以前、OpenCV を入れたフォルダに移動
  * opencv3411/ となっていたので、そこで、Opencv と contrib のディレクトを削除
  * 後は、3.4 章に従うが、ここで、`V4L=ON` とした
  * 3.5 章の確認まで問題なくできたことを確認した
 
  ### ダメだった
  * カメラを動かそうとすると、libgtk2.0-dev をインストールして、makeし直せっていうエラーメッセージが…。
  * `sudo apt-get install libgtk2.0-dev` を実行した
  * 後は、先の手順でアンインストールし、やり直し。
