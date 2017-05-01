#!/usr/bin/python

import time
import sys
import subprocess


def main(video_list):
	input_file = open(video_list)
	line_index = 0
	videos_to_delete = []
	for input_line in input_file:
		line_index += 1
		if line_index == 1: continue
		inputline = input_line.strip()
		video_id = inputline.split(' ')[-1][1:-1]
		time_string = " ".join(inputline.split(' ')[0:-1])

		# time string versions :
		#  motion_2017-04-29_10.45.42_568.mp4
		#  Mon 17 Apr 12:18:54 BST 2017
		#  Sun Apr 23 16:44:49 2017
		#print (time_string)
		time_codes = "BST","UTC"
		for x in time_codes: time_string=time_string.replace(x,"")

		time_string_formats = ["motion_%Y-%m-%d_%H.%M.%S_%f.mp4","%a %d %b %H:%M:%S %Y","%a %b %d %H:%M:%S %Y"]

		time_string_index = 0
		for y in time_string_formats:
			try:
				time.strptime(time_string,y)
				time_string_format = y
				break
			except:
				pass
			time_string_index += 1
		if time_string_index == len(time_string_formats):
			print ("Did not match any known time formats: ",inputline)
			continue

		time_val = time.strptime(time_string,time_string_format)
		time_in_seconds = time.mktime(time_val)

		#print (video_id,time_string,time_in_seconds)
		now = time.time()
		seconds_in_60_days = 5184000
		if time_in_seconds < (now - seconds_in_60_days):
			#print ("Delete video id {} : {}".format(video_id,time_string))
			videos_to_delete.append(video_id)

	if len(videos_to_delete) >= 1:
		print ("There are {} video(s) to delete".format(len(videos_to_delete)))
		output_file_name = "/tmp/del_video_list.csv"
		output_file = open(output_file_name,'a')
		for x in videos_to_delete:
			output_file.write("{}\n".format(x))
		output_file.close()







if __name__ == "__main__":
	video_list = sys.argv[1]
	main(video_list)