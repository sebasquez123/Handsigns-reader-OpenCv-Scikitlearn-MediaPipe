# CONNECT TO SSH IP
ssh hostname@00.000.000.000
# POWERSHELL ACROSS SSH
## What is this for:
We are creating the first folders and first files from windows disk, its done this way because the files are inside windows folders and we need to pass them to raspberry by searching them locally.

### CREATE FOLDER
mkdir ~/$DEST  --> from linux shell

### INPUT FILES INSIDE FROM WINDOWS
scp "C:\Users\sebas\OneDrive\Escritorio\DEV PERSONAL\VISION ARTIFICIAL\Pattern-reader-with-Cv-raspberry\requirements_rpi.txt" sebas@10.153.185.147:~/webrtc_server/

scp -r "C:\Users\sebas\OneDrive\Escritorio\DEV PERSONAL\VISION ARTIFICIAL\Pattern-reader-with-Cv-raspberry\src\server" sebas@10.153.185.147:~/webrtc_server/

# LINUX RASPBERRY CONSOLE
## What is this for:
once ssh connection stablished through powershell windows console, raspberry communicates through linux console interface, waiting for first time project creation and files insertion. here we are downloading and installing fundamental files to get it work by enabling python environment.
## EACH TIME WE SET A NEW VENV:
### STAND UP ON FOLDER
cd ~/webrtc_server
### CREATE VENV 
python3 -m venv venv
### ACTIVATE SCRIPTS
source venv/bin/activate
### PREPARE COMPILATION TOOLS FOR VIDEO
sudo apt update
sudo apt install -y ffmpeg v4l-utils libsrtp2-1 libsrtp2-dev
### INSTALL PROJECT DEPENDENCIES
pip install --upgrade pip wheel setuptools
sudo apt install python3-opencv -y -> in this case its needed only with APT ubuntu.
pip install -r requirements_rpi.txt
### VERIFY INSTALLED DEPENDENCIES
pip list
### CONNECT CAMERA OR DEVICES & VERIFY.
lsusb
### CONNECT SPEAKER  & VERIFY.
aplay -l
speaker-test -D plughw:1,0 -c2 -t wav
### UPDATE PACKAGE MANAGER & INSTALL HELPER FOR TESTING CAMERA
sudo apt update
sudo apt install v4l-utils
### LIST CAMERA AND REST OF DEVICES WITH DETAIL INFO
v4l2-ctl --list-devices
### LIST OF FOLDERS AND FILES, MAKE SURE WE ARE IN THE CORRECT MAIN.PY
ls -l <other folder>
### TEST RUNNING THE MAIN.PY OR THE MAIN PIPELINE.
python server/WebRTC.py
### ONCE RUNNING USE:
<0.0.0.0> → means all the available interfaces can get in
<127.0.0.1> or <localhost> → just available for the raspberry itself
<192.168.x.x>→ Raspberry LAN ip, accessable from any other devices.

## TROUBLESHOOTING
### IF SOME FAILS DUE TO LACK OF LIBRARIES THAT ONLY CAN BE INSTALLED AT APT 
- allow virtual environment uses the global apt python global env.

rm -rf venv
python3 -m venv venv --system-site-packages

- install all packages asked by OS, if it's not found from last requirements instalation.

## TO DELETE AND RENUEW FILES.
rm -rf ~/webrtc_server 

## TO DISABLE OLF VENV
- each time old folders are deleted, we must create another venv into the newest folder.
  
deactivate
python3 -m venv venv




# WIFI NETWORK MANAGEMENT.

## TO SEE NETWORKS
nmcli dev wifi list

## CONFIGURE NETWORK IN NANO
network={
    ssid="UTP"
    key_mgmt=NONE
    priority=1
} 

## UTP RASPBERRY IP 
10.253.20.182
## SEBAS RASPBERRY IP 
10.153.185.147