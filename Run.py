
mager
Andrew Mager
SmartApp Code SlingerAug '154 
I recently bought the $5 Amazon dash button. While the thought of pushing a button and having Kraft Mac & Cheese87 arrive at my doorstop two days later is intriguing, I'd rather hack the button.

The Dash has a wifi chip that communicates with the Amazon mobile app, but we can interrupt that final step and make it do whatever we want.

First, I'll show the video and then provide instructions to replicate this at home.

Hack the Amazon Dash button to control a SmartThings switch
Here's how it works...

Step 1: Get the MAC address of the Dash button
Open up the Amazon shopping app, and configure the Dash button to work with your local network. Click Settings → Dash Devices → Manage devices. Add your SSID and network password, and watch the Dash button light up with a blue LED.

Now, once you get to the screen where you need to select which item to purchase, close the app. Don't actually choose an item.

IMG_0774.PNG640x1136 189 KB
Your dash is now talking to your wifi network, but isn't ordering any food.

Next, create a text file and name it listen.py. Paste this code in and save it (shoutout to Ted Benson268):

from scapy.all import *

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      print "ARP Probe from: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=10)
This script uses a Python library called Scapy which lets you intercept network packets and do whatever you want with them. Here's an interactive tutorial1.1k.

It took me about 5 minutes to get Scapy to work with my operating system (OS X 10.11). Once you get it working, run the Python script: python listen.py.

Your terminal should output a MAC address. There are a few errors, but you can ignore them.

Screen_Shot_2015-08-12_at_4_45_00_PM.png1872x984 281 KB
Now that we have the MAC address, let's update our listen.py script:

from scapy.all import *

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc == 'a0:02:dc:ed:13:cc': # Mac & Cheese
        print "Pushed Mac & Cheese"
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=10)
Your MAC address will be different.

Step 2: Write a SmartApp that accepts HTTP requests to control switches
This is the easy part.

@Jim wrote an awesome SmartApp that creates endpoints and lets you control switches with PUT requests.

Here is the code: https://github.com/SmartThingsCommunity/Code/blob/master/smartapps/hackathon-demo/restful-switch.groovy738

When creating the SmartApp, make sure to enable OAuth.

Install the SmartApp, select a switch to control, and take note of the API token and API Endpoint.

Screen_Shot_2015-08-12_at_4_51_29_PM.png2300x1636 643 KB
Step 3: Update Python script to make HTTP requests to SmartThings when the button is pushed
Now, all we have to do is make a PUT request to the SmartApp within the Python script and the light should toggle on and off.

Here's the updated Python script:

from scapy.all import *
import requests

def toggle_st():
    url = 'YOUR_API_ENDPOINT'
    headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
    data = '{"command":"toggle"}'
    r = requests.put(url, data=data, headers=headers)

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc == 'YOUR_MAC_ADDRESS': # Mac & Cheese
        print "Toggle the light"
        toggle_st()
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=10)
And that's it. Now you can use a $5 buttonfrom scapy.all import *
import requests

def toggle_st():
    url = 'YOUR_API_ENDPOINT'
    headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
    data = '{"command":"toggle"}'
    r = requests.put(url, data=data, headers=headers)

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc == 'YOUR_MAC_ADDRESS': # Mac & Cheese
        print "Toggle the light"
        toggle_st()
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=10)
