# Getting Started With Jetson Xavier NX Developer Kit

## 1. イメージファイルのダウンロード (コンピュータを用いる)
* 以下からイメージファイル (Jetson Xavier NX Developer Kit SD Card Image) をコンピュータにダウンロードする

<https://developer.nvidia.com/jetson-nx-developer-kit-sd-card-image>

## 2. microSDカードに書き込み (コンピュータを用いる)
* この時点ではmicroSDカードをコンピュータへ挿入しない
* ターミナルを起動し，コンピュータへ既に挿入されている外部デバイスを調べる

```
diskutil list external | fgrep '/dev/disk'
```

* microSDカードをコンピュータへ挿入する．読み取りのエラー画面が表示された場合は無視する
* 再び外部デバイスを調べ，microSDカードのデバイス名を確認する (e.g.; /dev/disk2)

```
diskutil list external | fgrep '/dev/disk'
```

* microSDカードのパーティションを消去する．正しいデバイス名 (disk\<n>) を指定しているか注意する

```
sudo diskutil partitionDisk /dev/disk<n> 1 GPT "Free Space" "%noformat%" 100%
```

* 圧縮されたイメージファイルを解凍してmicroSDカードに書き込む．このとき，デバイス名を /dev/disk ではなく /dev/rdisk としてアクセスする

```
/usr/bin/unzip -p ~/Downloads/jetson-nx-jp451-sd-card-image.zip | sudo /bin/dd of=/dev/rdisk2 bs=1m
```

* 書き込みが完了した後，読み取りのエラー画面が表示されるが無視する

## 3. Jetsonの起動

* microSDカードをJetsonのスロット (本体の下側) へ挿入
* ディスプレイの電源を入れ，Jetsonへ接続
* キーボードおよびマウスをJetsonへ接続
* 電源ケーブルををJetsonへ接続．Jetsonの電源が入り，自動的に起動する


## 4. Jetsonの初期設定
Jetsonの電源が入るとMicro-USBコネクターの隣にある緑色のLEDが点灯する．ウィザードに従って初期設定を行う

