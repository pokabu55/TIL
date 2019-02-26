### パッケージの確認
```
!pip list
```

### インストール
* 無かったら、インストール
```
!pip install tensorboardcolab
```

### サンプル
```
from tensorboardcolab import TensorBoardColab, TensorBoardColabCallback
tbc=TensorBoardColab()
```
* Kerasを使用していると仮定して
```
model.fit(......,callbacks=[TensorBoardColabCallback(tbc)])
```
