import requests
from datetime import datetime
import smtplib
import time
GMT_HOUR = 8
hkt_sunrise = 0
hkt_sunset = 0
is_dark = None
TOLORENCE = 5
iss_latitude = None
iss_longitude = None

my_email = "shopisoeasy@gmail.com"
my_password = "h0wMuch$"

def hkt_converter(sunrise, sunset):
    global hkt_sunrise, hkt_sunset
    if sunrise + 8 > 24:
        hkt_sunrise = sunrise % 24
    else:
        hkt_sunrise = sunrise
    if sunset + 8 > 24:
        hkt_sunset = sunset % 24
    else:
        hkt_sunset = sunset



MY_LAT = 22.292923 # Your latitude
MY_LONG = 114.271015 # Your longitude

parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

def is_overhead():
    global iss_latitude, iss_longitude
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])


    if MY_LAT - TOLORENCE <= iss_latitude <= MY_LAT + 5 and MY_LONG - TOLORENCE <= iss_longitude <= MY_LONG + TOLORENCE:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    hkt_converter(sunrise + GMT_HOUR, sunset + GMT_HOUR)


    time_now = datetime.now()
    time_now_hour = time_now.hour
    if time_now_hour > hkt_sunset or time_now_hour < hkt_sunrise:
        return True



# -----------------------------if is_overhead and is_night True, send email ------------------------------#

#---- to make it continue running every 60 sec in the background-------------#

while True:
    time.sleep(60)
    if is_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs="kamiklza@hotmail.com", msg="Subject: ISS Checker\n\n"
                                                                                     "Look up to the sky!")
        connection.close()
    else:
        print("Noting to see")








#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



