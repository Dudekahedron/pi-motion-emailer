# minor style stuff: pep8 suggests keeping imports on separate lines, probably so they are easy to comment out
# in IDE's with keyboard shortcuts like ctrl+/, and so that debuggers will execute each line independently instead of all at once
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
	current = max(glob.iglob('/media/pi/EXTSD/Security/*.jpg'), key=os.path.getctime)
	return current

#instructions to send email with attachment if a new file is found
fromaddr="sender email"
toaddr="reciever email"
msg=MIMEMultipart()
msg['From']=fromaddr
msg['To']=toaddr
msg['Subject']="Motion Detected!"


# I'm not really sure about the double loop thing, but if I try to fix it in this commit, the diff will look ugly, so
# here's my first round of comments
while True:
	initial_file = get_most_recent_file()
	while True:
		# you can skip a lot of work here by moving the file read into the else block
		current_file = get_most_recent_file()
		if initial_file == current_file:
			# simply waiting for a new file to be found
			time.sleep(0.1)
		else:
			# have a new file, send it
			# not sure why casting to string here, but I'll leave it
			filename=str(current_file)
			# you can use os.path here, though:
			filename=os.path.basename(filename)
			attachment=open(filename,"rb")
			# also inconsistently using new vs filename; so, changed to more consistent
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
			#gmail password, or app password if 2-factor is enabled
			# a common pattern for using plaintext passwords in code is to save them as environment variables
			# either injected at runtime securely by some kind of CI system, or if you're just running it on
			# your local machine, maybe exported in a ~/.bashrc file, e.g. 
			# export gmail_password="<password>"
			# then you can load the password by using os.environ, and not have to worry about accidentally
			# checking in your passwords to github
			server.login(fromaddr, os.environ["gmail_password"])
			text=msg.as_string()
			server.sendmail(fromaddr,toaddr,text)
			server.quit()
			break
