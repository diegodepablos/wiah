# wiah
Who Is At Home?

A little python script that checks if any family member is at home or not, written with a raspberry pi in mind.

arp-scan executable is required to work. To install it just type (debian):

sudo apt-get install arp-scan

This script requires elevation privileges (root)

Add a crontab to execute every five minutes (*/5 * * * *):

sudo crontab -e -u root

Add your user token and app token from pushover.net to receive push notifications to your device.
