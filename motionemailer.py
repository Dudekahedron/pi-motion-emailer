import os,glob,time,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#these are identical because I have no idea what I'm doing
def current():
	current = max(glob.iglob(os.path.join('/media/pi/EXTSD/Security','*.jpg')),key=os.path.getctime)
	return current
def newest():
	newest = max(glob.iglob(os.path.join('/media/pi/EXTSD/Security','*.jpg')),key=os.path.getctime)
	return newest
#instructions to send email with attachment if a new file is found
msg=MIMEMultipart()
msg['From']=fromaddr
msg['To']=toaddr
msg['Subject']="Motion Detected!"
while True:
	cur=current()
	while True:
		new=newest()
		filename=str(new)
		filename=filename.replace('/media/pi/EXTSD/Security/','')
		attachment=open(new,"rb")
		if new==cur:
			#simply waiting for a new file to be found
			time.sleep(0.1)
		else:
			motiontime = new.replace('_',':')
			motiontime = motiontime.replace('/media/pi/EXTSD/Security/','')
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
			server.login(fromaddr,"password")
			text=msg.as_string()
			server.sendmail(fromaddr,toaddr,text)
			server.quit()
			break
