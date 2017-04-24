#!/usr/bin/env python3
import sys
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
		self.filename = "unknown"
		
	def	Initialise_DB(self):
		self.DB = database.MySQLdb()
		self.DB.dbhost = self.db_host
		self.DB.dbuser = self.db_username
		self.DB.dbpassword = self.db_passwd
		self.DB.db = self.db_name
		
	def add_to_queue(self):
		sql_cmd = """INSERT into VideoData
		(DATEANDTIME,VIDEONAME,CAMERAID,UPLOADED)
		VALUES
		(now(),"%s","%s",0);
		""" % (self.filename,self.cam_id)
		print (sql_cmd)
		result = self.DB.Insert(sql_cmd)
		
		
		
		

if __name__ == "__main__":
	print ("Loading Variables")
	variables = load_variables.load_variables(r'/opt/youtube_uploader/etc/queue_monitor.ini')
	print ("Initialising queue monitor class")
	queue_monitor = main()
	queue_monitor.db_host = variables['database_host']
	queue_monitor.db_name = variables['database_name']
	queue_monitor.db_username = variables['database_user']
	queue_monitor.db_passwd = variables['database_password']
	queue_monitor.cam_id = variables['camera_id']
	queue_monitor.retries_before_ignore = variables['retries_before_fail']
	
	print ("connecting to DB")
	queue_monitor.Initialise_DB()
	
	print ("Adding Entry to DB")
	queue_monitor.filename = sys.argv[1]
	queue_monitor.add_to_queue()