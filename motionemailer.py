# minor style stuff: pep8 suggests keeping imports on separate lines, probably so they are easy to comment out
# in IDE's with keyboard shortcuts like ctrl+/, and so that debuggers will execute each line independently instead of all at once
#
# Good to know, I will do it this way.

import os
import glob
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# if the function is the same, only define it once, then call it wherever you need it. I've deleted the second copy, and
# will only use the first below. I also gave it a more descriptive name.

def get_most_recent_file():

	# you use os.path.join, but you also use the path separator character in your paths (in unix, "/")
	# if you care about portability, you should
	# os.path.join('media', 'pi', 'EXTSD', 'Security', '*.jpg')
	# however, in this case, I don't think you do, so you can just use the raw string and forget about os.path
	#
	# without using os.path.join I seem to be unable to get a filepath to use later in the attachment part of the email code
	#
	# IDEA though! I think I could use the absolute path only once in the attachment=, trying that.
	#
	# IT WORKED!
	
	current = max(glob.iglob('/media/pi/EXTSD/Security/*.jpg'), key=os.path.getctime)
	return current

# instructions to send email with attachment if a new file is found

fromaddr="RPi.Dudek@GMail.com"

# I had a hell of a time figuring out os.environ
# so currently rc.local runs a short script that imports os, then sets os.environ['gmail_password']='password'

frompass=os.environ["gmail_password"]
toaddr="StanleyRussellDudek@GMail.com"
msg=MIMEMultipart()
msg['From']=fromaddr
msg['To']=toaddr
msg['Subject']="Motion Detected!"

# OK, a more or less "opinions" change that I would make here:
# two while loops is not really necessary, and kind of clouds up what's actually happening.
# You can accomplish the same thing with a single loop, and simply updating initial_file anytime it changes, and never breaking the loop
#
# This is good and I will implement it.

initial_file = get_most_recent_file()

# for the record: python linters will complain if you use while True, as the compiled bytecode for `while 1` executes faster
# http://stackoverflow.com/questions/3815359/while-1-vs-for-whiletrue-why-is-there-a-difference
# however, for simple programs like this, I'm of the opinion that readability > minor execution efficiency 
#
# Just for best practice, I'll learn to do this.

while 1:

	# you can skip a lot of work here by moving the file read into the else block
	
	current_file = get_most_recent_file()
	if initial_file == current_file:
	
		# simply waiting for a new file to be found
		
		time.sleep(0.1)
	else:
	
		# to make sure we don't try to process this again, set initial_file to current_file
		# and next loop we'll hit the if condition and sleep
		#
		# I like the way this works.
		
		initial_file = current_file		
		attachment=open('/media/pi/EXTSD/Security/'current_file,"rb")
		
		# have a new file, send it
		# not sure why casting to string here, but I'll leave it
		# you can use os.path here, though:
		#
		# str no longer necessary, I thought I had to have it to use .replace
		
		filename=current_file
		filename=os.path.basename(filename)
		
		# also inconsistently using new vs filename; so, changed to more consistent
		#
		# Thanks!
		
		motiontime = filename.replace('_',':')
		
		# basename again
		
		motiontime = os.path.basename(motiontime)
		motiontime = motiontime.replace('.jpg','')
		body='Your Raspberry Pi has detected motion at '+motiontime+'!'
		msg.attach(MIMEText(body,'plain'))
		part=MIMEBase('application','octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition',"attachment; filename= %s"%filename)
		msg.attach(part)
		server=smtplib.SMTP('smtp.gmail.com',587)
		server.starttls()
		
		# gmail password, or app password if 2-factor is enabled
		# 
		# a common pattern for using plaintext passwords in code is to save them as environment variables
		# either injected at runtime securely by some kind of CI system, or if you're just running it on
		# your local machine, maybe exported in a ~/.bashrc file, e.g. 
		# export gmail_password="<password>"
		# then you can load the password by using os.environ, and not have to worry about accidentally
		# checking in your passwords to github
		
		server.login(fromaddr, frompass)
		text=msg.as_string()
		server.sendmail(fromaddr,toaddr,text)
		server.quit()
