#! /usr/bin/env python

# imports
import subprocess, httplib, urllib, os
from qhue import Bridge

#config
cfg = os.path.dirname(os.path.abspath(__file__)) + "/.connected"
family = [
		('XX:XX:XX:XX:XX:XX', 'Mike'),
		('ZZ:ZZ:ZZ:ZZ:ZZ:ZZ', 'Pat')
	 ]
connected = []
pushtoken 	= ""
pushuser 	= ""
maxattemps 	= 5

#Custom functions
def loadconnected():
	with open(cfg, 'r') as file:
		for line in file:
			connected.append(line.strip().rsplit("#"))

def saveconnected():
	with open(cfg, 'w') as file:
		for (mac,attempts) in connected:			
			file.write(mac.upper() + '#' + str(attempts) + '\n')

def sendnotification(connected, member):	
	message = "%s has left home" % member
	if connected:
		message = "%s has arrived home" % member
		
	#Pushover integration
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
  	urllib.urlencode({
    				"token": pushtoken,
    				"user": pushuser,
    				"message": message,
  			}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()

################# MAIN #####################################

#read cfg
loadconnected()

scan = subprocess.Popen(["arp-scan", "-lq", "-r", "5"], stdout=subprocess.PIPE)
grep = subprocess.Popen(["grep", "-io", "[0-9A-F]\{2\}\(:[0-9A-F]\{2\}\)\{5\}"], stdin=scan.stdout, stdout=subprocess.PIPE)

# Allow scan to receive a SIGPIPE if grep exits
scan.stdout.close()
output = grep.communicate()

for (mac,member) in family:
	#print "Checking if %s is connected" % member
	for clients in output:
		if clients!=None:			
			client = clients.rsplit("\n")
			success = False			
			for cmac in client:
				#print "Checking MAC %s" % cmac
				if cmac.upper()==mac.upper():
					#print "%s is connected" % member
					success = True
					found = False
					for (omac, attemps) in connected:
						if omac.upper()==mac.upper():
							#already connected
							found = True
							#reset counter
							connected = [i for i in connected if i[0] != mac.upper()]
							connected.append((mac.upper(), 0))
							break
					if not found:
						connected.append((mac.upper(), 0))
						sendnotification(True, member)					
					break
			if not success:
				#print "%s is NOT connected" % member
				for (omac, attemps) in connected:
					if omac.upper()==mac.upper():												
						if int(attemps) > maxattemps:
							#remove from connected
							connected = [i for i in connected if i[0] != mac.upper()]							
							sendnotification(False, member)	
						else:
							connected = [i for i in connected if i[0] != mac.upper()]	
							connected.append((mac.upper(), int(attemps)+1))
						
#save results to file
saveconnected()
