#!/usr/bin/env python
# coding: utf-8

import sys
import calendar
import requests
import zenhan
import argparse
from icalendar import Calendar, Event, vDate
import datetime

class CSV_Struct:
    """.csvに書き込む際の構造体."""
    def __init__(self):
        self.sub = ''
        self.start = ''
        self.end = ''
        # 終日はTRUEとしておく
        self.ALL_DAY = 'TRUE'

def month_search(line):
    """月の行かコメントアウト行か予定の行かを検出し,intで返す."""
    # 月の表示のテンプレート
    month_temp = ['<h4>＜', '月＞</h4>']
    # 検索方法が汚すぎる
    if month_temp[0] in line and month_temp[1] in line:
        month = int(zenhan.h2z(line.replace(month_temp[0], '').replace(month_temp[1], '').replace(' ', '')))
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

def span_search(line):
    """期間予定であるかを検出し,boolで返す."""
    zen_tilde = '～'
    # '～'が最初に検出された列
    index = line.find(zen_tilde)
    # .findで検出されない場合-1が返される
    if index != -1:
        # 2～5年といった学年の間隔を～記号で表しているため、その対策
        # ～の２つ後にあるというスタイルに依存
        # つまり一日予定
        if line.startswith('年', index + 2):
            return -1
        # 月が変わる特殊な期間予定の場合の対策
        elif line.startswith('月', index + 2) or line.startswith('月', index + 3):
            return -2
        # 期間予定
        else:
            return 0
    # 一日予定
    else:
        return -1

def digit_conv(var):
    """intを取得し,二桁のstrで返す."""
    zero = '0'
    # 一桁の時,'0'を先頭につける
    if var < 10:
        # ex. month:4 → 04
        return zero + str(var)
    else:
        return str(var)

def date_start_search(line):
    """予定開始の日付を検出し,strで返す."""
    # 全角スペース
    zen_space = '　'
    # 全角0
    zen_zero = '０'
    nichi = '日'
    dollar = '$'
    # 全角スペースを0に置き換えることで無理やり対応
    line = line.replace(zen_space, zen_zero)
    index = line.find(nichi)
    # 日と曜日の位置関係から誤表記を訂正
    index_first_dollar = line.find(dollar, index + 1)
    if index + 1 != index_first_dollar:
        index = index_first_dollar

    # ex. １ → ０１
    #if line[index - 1] == zen_space:
    #    line[index - 1] = zen_zero
    return zenhan.z2h(line[index - 2:index])

def date_end_search(line):
    """月表記のない予定終了の日付を検出し,strで返す."""
    zen_tilde = '～'
    # 全角スペース
    zen_space = '　'
    # 全角0
    zen_zero = '０'
    nichi = '日'
    dollar = '$'
    # 全角スペースと全角チルダを0に置き換えることで無理やり対応
    line = line.replace(zen_space, zen_zero)
    line = line.replace(zen_tilde, zen_zero)
    index_first_date = line.find(nichi)
    # 二度目のnichiの位置を検出
    index_second_date = line.find(nichi, index_first_date + 1)
    # 日と曜日の位置関係から誤表記を訂正
    index_second_dollar = line.find(dollar, index_first_date + 2)
    if index_second_date + 1 != index_second_dollar:
        index_second_date = index_second_dollar

    return zenhan.z2h(line[index_second_date - 2:index_second_date])

def month_date_end_search(line):
    """月表記のある予定終了の日付を検出し,intとintで返す."""
    zen_tilde = '～'
    # 全角スペース
    zen_space = '　'
    # 全角0
    zen_zero = '０'
    nichi = '日'
    tsuki = '月'
    dollar = '$'
    # 全角スペースを0に置き換えることで無理やり対応
    line = line.replace(zen_space, zen_zero)
    line = line.replace(zen_tilde, zen_zero)
    index_month = line.find(tsuki)
    # 日が一桁の場合の対策
    line = line.replace(tsuki, zen_zero, 1)
    # 二度目のnichiの位置を検出
    index_second_date = line.find(nichi, index_month + 1)
    # 日と曜日の位置関係から誤表記を訂正
    index_second_dollar = line.find(dollar, index_month + 1)
    if index_second_date + 1 != index_second_dollar:
        index_second_date = index_second_dollar
    # 月, 日を返す
    return int(zenhan.z2h(line[index_month - 2:index_month])), int(zenhan.z2h(line[index_second_date - 2:index_second_date]))

def date_end_next(year, month, date):
    """intで取得して,予定終了の日付を計算し,boolとstrで返す."""
    april = 4
    # 10日
    tenth = 10
    # 1~3月はmonthrangeに次の年を入力
    if month < april:
        year = year + 1
    # 月始め
    start = '01'
    end = calendar.monthrange(year, month)
    # 月またぎの有無と終了日を返す
    if date == end[1]:
        return True, start
    else:
        # 引数dateの次の日
        next_date = date + 1
        return False, digit_conv(next_date)

def sub_search(line):
    """予定内容を検出し,strで返す."""
    # ダラーマーク
    dollar = '$'

    # ダラーマークの削除
    line = line.replace(dollar, '')

    # 全角スペース
    zen_space = '　'
    # 右端から検索
    index = line.rfind(zen_space)

    # 学校か寮かのタグ付け
    dormitory = '寮'
    school_tag = '【学校】'
    dormitory_tag = '【寮】'

    if dormitory in line:
        return dormitory_tag + line[index + 1:]
    else:
        return school_tag + line[index + 1:]

def remove_garbage(line):
    """内容のうち,検出に必要ないもの(曜日を除く)を取り除き,strで返す."""
    # 半角space
    han_space = ' '
    # 全角space
    zen_space = '　'
    # ulタグ
    ul = ['<ul>', '</ul>']
    # liタグ
    li = ['<li>', '</li>']
    # brタグ
    br = '<br>'

    # ulタグを取り除く
    line = line.replace(ul[0], '')
    line = line.replace(ul[1], '')

    # 文字列左の空白列を取り除く
    line = line.lstrip()
    # 文字列左に半角スペースを追加(ヤケクソガバガバソース)
    line = zen_space + line[0:]

    # liタグを取り除く
    line = line.replace(li[0], '')
    line = line.replace(li[1], '')

    line = line.replace(br, '')
    return line

def replace_week(line):
    """内容のうち，曜日表記を$に置換"""
    # 曜日
    days = ['（日）', '（月）', '（火）', '（水）', '（木）', '（金）', '（土）']
    # ダラーマーク
    dollar = '$'
    # 曜日表記を除去する
    for day in days:
        line = line.replace(day, dollar)
    return line

def yesno():
    """yes/no入力の判定を行う."""
    s = input()
    if s in ("y", "yes", "1", "true", "t"):
        return True
    elif s in ("n", "no", "0", "false", "f"):
        return False
    else:
        raise ValueError("\tA y or n response is required\n\t\t" + s + " is not defined")

def main():
    # 津山工業高等専門学校 行事予定 URL(2016/08/17現在)
    # まあ毎年URL変わるようだったら入力制にするかも
    URL = "http://www.tsuyama-ct.ac.jp/gyoujiVer4/gyouji.html"
    # カレンダーで読み込み可能にする為の.csv用ヘッダ
    CSV_HEAD = 'Subject,Start Date,End Date,All Day Event\n'

    print("4月~3月までの一年間の行事予定を出力します")
    print("URL:" + URL)
    print("予定表に対応する西暦を年度で入力してください")

    # コマンドライン引数の個数を取得
    argc = len(sys.argv)

    # ヘルプオプション検出用
    HELP_OPTION = ['-h', '--help']
    # 西暦入力オプション検出用
    YEAR_OPTION = ['-y', '--year']
    # 予定切り分けオプション(ex.oo開始, oo終了)検出用
    LIMIT_OPTION = ['-l', '--limit']

    # 西暦の入力
    if argc == 1:
        year = input()
        if year.isdigit():
            year = int(year)
        else:
            raise ValueError("\tA Number response is required\n\t\t" + year + " is not defined")
    else:
        year = sys.argv[1]
        if year.isdigit():
            year = int(year)
            print(year)
        else:
            raise ValueError("\tA Number response is required\n\t\t" + year + " is not defined")

    if year <= 2000 or year >= 2027:
        print("注意:このソフトの制作年から大きく異なるようです\n本当にこの西暦でよろしいですか\ny/n")
        if yesno():
            pass
        else:
            sys.exit()

    # Requests オブジェクト
    r = requests.get(URL)

    # ステータスコードによる例外処理
    if r.status_code != 200:
        raise ConnectionError("\tStatus Code is not equal 200.\n\tStatus Code: " + r.status_code)

    # Encodingをutf-8に変更
    if r.encoding == 'ISO-8859-1':
        r.encoding = 'utf-8'

    # ローカルに書き込み
    f = open('./gyouji.html', 'w')
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

    # iCalヘッダ生成
    cal = Calendar()
    cal.add('proid', '津山高専行事予定' + str(year) + '年度版(calconv)')
    cal.add('version', '2.0')

    # 後ろの改行文字を取り除く
    i = 0
    for line in lines:
        lines[i] = line.rstrip()
        i = i + 1

    # 予定表部分終了部分(テキストそのままのため、何か終了検出方法を考えるべき)
    SCHEDULE_END = '</div>'
    # 4月の予定が読み込み開始されたかのフラグ
    month_start_flag = False
    # 予定がコメントアウト中の行にあるかのフラグ
    comout_flag = False
    i = 0
    # for-eachで一行のリストごとに処理
    for line in lines:
        # 検出に必要のない文字列を取り除く
        line = remove_garbage(line)
        # 曜日を$に置換
        line = replace_week(line)

        # 改行のみの行を取り除く
        # remove_garbage()のガバガバ操作の影響でソースが気持ち悪い
        # 変なHTMLソースに対応するため
        if line != "　":
            print(line)
            month_searching = month_search(line)
            # 月の行以外はmonthを変えない
            if month_search(line) >= 1:
                month = month_searching
            if month_searching == 4:
                month_start_flag = True

            if month_start_flag:
                # 予定表部分が終了した場合,breakする
                if SCHEDULE_END in line:
                    break
                # コメントアウト行終了時にフラグを下ろす
                elif month_searching == -1:
                    comout_flag = False
                # コメントアウト行開始時にフラグを立てる
                elif month_searching == -2:
                    comout_flag = True
                # コメントアウト行でないかつ月表示の行でない場合の処理
                elif not comout_flag and month_searching == 0:
                    # 構造体を渡す
                    csv_write = CSV_Struct()

                    if month <= 12:
                        csv_write.start = digit_conv(month) + '/'

                    # 期間予定かの検出
                    date_end = [] # date_end初期化
                    span = span_search(line)
                    csv_write.start = csv_write.start + date_start_search(line) + '/'
                    # 一日予定
                    if span == -1:
                        # 月末の場合は次の月の始めを設定
                        date_end = date_end_next(year, month, int(date_start_search(line)))
                        if date_end[0]:
                            if month == 12:
                                jan = '01'
                                csv_write.end = jan + '/'
                            else:
                                csv_write.end = digit_conv(month + 1) + '/'
                        else:
                            csv_write.end = digit_conv(month) + '/'

                        csv_write.end = csv_write.end + date_end[1] + '/'
                    # 期間予定
                    elif span == 0:
                        date_end = date_end_next(year, month, int(date_end_search(line)))
                        if date_end[0]:
                            if month == 12:
                                jan = '01'
                                csv_write.end = jan + '/'
                            else:
                                csv_write.end = digit_conv(month + 1) + '/'
                        else:
                            csv_write.end = digit_conv(month) + '/'

                        csv_write.end = csv_write.end + date_end[1] + '/'
                    # 月と書かれた期間予定
                    elif span == -2:
                        mde = month_date_end_search(line)
                        date_end = date_end_next(year, int(mde[0]), int(mde[1]))
                        if date_end[0]:
                            if month == 12:
                                jan = '01'
                                csv_write.end = jan + '/'
                            else:
                                csv_write.end = digit_conv(int(mde[0]) + 1) + '/'
                        else:
                            csv_write.end = digit_conv(int(mde[0])) + '/'

                        csv_write.end = csv_write.end + date_end[1] + '/'

                    # 1日
                    first = '01'
                    # startは1~3月なら次の年を設定
                    if month < 4:
                        csv_write.start = csv_write.start + str(year + 1)
                    else:
                        csv_write.start = csv_write.start + str(year)
                    decem = 12
                    # endは12月予定かつ月を跨いでいるまたは,1~3月なら次の年を設定
                    if month == decem and span == -2 or month == decem and date_end[0] or month < 4:
                        csv_write.end = csv_write.end + str(year + 1)
                    else:
                        csv_write.end = csv_write.end + str(year)
                    csv_write.sub = sub_search(line)

                    # 各種表示
                    print("start: " + csv_write.start)
                    print("end: " + csv_write.end)
                    print("sub: " + csv_write.sub)

                    # iCal形式の作成
                    event = Event()
                    event.add('summary', csv_write.sub)
                    dt = datetime.datetime.strptime(csv_write.start, "%m/%d/%Y")
                    event.add('dtstart', vDate(dt))
                    dt = datetime.datetime.strptime(csv_write.end, "%m/%d/%Y")
                    event.add('dtend', vDate(dt))

                    # .csvに書き込む
                    f = open('./schedule.csv', 'a')
                    f.write(csv_write.sub + "," +
                            csv_write.start + "," +
                            csv_write.end + "," +
                            csv_write.ALL_DAY + "\n")
                    f.close()

                    # cal(iCal)に書き込む
                    cal.add_component(event)

    # .icsに書き込む
    f = open('./schedule.ics', 'w')
    print(cal.to_ical().decode('utf-8'))
    f.write(cal.to_ical().decode('utf-8'))
    f.close()

    # ダウンロードしたWebページの削除
    f = open('./gyouji.html', 'w')
    f.write('')
    f.close()

    print("\nSuccessful!")

# モジュール利用された場合のため
if __name__ == '__main__':
    main()

# Issue: Webサイトソースが改行(CR, CRLF, LF)を用いず<br>として形式を保っている場合に対応できていない.
#        期間制予定かの検出に～の２つ後にあるというスタイルに依存した判定を行っている.
#        予定表部分終了部分がテキストそのまま.
