#!/usr/bin/env python
#coding=utf-8

# Modifier: CRMMC-CreamTes-KGDSave SoftWare Studio 2018-2020'
# Thanks for nondanee
#need a tools use order: pip install pycryptodome mutagen requests urllib3
#to install it!
#it can be used on Windows,Linux,Mac on Python3 or Python2
print ('*')
print ('_  _          ___ __  __         _')
print ('| \| |__ _ __ |_  )  \/  |_  _ __(_)__')
print ("| .` / _| '  \ / /| |\/| | || (_-< / _|")
print ('|_|\_\__|_|_|_/___|_|  |_|\_,_/__/_\__|')
print ('===============================')
print ('CopyRight 2018-2020 KGDSAVE SOFTWARE STUDIO')
print ('Coded by CRMMC')
print ('Sources: github.com/crmmc/Ncm2Music')
print ('This is a tool to convent ncm file to music ')
print ('add Music tags and get lyric,picture')
print ('===============================')
print ('')
print ('[MAIN]Importing Librarys')
import binascii
import struct
import base64
import json
import time
import threading
import re
import os
import sys
import glob
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import mutagen.id3
from Crypto.Cipher import AES
from mutagen.mp3 import MP3, EasyMP3 
from mutagen.flac import FLAC
from mutagen.flac import Picture
from mutagen.easyid3 import EasyID3
from mutagen.id3 import COMM,APIC,ID3
if sys.version_info < (3, 4):
    print ('[MAIN]Running in Python2')
    print ('[MAIN]reset system encoding to utf-8')
    reload(sys)
    sys.setdefaultencoding('utf-8')
print ('[MAIN]Library Load OK!')

def Getlrc(neteaseID):
	lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(neteaseID) + '&lv=1&kv=1&tv=-1'
	lyric = requests.get(lrc_url)
	json_obj = lyric.text
	j = json.loads(json_obj)
	return j



def dump(file_path,Thnom):
    core_key = binascii.a2b_hex("687A4852416D736F356B496E62617857")
    meta_key = binascii.a2b_hex("2331346C6A6B5F215C5D2630553C2728")
    unpad = lambda s : s[0:-(s[-1] if type(s[-1]) == int else ord(s[-1]))]
    f = open(file_path,'rb')
    header = f.read(8)
    assert binascii.b2a_hex(header) == b'4354454e4644414d'
    f.seek(2, 1)
    key_length = f.read(4)
    key_length = struct.unpack('<I', bytes(key_length))[0]
    key_data = f.read(key_length)
    key_data_array = bytearray(key_data)
    for i in range (0,len(key_data_array)): key_data_array[i] ^= 0x64
    key_data = bytes(key_data_array)
    cryptor = AES.new(core_key, AES.MODE_ECB)
    key_data = unpad(cryptor.decrypt(key_data))[17:]
    key_length = len(key_data)
    key_data = bytearray(key_data)
    key_box = bytearray(range(256))
    c = 0
    last_byte = 0
    key_offset = 0
    for i in range(256):
        swap = key_box[i]
        c = (swap + last_byte + key_data[key_offset]) & 0xff
        key_offset += 1
        if key_offset >= key_length: key_offset = 0
        key_box[i] = key_box[c]
        key_box[c] = swap
        last_byte = c
    meta_length = f.read(4)
    meta_length = struct.unpack('<I', bytes(meta_length))[0]
    meta_data = f.read(meta_length)
    meta_data_array = bytearray(meta_data)
    for i in range(0,len(meta_data_array)): meta_data_array[i] ^= 0x63
    meta_data = bytes(meta_data_array)
    meta_data = base64.b64decode(meta_data[22:])
    cryptor = AES.new(meta_key, AES.MODE_ECB)
    meta_data = unpad(cryptor.decrypt(meta_data))[6:]
    meta_data = json.loads(meta_data)
    crc32 = f.read(4)
    crc32 = struct.unpack('<I', bytes(crc32))[0]
    f.seek(5, 1)
    image_size = f.read(4)
    image_size = struct.unpack('<I', bytes(image_size))[0]
    image_data = f.read(image_size)
    file_name = meta_data['musicName'] + ' - ' + meta_data['artist'][0][0] + '.' + meta_data['format']
    file_name = str(file_name)
    if os.path.exists(file_name):
        print ('[+][Thread:{}]Now '.format(Thnom) + '[' + str(meta_data['format']) + ']['  + 'MusicID:' + str(meta_data['musicId']) + ']['+ str(meta_data['bitrate']/1000) + 'kbps] [' + str(file_path) +']>>>[' + str(file_name) + ']')
        print ('[!]File is exist!')
        if (os.path.getsize(file_name) < (os.path.getsize(file_path) - (3*1024))):
            print ('[!]Bad File!')
            os.remove(file_name)
            dump(file_path,Thnom)
            return 0
    else:
    	print ('[+][Thread:{}]Now '.format(Thnom) + '[' + str(meta_data['format']) + ']['  + 'MusicID:' + str(meta_data['musicId']) + ']['+ str(meta_data['bitrate']/1000) + 'kbps] [' + str(file_path) +']>>>[' + str(file_name) + ']')
    	m = open((os.path.join(os.path.split(file_path)[0],file_name)),'wb')
    	chunk = bytearray()
    	while True:
        	chunk = bytearray(f.read(0x8000))
        	chunk_length = len(chunk)
        	if not chunk:
        		break
        	for i in range(1,chunk_length+1):
        		j = i & 0xff;
        		chunk[i-1] ^= key_box[(key_box[j] + key_box[(key_box[j] + j) & 0xff]) & 0xff]
        	m.write(chunk)
    	m.close()
    	f.close()
    picdata = ''
    music_id = meta_data['musicId']
    music_name = meta_data['musicName']
    music_lrc = meta_data['musicName'] + ' - ' + meta_data['artist'][0][0]
    try:
    	picurl = meta_data['albumPic']
    	picdata = requests.get(picurl).content
    except:
    	print ('[!][Thread:{}]Get Picture From Internet Error!'.format(Thnom))
    if meta_data['format'] == 'mp3':
    	mp3_info = MP3(file_name, ID3=EasyID3)
    	arhhc = Getlrc(music_id)
    	mp3_info['album'] = meta_data['album']
    	mp3_info['artist'] = meta_data['artist'][0][0]
    	mp3_info['title'] = meta_data['musicName']
    	mp3_info['discsubtitle'] = meta_data['alias'] 
    	mp3_info['lyricist'] = str(arhhc['lrc']['lyric'])
    	mp3_info.save()
    	hh = ID3(file_name)
    	hh.update_to_v23()
    	hh.save()
    	hh['APIC:'] = (APIC(mime='image/jpg',  data=picdata))
    	hh.save()
    	if 'lrc' in arhhc:
        	try:
        		f = open((music_lrc+'.lrc'),'w')
        		f.write(str(arhhc['lrc']['lyric']))
        		f.close()
        	except:
        		print ('[!][Thread:{}]LRC Get Error!'.format(Thnom))
    	if 'tlyric' in arhhc:
    		try:
    			l = open((music_lrc+'.tlyric'),'w')
    			l.write(str(arhhc['tlyric']['lyric']))
    			l.close()
    		except:
        		print ('[!][Thread:{}]Tlyric Get Error!'.format(Thnom))
    elif meta_data['format'] == 'flac':
    	audio = FLAC(file_name)
    	audio["title"] = meta_data['musicName']
    	audio['album'] = meta_data['album']
    	audio['artist'] = meta_data['artist'][0][0]
    	audio['comment'] = meta_data['alias']
    	app = Picture()
    	app.data = picdata
    	app.type = mutagen.id3.PictureType.COVER_FRONT 
    	app.mime = u"image/jpeg"
    	audio.add_picture(app)
    	try:
    		audio.save()
    		arhhc = Getlrc(music_id)
    		if 'lrc' in arhhc:
        		try:
        			f = open((music_lrc+'.lrc'),'w')
        			f.write(str(arhhc['lrc']['lyric']))
        			f.close()
        		except:
        			print ('[!][Thread:{}]LRC Get Error!'.format(Thnom))
    		if 'tlyric' in arhhc:
    			try:
    				l = open((music_lrc+'.tlyric'),'w')
    				l.write(str(arhhc['tlyric']['lyric']))
    				l.close()
    			except:
        			print ('[!][Thread:{}]Tlyric Get Error!'.format(Thnom))
    	except:
    		print ('[!]{}FLAC Tags Save Error!'.format(Thnom))
    		sfnr='title:'+meta_data['musicName']+'#$#' + 'artist:' + meta_data['artist'][0][0] +'#$#' +'album:'+ meta_data['musicName']+ '#$#albumPic:'+meta_data['albumPic']
    		rew =open((file_name+'.songinfo'),'w')
    		rew.write(sfnr)
    		rew.close()
    		print ('[!][Thread:{}]Song Tags Has Been Saved On A SongInfo File!'.format(Thnom));
    else:
    		print ('[!][Thread:]{}Unknow Type:'.format(Thnom)+meta_data['format'])

def MultiThreadChild(list,Number):
	global dfgg
	global totsong
	print ('[+][Thread:{}] Thread Ready! Get Task: {}'.format(Number,len(list)))
	for ncm1f in list:
		time.sleep(Number)
		try:
			dump(ncm1f,Number)
			totsong = totsong + 1
		except:
			dfgg.write(ncm1f +'##File code Error!'+ "\n")
			continue
	print ('[+]Thread {} :Task Finish!'.format(Number))

if __name__ == '__main__':
	global AllTheardNumber
	AllTheardNumber = 4
	ncmfiles = glob.glob("*.ncm")
	if len(ncmfiles) < 1:
		print ('[MAIN]NCM Files No Found!')
		exit (0)
	if len(ncmfiles) < AllTheardNumber:
		AllTheardNumber = len(ncmfiles)
	t=[0,]*AllTheardNumber
	global dfgg
	global totsong
	totsong = 0
	print ('[MAIN]Running in a '+ sys.platform + ' system')
	try:
		dfgg = open('ncm2music_error.txt','a')
	except:
		print ('[!]Open log file error!')
	print ('[MAIN]There are ' + str(len(ncmfiles)) + ' Files ')
	ttbig = 0
	for tii in ncmfiles:
		ttbig = ttbig + os.path.getsize(tii)/1024/1024.0*1.6
	dw = 's'
	if ttbig > 60:
		ttbig = ttbig / 60.0
		dw = 'min'
		if ttbig > 60:
			ttbig = ttbig / 60.0
			dw = 'h'
	print ('[MAIN]eta ' + str(round(ttbig,2)) + ' ' + dw)
	print ('[MAIN]Open {} Threads To Convent This Files!'.format(AllTheardNumber))
	last = int(len(ncmfiles) % AllTheardNumber)
	avg = int((len(ncmfiles)-last)/AllTheardNumber)
	for ppo in range(0,AllTheardNumber):
		ncmlist =[]
		if ppo == (AllTheardNumber - 1):
			for o in range(int(avg*ppo),int(avg * (ppo+1)+ last)):
				ncmlist.append(ncmfiles[o])
			t[ppo] =threading.Thread(target=MultiThreadChild,args=(ncmlist,ppo),daemon=True)
			t[ppo].start()
			ncmlist = []
		else:
			for o in range(int(avg*ppo),int(avg * (ppo+1) )):
				ncmlist.append(ncmfiles[o])
			t[ppo] =threading.Thread(target=MultiThreadChild,args=(ncmlist,ppo),daemon=True)
			t[ppo].start()
			ncmlist = []
	print ('')
	while(totsong < len(ncmfiles)):
		print ('[MAIN]'+ '[' + time.asctime() +']Prograss: [' +  str(totsong) + '/' + str(len(ncmfiles)) + ']')
		try:
			time.sleep(10)
		except:
			print ('[!]Warning! Main Thread Exit!')
	print ('[MAIN]'+ '[' + time.asctime() +']Prograss: [' +  str(totsong) + '/' + str(len(ncmfiles)) + ']')
	if os.path.getsize('ncm2music_error.txt') < 10:
		os.remove('ncm2music_error.txt')
	print ("[MAIN]ALL Jobs Done!")
	dfgg.close()

