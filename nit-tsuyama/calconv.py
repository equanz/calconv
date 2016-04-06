# !/usr/bin/env python
# coding: utf-8

import requests
import zenhan

""".csvに書き込む際の構造体."""
class CSV_Struct:
    def __init__(self, sub, start, end):
        self.sub = sub
        self.start = start
        self.end = end
        # 終日はTRUEとしておく
        self.ALL_DAY = "TRUE"

"""何月であるかを検出し、返す."""
def month_search(line):
    # 月の表示のテンプレート
    month_temp = ['<h3>＜', '月＞</h3>']
    # 検索方法が汚すぎる
    if month_temp[0] in line and month_temp[1] in line:
        month = int(zenhan.h2z(line.replace(month_temp[0], '').replace(month_temp[1], '')))
        return month
    # コメントアウトされた予定を除外
    elif '<!--' in line:
            # コメントアウトが一行で終わった場合の対策
            if '-->' in line:
                return -1
            else:
                return -2
    elif '-->' in line:
        return -1
    else:
        return 0

"""期間制の予定であるかを検出し、真偽を返す."""
def span_search(line):
    index = line.find('～')
    # .findで検出されない場合-1が返される
    if index != -1:
        # 2〜5年といった学年の間隔を〜記号で表しているため、その対策
        # 〜の２つ後にあるというスタイルに依存
        if line.startswith('年', index + 2):
            return -1
        # 月が変わる特殊な場合の対策
        elif line.startswith('月', index +2):
            return -2
        return 0
    else:
        return -1

#
'''
"""日付を検出し、返す."""
def date_search(line):
'''

# 津山工業高等専門学校 行事予定 URL(2016/04/03現在)
# まあURL変わるようだったら入力制にするかも
# (2016/04/03現在)サイトはShift-JIS(半ギレ
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

f = open('./schedule.csv', 'w')
# .csvにヘッダを書き込む
f.write(CSV_HEAD)
f.close()

# 4月の予定が読み込み開始されたかのフラグ
month_start_flag = False
# 予定がコメントアウト中の行にあるかのフラグ
comout_flag = False
i = 0
# for-eachで一行のリストごとに処理
for line in lines:
    # 月の行かコメントアウト開始終了時以外はmonthを変えない
    if month_search(line) != 0:
        month = month_search(line)
    if month == 4:
        month_start_flag = True

    if month_start_flag:
        # コメントアウト行終了時にフラグを下ろす
        if month == -1:
            print("コメアウト終了")
            comout_flag = False
        # コメントアウト行開始時にフラグを立てる
        elif month == -2:
            print("コメアウト開始")
            comout_flag = True
        # コメントアウト行でない場合の処理
        elif not comout_flag:
            # 日付を検出
            print("大丈夫な予定")
            '''
            # 構造体を渡す
            csv_write = CSV_Struct()
            # 西暦を入力
            year = "2016"
            if month < 10:
                csv_write.start = year + "0" + str(month)
            # 期間制予定かの検出
            span = span_search(line)
            if span = 0:
                # ex. month:4 → 04

            # 一日予定
            elif span = -1:
            # 月をまたぐ期間制予定
            elif span = -2:

# GitHubにアップする際のWebサイトソース削除
f = open('./gyouji.html', 'w')
f.write('')
f.close()

# Issue: Webサイトソースが改行(CR, CRLF, LF)を用いず<br>として形式を保っている場合に対応できていない.
#        期間制予定かの検出に〜の２つ後にあるというスタイルに依存した判定を行っている.
'''
