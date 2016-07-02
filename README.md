# Calendar Converter

## Summary
webサイト作成の見づらいカレンダーを.csv等のGoogleカレンダーなどで読み込める形式に変換します。  
各webサイトのhtml形式にとても依存するため、他のサイトへの転用は難しいと思います。

Linux, Python3での動作確認、開発をしています。

  * nit-tsuyama/
    - [津山工業高等専門学校 行事予定](http://www.tsuyama-ct.ac.jp/honkou/annai/gyouji.htm)の変換

## Require
* Python3
  - sys
  - requests
  - zenhan
  - calendar
* 変換元Webページ
  - [津山工業高等専門学校 行事予定](http://www.tsuyama-ct.ac.jp/honkou/annai/gyouji.htm)

## Usage
1.　以下コマンドを入力します。  
※コマンドは環境によって変わる可能性があります。Python3用のコマンドを実行してください。  
※pip3は環境によってsudo権限を付与して実行してください。
```
$ cd (ダウンロード先)/calconv/(必要なカレンダーのディレクトリ(nit-tsuyama等))
$ pip3 install -r requirements.txt
$ python3 calconv.py
(変換する行事予定の西暦を年度表記で入力)
```
2.　カレントディレクトリにschedule.csvが生成されます。  
3.　各カレンダーの形式への変換は、schedule.csvの変換(Google Calendar等)で対応してください。

## Author
* [rikyuusima](https://github.com/rikyuusima)
  - nit-tsuyama/

## License
ソースコードは[MIT License](./LICENSE.txt)で提供します。  
ダウンロードしたWebサイトはサイトの表記に従ってください(現状のソースではダウンロードしたサイトのソースは処理後、削除されます)。
