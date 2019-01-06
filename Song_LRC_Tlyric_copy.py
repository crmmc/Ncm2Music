#!/bin/env python2
import os,glob,re

def turnname():
	for t in glob.glob('*.lyric'):
		os.system('mv "' + t + '" "' + t.replace('.lyric','') + '.ylc"')  #os.rename(t,t.replace('.lrc1','') + '.ylc')
	for y in glob.glob('*.tlyric'):
		os.system('mv "' + y + '" "' + y.replace('.tlyric','') + '.tlc"')  #os.rename(y,y.replace('.tlyric','') + '.tlc')
		
		
def gtm(gyy):
	return re.findall(r'\[(.*?)\]',gyy)
	
def lrcTOlyric():
	for y in glob.glob('*.lrc'):
		os.system('mv "' + y + '" "' + y.replace('.lrc','') + '.lyric"')
	
def hebing(songname):
	ty1 = songname + '.ylc'
	ty2 = songname + '.tlc'
	ttty= open(songname + '.lrc','w')
	tt1 = open(ty1,'r').read()
	tt2 = open(ty2,'r').read()
	yn = tt2.split("\n")
	for yu in tt1.split("\n"):
		gh = ""
		for i in yn:
			if gtm(i) == gtm(yu):
				ttty.write(yu +"\n" + i + "\n")
				#print (yu +"\n" + i)
	ttty.close()
	try:
		os.remove(ty1)
		os.remove(ty2)
	except:
		print ('REMOVE ' + ty1 + ' & ' + ty2 + ' FAILD!')
#lrcTOlyric()
turnname()
for i in glob.glob('*.tlc'):
	hhiu = i.replace('.tlc','')
	if os.path.exists(hhiu + '.ylc'):
		hebing(hhiu)
	print ('[' + hhiu + '] ===> [' + hhiu + '.lrc]')
print ('Turning Names.....')
for u in glob.glob('*.lrc'):
	for o in glob.glob('*.mp3'):
		nj = u.replace('.lrc','')
		if o.find(nj):
			uj = o.replace('.mp3','') + '.lrc'
			print ('[' + nj + '.lrc]>>>[' + uj + ']')
			os.rename(nj + '.lrc',uj)
		else:
			for o in glob.glob('*.flac'):
				nj = u.replace('.lrc','')
				if o.find(nj):
						uj = o.replace('.flac','') + '.lrc'
						print ('[' + nj + '.lrc]>>>[' + uj + ']')
						os.rename(nj + '.lrc',uj)
print ('All Done!')