# Calendar Converter

[![Build Status](https://travis-ci.org/equanz/calconv.svg?branch=master)](https://travis-ci.org/equanz/calconv)  
[![CircleCI](https://circleci.com/gh/equanz/calconv.svg?style=svg)](https://circleci.com/gh/equanz/calconv)

## Summary
webサイト作成の見づらいカレンダーを.csv等のGoogleカレンダーなどで読み込める形式に変換します。  
各webサイトのhtml形式にとても依存するため，他のサイトへの転用は難しいと思います。

Linux, Python3での動作確認，開発をしています。

* nit-tsuyama/
  - [行事予定｜津山工業高等専門学校](http://www.tsuyama-ct.ac.jp/gyoujiVer4/gyouji.html)の変換

## Require
* Python3
  - sys
  - requests
  - zenhan
  - calendar
* 変換元Webページ
  - [行事予定｜津山工業高等専門学校](http://www.tsuyama-ct.ac.jp/gyoujiVer4/gyouji.html)

## Usage
1.以下コマンドを入力します。  
※コマンドは環境によって変わる可能性があります。Python3用のコマンドを実行してください。  
※pip3は環境によってsudo権限を付与して実行してください。
```
$ cd (ダウンロード先)/calconv
$ pip3 install -r requirements.txt
$ python3 -m (必要なカレンダーのディレクトリ(nit-tsuyama等)).calconv ...
```
2.カレントディレクトリにschedule.csvが生成されます。  
3.各カレンダーの形式への変換は，schedule.csvの変換(Google Calendar等)で対応してください。

## Author
* [equanz](https://github.com/equanz)
  - nit-tsuyama/

## License
ソースコードは[MIT License](./LICENSE.txt)で提供します。  
ダウンロードしたWebサイトはサイトの表記に従ってください(現在はダウンロードしたサイトのソースは処理後，削除されます)。
