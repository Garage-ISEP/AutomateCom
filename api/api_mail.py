import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import pandas as pd

labtemplate = "[XLab]"
roomtemplate = "[Numero de salle]"
datetemplate = "20-04-2023 (Jeudi)"
hourtemplate = "18h30 - 20h"
roomtemplate2 = "L012"
commenttemplate = "[Extra commentaire]"
TEMPLATE = "ressources/assets/template.html"


def send_email(receiver: str, lab: str, name: str, date: str, hour: str, location: str, comment = ""):
    """
    Send mail using an HTML template with all the information. The current template is for room reservation.
    :param receiver : Mail of the receiver
    :param comment: Add a comment
    :param lab: The lab organizing the event
    :param name: The name of the event
    :param date: format de la date : DD-MM-AAA
    :param hour: format de l'heure : HH:MM - HH:MM
    :param location : nom de la salle ou de la localisation
    :return:
    """

    # Email Configuration
    receiver_email = receiver
    subject = "Réservation de salle GarageISEP - " + name

    message = str(open(TEMPLATE, "r"))

    message.replace(labtemplate, lab)
    message.replace(roomtemplate, location)
    message.replace(roomtemplate2, location)
    date = pd.Timestamp(date)
    message.replace(datetemplate, f'{date}({date.day_name})')
    message.replace(hourtemplate, hour)
    message.replace(commenttemplate, comment)

    print(message)

    # Create email message
    email_message = MIMEMultipart()
    email_message["From"] = os.getenv("MAIL_ADRESS_1")
    email_message["To"] = receiver_email
    email_message["Subject"] = subject
    email_message.attach(MIMEText(message, "plain"))

    # Send email
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.login(os.getenv("MAIL_ADRESS_1"), os.getenv("MA1_PASSWORD"))
        server.send_message(email_message)
    print("Email sent successfully!")

if __name__ == '__main__':
    pass