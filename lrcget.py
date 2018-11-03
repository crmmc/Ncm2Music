#!/bin/env python
import requests
import json
import re
def Getlrc(neteaseID):
	lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(neteaseID) + '&lv=1&kv=1&tv=-1'
	lyric = requests.get(lrc_url)
	json_obj = lyric.text
	j = json.loads(json_obj)
	lrc = j['lrc']['lyric']
	if j.has_key('tllrc') :
		tllrc =  j['tllrc']['lyric']
	else:
		tllrc = 'no'
	return lrc + '#%$%#' + tllrc

print (Getlrc(28851139))
