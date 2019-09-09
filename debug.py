import os

def isDebug():
	return not os.path.isdir("/home/pi")