#!/usr/bin/python

##        SEND ALERTS: 
##        This script contains methods that send SMS / Email alerts. The settings and recipients are read from an ini file [set as 'config_file'].
##        Author: Yameen Rasheed
##        04 March 2013
  
import sys
import string
import urllib
import urllib2
import urlparse
import smtplib

from email.mime.text import MIMEText
from ConfigParser import SafeConfigParser

config_file ='/mnt/example/alertinator/config.ini'

def send_alert(error_desc, msg):
    ## Send SMS Alerts
    for recipient in get_sms_recipients():
        send_sms(recipient, msg)
    ## Send Email Alerts
    for email_recipient in get_email_recipients():
        send_email(email_recipient, error_desc, msg)

def get_sms_recipients():
    parser = SafeConfigParser()
    parser.read(config_file)
    return parser.get('ContactList','sms_list').split("|")

def get_email_recipients():
    parser = SafeConfigParser()
    parser.read(config_file)
    return parser.get('ContactList','email_list').split("|")

def send_sms(mobile_no, msg):
    parser = SafeConfigParser()
    parser.read(config_file)
    
    url = parser.get('SMSC','sms_url') 
    user =  parser.get('SMSC','sms_user') 
    pwd  =  parser.get('SMSC','sms_pwd') 

    values = {'User':user,
              'Password':pwd,
	      'PhoneNumber':mobile_no,
              'Text':msg}

    data = urllib.urlencode(values)
    req = urllib2.Request(url,data)
    resp = urllib2.urlopen(req)
    print '\tSMS alert sent to {}'.format(mobile_no)
    return

def send_email(recipient, error_desc, msg):
    parser = SafeConfigParser()
    parser.read(config_file)
    smtp_host = parser.get('SMTP','smtp_host') 
    smtp_sender = parser.get('SMTP', 'smtp_sender')

    message = MIMEText(msg)
    message['Subject'] = 'ALERT: {} detected'.format(error_desc)
    message['From'] = smtp_sender
    message['To'] = recipient
    
    s = smtplib.SMTP(smtp_host)
    s.sendmail(smtp_sender, recipient, message.as_string())
    print '\tEmail sent to {}'.format(recipient)
    s.quit()
    

