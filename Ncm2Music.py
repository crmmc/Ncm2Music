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
import shutil
import base64
import json
import re
import os
import sys
import glob
import requests
import mutagen.id3
from Crypto.Cipher import AES
from mutagen.mp3 import MP3, EasyMP3 
from mutagen.flac import FLAC
from mutagen.flac import Picture
from mutagen.easyid3 import EasyID3
from mutagen.id3 import COMM,APIC,ID3
errnum = 0
if sys.version_info < (3, 0):
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



def dump(file_path,nm1,nm2):
    global errnum
    errnum = 1
    core_key = binascii.a2b_hex("687A4852416D736F356B496E62617857")
    meta_key = binascii.a2b_hex("2331346C6A6B5F215C5D2630553C2728")
    unpad = lambda s : s[0:-(s[-1] if type(s[-1]) == int else ord(s[-1]))]
    try:
    	f = open(file_path,'rb')
    except:
    	print ('Open File [' + file_path +"] Error! please try to  Delete special characters hit by files!")
    	return -1
    errnum =2
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
    meta_data = unpad(cryptor.decrypt(meta_data)).decode('utf-8')[6:]
    meta_data = json.loads(meta_data)
    crc32 = f.read(4)
    crc32 = struct.unpack('<I', bytes(crc32))[0]
    f.seek(5, 1)
    image_size = f.read(4)
    image_size = struct.unpack('<I', bytes(image_size))[0]
    image_data = f.read(image_size)
    file_name = meta_data['musicName'] + ' - ' + meta_data['artist'][0][0]
    file_name = re.sub('[\/:*?"<>|].','-',file_name)
    file_name = file_name.replace(" ",'-')
    music_lrc = file_name
    file_name = str((file_name + '.' + meta_data['format']).encode('utf-8').decode('utf-8'))
    errnum =3
    if os.path.exists(file_name):
    	print ('[+]Now [' + str(nm1) + '/' + str(nm2) + '][' + str(meta_data['format']) + ']['  + 'MusicID:' + str(meta_data['musicId']) + ']['+ str(meta_data['bitrate']/1000) + 'kbps] [' + str(file_path) +']>>>[' + str(file_name) + ']')
    	print ('[!]File is exist!')
    else:
    	print ('[+]Now [' + str(nm1) + '/' + str(nm2) + '][' + str(meta_data['format']) + ']['  + 'MusicID:' + str(meta_data['musicId']) + ']['+ str(meta_data['bitrate']/1000) + 'kbps] [' + str(file_path) +']>>>[' + str(file_name) + ']')
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
    errnum =4
    picdata = ''
    music_id = meta_data['musicId']
    music_name = meta_data['musicName']
    try:
    	picurl = meta_data['albumPic']
    	picdata = requests.get(picurl).content
    except:
    	print ('[!]Get Picture From Internet Error!')
    if meta_data['format'] == 'mp3':
    	mp3_info = MP3(file_name, ID3=EasyID3)
    	#mp3_info.ID3.update_to_v23()
    	#mp3_info.update()
    	arhhc = Getlrc(music_id)
    	mp3_info['album'] = meta_data['album']
    	mp3_info['artist'] = meta_data['artist'][0][0]
    	mp3_info['title'] = meta_data['musicName']
    	mp3_info['discsubtitle'] = meta_data['alias']
    	try:
    		mp3_info['lyricist'] = str(arhhc['lrc']['lyric'].encode('utf-8'))
    	except:
    		hsvsbs = 'hshs'
    	mp3_info.save()
    	hh = ID3(file_name)
    	hh.update_to_v23()
    	hh.save()
    	hh['APIC:'] = (APIC(mime='image/jpg',  data=picdata))
    	hh.save()
    	errnum =5
    	#print (music_lrc)
    	if 'lrc' in arhhc:
        	try:
        		f = open((music_lrc+'.lrc'),'w')
        		f.write(arhhc['lrc']['lyric'])
        		f.close()
        	except:
        		print ('[!]LRC Get Error!')
    	if 'tlyric' in arhhc:
    		try:
    			l = open((music_lrc+'.tlyric'),'w')
    			l.write(arhhc['tlyric']['lyric'])
    			l.close()
    		except:
        		print ('[!]Tlyric Get Error!')
    	errnum = 6
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
    	#audio.pictures.append(app)
    	#audio.save()
    	try:
    		audio.save()
    		#picfile=meta_data['musicName'] + ' - ' + meta_data['artist'][0][0]+'.jpg'
    		#mpic = open(picfile,'w')
    		#mpic.write(picdata)
    		#mpic.close()
    		#print ('[+]Music Image >>>['+picfile+']')
    		arhhc = Getlrc(music_id)
    		if 'lrc' in arhhc:
        		try:
        			f = open((music_lrc+'.lrc'),'w')
        			f.write(arhhc['lrc']['lyric'])
        			f.close()
        		except:
        			print ('[!]LRC Get Error!')
    		if 'tlyric' in arhhc:
    			try:
    				l = open((music_lrc+'.tlyric'),'w')
    				l.write(arhhc['tlyric']['lyric'])
    				l.close()
    			except:
        			print ('[!]Tlyric Get Error!')
    	except:
    		print ('[!]FLAC Tags Save Error!')
    		sfnr='title:'+meta_data['musicName']+'#$#' + 'artist:' + meta_data['artist'][0][0] +'#$#' +'album:'+ meta_data['musicName']+ '#$#albumPic:'+meta_data['albumPic']
    		rew =open((file_name+'.songinfo').decode('utf-8'),'w')
    		rew.write(sfnr)
    		rew.close()
    		print ('[!]Song Tags Has Been Saved On A SongInfo File!');
    else:
    		print ('[!]Unknow Type:'+meta_data['format'])
    errnum = 0
    return 0
if __name__ == '__main__':
	ncmfiles = glob.glob("*.ncm")
	nm2 =len(ncmfiles)
	nm1 = 0
	print ('[MAIN]Running in a '+ sys.platform + ' system')
	try:
		dfgg = open('ncm2music_error.txt','a')
	except:
		print ('[!]Open log file error!')
	print ('[MAIN]There are ' + str(len(ncmfiles)) + ' Files ')
	ttbig = 0
	try:
		for tii in ncmfiles:
			ttbig = ttbig + os.path.getsize(tii)/1024/1024.0*1.6
	except:
		ttbig = -1
	dw = 's'
	if ttbig > 60:
		ttbig = ttbig / 60.0
		dw = 'min'
		if ttbig > 60:
			ttbig = ttbig / 60.0
			dw = 'h'
	print ('[MAIN]eta ' + str(round(ttbig,2)) + ' ' + dw)
	print ('')
	for ncmf in ncmfiles:
		#dump(ncmf,nm1,nm2)
		try:
			nm1 = nm1 + 1
			#print ('[MAIN] Task '+ str(nm1) + ' Running!')
			dump(ncmf,nm1,nm2)
			#print ('[MAIN] Task '+ str(nm1) + ' running Done!')
		except:
			dfgg.write(ncmf +'##File code Error!'+ "  ErrorCode:"+ str(errnum) + "\n")
			fpath = "./ERRORFILES"
			if not os.path.exists(fpath):
				os.makedirs(fpath)
				shutil.move(ncmf,fpath + "/" + ncmf)          
				print ('move [ ' + ncmf + ' ]->[ ' + fpath + "/" + ncmf + ' ]')
				continue
	print("[MAIN]ALL Jobs Done!")
	dfgg.close()
