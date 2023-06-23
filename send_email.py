import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import config
from logger import logger


def send_email(
    subject: str,
    body: str,
    from_addr: str = f'Bond Helper <{config("smtp", "user")}>',
    to_addr: str | list = config("smtp", "user"),
):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = type(to_addr) == list and ", ".join(to_addr) or to_addr

    # Convert the body to a MIMEText object and attach it to the message container.
    part = MIMEText(body, "html")
    msg.attach(part)

    # Send the message using the SMTP server.
    try:
        smtpObj = smtplib.SMTP(
            host=config("smtp", "host"),
            port=config("smtp", "port"),
        )
        smtpObj.starttls()  # Enable TLS encryption
        smtpObj.login(
            config("smtp", "user"), config("smtp", "password")
        )  # Login to the SMTP server
        smtpObj.sendmail(from_addr, to_addr, msg.as_string())
        logger.log_info("✅ Successfully sent email")
    except smtplib.SMTPException as e:
        logger.log_warn(f"❌ Error: unable to send email. {e}")
