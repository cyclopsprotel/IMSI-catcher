# IMSI-catcher for Raspberry PI with HackRF
This program shows you IMSI numbers, country, brand and operator of cellphones around you.  
  
/!\ This program was made to understand how GSM network work. Not for bad hacking !  

## What you need

1 Raspberry Pi
1 [HackRF](https://greatscottgadgets.com/hackrf/)  
  
  
## Setup

### Headless Raspberry PI

git clone https://github.com/Oros42/IMSI-catcher.git

sudo apt install python3-numpy python3-scipy python3-scapy


## Run

## For headless Raspberry Pi with HackRF

Open 2 terminals:

In terminal 1:

	sudo python3 simple_IMSI-catcher.py

In terminal 2:

	python grgsm_livemon_headless.py -f 945.4M -s 8000000
	
	#Recieving amp is enabled by default in this version, be aware.
	
You can now watch the output in terminal 1, and raw data (mostly 2b) in terminal 2. Change frequency as desired.

  
### With an old version of gr-gsm
  
Open 2 terminals.  
In terminal 1
```
sudo python3 simple_IMSI-catcher.py --sniff
```  
You can add -h to display options.  
  
In terminal 2, search a frequency to listen :
```
grgsm_scanner
```

Next, ask grgsm_livemon to use one of these frequencies:
```
grgsm_livemon -f <your_frequency>M
```
Example :  
```
grgsm_livemon -f 938.2M
```

It should start producing output like :
```
15 06 21 00 01 f0 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b
25 06 21 00 05 f4 f8 68 03 26 23 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b
49 06 1b 95 cc 02 f8 02 01 9c c8 03 1e 57 a5 01 79 00 00 1c 13 2b 2b
...
```
You can change the frequency if you want.



### With version of gr-gsm >= 0.41.2-1

Open 2 terminals.  
In terminal 1
```
python3 simple_IMSI-catcher.py
```  
You can add -h to display options.  


In terminal 2

```
python scan-and-livemon
```

This step can take a few minutes to get started, as it first run
grgsm_scanner to find nearby base stations and ask
grgsm_livemon_headless to receive the signal from the strongest
signals.

Or first find the frequencies of the nearby base stations.

```
grgsm_scanner
```

Next, ask grgsm_livemon to use one of these frequencies:

```
grgsm_livemon -f <your_frequency>M
```
Example :  
```
grgsm_livemon -f 938.2M
```

It should start producing output like :
```
15 06 21 00 01 f0 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b
25 06 21 00 05 f4 f8 68 03 26 23 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b
49 06 1b 95 cc 02 f8 02 01 9c c8 03 1e 57 a5 01 79 00 00 1c 13 2b 2b
...
```

You can change the frequency if you want.

### For all


Now, watch terminal 1 and wait. IMSI numbers should appear :-)  
If nothing appears after 1 min, change the frequency.  
  
Doc : https://fr.wikipedia.org/wiki/Global_System_for_Mobile_Communications  
Example of frequency in France : 9.288e+08 Bouygues  
  
You can watch GSM packets with  
```
sudo wireshark -k -Y '!icmp && gsmtap' -i lo
```

## Optional
 
Get immediate assignment :  
```
sudo python immediate_assignment_catcher.py
```

Find frequencies
----------------

You can either use the grgsm_scanner program from gr-gsm mentioned
above, or fetch the kalibrate-hackrf tool like this:

```
sudo apt-get install automake autoconf libhackrf-dev
git clone https://github.com/scateu/kalibrate-hackrf
cd kalibrate-hackrf/
./bootstrap
./configure
make
sudo make install
```
Run  
```
kal -s GSM900
```
```
kal: Scanning for GSM-900 base stations.
GSM-900:
	chan:   14 (937.8MHz + 10.449kHz)	power: 3327428.82
	chan:   15 (938.0MHz + 4.662kHz)	power: 3190712.41
...
```
  
# Links

Setup of Gr-Gsm : https://github.com/ptrkrysik/gr-gsm/wiki/Installation  
Frequency : http://www.worldtimezone.com/gsm.html and https://fr.wikipedia.org/wiki/Global_System_for_Mobile_Communications  
Mobile Network Code : https://en.wikipedia.org/wiki/Mobile_Network_Code  
Scapy : http://secdev.org/projects/scapy/doc/usage.html  
IMSI : https://fr.wikipedia.org/wiki/IMSI  
Realtek RTL2832U : https://osmocom.org/projects/sdr/wiki/rtl-sdr and http://doc.ubuntu-fr.org/rtl2832u and http://doc.ubuntu-fr.org/rtl-sdr  
