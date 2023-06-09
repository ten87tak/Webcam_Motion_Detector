import smtplib
import imghdr
from email.message import EmailMessage

# Set your app password, sender/receiver email address:
PASSWORD = "Enter Your App Password Here"
SENDER = "Enter Your Email Address"
RECEIVER = "Enter Your Email Address"


def send_email(image):
    print("The send_email function started.")
    message = EmailMessage()
    message["Subject"] = "New customer came in!"
    message.set_content("See the attached photo that shows the new customer:)")

    with open(image, "rb") as file:
        content = file.read()
    message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, message.as_string())

    print("The send_email function ended.")


if __name__ == "__main__":
    send_email(image="images/1.png")


