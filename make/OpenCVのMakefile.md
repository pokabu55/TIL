# OpenCV 用の Makefile の書き方
## ベースのMakefile
* ベースとなる Makefile は、[「シンプルで応用の効くmakefileとその解説」](http://urin.github.io/posts/2013/simple-makefile-for-clang)を参考にしました。

## OpenCVのMakefile
* [ここ](https://gist.github.com/kevinhughes27/5311609)を参考にしました。

## 出来上がった Makefile 
* 上記２つを合体させました。
```
COMPILER  = g++
CFLAGS    = -g -MMD -MP -Wall -Wextra -Winit-self -Wno-missing-field-initializers
ifeq "$(shell getconf LONG_BIT)" "64"
  LDFLAGS = `pkg-config opencv --cflags --libs`
else
  LDFLAGS =
endif
LIBS      = 
INCLUDE   = -I./include
TARGET    = ./bin/$(shell basename `readlink -f .`)
SRCDIR    = ./src
ifeq "$(strip $(SRCDIR))" ""
  SRCDIR  = .
endif
SOURCES   = $(wildcard $(SRCDIR)/*.cpp)
OBJDIR    = ./obj
ifeq "$(strip $(OBJDIR))" ""
  OBJDIR  = .
endif
OBJECTS   = $(addprefix $(OBJDIR)/, $(notdir $(SOURCES:.cpp=.o)))
DEPENDS   = $(OBJECTS:.o=.d)

$(TARGET): $(OBJECTS) $(LIBS)
	$(COMPILER) -o $@ $^ $(LDFLAGS)

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	-mkdir -p $(OBJDIR)
	$(COMPILER) $(CFLAGS) $(INCLUDE) -o $@ -c $<

all: clean $(TARGET)

clean:
	-rm -f $(OBJECTS) $(DEPENDS) $(TARGET)

-include $(DEPENDS)
```
## 注意点
* ディレクトリ構成を下記のようにしています
```
example
|-- makefile
|-- bin
|   `-- example   <- (TARGET) 実行ファイル
|-- include
|   `-- example.h
|-- obj           <- (OBJDIR) 中間ファイル生成先ディレクトリ
|   |-- example.d <- (DEPENDS) 依存関係ファイル
|   `-- example.o <- (OBJECTS) オブジェクトファイル
`-- source
    `-- example.cpp
```
