import json
import time
import requests
from datetime import datetime
import smtplib, ssl

# Send Email if vaccine is available
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = input("Type your email address and press enter: \n")
password = input("Type your password and press enter: \n")
district_id = input("Type your District ID and press enter: \n") # 581 - Hyderabad

context = ssl.create_default_context()

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()

server.login(sender_email, password)

while True:
    try:
        params = {
            "district_id": district_id,
            "date": "29-05-2021"
        }
        data = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict', params=params)
        json_data = json.loads(data.text)
        json_data = json_data['sessions']
        print("Checking availability at " + str(datetime.now()) + ", API Call Response: " + str(data))
        for i in json_data:
            if i['vaccine'] == "COVAXIN" and int(i['available_capacity_dose1']) > 0 and int(i['min_age_limit']) == 18:
                server.sendmail(sender_email, '20311a05f0@sreenidhi.edu.in', str(i))
                print('mail sent')
        time.sleep(30)
    except:
        print("Lost Internet Connection")

