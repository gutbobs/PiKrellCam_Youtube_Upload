#!/usr/bin/env python3
import os
import time
import subprocess
import urllib.parse
import smtplib
from modules import database
from modules import load_variables

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class main:
	def __init__(self):
		self.db_host = "localhost"
		self.db_name = "PiCamYoutube"
		self.db_username = "queue_monitor"
		self.db_passwd = "Password1"
		self.cam_id = 1
		self.retries_before_ignore = 3
		self.loop_time = 5
		self.email_on_upload="yes"
		self.email_to="root@localhost"
		self.email_from="root@localhost"
		self.email_server="localhost"
		
	def	Initialise_DB(self):
		self.DB = database.MySQLdb()
		self.DB.dbhost = self.db_host
		self.DB.dbuser = self.db_username
		self.DB.dbpassword = self.db_passwd
		self.DB.db = self.db_name
		
	def send_email(self,to,subject,body):
		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] = "root"
		msg['To'] = to

		msg.attach(MIMEText(body, 'plain'))
		server= smtplib.SMTP(self.email_server)
		server.sendmail(self.email_from,self.email_to,msg.as_string())
		server.quit
        
	def check_queue(self):
		sql_cmd = """select `INDEX`,`DATEANDTIME`,`VIDEONAME` 
		from {db_name}.VideoData
		where UPLOADED = 0 
		and UPLOADATTEMPTS <= {failed_attemps}""".format(db_name = self.db_name,
			failed_attemps = self.retries_before_ignore)
		#print (sql_cmd)
		result = self.DB.Query(sql_cmd)
		#print (len(result))
		#print (result)
		for item in result:
			#print (item['VIDEONAME'])
			filename = item['VIDEONAME']
			title = filename.split('/')[-1]
			description = time.ctime()
			
			if not os.path.exists(filename): 
				print ("%s: file not found" % filename)
				sql_cmd = "UPDATE `VideoData` set `UPLOADED`='2',`UPLOADRESULT`='not found' where `INDEX`='{index}';".format(index=item['INDEX'])
				self.DB.Update(sql_cmd)
				continue

			print ("Uploading %s" % item['VIDEONAME'])
			cmd_line = 'sudo python /opt/youtube_uploader/upload_video.py --file="%s" --title="%s" --description="%s" --privacyStatus="private"' % (filename,title,description)
			p = subprocess.Popen(cmd_line,shell=True,stdout=subprocess.PIPE)
			cmd_result = p.communicate()
			#print (cmd_result)
			#print (p.returncode)

                       
			if (p.returncode == 0):
				sql_cmd = """UPDATE `VideoData`
				set `UPLOADED`='1', `UPLOADATTEMPTS`='%s'
				where `INDEX`='%s';""" % (1,item['INDEX'])
				#print (sql_cmd)
				db_update_result = self.DB.Update(sql_cmd)
				#print (db_update_result)
			else:
				print ("upload failed")
				print (cmd_result)
			sql_cmd = "UPDATE `VideoData` set `UPLOADRESULT`='{cmd_res}',`UPLOADED`='1' where `INDEX`='{index}' ;".format(cmd_res=urllib.parse.quote_plus(cmd_result[0]),index=item['INDEX'])
			#print (sql_cmd)
			self.DB.Update(sql_cmd)

			if self.email_on_upload == "yes":
				subject = "PiKRellCam Video Uploaded"
				body = "A video has been uploaded to youtube. The cmd result was %s" % cmd_result[0]
				print ("Sending Email")
				self.send_email(self.send_to,subject,body)			

		
		
		
	

if __name__ == "__main__":
	variables = load_variables.load_variables(r'/opt/youtube_uploader/etc/queue_monitor.ini')
	queue_monitor = main()
	queue_monitor.db_host = variables['database_host']
	queue_monitor.db_name = variables['database_name']
	queue_monitor.db_username = variables['database_user']
	queue_monitor.db_passwd = variables['database_password']
	queue_monitor.cam_id = variables['camera_id']
	queue_monitor.retries_before_ignore = variables['retries_before_fail']
	queue_monitor.email_on_upload = variables['email_on_upload']
	queue_monitor.email_to = variables['email_to']
	queue_monitor.email_from = variables['email_from']
	queue_monitor.email_server = variables['email_server']
	
	queue_monitor.Initialise_DB()
	
	loop_count = 0
	while 1:
		loop_count += 1
		try:
			queue_monitor.check_queue()
			time.sleep(int(queue_monitor.loop_time))
		except:
			time.sleep(10)
		#print (loop_count)
