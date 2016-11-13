import os
import glob
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def get_most_recent_file():
	current = max(glob.iglob('/media/pi/EXTSD/Security/*.jpg'), key=os.path.getctime)
	return current
fromaddr="RPi.Dudek@GMail.com"
frompass=os.environ["gmail_password"]
toaddr="StanleyRussellDudek@GMail.com"
msg=MIMEMultipart()
msg['From']=fromaddr
msg['To']=toaddr
msg['Subject']="Motion Detected!"
initial_file = get_most_recent_file()
while 1:
	current_file = get_most_recent_file()
	if initial_file == current_file:
		time.sleep(0.1)
	else:
		initial_file = current_file		
		attachment=open('/media/pi/EXTSD/Security/'current_file,"rb")
		filename=current_file
		filename=os.path.basename(filename)
		motiontime = filename.replace('_',':')
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
		server.login(fromaddr, frompass)
		text=msg.as_string()
		server.sendmail(fromaddr,toaddr,text)
		server.quit()
