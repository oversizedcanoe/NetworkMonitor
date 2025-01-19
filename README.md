# NetworkMonitor
A tool to monitor devices connected to a network.


## Architecture
This application has three main parts.

### Service
This is an always-running background service which uses [nmap](https://nmap.org/) to query the local network to check for currently connected devices. After each query, this service does a few things:
- Adds new connected devices to a local SQLite database
- Updates the last connected time to now for previously-connected devices
- Optionally, notify users of newly connected devices and previously-connected devices which require notifying
  - Currently, only email notifications (to and from your own email) are supported
  
### API
This is a [Falcon](https://falcon.readthedocs.io/en/stable/) REST API for access to the connected devices.

### Web
This is a simple React UI to view current and previously connected devices, as well as make basic edits to them (provide user-friendly names, configure which devices require notifications).

## Running NetworkMonitor
This assumes you already have Python, Node, and NPM installed. 

First, download nmap [here](https://nmap.org/download).

After downloading this repo or cloning it, start a Python virtual environment and install `requirements.txt` (Windows shown below):

```
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```

Next, in `/Service`, rename `template.env` to `email.env` and update the email and password to your desired email and the base64 hash of it's password. This will be the email which sends and receives emails. 

Finally, open three terminals in the project base folder and run each application separately (ensure the API and Service are ran in venv):
- Service:
```
cd .\service\
python .\main.py
```
- API:
```
cd .\api\
python .\main.py
```
- Web:
```
cd .\web\
npm install
npm run dev
```

## What's the Purpose?
I dunno, it was just fun to build.

This could be extended or used to do things like:
- Add more notification events, such as executing an Alexa skill, or sending some sort of API request to turn on a smart home device
- Store statistics on how long devices were connected to a network
- Home security (ensure strangers are not using your wifi)

## Demo
![image](https://github.com/user-attachments/assets/f4fbded9-0aca-4d93-bcab-66c752635441)

![image](https://github.com/user-attachments/assets/b1913a00-353e-4b3c-a8ad-9a4f4256b6b0)

![image](https://github.com/user-attachments/assets/df05a9b1-809b-4ec2-bed0-c47353580854)

## Todo
- Figure out a better way to run all three portions at once/in one command
- Better mobile display
- Ensure everything can be hosted on a device on a network and accessed from other devices (i.e. not just localhost)
- Ensure Linux works
- Some devices can appear connected on one query, then disconnected on the next, over and over. It would be cool to implement a buffer/debounce (only notify if connected after being disonnected for 3 queries, etc)  
