import functools
import json
import datetime
import requests
import nicehash

API_KEY = ""
API_SECRET = ""
ORG_ID = ""
RIG_ID = ""
ALGO_CODE = ""

DISCORD_WEBHOOK = ""
MINING_WATTAGE = 
ELECTRICITY_PRICE_UNIT = ""
ELECTRICITY_PRICE_PER_KWh = 

def getDB():
    with open("data.json", "r") as f:
        return json.load(f)


def overwriteDB(data):
    with open("data.json", "w") as f:
        json.dump(data, f)
        print("New Entry added")

    sendDiscordMessage()


def API(start, end):
    api = nicehash.private_api(host="https://api2.nicehash.com", key=API_KEY,
                               secret=API_SECRET, organisation_id=ORG_ID)

    params = "rigId=" + RIG_ID + "&algorithm=" + str(ALGO_CODE) + "&afterTimestamp=" + \
        str(int(start.timestamp() * 1000)) + \
        "&beforeTimestamp=" + str(int(end.timestamp() * 1000))

    response = api.request(
        method="GET", path="/main/api/v2/mining/rig/stats/algo", query=params, body="")

    return response["data"]


def calculateTime(start, end):
    data = API(start, end)

    totalSeconds = 0
    lastTime = 0

    for point in data:
        # Currently mining
        if lastTime - point[0] == 300000:
            lastTime = point[0]
            totalSeconds += 300
        else:
            lastTime = point[0]

    return datetime.timedelta(seconds=totalSeconds)


def updateUptimeData():
    db = getDB()

    if db == []:
        now = datetime.datetime.now()
        weekAgo = now - datetime.timedelta(days=1)

        print("First Entry")

        time = calculateTime(weekAgo, now)

        data = [{
            "start": weekAgo.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "uptime-seconds": time.total_seconds()
        }]

        overwriteDB(data)

    else:
        now = datetime.datetime.now()
        newStart = datetime.datetime.strptime(
            db[0]["end"], "%Y-%m-%dT%H:%M:%S")

        print("New Entry")

        if now - newStart > datetime.timedelta(minutes=5):
            time = calculateTime(newStart, now)

            data = {
                "start": newStart.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": now.strftime("%Y-%m-%dT%H:%M:%S"),
                "uptime-seconds": time.seconds
            }

            if data:
                overwriteDB(db.insert(0, data))

        else:
            print("Already got data - wait 5 minutes")


def sendDiscordMessage():
    db = getDB()
    start = datetime.datetime.strptime(db[0]["start"], "%Y-%m-%dT%H:%M:%S")
    end = datetime.datetime.strptime(db[0]["end"], "%Y-%m-%dT%H:%M:%S")
    seconds = datetime.timedelta(seconds=db[0]["uptime-seconds"])

    body = "Uptime monitor recently recorded **" + str(seconds) + "** of mining\n"

    data = {
        "username": "NiceHash Uptime Monitor",
        "avatar_url": "https://www.nicehash.com/static/logos/logo_small_dark.png",
        "embeds": [{
            "title": "Nicehash Uptime Monitor Update",
            "description": body,
            "fields": [
              {
                "name": "From",
                "value": '\n'.join(str(start).split(' ')),
                "inline": True
              },
              {
                "name": "To",
                "value": '\n'.join(str(end).split(' ')),
                "inline": True
              },
              {
                "name": "Period",
                "value": str(end - start),
                "inline": True
              },
            ]
        }]
    }

    requests.post(DISCORD_WEBHOOK, json=data)

    # Monthly Report
    if (end.year - start.year) * 12 + (end.month - start.month) > 0:

      stoppingIndex = len(db)

      # Filter data so only this months is present
      for i in range(len(db)):
        if datetime.datetime.strptime(db[i]["start"], "%Y-%m-%dT%H:%M:%S").month != start.month:
          stoppingIndex = i

      monthsData = db[:stoppingIndex]

      totalTime = functools.reduce(lambda a, b : a["uptime-seconds"] + b["uptime-seconds"], monthsData)
      if len(monthsData) == 1:
        totalTime = monthsData[0]["uptime-seconds"]

      timeDelta = datetime.timedelta(seconds=totalTime)

      electricityCost = ELECTRICITY_PRICE_UNIT + str(int(ELECTRICITY_PRICE_PER_KWh) * int(MINING_WATTAGE) * 0.001 * timeDelta.total_seconds() / 3600)

      body = "For the month of **" + start.strftime("%B %Y") + "**\nYou mined for **" + str(timeDelta) + "**\nWhich is equal to **" + electricityCost + "**"
      
      data = {
        "username": "NiceHash Uptime Monitor",
        "avatar_url": "https://www.nicehash.com/static/logos/logo_small_dark.png",
        "embeds": [{
            "title": "Monthly Report",
            "description": body
        }]
      }
      requests.post(DISCORD_WEBHOOK, json=data)


updateUptimeData()