<h1>Netease Cloud Music Copyright Protection File Dump (Python version)</h1>

<h2>简介</h2>


<p>Python版本解密ncm文件，根据贴吧某位大神的源码再开发而来，加了很多使用功能，比如嵌入歌曲tags和封面图片(flac嵌入图片有问题，但是保存为同名文件播放器是可以识别的,想要嵌入文件的童鞋可以自己琢磨一下mutagen库)还有下载歌词啥的。</p>


<h3>依赖 pycrypto库</h3>

<code>pip(3) install pycrypto</code>
推荐使用下面的库！不安装上面的库
<code>pip3 install -i https://pypi.douban.com/simple pycryptodome</code>
嘤嘤嘤，嫌弃官方源太慢可以自行百度国内pypi源然后更换
使用<code>pip install pycryptodome mutagen requests urllib3</code>来安装依赖库

<h3>使用方法：</h3>
直接将Ncm2Music.py复制到有.ncm文件的文件夹里运行即可。

<h3>文件列表:</h3>
<p>-----Ncm2Music.py 程序主体，推荐使用pyinstaller编译出来使用，直接运行于python2和3中</p>
<p>-----Ncm2Music_py2.py 此版本显示的歌曲信息更详细，没啥区别,但是这个版本我维护的不是很频繁，不推荐使用。</p>
<p>-----ncmdump.py 某贴吧大神的ncm文件转换器，此文件是源代码，上传供大家使用，代码来源可以在github上搜ncmdump这个项目</p>
<p>-----lrcget.py 根据网易云歌曲ID来获取歌词的源码，上传供大家使用，原理来自互联网。</p>
<p>-----SongList_LRC_Getter.py 获取一个歌单里所有歌曲的歌词，可以单独使用来获取歌词，普通歌词保存为lrc翻译歌词保存为tlyric</p>
<p>-----README.md 说明文件</p>

copyright 2018-2020 KGDSAVE SOFTWARE STUDIO - CRMMC 