# !/usr/bin/env python
# coding: utf-8

from datetime import datetime
import requests
import zenhan
import calendar

""".csvに書き込む際の構造体."""
class CSV_Struct:
    def __init__(self):
        self.sub = ''
        self.start = ''
        self.end = ''
        # 終日はTRUEとしておく
        self.ALL_DAY = 'TRUE'

"""何月であるかを検出し,返す."""
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
    # コメントアウト終了時
    elif '-->' in line:
        return -1
    # 予定の行の時
    else:
        return 0

"""期間予定であるかを検出し,真偽を返す."""
def span_search(line):
    index = line.find('〜')
    # .findで検出されない場合-1が返される
    if index != -1:
        # 2〜5年といった学年の間隔を〜記号で表しているため、その対策
        # 〜の２つ後にあるというスタイルに依存
        # つまり一日予定
        if line.startswith('年', index + 2):
            return -1
        # 月が変わる特殊な期間予定の場合の対策
        elif line.startswith('月', index +2):
            return -2
        # 期間予定
        else:
            return 0
    # 一日予定
    else:
        return -1

"""予定開始の日付を検出し,返す."""
def date_start_search(line):
    # 全角スペース
    zen_space = '　'
    # 全角0
    zen_zero = '０'
    # 全角スペースを0に置き換えることで無理やり対応
    line = line.replace(zen_space, zen_zero)
    index = line.find('日')
    # ex. １ → ０１
    #if line[index - 1] == zen_space:
    #    line[index - 1] = zen_zero
    return zenhan.z2h(line[index - 2:index])

"""予定終了の日付が月末でないかを検出し,返す."""
def date_end_search(line, year, month, date):
    hoge = calendar.monthrange(year, month)
    # 月の最終日の場合Trueを返す
    if date == hoge[1]:
        return True
    else:
        return False

# 津山工業高等専門学校 行事予定 URL(2016/04/03現在)
# まあURL変わるようだったら入力制にするかも
# (2016/04/03現在)サイトはShift-JIS(半ギレ
URL = "http://www.tsuyama-ct.ac.jp/honkou/annai/gyouji.htm"
# カレンダーで読み込み可能にする為の.csv用ヘッダ
CSV_HEAD = 'Subject,Start Date,End Date,All Day Event\n'
# 西暦を入力
year = "2016"
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

# 後ろの改行文字を取り除く
i = 0
for line in lines:
    lines[i] = line.rstrip()
    i = i + 1

# 予定表部分終了部分(テキストそのままのため、何か終了検出方法を考えるべき)
month_end = '<hr class="s60">'
# 4月の予定が読み込み開始されたかのフラグ
month_start_flag = False
# 予定がコメントアウト中の行にあるかのフラグ
comout_flag = False
i = 0
# for-eachで一行のリストごとに処理
for line in lines:
    # 改行のみの行を取り除く
    if line != '':
        month_searching = month_search(line)
        # 月の行以外はmonthを変えない
        if month_search(line) >= 1:
            month = month_searching
        if month_searching == 4:
            month_start_flag = True

        if month_start_flag:
            # 予定表部分が終了した場合,breakする
            if month_end in line:
                break
            # コメントアウト行終了時にフラグを下ろす
            elif month_searching == -1:
                comout_flag = False
            # コメントアウト行開始時にフラグを立てる
            elif month_searching == -2:
                comout_flag = True
            # コメントアウト行でないかつ月表示の行でない場合の処理
            elif not comout_flag and month_searching == 0:
                # 日付を検出
                print(line)

                # 構造体を渡す
                csv_write = CSV_Struct()

                if month < 10:
                    # ex. month:4 → 04
                    csv_write.start = "0" + str(month) + '/'
                elif month <= 12:
                    csv_write.start = str(month) + '/'
                # 終了日が次の年である場合の対策
                end_next_year = False

                # 期間予定かの検出
                span = span_search(line)
                csv_write.start = csv_write.start + date_start_search(line) + '/'
                # 一日予定
                if span == -1:
                    # 月末の場合は次の月の始めを設定
                    if date_end_search(line, int(year), month, int(date_start_search(line))):
                        if month + 1 < 10:
                            # ex. month + 1:4 → 04
                            csv_write.end = "0" + str(month + 1) + '/'
                        elif month + 1 < 12:
                            csv_write.end = str(month + 1) + '/'
                        elif month + 1 == 12:
                            # 12月の次は1月を設定
                            jan = "01"
                            csv_write.end = jan + '/'
                        # 月末の次は1日を設定
                        first = "01"
                        csv_write.end = csv_write.end + first + '/'
                        if month + 1 < 4:
                            end_next_year = True
                    else:
                        if month < 10:
                            # ex. month + 1:4 → 04
                            csv_write.end = "0" + str(month) + '/'
                        elif month < 12:
                            csv_write.end = str(month) + '/'
                        # 日付は1加えるだけ(無理) 03 + 1 → 無理
                        csv_write.end = csv_write.end + str(int(date_start_search(line)) + 1) + '/'
                # 期間予定
                elif span == 0:
                    print("期間予定である！")
                # 月をまたぐ期間予定
                elif span == -2:
                    print("月をまたぐ期間予定ナリ〜")

                # 1~3月は次の年を設定
                if month < 4:
                    csv_write.start = csv_write.start + str(int(year + 1))
                csv_write.end = csv_write.end + year
                print("start: " + csv_write.start)
                # .csvに書き込む
                f = open('./schedule.csv', 'a')
                f.write(csv_write.sub + "," +
                        csv_write.start + "," +
                        csv_write.end + "," +
                        csv_write.ALL_DAY + "\n")
                f.close()

# GitHubにアップする際のWebサイトソース削除
f = open('./gyouji.html', 'w')
f.write('')
f.close()

# Issue: Webサイトソースが改行(CR, CRLF, LF)を用いず<br>として形式を保っている場合に対応できていない.
#        期間制予定かの検出に〜の２つ後にあるというスタイルに依存した判定を行っている.
#        予定表部分終了部分がテキストそのまま.
