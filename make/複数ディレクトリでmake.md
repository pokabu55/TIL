### 目的
* 複数ディレクトリで構成されている場合のMakefileを作りたい！
* [ここ](http://gmaj7sus4.hatenablog.com/entry/2013/11/17/234201)を参考にしました。

### 想定するディレクトリ構成
* 構成は、以下の通り。
* subModuleA とか subModuleB とかの単体テストを想定してます。

```
.
├── Makefile
├── dirA
│   ├── inc
│   │   └── subModuleA.h
│   └── src
│       └── subModuleA.cpp
├── dirB
│   ├── inc
│   │   └── subModuleB.h
│   └── src
│       └── subModuleB.cpp
└── main.cpp
```
### Makefile のサンプル
```
GCC    = g++
CFLAGS = -O2 -MMD -Wall -Wextra
INCLUDE= -I../dirA/inc -I../dirB/inc
SRCS   = main.cpp dirA/src/subModuleA.cpp dirB/src/subModuleB.cpp
TARGET = SampleExe

OBJS   = $(SRCS:.cpp=.o)
DEPS   = $(SRCS:.cpp=.d)
TILDE  = $(SRCS:.cpp=.cpp~)

.cpp.o:
	$(GCC) $(CFLAGS) -c $< -o $@ $(INCLUDE)

$(TARGET): $(OBJS)
	$(GCC) $(CFLAGS) -o $@ $+

default: $(OBJS) $(TARGET)

clean:
	$(RM) $(OBJS) $(DEPS) $(TILDE) $(TARGET)

-include $(DEPS)
```

### 使い方
* `make` ビルドして、実行ファイル、.o、.d ファイルを生成
* `make clean` で、実行ファイル、.o、.d ファイルを削除

### 今後の課題
* ソースファイルが個々に設定されてる点について
  * ディレクトリで一括でまとめたい場合もあるし…
  * 個々で対応したい場合もあるし…
* .o, .d ファイルが、それぞれのディレクトリに入る。今後はまとめたい。
 
