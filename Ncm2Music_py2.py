#!/usr/bin/env python
# -*- coding:utf-8


# Modifier: CRMMC-CreamTes-KGDSave SoftWare Studio 2018-2020'
# Thanks for nondanee
#need a tools use order: pip install pycryptodome mutagen requests urllib3
#to install it!
#it can be used on Windows,Linux,Mac on Python3 or Python2
import binascii
import struct
import base64
import json
import re
import os
import requests
import mutagen.id3
from Crypto.Cipher import AES
from mutagen.mp3 import MP3, EasyMP3 
from mutagen.flac import FLAC
from mutagen.flac import Picture
from mutagen.easyid3 import EasyID3
from mutagen.id3 import COMM,APIC,ID3


def Getlrc(neteaseID):
	lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(neteaseID) + '&lv=1&kv=1&tv=-1'
	lyric = requests.get(lrc_url)
	json_obj = lyric.text
	j = json.loads(json_obj)
	return j



def dump(file_path):
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
    meta_data = unpad(cryptor.decrypt(meta_data)).decode('utf-8')[6:]
    meta_data = json.loads(meta_data)
    # print (meta_data)
    crc32 = f.read(4)
    crc32 = struct.unpack('<I', bytes(crc32))[0]
    f.seek(5, 1)
    image_size = f.read(4)
    image_size = struct.unpack('<I', bytes(image_size))[0]
    image_data = f.read(image_size)
    file_name = meta_data['musicName'] + ' - ' + meta_data['artist'][0][0] + '.' + meta_data['format']
    print('')
    print('')
    print ('Music Info :')
    print ('==========================')
    print ('---Name:' + meta_data['musicName'])
    print ('---Format:'+ meta_data['format'])
    print ('---MusicArtist:' + meta_data['artist'][0][0])
    print ('---MusicBitrate:'+ str(meta_data['bitrate']/1000) + 'kbps')
    print ('---MusicID:'+str(meta_data['musicId']))
    print ('---MusicPIC:'+meta_data['albumPic'])
    print ('==========================')
    if os.path.exists(file_name):
    	#print ('Now [' + file_path +']>>>[' + file_name + ']')
    	print ('File is exist!')
    else:
    	#print ('Now [' + file_path +']>>>[' + file_name + ']')
    	m = open(os.path.join(os.path.split(file_path)[0],file_name),'wb')
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
    print ('[*]Start to SET music tags')
    print ('[-]Now Try to download Music PIC')
    picdata = ''
    music_id = meta_data['musicId']
    music_name = meta_data['musicName']
    music_lrc = meta_data['musicName'] + ' - ' + meta_data['artist'][0][0]
    try:
    	picurl = meta_data['albumPic']
    	picdata = requests.get(picurl).content
    	#print ('Download [' + meta_data['albumPic'] + ']>>>[MP3.JPG]')
    except:
    	print ('[!]Get Picture From Internet Error!')
    if meta_data['format'] == 'mp3':
    	mp3_info = MP3(file_name, ID3=EasyID3)
    	mp3_info['album'] = meta_data['musicName']
    	mp3_info['artist'] = meta_data['artist'][0][0]
    	mp3_info['title'] = meta_data['musicName']
    	mp3_info.save()
    	hh = ID3(file_name)
    	#hh.update_to_v23()
    	hh['APIC:'] = (APIC(mime='image/jpg',  data=picdata))
    	hh.save()
    	print ('[+]MP3 Tag Add Successful!')
    	print ('[+]Music Lyric Getting...')
    	arhhc = Getlrc(music_id)
    	#print (type(arhhc['lrc']['lyric']))
    	if arhhc.has_key('lrc'):
        	try:
        		f = open(music_lrc+'.lrc','w')
        		f.write(str(arhhc['lrc']['lyric'].encode('utf-8')))
        		f.close()
        	except:
        		print ('Error!')
    	if arhhc.has_key('tlyric'):
    		try:
    			l = open(music_lrc+'.tlyric','w')
    			l.write(str(arhhc['tlyric']['lyric'].encode('utf-8')))
    			l.close()
    		except:
        		print ('Error!')
    elif meta_data['format'] == 'flac':
    	print ('[+]Adding Tags....')
    	audio = FLAC(file_name)
    	audio["title"] = meta_data['musicName']
    	audio['album'] = meta_data['musicName']
    	audio['artist'] = meta_data['artist'][0][0]
    	#audio.add_picture(picdata)
    	#audio.pictures.append(picdata)
    	#audio.save()
    	try:
    		audio.save()
    		picfile=meta_data['musicName'] + ' - ' + meta_data['artist'][0][0]+'.jpg'
    		mpic = open(picfile,'w')
    		mpic.write(picdata)
    		mpic.close()
    		print ('[+]Music Image >>>['+picfile+']')
    		print ('[+]Music Lyric Getting...')
    		arhhc = Getlrc(music_id)
    		#print (type(arhhc['lrc']['lyric']))
    		if arhhc.has_key('lrc'):
        		try:
        			f = open(music_lrc+'.lrc','w')
        			f.write(str(arhhc['lrc']['lyric'].encode('utf-8')))
        			f.close()
        		except:
        			print ('Error!')
    		if arhhc.has_key('tlyric'):
    			try:
    				l = open(music_lrc+'.tlyric','w')
    				l.write(str(arhhc['tlyric']['lyric'].encode('utf-8')))
    				l.close()
    			except:
        			print ('Error!')
    	except:
    		print ('[!]FLAC Tags Save Error!')
    		sfnr='title:'+meta_data['musicName']+'#$#' + 'artist:' + meta_data['artist'][0][0] +'#$#' +'album:'+ meta_data['musicName']+ '#$#albumPic:'+meta_data['albumPic']
    		rew =open(file_name+'.songinfo','w')
    		rew.write(sfnr.decode('utf-8'))
    		rew.close()
    		print ('[!]Song Tags Has Been Saved On A SongInfo File!');
    else:
    		print ('[!]Unknow Type:'+meta_data['format'])
if __name__ == '__main__':
	import sys
	import glob
	ncmfiles = glob.glob("*.ncm")
	print ('Running in a '+ sys.platform + ' system')
	n = 0
	try:
		dfgg = open('ncm2music_error.txt','a')
	except:
		print ('Open file error!')
	for ncmf in ncmfiles:
		n = n+ 1
		#dump(ncmf)
		try:
			print ('[MAIN] Task '+ str(1) + ' Running!')
			dump(ncmf)
			print ('[MAIN] Task '+ str(1) + ' running Done!')
		except:
			dfgg.write(ncmf + '##File code Error!')
			continue
	print("[MAIN]ALL Jobs Done!")
	dfgg.close()
