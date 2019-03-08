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
