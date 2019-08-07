#!/bin/env python3
#encoding:utf-8
import sys,glob
from bs4 import BeautifulSoup
import time,os,re,json,requests
from urllib import parse

header = {
		'Host': 'music.163.com',
		'Referer': 'https://music.163.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
	}
	
	
def HtmlGet(url,header={},callback=3):
    if callback < 0:
    	print ("[HTML] Error!")
    	return None
    try:
    	return requests.get(url,headers=header).content
    except:
    	print ('[HTML]CallBack {}'.format(callback))
    	time.sleep(2)
    	return HtmlGet(url,header,callback-1)
    return None

def MV(sfrom,sto):
  if len(sfrom) < 0:
    return 2
  if sys.platform.find("win") > -1:
    return os.system('move "' + sfrom + '" "' + sto + '"')
  elif sys.platform.find("linux") > -1:
    return os.system('mv "' + sfrom + '" "' + sto + '"')
  return 1

def delname():
	print ('del empty files!')
	for r in glob.glob('*'):
		if os.path.getsize(r) < 32:
			os.remove(r)
			print ('[' + r + '] Delete !')

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

def Getlrc(neteaseID):
	lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(neteaseID) + '&lv=1&kv=1&tv=-1'
	lyric = requests.get(lrc_url)
	json_obj = lyric.text
	j = json.loads(json_obj)
	return j

def gtm(gyy):
	return re.findall(r'\[(.*?)\]',gyy)

def download(IGET):
	for muu in IGET:
		music_name = muu[1].replace('.lrc','')
		music_id = muu[0]
		print (music_name + '   ' +music_id)
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
			open(muu[1],'w').write(tolrc)
			print ('Get [' + music_name + '] Successful!')
		except:
			open('err.log').write('ERROR_IN_WRITE_ALL_lyric_tlyric:'+music_name+"\n")
		
def NameToID(name):
	url1 = 'http://s.music.163.com/search/get/?type=1&filterDj=true&s=' + parse.quote(name) + '&limit=2&offset=0&callback='
	geted = HtmlGet(url1)
	if geted == None:
		return -1
	else:
		try:
			a = json.loads(geted)
			return int(a['result']['songs'][0]['id'])
		except:
			return -1
	
def FileToID(ftype):
	Nolrc=[]
	a = glob.glob('*.' + ftype)
	for i in a:
		lrcN = i.replace('.' + ftype,'.lrc')
		if os.path.exists(lrcN):
			print ('[SONG] Exists!')
			continue
		else:
			print ('[SONG] Append==> ' + lrcN)
			Nolrc.append(lrcN)
	return Nolrc
	
#http://s.music.163.com/search/get/?type=1&filterDj=true&s=%E5%BC%80%E5%BF%83&limit=2&offset=0&callback=


def LAID(list):
	list2 = []
	for o in list:
		i = o.replace('.lrc','')
		id = NameToID(i)
		if id == -1:
			print ('Get ' + str(i) + ' Error!')
			open('failsong.txt','a').write('ID_ERROR:' + str(i) + "\n")
			continue
		else:
			list2.append([str(id),o])
	return list2
	
	
print ('Start!')
ALLY = FileToID('flac') + FileToID('mp3')
a = LAID(ALLY)
download(a)
print ('Complete!')
