
# coding: utf-8

# In[1]:


print('The hunt has begun.') 
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import smtplib
import time


# In[2]:


session = Session(server_token='xU9p-qMcopVdb2-PAfy9T-Tyqox_yqnT4CRCGUhu')
client = UberRidesClient(session)
client_email_address = 'chrisprabhu2@gmail.com'
client_password = 'isbvgwqwdwmkzdhg'

email_to = 'chrisprabhu2@gmail.com'


# In[3]:


s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(client_email_address, client_password)
msg = MIMEMultipart()


# In[4]:


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


# In[5]:


def send_email(email_to, message_subject, the_message):
    msg['From'] = client_email_address
    msg['To'] = email_to
    msg['Subject'] =  message_subject
    msg.attach(MIMEText(the_message, 'plain'))
    s.send_message(msg)


# In[6]:


def SurgeHunter(): 
    estimate = get_prices()
    surge_multiplier = estimate / 37
    if estimate/37 > 2:
        send_email(email_to,f'{surge_multiplier} Active Surge','Hunt')
    del estimate
    del surge_multiplier


# In[7]:


schedule.every().day.at("20:00").do(send_email,'chrisprabhu2@gmail.com', 'test run clocked for 8:00PM', 'the hunt continues')
schedule.every().day.at("21:00").do(send_email,'chrisprabhu2@gmail.com', 'test run clocked for 8:00PM', 'the hunt continues')


# In[8]:


schedule.every(2).minutes.do(SurgeHunter)


# In[9]:


while True:
    schedule.run_pending()
    time.sleep(60)

