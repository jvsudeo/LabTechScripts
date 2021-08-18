#!/usr/bin/env python3

import os
import sys, time

def usage():
	print("python3 runClearpod.py []"
		"\nEnter POD between 1-18 or enter 'all' for all devices"
		"\nView errorLogs.txt for any pods that did not clear and donePods.txt to check which cleared"
		"\n To run routers only or switches only, enter 'allRouters' / 'allSwitches' ")


routers=[6001,6002,6005,6006,6009,6010,6013,6014,6017,6018,6021, 6022]
switches=[6003,6004,6007,6008,6011,6012,6015,6016,6019,6020,6023,6024]

os.system("echo > errorLogs.txt")
os.system("echo > donePods.txt")

try:
	pod = sys.argv[1]
	if pod == "all":
		for i in range(1,4):
			hostend = 203 + i
			host = "10.41.30." + str(hostend)
			for port in range(6001, 6025):
				if port == 6016:
					os.system("python3 clearPod.py " + host + " " +  str(port) + " ")
					
				else:
					os.system("python3 clearPod.py " + host + " " +  str(port) + " " + "&")
						


	elif pod == "allRouters":
		for i in range(1,4):
			hostend = 203 + i
			host = "10.41.30." + str(hostend)
		
			for port in routers:
				if port == 6022:
					os.system("python3 clearPod.py " + host + " " +  str(port) + " ")

				else:
					os.system("python3 clearPod.py " + host + " " +  str(port) + " " "&")
					time.sleep(1)


	elif pod == "allSwitches":
		for i in range(1,4):
			hostend = 203 + i
			host = "10.41.30." + str(hostend)
		
			for port in switches:
				if port == 6024:
					os.system("python3 clearPod.py " + host + " " +  str(port) + " ")

				else:
					os.system("python3 clearPod.py " + host + " " +  str(port) + " " "&")
					time.sleep(1)

	else:

		pod = int(pod)
		if pod > 18 or pod < 1:
			raise Exception
			#next line is where I left out last

		if float(pod) / 6 < 1:
			hostend = 203 + 1
			#pod can either be 1,2,3,4,5,6

		elif float(pod) / 6 < 2:
			hostend = 203 + 2
			#pod can either be 7,8,9,10,11,12
		elif float(pod) / 6 < 3:
			hostend = 203 + 3
			#pod can either be 13,14,15,16,17,18
		

		if pod % 6 == 1:
			a=6001
			b=6005
		elif pod % 6 == 2:
			a=6005
			b=6009
		elif pod % 6 == 3:
			a=6009
			b=6013
		elif pod % 6 == 4:
			a=6013
			b=6017
		elif pod % 6 == 5:
			a=6017
			b=6021
		elif pod % 6 == 0:
			a=6021
			b=6025


		host = "10.41.30." + str(hostend)
		

		for port in range(a,b):
			os.system("python3 clearPod.py " + host + " " +  str(port) + " " + "&")

			
except: 
	usage()

