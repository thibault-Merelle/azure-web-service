import smtplib, ssl
import threading
import os 
import sys

def mailing(mail, mymessage):
    sender_mail=os.environ['SENDER_MAIL']
    dest_mail = mail
    password=os.environ['SENDER_PWD']
    message = mymessage

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_mail, password)
    print("logging sender_mail success")
    server.sendmail(sender_mail, dest_mail, message)
    print("mail has been send to ", dest_mail)
    server.quit()