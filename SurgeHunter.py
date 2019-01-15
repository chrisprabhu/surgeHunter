# Import all the required dependencies: 

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import smtplib
import time
import datetime

# Define the session: 
session = Session(server_token='xU9p-qMcopVdb2-PAfy9T-Tyqox_yqnT4CRCGUhu')
client = UberRidesClient(session)
client_email_address = 'chrisprabhu2@gmail.com'
client_password = 'isbvgwqwdwmkzdhg'

# Email to this address: 
email_to = 'chrisprabhu2@gmail.com'

# Connect my email to the email server: 
s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(client_email_address, client_password)
msg = MIMEMultipart()

# Define the function which gets the prices between Laguna Beach and Home: 
def get_prices():
    response = client.get_price_estimates(
    start_latitude=33.54281,
    start_longitude=-117.78352,
    end_latitude=33.659687,
    end_longitude=-117.652535
)
    response_json = response.json['prices']
    high_estimate = response_json[0]['high_estimate']
    low_estimate = response_json[0]['low_estimate']
    estimate_avg = (high_estimate + low_estimate)/2
    return estimate_avg

# Define the function which will send an email: 
def send_email(email_to, message_subject, the_message):
    msg['From'] = client_email_address
    msg['To'] = email_to
    msg['Subject'] =  message_subject
    msg.attach(MIMEText(the_message, 'plain'))
    s.send_message(msg)

# Define the Surge Hunting application: 
query_count = 0
def SurgeHunter():
    estimate = get_prices()
    # surge_multiplier = estimate / 37
    if estimate > (37 + 5):
        send_email(email_to,f'{surge_multiplier} Active Surge','Hunt')
    print ('The API has been queried this many times:', query_count)
    query_count = query_count + 1
    del estimate
    del surge_multiplier

# Define a function to pring the current date and time: 
def printTime():
    print("The hunt continues. Another 10 minutes have passed. The current date and time are:  " + str(datetime.datetime.now()))

# All the scheduled events: 

schedule.every().day.at("23:00").do(send_email(email_to, 'test run clocked for 11:00PM', 'the hunt continues'))
schedule.every(20).minutes.do(SurgeHunter)
schedule.every(10).minutes.do(printTime)

# Print the starting time of the script: 
print(datetime.datetime.now())
print('The hunt has begun.')

count = 0
while True:
    print ('The WHILE loop has run this many times:', count)
    count = count + 1
    schedule.run_pending()
    time.sleep(1)

