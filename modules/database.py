#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql.cursors

class MySQLdb:
	def __init__(self):

		self.dbhost = ""
		self.dbuser = ""
		self.dbpassword = ""
		self.db = ""

	def Connect(self):
		self.connection = pymysql.connect(host = self.dbhost,
			user = self.dbuser,
			password = self.dbpassword,
			db = self.db,
			cursorclass = pymysql.cursors.DictCursor)


	def Query(self,query):
		#print (query)
		self.Connect()
		with self.connection.cursor() as cursor:
			cursor.execute(query)
			result = cursor.fetchall()
			return result

	def Update(self,query):
		#print (query)
		self.Connect()
		with self.connection.cursor() as cursor:
			cursor.execute(query)
		self.connection.commit()

	def Insert(self,query):
		#pyprint (query)
		self.Connect()
		with self.connection.cursor() as cursor:
			cursor.execute(query)
		self.connection.commit()

	def Delete(self,query):
		#print (query)
		self.Connect()
		with self.connection.cursor() as cursor:
			cursor.execute(query)
		self.connection.commit()