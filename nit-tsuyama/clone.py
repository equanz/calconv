# !/usr/bin/env python
# coding: utf-8

import requests

URL = "http://www.tsuyama-ct.ac.jp/honkou/annai/gyouji.htm"
# カレンダーで読み込み可能にする為の.csv用ヘッダ
CSV_HEAD = 'Subject,Start Date,End Date,All Day Event\n'
# Requests オブジェクト
r = requests.get(URL)
# ISO-8859-1のエンコーディングを変更(半ギレ
if r.encoding == 'ISO-8859-1':
    r.encoding = 'Shift_JIS'

f = open('./gyouji.html', 'w')
# r.textの文字コードはutf-8になる
f.write(r.text)
r = None
f.close()

f = open('./gyouji.html', 'r')
# ファイルから一行ごとリストに読み出し
lines = f.readlines()
f.close()

i = 0
for line in lines:
    lines[i] = line.strip()
    i = i + 1

print(lines)

# GitHubにアップする際のWebサイトソース削除
f = open('./gyouji.html', 'w')
f.write('')
f.close()
