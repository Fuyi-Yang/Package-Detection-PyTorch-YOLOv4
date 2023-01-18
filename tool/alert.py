import smtplib
from email.message import EmailMessage
import pyautogui
import pywhatkit
import datetime
import time
from instabot import Bot

def email_alert(subject, body, to): # Sends message to Email or phone number
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "xxx@email.com"
    msg['from'] = user
    password = ""

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    print("email sent")
    server.quit()

def whatsapp_alert(body, to): #Sends message to whatsapp;  requires phone number
    time = datetime.datetime.now()
    pywhatkit.sendwhatmsg(to, body, time.hour, time.minute)

def messenger_alert(body, to): #Sends message to Messenger; cursor needed
    pyautogui.typewrite(body)
    pyautogui.press('enter')

def instgram_alert(body, to): #Sends message to Instagram; requires username
    mybot = Bot()
    mybot.login(username = "", password= "")
    send_to = mybot.get_user_id_from_username(to)
    mybot.follow(send_to)
    mybot.send_message(body, [send_to])

if __name__ == '__main__':
    email_alert("Your package has arrived",
                "Hi, \n\n We have detected that your package has arrived. Please pick it up!!", "xxx@email.com")
    whatsapp_alert("Hi, \n\n We have detected that your package has arrived. Please pick it up!!", "+1 1111111111")
