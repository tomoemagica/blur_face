# blur_face

blur_face
 
ダウンロード

workspaceにblur_face.pyとblur_faceフォルダとその中身のファイルを置きます

使用方法

workspaceでコマンドプロンプトで実行

py blur_face (-t blur_threshold(float))

py blur_face.py

py blur_face.py -t 50.0

など

-t 50.0の数値が大きいほど、blur判定、ボケた画像の扱いが厳しくなります

指定しなかった時のデフォルトは40.0です


機能

data_src\alignedの下に、

no_face(顔が検出できなかった)、not_blur(顔がピンボケや手ブレしていない)、blur(顔がピンボケや手ブレしている)

3つのフォルダを作成して、それぞれ判定した顔画像をdata_src\alignedから移動します

100％ではありません。blurフォルダにもDFLの学習として使用できそうな顔が残ります

not_blurフォルダにも、ジャギーなどで、DFLの学習として使用できなさそうな顔が残ります

no_faceフォルダは、DFLの顔抽出とは違う物を使用しているので、本プログラムでは顔が検出できなかっただけです

DFLとしては顔を検出できている画像も含みます

後で手動で移動等が必要です
