#!/usr/bin/env python
#coding=utf-8
# Modifier: CRMMC-CreamTes-KGDSave SoftWare Studio 2018-2020'
# Thanks for nondanee
#need a tools use order: pip install pycryptodome mutagen requests urllib3 pillow
#to install it!
#it can be used on Windows,Linux,Mac on Python3
#////////////////////////////////;
#This variable defines the number of threads
#Its value is four by default.
#It is recommended to change the value to (CPU cores-1) * 2
AllTheardNumber = 8
#Please be careful to change the following, it may prevent the program from running again
#///////////////////////////////;
import binascii
import struct
import base64
import json
import time
from multiprocessing import Process
import multiprocessing
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
from PIL import Image

def sOUT(text):
    sys.stdout.write(text)
    sys.stdout.flush()

def EOut(text):
    try:
        d = open('ncm2music_error.txt','a')
        d.write(text)
        d.close()
    except:
        print ('[!]Open log file error!')
    return 0
    
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

def GetLrcF(id,sname):
    try:
        lrc_url = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(id) + '&lv=-1&kv=-1&tv=-1'
        #lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(id) + '&lv=1&kv=1&tv=-1'
        lyric = requests.get(lrc_url,headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 10; Redmi K20 Pro MIUI/V11.0.4.0.QFKCNXM)','Host':'music.163.com'})
        json_obj = lyric.text
        arhhc = json.loads(json_obj)
    except:
        print ('Get lrc error!')
        EOut('ERROR_IN_GET_HTML_lyric_tlyric:'+music_name+"\n")
        return ''
    try:
        if len(arhhc['lrc']['lyric']) < 10:
            return -1
    except:
        EOut('ERROR_IN_GET_ALL_lyric_tlyric:'+music_name+"\n")
    if 'tlyric' in arhhc:
        if 'lyric' in arhhc['tlyric']:
            tolrc = TwoToOne(str(arhhc['lrc']['lyric']),str(arhhc['tlyric']['lyric']))
        else:
            tolrc = str(arhhc['lrc']['lyric'])
    else:
        tolrc = str(arhhc['lrc']['lyric'])
    try:
        open(sname + '.lrc' ,'w').write(tolrc)
        print ('[Lyric] Get [' + sname + '] Successful!')
    except:
        EOut('ERROR_IN_WRITE_ALL_lyric_tlyric:'+music_name+"\n")
            
def CFG(a):
    return a.replace('：','').replace('[','').replace(']','').replace('。','').replace('？','').replace('，','').replace('“','').replace('”','').replace('"','').replace("'",'').replace(':','_').replace('/','').replace('?','')

#网易云音乐解密源码 开始
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
    file_name = CFG(file_name)
    if os.path.exists(file_name):
        print ("\n" + '[+][Process:{}]Now '.format(Thnom) + '[' + str(meta_data['format']) + ']['  + 'MusicID:' + str(meta_data['musicId']) + ']['+ str(meta_data['bitrate']/1000) + 'kbps] [' + str(file_path) +']>>>[' + str(file_name) + ']')
        print ('[!]File is exist!')
        if (os.path.getsize(file_name) < (os.path.getsize(file_path) - (3*1024))):
            print ('[!]Bad File!')
            DelFile(file_name)
            dump(file_path,Thnom)
            return 0
    else:
        print ("\n" + '[+][Process:{}]Now '.format(Thnom) + '[' + str(meta_data['format']) + ']['  + 'MusicID:' + str(meta_data['musicId']) + ']['+ str(meta_data['bitrate']/1000) + 'kbps] [' + str(file_path) +']>>>[' + str(file_name) + ']')
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
    music_id = meta_data['musicId']
    music_name = file_name.split(' - ')[0]
    music_lrc = file_name.replace('.' + str(meta_data['format']),'')
    if len(image_data) < 1000:
        try:
            picurl = meta_data['albumPic']
            image_data = requests.get(picurl).content
            print ('Album Picture Getted! Convent to type jpeg')
            f = BytesIO()
            image_data = Image.open(io.BytesIO(image_data)).save(f,'jpeg')
            image_data = f.getvalue()
        except:
            print ("\n" + '[!][Process:{}][{}]Get Picture From Internet Error!'.format(Thnom,file_path))
    if meta_data['format'] == 'mp3':
        mp3_info = MP3(file_name, ID3=EasyID3)
        mp3_info['album'] = meta_data['album']
        mp3_info['artist'] = meta_data['artist'][0][0]
        mp3_info['title'] = meta_data['musicName']
        mp3_info['discsubtitle'] = meta_data['alias'] 
        #mp3_info['lyricist'] = str(arhhc['lrc']['lyric'])
        mp3_info['lyricist'] = str('Convent By Ncm2Music. CopyRight 2018-2019. KGDsave SoftWare Studio')
        mp3_info.save()
        hh = ID3(file_name)
        hh.update_to_v23()
        hh.save()
        hh['APIC:'] = (APIC(data=image_data))
        hh['APIC:'] = (APIC(mime='image/jpeg',  data=image_data))
        try:
            hh.save()
        except:
            open(music_lrc+'.jpg','wb').write(image_data)
            print ("\n" + '[![Process{} : [{}]MP3 Tags Save Error!'.format(Thnom,file_path))
        try:
            GetLrcF(music_id,music_lrc)
        except:
            print ('MP3 Lyric Get Error!')
    elif meta_data['format'] == 'flac':
        audio = FLAC(file_name)
        audio["title"] = meta_data['musicName']
        audio['album'] = meta_data['album']
        audio['artist'] = meta_data['artist'][0][0]
        audio['comment'] = meta_data['alias']
        app = Picture()
        app.data = image_data
        app.type = mutagen.id3.PictureType.COVER_FRONT 
        app.mime = "image/jpeg"
        audio.add_picture(app)
        try:
            audio.save()
        except:
            sfnr='title:'+meta_data['musicName']+'#$#' + 'artist:' + meta_data['artist'][0][0] +'#$#' +'album:'+ meta_data['musicName']+ '#$#albumPic:'+meta_data['albumPic']
            open((file_name+'.songinfo'),'w').write(sfnr)
            open(music_lrc+'.jpg','wb').write(image_data)
            print ('[!][Process:{}][{}]Song Tags Has Been Saved On A SongInfo File!'.format(Thnom,file_path));
        try:
            GetLrcF(music_id,music_lrc)
        except:
            print ('[!][Process:{}][{}]FLAC lyric Get Error!'.format(Thnom,file_path))
    else:
            print ("\n" + '[!][Process:{}]Unknow Type:'.format(Thnom)+meta_data['format'])
#网易云音乐 解密源码 结束

#QQ音乐解密源码
#开始
def QQmapL(v):
    key = [0x77, 0x48, 0x32, 0x73, 0xDE, 0xF2, 0xC0, 0xC8, 0x95, 0xEC, 0x30, 0xB2,
        0x51, 0xC3, 0xE1, 0xA0, 0x9E, 0xE6, 0x9D, 0xCF, 0xFA, 0x7F, 0x14, 0xD1,
        0xCE, 0xB8, 0xDC, 0xC3, 0x4A, 0x67, 0x93, 0xD6, 0x28, 0xC2, 0x91, 0x70,
        0xCA, 0x8D, 0xA2, 0xA4, 0xF0, 0x08, 0x61, 0x90, 0x7E, 0x6F, 0xA2, 0xE0,
        0xEB, 0xAE, 0x3E, 0xB6, 0x67, 0xC7, 0x92, 0xF4, 0x91, 0xB5, 0xF6, 0x6C,
        0x5E, 0x84, 0x40, 0xF7, 0xF3, 0x1B, 0x02, 0x7F, 0xD5, 0xAB, 0x41, 0x89,
        0x28, 0xF4, 0x25, 0xCC, 0x52, 0x11, 0xAD, 0x43, 0x68, 0xA6, 0x41, 0x8B,
        0x84, 0xB5, 0xFF, 0x2C, 0x92, 0x4A, 0x26, 0xD8, 0x47, 0x6A, 0x7C, 0x95,
        0x61, 0xCC, 0xE6, 0xCB, 0xBB, 0x3F, 0x47, 0x58, 0x89, 0x75, 0xC3, 0x75,
        0xA1, 0xD9, 0xAF, 0xCC, 0x08, 0x73, 0x17, 0xDC, 0xAA, 0x9A, 0xA2, 0x16,
        0x41, 0xD8, 0xA2, 0x06, 0xC6, 0x8B, 0xFC, 0x66, 0x34, 0x9F, 0xCF, 0x18,
        0x23, 0xA0, 0x0A, 0x74, 0xE7, 0x2B, 0x27, 0x70, 0x92, 0xE9, 0xAF, 0x37,
        0xE6, 0x8C, 0xA7, 0xBC, 0x62, 0x65, 0x9C, 0xC2, 0x08, 0xC9, 0x88, 0xB3,
        0xF3, 0x43, 0xAC, 0x74, 0x2C, 0x0F, 0xD4, 0xAF, 0xA1, 0xC3, 0x01, 0x64,
        0x95, 0x4E, 0x48, 0x9F, 0xF4, 0x35, 0x78, 0x95, 0x7A, 0x39, 0xD6, 0x6A,
        0xA0, 0x6D, 0x40, 0xE8, 0x4F, 0xA8, 0xEF, 0x11, 0x1D, 0xF3, 0x1B, 0x3F,
        0x3F, 0x07, 0xDD, 0x6F, 0x5B, 0x19, 0x30, 0x19, 0xFB, 0xEF, 0x0E, 0x37,
        0xF0, 0x0E, 0xCD, 0x16, 0x49, 0xFE, 0x53, 0x47, 0x13, 0x1A, 0xBD, 0xA4,
        0xF1, 0x40, 0x19, 0x60, 0x0E, 0xED, 0x68, 0x09, 0x06, 0x5F, 0x4D, 0xCF,
        0x3D, 0x1A, 0xFE, 0x20, 0x77, 0xE4, 0xD9, 0xDA, 0xF9, 0xA4, 0x2B, 0x76,
        0x1C, 0x71, 0xDB, 0x00, 0xBC, 0xFD, 0xC,  0x6C, 0xA5, 0x47, 0xF7, 0xF6,
        0x00, 0x79, 0x4A, 0x11]
    if v >= 0:
        if v > 32767:
            v %= 32767
    else:
        v = 0
    return key[(v * v + 80923) % 256]

def QQconvert(fin,RNUM):
    fou = fin.split('.')[-1]
    if fou == 'qmcflac':
        fout = fin.replace('qmcflac','flac').replace(' [mqms2]','')
    elif fou == 'qmc0' or fou == 'qmc3':
        fout = fin.replace('qmc0','mp3').replace('qmc3','mp3').replace(' [mqms2]','')
    else:
        print ('Not A QQMusic File!')
        return -1
    del (fou)
    print ('Process {}: Decrypting {} --> {}'.format(fin,RNUM,fout))
    afi = open(fin,'rb')
    afo = open(fout,'wb')
    all = afi.read()
    ab1 = bytearray(all)
    del(all)
    for i in range(0,len(ab1)):
        ab1[i] ^= QQmapL(i)
    afo.write(ab1)
    del(ab1)
    afi.close()
    afo.close()
    print ('Process {}: Done decrypt {} --> {}'.format(fin,RNUM,fout))
    return 0

#QQ音乐解密源码 结束

def MultiThreadChild(list,Number):
    print ("\n" + '[+][Process:{}] Process Ready! Get Task: {}'.format(Number,len(list)))
    time.sleep(Number)
    for music1f in list:
        try:
            if music1f.split('.')[-1] == 'ncm':
                dump(music1f,Number)
            else:
                QQconvert(music1f,Number)
        except:
            EOut(music1f +'##File code Error!'+ "\n")
            continue
    print ("\n" + '[+][Process {} :Task Finish!'.format(Number))

def delname():
    print ('del empty files!')
    for r in glob.glob('*'):
        if os.path.getsize(r) < 32:
            try:
                os.remove(r)
                print ('[' + r + '] Delete !')
            except:
                print ('[' + r + '] Delete Error!')

def gtm(gyy):
    return re.findall(r'\[(.*?)\]',gyy)
    
if __name__ == '__main__':
    multiprocessing.freeze_support()
    print ('*')
    print (' _  _          ___ __  __         _')
    print ('| \| |__ _ __ |_  )  \/  |_  _ __(_)__')
    print ("| .` / _| '  \ / /| |\/| | || (_-< / _|")
    print ('|_|\_\__|_|_|_/___|_|  |_|\_,_/__/_\__|')
    print ('===============================')
    print ('CopyRight 2020-2021 KGDSAVE SOFTWARE STUDIO')
    print ('Coded by CRMMC')
    print ('Sources: github.com/crmmc/Ncm2Music')
    print ('This is a tool to convent ncm file to music ')
    print ('add Music tags and get lyric,picture')
    print (' And it can only convent qmc0,qmc3 and qmcflac to music')
    print ('===============================')
    print ('Time: ' + time.asctime())
    time.sleep(2)
    ncmfiles = glob.glob("*.ncm") + glob.glob('*.qmc3') + glob.glob('*.qmcflac') + glob.glob('*.qmc0')
    if len(ncmfiles) < 1:
        print ('[MAIN]Netease Music or QQMusic Files No Found!')
        os._exit(0)
    if len(ncmfiles) < AllTheardNumber:
        AllTheardNumber = len(ncmfiles)
    t=[0,]*AllTheardNumber
    print ('[MAIN]Running in a '+ sys.platform + ' system')
    print ('[MAIN]There are ' + str(len(ncmfiles)) + ' Files ')
    print ('[MAIN]Open {} Processes To Convent This Files!'.format(AllTheardNumber))
    print ('[MAIN]Press "Ctrl + c" to stop convent')
    last = int(len(ncmfiles) % AllTheardNumber)
    avg = int((len(ncmfiles)-last)/AllTheardNumber)
    for ppo in range(0,AllTheardNumber):
        ncmlist =[]
        if ppo == (AllTheardNumber - 1):
            for o in range(int(avg*ppo),int(avg * (ppo+1)+ last)):
                ncmlist.append(ncmfiles[o])
            t[ppo] =Process(target=MultiThreadChild,args=(ncmlist,ppo),)
            t[ppo].daemon=True
            t[ppo].start()
            ncmlist = []
        else:
            for o in range(int(avg*ppo),int(avg * (ppo+1) )):
                ncmlist.append(ncmfiles[o])
            t[ppo] =Process(target=MultiThreadChild,args=(ncmlist,ppo),)
            t[ppo].daemon=True
            t[ppo].start()
            ncmlist = []
    nnu = 0
    time.sleep(2)
    print ('[Main] Waiting until All Process Finish!')
    try:
        for k in t:
            k.join()
    except:
        print ('[!]Warning! Main Thread Exit!')
    print ('[MAIN]'+ '[' + time.asctime() +']')
    if os.path.exists('ncm2music_error.txt'):
        if os.path.getsize('ncm2music_error.txt') < 10:
            DelFile('ncm2music_error.txt')
        else:
            print ('Please see -> ncm2music_error.txt <- Log file!')
    delname()
    print ("[MAIN]ALL Jobs Finish!")

