# !/usr/bin/env python
# coding: utf-8
line = '　１２日（月）～８月７日（金）　後期授業料免除申請受付開始'
# line = '　１０日（土）　２～５年第２回単位認定試験<br>'
# line = '　２７日（火）～１月４日（水）　一斉休業<br>'
index = line.find('～')
# .findで検出されない場合-1が返される
if index != -1:
    # 2〜5年といった学年の間隔を〜記号で表しているため、その対策
    # 〜の２つ後にあるというスタイルに依存
    # つまり一日予定
    if line.startswith('年', index + 2):
        print("-1")
    # 月が変わる特殊な期間予定の場合の対策
    elif line.startswith('月', index + 2) or line.startswith('月', index + 3):
        print("-2")
    # 期間予定
    else:
        print("0")
# 一日予定
else:
    print("-1")
