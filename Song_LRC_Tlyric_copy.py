#!/bin/env python
#coding=utf-8
import os,glob,re,chardet,sys

def delname():
	print ('del empty files!')
	for r in glob.glob('*'):
		if os.path.getsize(r) < 32:
			os.remove(r)
			print ('[' + r + '] Delete !')

def MV(sfrom,sto):
	if len(sfrom) < 0:
		return 2
	if sys.platform.find("win") > -1:
		return os.system('move "' + sfrom + '" "' + sto + '"')
	elif sys.platform.find("linux") > -1:
		return os.system('mv "' + sfrom + '" "' + sto + '"')
	return 1  

def turnname():
	print ('ALL lrc to ylc')
	for t in glob.glob('*.lrc'):
		MV(t,t.replace('.lrc','') + '.ylc"')  #os.rename(t,t.replace('.lrc1','') + '.ylc')
	print ('ALL Tlrc to tlc')
	for y in glob.glob('*.tlyric'):
		MV(y,y.replace('.tlyric','') + '.tlc"')  #os.rename(y,y.replace('.tlyric','') + '.tlc')
		
		
def gtm(gyy):
	return re.findall(r'\[(.*?)\]',gyy)
	
def last():
	for y in glob.glob('*.ylc'):
		MV( y,y.replace('.ylc','.lrc"'))
	for y in glob.glob('*.tlc'):
		MV(y,y.replace('.tlc','.lrc"'))

def hebing(songname):
	ty1 = songname + '.ylc'
	ty2 = songname + '.tlc'
	print ('TURNING  :' + ty1 + '  ' + ty2)
	ttty= open(songname + '.lrc','w')
	tt1 = open(ty1,'r').read()
	tt2 = open(ty2,'r').read()
	yn = tt2.split("\n")
	for yu in tt1.split("\n"):
		gh = ""
		for i in yn:
			try:
				if (gtm(i) == gtm(yu)) or (str(gtm(i)[0]) + '0' == str(gtm(yu)[0])) or (str(gtm(i)[0]) == str(gtm(yu)[0]) + '0') or (gtm(i)[0] == gtm(yu)[0]):
					ttty.write(yu +"\n" + i + "\n")
					#print (yu +"\n" + i)
				else:
					#print (gtm(i)[0] + ' <> ' + gtm(yu)[0])
					continue
			except:
				continue
	ttty.close()
	try:
		if os.path.getsize(songname + '.lrc') > (os.path.getsize(songname + '.ylc')/2):
			os.remove(ty1)
			os.remove(ty2)
		else:
			print ('Error!	' + ty1)
			os.remove(songname + '.lrc')
	except:
		print ('REMOVE ' + ty1 + ' & ' + ty2 + ' FAILD!')

delname()
turnname()
#os.system('clear')
for i in glob.glob('*.ylc'):
	hhiu = i.replace('.ylc','')
	if os.path.exists(hhiu + '.tlc'):
		hebing(hhiu)
		print ('[' + hhiu + '] ===> [' + hhiu + '.lrc]')

delname()
last()
print ('All Done!')
