import smtplib, ssl
import threading


def mailing(mail, mymessage):
    sender_mail = "dupondj587@gmail.com"
    dest_mail = str(mail)
    password = input(str("Enter your mail password: "))
    message = mymessage

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_mail, password)
    print("logging sender_mail success")
    server.sendmail(sender_mail, dest_mail, message)
    print("mail has been send to ", dest_mail)
    server.quit()