#!/bin/env python3
import sys
from bs4 import BeautifulSoup
import time,os,re,json,requests
def Getlrc(neteaseID):
	lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(neteaseID) + '&lv=1&kv=1&tv=-1'
	lyric = requests.get(lrc_url)
	json_obj = lyric.text
	j = json.loads(json_obj)
	return j
	
def TwoToOne(l1,l2):
	yn = l2.split("\n")
	ttty = ''
	for yu in l1.split("\n"):
		gh = ""
		for i in yn:
			try:
				if (gtm(i) == gtm(yu)) or (str(gtm(i)[0]) + '0' == str(gtm(yu)[0])) or (str(gtm(i)[0]) == str(gtm(yu)[0]) + '0') or (gtm(i)[0] == gtm(yu)[0]):
					ttty = ttty + yu +"\n" + i + "\n"
				else:
					continue
			except:
				continue
	return ttty

def download(songlistID):
	url = 'http://music.163.com/m/playlist?id='+str(songlistID)
 
	header = {
		'Host': 'music.163.com',
		'Referer': 'https://music.163.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
	}
 
	res = requests.get(url, headers=header,timeout = 15).text
	songlist = re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>', res)
	n = 0
	for muu in songlist:
		n = n+ 1
		if n == 5:
			time.sleep(1)
			n = 0
		music_name = muu[1]
		music_id = muu[0]
		print (music_name + '   ' +music_id)
		song_url = "http://music.163.com/song/media/outer/url?id=%s" % music_id
		music_lrc = music_name.replace('/',' ')
		arhhc = Getlrc(music_id)
		try:
			if len(arhhc['lrc']['lyric']) < 10:
				continue
		except:
			open('err.log').write('ERROR_IN_GET_ALL_lyric_tlyric:'+music_name+"\n")
			continue
		if 'tlyric' in arhhc:
			if 'lyric' in arhhc['tlyric']:
				tolrc = TwoToOne(str(arhhc['lrc']['lyric']),str(arhhc['tlyric']['lyric']))
			else:
				tolrc = str(arhhc['lrc']['lyric'])
		else:
			tolrc = str(arhhc['lrc']['lyric'])
		try:
			open(music_name + '.lrc','w').write(tolrc)
			print ('Get [' + music_name + '] Successful!')
		except:
			errorfile.write('WRITE ALL ERROR:' +music_name+ ':' + music_id +"\n")
		
errorfile = open('error.list','a')
errorfile.write(str(time.asctime()).encode('utf-8') + "\n")
download(2117303846)
errorfile.close()
import glob,os
print ('Turning Names.....')
for i in glob.glob('*.mp3'):
	hg = i.split('.')[0].split(' - ')
	if len(hg) == 2:
		sn = hg[1].split('.')[0] + '.lrc'
		snd = i.split('.')[0] + '.lrc'
		if os.path.exists(sn):
			print ('[' + sn + ']>>>[' + snd + ']')
			os.rename(sn,snd)
print ('MP3 Lyric Turn Done!')
for i in glob.glob('*.flac'):
	hg = i.split('.')[0].split(' - ')
	if len(hg) == 2:
		sn = hg[1].split('.')[0] + '.lrc'
		snd = i.split('.')[0] + '.lrc'
		if os.path.exists(sn):
			print ('[' + sn + ']>>>[' + snd + ']')
			os.rename(sn,snd)
print ('FLAC Lyric turn done!')