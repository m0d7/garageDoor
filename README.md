YouTube Video Instructions found here: https://youtu.be/Fcx6wANw9KM

Setting up a Flask web server to control your garage door & display the door status & log usage.

--------------------------------------------------------------------
Products I used in this video:
--------------------------------------------------------------------

Raspberry Pi Zero W with case on Amazon: https://amzn.to/34ujK5C

Raspberry Pi Zero W on Adafruit: https://www.adafruit.com/product/3400

4 Channel Relay (to Open Garage Door): https://amzn.to/3b4lHbD

Magnetic Reed Switch (You need 2): https://amzn.to/39YG7kU

Jumper/Breadboard wire 120ct: https://amzn.to/2V3fFlV

Hammer Header & Install Kit on Amazon: https://amzn.to/3b5RbxX

Hammer Headers on Adafruit: https://www.adafruit.com/product/3662

--------------------------------------------------------------------
Setup Instructions:
--------------------------------------------------------------------

1.  --First setup your Raspberry Pi: https://www.youtube.com/watch?v=EeEU_8HG9l0 
2.  --Lets upgrade the apt-get program: 
sudo apt-get update

3.  --Next install the Flask Web Server and required packages: 
sudo apt-get install python3-flask
sudo apt install python3-pip -y
sudo pip3 install -r requirements.txt

4.  --Install the GIT application so you can download my Github code: 
sudo apt-get install git 

5.  --Download my Github code: 
sudo git clone https://github.com/m0d7/garageDoor
 
6.  --Test out setup and webpage (default port is 5000)
cd GarageWeb
     --Test Relay connections
python3 relaytest.py
     --Test Magnetic Reed Switches
python3 log.py
     --Test out Webpage securely via HTTPS (https://Rasp_Pi_IP_Address:5000)
python3 web.py

NOTE: The application now uses HTTPS with a self-signed certificate for secure access.
When first accessing the page, your browser will show a security warning - you'll need to
accept the self-signed certificate by clicking "Advanced" and then "Proceed" (exact wording
varies by browser).

 7.  --To Setup this code to run automatically on system boot up:
sudo nano /etc/rc.local
     --Add the next 2 lines before the last line "exit 0"
sudo python3 /home/pi/GarageWeb/web.py &
sudo python3 /home/pi/GarageWeb/log.py &
exit 0

8.  --Change the default password of "12345678"
sudo nano web.py
     --find the 2 lines that contain "12345678" change to new password.

9.  --Change default port number (if desired) it'll be the last line of web.py

10.  --Reboot system and let program autostart
sudo reboot

11.  --Set up Port Forwarding on your Router to allow access when away from home.
     --Once setup, turn off WiFi on your phone and test. You'll need to know the REAL address of your home router.

--------------------------------------------------------------------
Wiring Diagram:
--------------------------------------------------------------------

<img src="https://github.com/shrocky2/GarageWeb/blob/master/Wiring%20Diagram.jpg">

--------------------------------------------------------------------
Additional Videos:
--------------------------------------------------------------------
Sonoff Garage Door Opener: https://youtu.be/f1JeKHraDf8

How to set up your Raspberry Pi: https://youtu.be/EeEU_8HG9l0

How to set up Port Forwarding on your Router: https://youtu.be/VhVV25zCFrQ
