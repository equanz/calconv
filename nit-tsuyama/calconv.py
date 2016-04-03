# !/usr/bin/env python
# coding: utf-8

import requests

# 津山工業高等専門学校 行事予定 URL(2016/04/03現在)
# まあURL変わるようだったら入力制にするかも
# (2016/04/03現在)サイトはShift-JIS(半ギレ
url = "http://www.tsuyama-ct.ac.jp/honkou/annai/gyouji.htm"
# Request オブジェクト
r = requests.get(url)
# ISO-8859-1のエンコーディングを変更(半ギレ
r.encoding = 'Shift_JIS'

f = open('./gyouji.html', 'w')
# r.textの文字コードはutf-8になる
f.write(r.text)
f.close()

f = open('./gyouji.html', 'r')
print(f.read())
f.close()

# GitHubにアップする際のHPソース削除
# (C)は守っておく
f = open('./gyouji.html', 'w')
f.write('')
f.close()
