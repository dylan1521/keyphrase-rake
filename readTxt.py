import re
import os.path


#找出当前文件夹下的所有子文件夹
def eachFile(dirpath):
	pathDir = os.listdir(dirpath)
	dirList = []
	for childDir in pathDir:
		child = os.path.join(dirpath,childDir)
		if os.path.isdir(child):
			dirList.append(child)
	return dirList

#读取子文件夹中每篇文档，并写入allWords中
def readFile(filepath):
	files = os.listdir(filepath)
	for filename in files:
		with open(os.path.join(filepath,filename),'r') as f:
			orignTxt = f.read().split()
			txt = []
			for i in range(len(orignTxt)):
				# if orignTxt[i]==('Item' or 'ITEM')  and orignTxt[i+1]=="2.":
				# 	break	
				# else:
					txt.append(orignTxt[i])
			# print (len(txt))
			txt = " ".join(txt)
		with open(os.path.join(filepath,r"allWords.txt"),'a') as f:
			f.write(txt)

# print (os.listdir(r'E:\company\40companies\ADMA'))
# readFile(r'E:\company\40companies\ADMS')

#将file merge在一起，写成class,dirpath是文件夹路径
class fileMerge(object):
	"""docstring for readfile"""
	def __init__(self):
		pass
	def read(self,dirpath):
		dirList = eachFile(dirpath)
		filedir = []
		for filelist in dirList:
			filedir.append(filelist)
			# readFile(filelist)
		return filedir
# merge = fileMerge()
# print (merge.read(r'E:\company\40companies'))



