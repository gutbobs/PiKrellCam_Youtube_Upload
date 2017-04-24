# PiKrellCam_Youtube_Upload

Youtube uploader to be used with rasperry pi PiKrellCam. PiKrellCam can be found here: http://billw2.github.io/pikrellcam/pikrellcam.html. I've got nothing to do with the project, but I do use it and appreciate it. I've installed PiKrellCam into it's default location and this code into /opt/youtube_uploader

description of files:

motion-end = called when pikrellcam has finished recording a video.  The change from the original is to call add_to_queue.py. original file usually lives in /home/pi/pikrellcam/scripts

add_to_queue.py = adds the file name of the recorded video to the database. Makes use of database and load_variables modules. lives in /opt/youtube_uploader

modules/ = should be in /opt/youtube_uploader and contains database and variable reading python modules

etc/ = should be in /opt/youtube_uploader and contains variables file. This contains variables used to connect to the database

queue_monitor.service = lives in /lib/systemd/system and defines the queue monitoring service. See http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/ for more info

queue_monitor.py = lives in /opt/youtube_uploader and monitors the database for new entries and then calls upload_video.py to send the videos to youtube

upload_video.py = googles example code for uploading videos to youtube via their API. basically as found here: https://developers.google.com/youtube/v3/guides/uploading_a_video but with the addition of some additional exit codes. Note that you'll need all your own API keys etc
