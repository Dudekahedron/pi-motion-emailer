import os,glob,time
#these are identical because I have no idea what I'm doing
def current():
	current = max(glob.iglob(os.path.join('/media/pi/EXTSD/Security','*.jpg')),key=os.path.getctime)
	return current
def newest():
	newest = max(glob.iglob(os.path.join('/media/pi/EXTSD/Security','*.jpg')),key=os.path.getctime)
	return newest
#basic identification confirmation, no doubt an awful way to do this
while True:
	cur=current()
	while True:
		new=newest()
		if new==cur:
			time.sleep(0.1)
			print('these files are identical')
		else:
			time.sleep(0.1)
			print('these files are different')
			break
