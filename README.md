
#Internet enabled Raspberry Pi fishing boat

Raspberry Pi in boat, which controls GPS, camera and the motors. Boat is steered and controlled from web ui.

## Boat software consists of three projects:
 - **BOAT**:  python program which handles steering, gps, camera and other stuff. That software is in this project.
 - **WEB UI**: Angular 2 based web client Software for this is in separate project: https://github.com/ilkkaparssinen/fisherboat-web
 - **SERVER**: node.js server gets boat information via websockets and passess them forward to clients. Websocket connection is used also to pass information from client to boat (steering & speed). node.js is in separate project https://github.com/ilkkaparssinen/fisherboat-server

## Boat features:
 - Two DC motors. Steering is done by adjusting the speed of the two motors (one on the right side and one on the left side). Controlling the motors is based on Adafruit Motor Hat and the libraries for that.
 - Internet connection (4G modem)
 - Boat can also "speak" if it has a connected speaker
 - On board camera which transmits very low res MJPEG (5 frames/second ) via web sockets. Also on spearate command it takes full photos and sends them. This is based on the Raspberyy PI camera module and it's python libraries.
 - GPS location (location, speed and direction) is sent to the web server and there to clients, which show this information with google maps.
 - Option for adding a flex control to detect fish catches. (We didn't use this - too many wires..., but the code is there).
 - Option for playing music. We had a plan for "scientific" program to test if some sounds atrract fishes. Program switches between two mp3 files + some amount of silence.
 - Different speed variation programs for different kind of fishing.
 - Python 2.7 client. These raspberry tests are the first time I have programmed with python (but I like it) so the solution might not be very pythonesque, but in general the solution is quite clean. 

## Web client features:
 - Speed and direction control of the boat
 - Multiple simultanous drivers (server acts as a publish & subscribe server, so everybody is in sync)
 - Real time video
 - Click the video screen and request for full res photo from boat
 - Set up different fishing programs / turn music on / off
 - Real time chat with other drivers and show notifications from the boat
 - Google maps - show location, direction and speed of the boat
 - Implemented with Angular 2 beta (things have changed in Angular 2 since that, and this was a learning project for me for Angular 2 - the software is ..uh.. not very stylish).
 
## Server features:
 - Web socket connection from the boat and to the clients. 
 - Simple pub/sub server
 - Serves the static angular 2 files for the web app
 - Can support multiple boats (each boat must have their own boat id)
 - Simple node.js websocket solution. This was a quick hack, but it turned out to be surprisingly robust - I just put it running to EC2 and it just keeps running and responsing whenever we test the boat. No problems.

## Boat hardware
  - Raspberry PI Model 2 B
  - Raspberry Pi camera module + standard libraries
  - ADAFRUIT DC & STEPPER MOTOR HAT FOR RASPBERRY PI and it's libraries
  - Adafruit Ultimate GPS: https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/introduction
  - 2 5V power sources - one for motors and one for raspberry pi
  - 2 cheap 5V DC Motors
  - Boat was made from an insulator foam stuff, which was easy to carve
  - Propellers, drive shafts, silicon tube and parts for attaching the drive shafts to motors from Hobby King. I have no experience in RC boat building, so our design was definitely quite bad - but it worked.
  - Option for Flex sensor https://www.adafruit.com/product/182, which is measured with MCP3008 (or similar). Look for libraries and instructions from: https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/overview
  
## Used libraries and settings
  - Python 2.7. For a long time I used Python 3.0 but ran to some truble with gps modules and switched back to 2.7.
  - A lot of them, and I have probably already forgotten some of them. The main ones are described excellently in Adafruit learning material (gps, flex sensors, motor hat etc.)
  - Different settings - getting the Huawei 4G modem to work was a pain. Also all kind of settings were needed along the way - but they too are explained better in other documentiotion.

## Software structure
 - fish.sh: shell script that starts the program. I used it from boot to autostart everything. 
 - fisherboat.py: main module. Just starts brainz.py
 - brainz.py: main loop. Starts different devices and controls them in a loop (every 0.2 seconds)
 - motors.py: control 2 dc motors
 - gpstracker.py: control gps module
 - player.py: play music and call espeak to give voice info
 - video.py: control camera - send mjpeg video + take full res photos
 - webconnection.py: web socket connection to server. Send status, video and photos. Receive steering commands. (There is the fixed ip address for server - change that to your own).
 - adcsensors.py: adc sensor reading for flex sensor. Currently not initialized (remove comments from brainz.py)
  
## Software license:
 - DWYWDBM-license: Do what you want, don't blame me
 - Warning - this is not a plug & play project - it has a lot of moving parts and requires some knowledge to how to set up a web server etc. this definitely is not a Raspberry Pi beginner project. 
 - Feel free to use any parts of the project.
 
