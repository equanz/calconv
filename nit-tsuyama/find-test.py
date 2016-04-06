# !/usr/bin/env python
# coding: utf-8
# line = '　１０日（土）　２～５年第２回単位認定試験<br>'
line = '　２７日（火）～１月４日（水）　一斉休業<br>'
index = line.find('～')
print(index)
print(line.startswith('年', index + 2))
print(line.find('）'))
