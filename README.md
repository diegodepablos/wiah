# WIAH
Who Is At Home?

A little python script that checks if any family member is at home or not, written for a raspberry pi in mind.

# Installation

1. Download source code to your home folder.
2. arp-scan executable is required to work. To install it just type (debian):

    sudo apt-get install arp-scan

3. Give executable permission to wiah.py

    sudo chmod +x wiah.py

4. Add a crontab to execute the script every minute (* * * * *). This script requires elevation privileges (root):
  
    sudo crontab -e -u root
  
5. Modify wiah.py and add your user token and app token from pushover.net to receive push notifications to your device.
6. Enjoy!
