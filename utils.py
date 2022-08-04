#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import re
import json
import shutil
import hashlib
import zlib
import subprocess
import platform

import gl

# 加载JSON文件
def LoadJSON(filename):
	if not os.path.isfile(filename):
		SaveJSON(filename, {}, True)
	with open(filename) as json_file:
		conf = json.load(json_file)
		return conf


# 保存JSON文件
def SaveJSON(filename, conf, can):
	with open(filename, 'w') as json_file:
		if can:
			json_file.write(json.dumps(conf))
		else:
			json_file.write(json.dumps(conf))


# log
def Log(type, msg):
	if platform.system() == "Windows":
		try:
			if gl.DEBUG:
				print(msg)
			else:
				print(msg.decode('utf-8').encode('gb2312'))
		except UnicodeDecodeError as err:
			print(msg)


def Debug(msg):
	Log(0, msg)


def Warning(msg):
	Log(1, msg)


def Info(msg):
	Log(2, msg)


# 计算文件MD5
def GetFileMD5(filename):
	if not os.path.isfile(filename): return
	myhash = hashlib.md5()
	f = file(filename, 'rb')
	while True:
		b = f.read(8096)
		if not b:
			break
		myhash.update(b)
	f.close()
	return myhash.hexdigest()


# 计算文件CRC
def GetFileCRC32(filename):
	if not os.path.isfile(filename): return ""
	with open(filename, "rb") as f:
		return '%x' % (zlib.crc32(f.read()) & 0xFFFFFFFF)


# 执行命令
def Call(code, filter=""):
	p = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.communicate()
	err = p.stderr.read()
	if err == "Everything up-to-date\n":
		err = ""
	with open(gl.LOGFILE, 'w') as log:
		if filter != "":
			log.write(re.sub(filter, "", p.stdout.read()))
			if err != "":
				err = re.sub(filter, "", err)
		else:
			log.write(p.stdout.read())
		if err != "":
			log.write(err)
			err = re.sub("remote:(.*?)\n", "", err)
			err = re.sub("To (.*?).git\n", "", err)
			err = re.sub("   (.*?)master\n", "", err)
			err = re.sub("From \n", "", err)
			err = re.sub("Cloning into(.*?)...\n", "", err)
			if err != "":
				Warning(err)
	return err == ""


# 更新进度
def Progress(p, m):
	if p > m:
		p = m
	strlen = 60.0
	c = (float(p) / float(m)) * strlen
	pstr = "\r%s%s [%d%%]\r" % (int(c) * '>', int(strlen - c) * '-', int(c / strlen * 100))
	sys.stdout.write(pstr)
	sys.stdout.flush()


# 清空目录
def EmptyTree(src, filter):
	filter.extend([".git", ".svn", ".gitignore", "Readme.md"])
	srcs = os.path.expanduser(src)
	if not os.path.exists(srcs):
		os.mkdir(srcs)
	windows = platform.system() == "Windows"
	for f in os.listdir(srcs):
		if not f.strip() in filter:
			file = os.path.join(src, f)
			if os.path.isdir(file):
				if windows:
					DelDir_windows(file)
				else:
					shutil.rmtree(file)
			else:
				if windows:
					DelFile_windows(file)
				else:
					os.remove(file)

# windows del file
def DelDir_windows(dir):
	subprocess.call(["rd", "/s", "/q", dir.replace('/', '\\')], shell=True)

# windows del dir
def DelFile_windows(file):
	subprocess.call(["del", "/f", "/q", file.replace('/', '\\')], shell=True)

# 复制目录
def CopyTree(src, tar, filter):
	EmptyTree(tar, filter)
	srcs = os.path.expanduser(src)
	for f in os.listdir(srcs):
		file = os.path.join(src, f)
		if os.path.isdir(file):
			shutil.copytree(file, os.path.join(tar, f))
		else:
			shutil.copyfile(file, os.path.join(tar, f))


# 由文件的crc32重命令文件
def CrcFile(file):
	crcName = GetFileCRC32(file)
	if crcName != "":
		pf = file.rfind('.')
		if pf > 0:
			thmNewFile = file[:pf] + '_' + crcName + file[pf:]
			os.rename(file, thmNewFile)
	return crcName


# 重命名指定目录下的所有文件
def CrcDir(src, maps, filter):
	srcs = os.path.expanduser(src)
	for f in os.listdir(srcs):
		name = f.strip()
		if name not in filter:
			file = os.path.join(src, f)
			if os.path.isdir(file):
				CrcDir(file, maps, filter)
			else:
				crcName = CrcFile(file)
				pf = name.rfind('.')
				maps[name] = name[:pf] + '_' + crcName + name[pf:]
