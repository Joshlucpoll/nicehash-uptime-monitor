# Nicehash Uptime Monitor

## What is this?
This program records and notifies how long a specific rig has been mining for using Nicehash. It can also work out your energy usage and cost for the month!

***Sidenote*** *-- This program only works with a single algorthim (e.g. DaggerHashimoto), so the [Nicehash QuickMiner](https://www.nicehash.com/quick-miner) is best used in this case*

## How does it work?
It uses Nicehash's API and Discord webhooks to look up when a rig has been mining and display that information. It uses a schedular to run at set time intervals and record information in a JSON file about the status of a rig. Every time the the program runs will add to this data file and send a notification to the specified Discord webhook. As well as this the monitor sends a monthly message with electricity usage and cost.

## Prerequisites
You will need [Python](https://www.python.org/downloads/) and the [requests package](https://pypi.org/project/requests/) for this program to work. 
As well as this you will need to obtain this information:

1. [An API Key and API Secret from Nicehash](#getting-api-keys-and-organisation-id)
2. [Your Organisation ID](#getting-api-keys-and-organisation-id)
3. [Your Rig ID](#getting-rig-id)
4. [Algorithm Code](#algorithm-codes) (usually "20", if DaggerHashimoto)
5. [A Discord Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
6. [Mining Wattage](#find-mining-wattage)
7. [Electricity price per KWh](#electricity-usage)


### Getting API Keys and Organisation ID

![](https://raw.githubusercontent.com/nicehash/rest-clients-demo/master/generate_key.gif)

1. Go to settings in the Nicehash dashboard:
![](https://i.imgur.com/kpDeHsS.png)


2. Go to 'API Keys' tab and click **CREATE NEW API KEY**
Also take note of your **Organisation ID** here:
![](https://i.imgur.com/AacsmEj.png)


3. Name the API Key whatever you want then allocate its permissions. This monitor only requires the *View mining data and statistics* permission:
![](https://i.imgur.com/ILdxsMy.png)

4. Press **GENERATE API KEY** and take note of both the **API Key code** and **API Secret Key Code**

### Getting Rig ID

1. Click the Rig you want to monitor:
![](https://i.imgur.com/nQMvR5K.png)

2. Take note of Rig ID:
![](https://i.imgur.com/kWsRYIP.png)

### Find Mining Wattage

1. Start mining with Nicehash and leave it running for a few minutes
2. Check on Nicehash dashboard the **Power** field for the GPU:
![](https://i.imgur.com/jVefwKJ.png)

### Electricity Usage
For the monitor to correctly calculate the electricity cost of mining you must provide your average price per KWh and the currency symbol of that price e.g. '£' or '$', etc

*Avoid using smaller denomination of currency like pence or cent as the final electricity cost will be outputted in the same denomination*

### Algorithm Codes

| Algorithm        |ID|
|------------------|--|
| Scrypt           | 0|
| SHA256           | 1|
| ScryptNf         | 2|
| X11              | 3|
| X13              | 4|
| Keccak           | 5|
| X15              | 6|
| Nist5            | 7|
| NeoScrypt        | 8|
| Lyra2RE          | 9|
| WhirpoolX        |10|
| Qubit            |11|
| Quark            |12|
| Axiom            |13|
| Lyra2REv2        |14|
| ScryptJaneNf16   |15|
| Blake256r8       |16|
| Blake256r14      |17|
| Blake256r8vnl    |18|
| Hodl             |19|
| DaggerHashimoto  |20|
| Decred           |21|
| CryptoNight      |22|
| Lbry             |23|
| Equihash         |24|
| Pascal           |25|
| X11Gost          |26|
| Sia              |27|
| Blake2s          |28|
| Skunk            |29|
| CryptoNightV7    |30|
| CryptoNightHeavy |31|
| Lyra2Z           |32|
| X16R             |33|
| CrpytoNightV8    |34|
| SHA256AsicBoost  |35|
| Zhash            |36|
| Beam             |37|
| GrinCuckaroo29   |38|
| GrinCuckatoo31   |39|
| Lyra2REv3        |40|
| MTP              |41|
| CrpytoNightR     |42|
| CuckoCycle       |43|
| GrinCuckarood29  |44|
| Beamv2           |45|
| X16Rv2           |46|
| Eaglesong        |48|
| GrinCuckaroom29  |49|
| GrinCuckatoo32   |50|
| Handshake        |51|
| KAWPOW           |52|
| Cuckaroo29BFC    |53|
| BeamV3           |54|
| CuckaRooz29      |55|
| Octopus          |56|

## Setup

### Download

Git clone:
`git clone https://github.com/joshlucpoll/nicehash-uptime-monitor`

Or [download ZIP](https://github.com/joshlucpoll/nicehash-uptime-monitor/archive/refs/heads/master.zip)

### Variables
Inside `main.py` you will find this block of code at the top:

```
API_KEY = ""
API_SECRET = ""
ORG_ID = ""
RIG_ID = ""
ALGO_CODE = ""

DISCORD_WEBHOOK = ""
MINING_WATTAGE = 
ELECTRICITY_PRICE_UNIT = ""
ELECTRICITY_PRICE_PER_KWh = 
```

Fill in all the values obtained in the [prerequisites stage](#prerequisites), making sure all the values **except** `MINING_WATTAGE` and `ELECTRICITY_PRICE_PER_KWh` are surrounded with speech marks: `"abc"`.

### Running the Monitor

To run this monitor you need to setup a schedular. Depending on if you are on [Windows](#windows) or [Linux](#linux) this is achieved in different ways. The timings of when the schedular should run the script can be between every 5 minutes to 7 days. Nicehash keeps statistic data for up to 7 days, so the script should be set to run at least every 7 days; data points are updated every 5 minutes, so the script shouldn't be run more than every 5 minutes. I found the **best timing to be 1 day** so when the monthly electricity cost is being calculated there is no overlap between months.

#### Windows

1. Create a `.bat` file in the same directory as `main.py` and enter `<Your Python.exe Path> <Path to main.py>` into it.

e.g. `"C:\Users\username\AppData\Local\Programs\Python\Python39" "C:\Users\username\Documents\nicehash-uptime-monitor\main.py"`

2. Search for Task Scheduler, and open it:
![](https://miro.medium.com/max/700/1*mZQ2Zy5su6r8QzCaGpLckw.png)

3. Click 'Create Basic Task' and name the task something appropriate:
![](https://miro.medium.com/max/700/1*rcZMqC46mIHnEkvTCNY87w.png)

4. Then choose daily as the trigger and leave the start date and time as is
![](https://miro.medium.com/max/700/1*xVl7Y3UWv4dGDV9GFCE8Ww.png)

5. Select 'Start a program' as the action:
![](https://miro.medium.com/max/700/1*qvt7Z6rQE_MpoNqONhXd8w.png)

6. Browse for the `.bat` file you just created and select it. **Make sure you include the 'Start in' parameter**, input the path to the folder where the `main.py` file is located:
e.g. `C:\Users\username\Documents\nicehash-uptime-monitor`
![](https://i.imgur.com/k3gKasO.png)

7. Click Finish! Now Task Schedular should execute the script every day.


#### Linux

1. Open crontab file: `crontab -e`
If this command fails, it's likely that cron is not installed. If you use a Debian based system (Debian, Ubuntu), try the following commands first: 
`sudo apt-get update`
`sudo apt-get install cron`
2. A text-editor will appear, add this line to file:
`0 8 * * * python3 <Path to main.py>`
3. Save file and exit.

This cron job executes daily at 8:00 am. You can adjust the time at which it executes by changing values as such:
`<minute> <hour> * * * python3 <Path to main.py>`

And your done! Cron should execute the script every day.

## Finishing Up

If everything is setup right you should receive a Discord message every-time the script is executed!