import glob,os
print 'Turning Names.....'
for u in glob.glob('*.tlyric'):
	os.rename(u,u.replace('.tlyric','.tlc'))
	print '[' + u + ']<<<>>>[' + u.replace('.tlyric','.tlc') + ']'
for i in glob.glob('*.mp3'):
	hg = i.split('.')[0].split(' - ')
	if len(hg) == 2:
		sn = hg[1].split('.')[0] + '.lrc'
		snd = i.split('.')[0] + '.lrc'
		an = hg[1].split('.')[0] + '.tlc'
		anr = i.split('.')[0] + '.tlc'
		if os.path.exists(sn):
			print ('[' + sn + ']>>>[' + snd + ']')
			os.rename(sn,snd)
		if os.path.exists(an):
			print ('[' + an + ']>>>[' + anr + ']')
			os.rename(an,anr)
print 'MP3 Lyric Turn Done!'
for i in glob.glob('*.flac'):
	hg = i.split('.')[0].split(' - ')
	if len(hg) == 2:
		sn = hg[1].split('.')[0] + '.lrc'
		snd = i.split('.')[0] + '.lrc'
		an = hg[1].split('.')[0] + '.tlc'
		anr = i.split('.')[0] + '.tlc'
		if os.path.exists(sn):
			print ('[' + sn + ']>>>[' + snd + ']')
			os.rename(sn,snd)
		if os.path.exists(an):
			print ('[' + an + ']>>>[' + anr + ']')
			os.rename(an,anr)
print 'FLAC Lyric turn done!'