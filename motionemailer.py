import os,glob

#these are identical because I have no idea what I'm doing
def current():
	current = max(glob.iglob(os.path.join('/media/pi/EXTSD/Security','*.jpg')),key=os.path.getctime)
	return current
def newest():
	newest = max(glob.iglob(os.path.join('/media/pi/EXTSD/Security','*.jpg')),key=os.path.getctime)
	return newest
