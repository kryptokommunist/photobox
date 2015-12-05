#!/usr/bin/python

import time, os, subprocess

while True:
    x = raw_input('Press enter...: ')
    snap = 0
    while snap < 4:
      print("pose!")
      time.sleep(1.5)
      print("SNAP")
      gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename /home/pi/photobox/photos/photobooth%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True)
      print(gpout)
      if "ERROR" not in gpout: 
        snap += 1
      time.sleep(0.5)
    gpout = subprocess.check_output("./home/pi/photobox/flickr-uploader/uploadr.py", stderr=subprocess.STDOUT, shell=True)
    print(gpout)
