## 参照記事
[ここ](https://uepon.hatenadiary.com/entry/2018/03/21/180329)参考にしました。

### 1. google-drive-ocamlfuseのインストール
* GoogleDrive を ローカルの Ubuntu にマウントするパッケージのインストール方法
```
# 1.1 google-drive-ocamlfuseのインストール
# Install a Drive FUSE wrapper.
# https://github.com/astrada/google-drive-ocamlfuse

!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse

print('done.')
```

### 2. Colabratory用の認証トークンの生成
* 下記サンプルに従い設定
* 途中、URLが出てきたらクリック
* 関連付けるgoogleアカウントを指定し、画面が更に切り替わったら「許可」を押すとコードが出てくる
* colabの実行画面に四角の枠が出てくるので、そのコードをコピペして完了
```
# 2 Colabratory用の認証トークンの生成
# Generate auth tokens for Colab
from google.colab import auth
auth.authenticate_user()

print('done.')
```

### 3. Drive FUSE library用の証明書の生成
* 2. とは別のコードだが、作業内容は同じ。
```
# 3. Drive FUSE library用の証明書の生成
# Generate creds for the Drive FUSE library.
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}

print('done.')
```

### 4. インスタンスにdriveというディレクトリを作り、そこにGoogle Driveをマウントする
* マウント先（googleDrive）にすでにファイルが存在するとエラーがでるので注意
* オプションで「空じゃない」って指定すると、めでたくマウントできました
* 以下の -o 以降が指定のオプションです
* `!google-drive-ocamlfuse drive/ -o nonempty`
* lsコマンドで確認
* 自分の使っているファイルが見えていれば、マウントOK
```
# 4. インスタンスにdriveというディレクトリを作り、そこにGoogle Driveをマウントする
# Create a directory and mount Google Drive using that directory.
!mkdir -p drive
!google-drive-ocamlfuse drive/ -o nonempty

print('Files in Drive:')
!ls drive/
```

### 5. その他注意事項
* 別ファイルでも上記を一度実行しておけば、2.3からでOK ー＞要確認。
* マウントはインスタンスの永続限界時間である12時間を超えるとインスタンスが初期化されるためマウントも解除される
* だが、ファイルが削除されるわけではない
* 再度インスタンスの接続を行ったらマウント処理を行うことを忘れないこと
* アイドル状態が90分続くと停止するが、12時間を超えていなければ大丈夫？？？
