#!/usr/bin/env python3
import time
import subprocess
import urllib.parse
from modules import database
from modules import load_variables

class main:
	def __init__(self):
		self.db_host = "localhost"
		self.db_name = "PiCamYoutube"
		self.db_username = "queue_monitor"
		self.db_passwd = "Password1"
		self.cam_id = 1
		self.retries_before_ignore = 3
		self.loop_time = 5
		
	def	Initialise_DB(self):
		self.DB = database.MySQLdb()
		self.DB.dbhost = self.db_host
		self.DB.dbuser = self.db_username
		self.DB.dbpassword = self.db_passwd
		self.DB.db = self.db_name
		
	def check_queue(self):
		sql_cmd = """select `INDEX`,`DATEANDTIME`,`VIDEONAME` 
		from {db_name}.VideoData
		where UPLOADED = 0 
		and UPLOADATTEMPTS <= {failed_attemps}""".format(db_name = self.db_name,
			failed_attemps = self.retries_before_ignore)
		#print (sql_cmd)
		result = self.DB.Query(sql_cmd)
		#print (len(result))
		for item in result:
			print (item['VIDEONAME'])
			filename = item['VIDEONAME']
			title = filename.split('/')[-1]
			description = time.ctime()
			
			cmd_line = 'sudo python /opt/youtube_uploader/upload_video.py --file="%s" --title="%s" --description="%s" --privacyStatus="private"' % (filename,title,description)
			p = subprocess.Popen(cmd_line,shell=True,stdout=subprocess.PIPE)
			cmd_result = p.communicate()
			print (cmd_result)
			print (p.returncode)
			if (p.returncode == 0):
				sql_cmd = """UPDATE `VideoData`
				set `UPLOADED`='1', `UPLOADATTEMPTS`='%s'
				where `INDEX`='%s';""" % (1,item['INDEX'])
				print (sql_cmd)
				db_update_result = self.DB.Update(sql_cmd)
				print (db_update_result)
			else:
				print ("upload failed")
				print (cmd_result)
			sql_cmd = "UPDATE `VideoData` set `UPLOADRESULT`='{cmd_res}',`UPLOADED`='1' where `INDEX`='{index}' ;".format(cmd_res=urllib.parse.quote_plus(cmd_result[0]),index=item['INDEX'])
			print (sql_cmd)
			self.DB.Update(sql_cmd)

		
		
		
	

if __name__ == "__main__":
	variables = load_variables.load_variables(r'/opt/youtube_uploader/etc/queue_monitor.ini')
	queue_monitor = main()
	queue_monitor.db_host = variables['database_host']
	queue_monitor.db_name = variables['database_name']
	queue_monitor.db_username = variables['database_user']
	queue_monitor.db_passwd = variables['database_password']
	queue_monitor.cam_id = variables['camera_id']
	queue_monitor.retries_before_ignore = variables['retries_before_fail']
	
	queue_monitor.Initialise_DB()
	
	loop_count = 0
	while 1:
		loop_count += 1
		queue_monitor.check_queue()
		time.sleep(int(queue_monitor.loop_time))
		print (loop_count)
