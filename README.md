# Passive IMSI-catcher for Raspberry Pi with HackRF
This program shows you IMSI numbers, country, brand and operator of cellphones around you.  
  
/!\ This program was only made to understand how GSM networks work and will NOT transmitt nor disrupt GSM traffic /!\

## What you need

1 Raspberry Pi

1 [HackRF](https://greatscottgadgets.com/hackrf/)  
  
  
## Setup

### Headless Raspberry Pi

ssh into your Raspberry Pi and:

Install gr-gsm from here: https://osmocom.org/projects/gr-gsm/wiki/Installation

then

	git clone https://github.com/hbsagen/IMSI-catcher.git

then

	sudo apt install python3-numpy python3-scipy python3-scapy

then


## Run

### For headless Raspberry Pi with HackRF

Open 2 terminals and ssh into your Raspberry Pi:

In terminal 1:

	cd IMSI-catcher

	sudo python3 simple_IMSI-catcher.py

In terminal 2:

	cd IMSI-catcher

	python grgsm_livemon_headless.py -f 945.4M -s 8000000
	
#Recieving amp is enabled by default in this version, be aware.
	
You can now watch the output in terminal 1, and raw data (mostly 2b) in terminal 2. Change frequency as desired.


## Find frequencies

ssh into your Raspberry Pi and:

	sudo apt-get install automake autoconf libhackrf-dev
	git clone https://github.com/scateu/kalibrate-hackrf
	cd kalibrate-hackrf/
	./bootstrap
	./configure
	make
	sudo make install

Run  

	kal -s GSM900
***
kal: Scanning for GSM-900 base stations.  
GSM-900:  
	chan:   14 (937.8MHz + 10.449kHz)	power: 3327428.82  
	chan:   15 (938.0MHz + 4.662kHz)	power: 3190712.41
***
  
# Links

Setup of Gr-Gsm : https://github.com/ptrkrysik/gr-gsm/wiki/Installation  
Frequency : http://www.worldtimezone.com/gsm.html and https://fr.wikipedia.org/wiki/Global_System_for_Mobile_Communications  
Mobile Network Code : https://en.wikipedia.org/wiki/Mobile_Network_Code  
Scapy : http://secdev.org/projects/scapy/doc/usage.html  
IMSI : https://fr.wikipedia.org/wiki/IMSI  
Realtek RTL2832U : https://osmocom.org/projects/sdr/wiki/rtl-sdr and http://doc.ubuntu-fr.org/rtl2832u and http://doc.ubuntu-fr.org/rtl-sdr  
