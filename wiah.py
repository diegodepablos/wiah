#! /usr/bin/env python

# imports
import subprocess,httplib, urllib

#config
cfg = ".connected"
family = [
		('XX:XX:XX:XX:XX:XX', 'Diego')
	 ]
connected = []

#pushover service
pushtoken 	= ""
pushuser 	= ""

#Custom functions
def sendnotification(connected, member):
	message = "%s has left home" % member
	if connected:
		message = "%s has arrived home" % member

	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
  	urllib.urlencode({
    				"token": pushtoken,
    				"user": pushuser,
    				"message": message,
  			}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()

#main
print "Who Is At Home?"
print "="*20

#read cfg
with open(cfg, 'r') as file:
	for line in file:
		connected.append(line.strip())

#print connected

scan = subprocess.Popen(["arp-scan", "-lq"], stdout=subprocess.PIPE)
grep = subprocess.Popen(["grep", "-io", "[0-9A-F]\{2\}\(:[0-9A-F]\{2\}\)\{5\}"], stdin=scan.stdout, stdout=subprocess.PIPE)

# Allow scan to receive a SIGPIPE if grep exits
scan.stdout.close()
output = grep.communicate()


for (mac,member) in family:
	success = False
	print "Checking if %s is connected" % member
	for clients in output:
		if clients!=None:
			client = clients.rsplit("\n")			
			for cmac in client:
				#print "Checking MAC %s" % cmac
				if cmac.upper()==mac.upper():
					print "%s is connected" % member
					success = True
					if not any(mac.upper() in s for s in connected):
						connected.append(mac.upper())
						sendnotification(True, member)					
					
					break
			if not success:
				print "%s is NOT connected" % member
				#remove from connected
				if any(mac.upper() in s for s in connected):
					connected.remove(mac.upper())
					sendnotification(False, member)
#save results to file
with open(cfg, 'w') as file:
	for mac in connected:
		file.write(mac.upper() + '\n')


