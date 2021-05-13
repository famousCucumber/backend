"""
Email Sender

Written by Eunhak Lee @famousCucmuber, SW Maestro 12
"""
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP, SMTP_SSL
from ssl import create_default_context
import argparse


def bool_checker(s) -> bool:
    l = s.lower()
    if l == "t" or l == "true":
        return True
    elif l == "f" or l == "false":
        return False

    raise TypeError("Not acceptable value as bool")


parser = argparse.ArgumentParser(description="Email Sender")
parser.add_argument("username", type=str, help="Sender's email info to log in")
parser.add_argument("password", type=str, help="Sender's password")
parser.add_argument("receivers", type=str, nargs='+')

content_selector = parser.add_argument_group("Content to send")
content_selector.add_argument("--content", type=str, help="Content to send", required=False)
content_selector.add_argument("--file", type=argparse.FileType('r', encoding='UTF-8'), required=False)

parser.add_argument('--host', default="smtp.gmail.com")
parser.add_argument('--port', default=465)
parser.add_argument("--ssl", type=bool_checker, default=True)


class EmailSender:
    host: str
    port: int
    ssl: bool
    username: str
    password: str

    def __init__(
        self,
        username: str, password: str,
        host: str, port: int = 465,
        ssl: bool = True
    ):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.ssl = ssl

    def send_email(self, receivers, content: str, subject: str = "Welcome to famousCucumber backend"):
        with SMTP_SSL(self.host, self.port, context=create_default_context()) as daemon:
            print("[!] Logging in as {} to server {}".format(self.username, self.host))
            daemon.login(self.username, self.password)
            print("[!] Logged in")

            print("[!] Building mail body")
            message = MIMEMultipart("Message")
            message["Subject"] = subject
            message["From"] = "famousCucumber <{}>".format(self.username)
            
            message.attach(MIMEText(content, "html"))

            print("[!] Built message")
            print(message.as_string())

            print("[!] Sending email to {}".format(receivers))
            print(daemon.sendmail(from_addr=self.username, to_addrs=receivers, msg=message.as_string()))
            print("[!] Sent")


if __name__ == "__main__":
    args = parser.parse_args()

    sender = EmailSender(
        username=args.username,
        password=args.password,
        host=args.host,
        port=args.port,
        ssl=args.ssl
    )
    print(sender.username, sender.password)
    print(sender.host, sender.port, sender.ssl)
    
    
    content = args.content or args.file.read()
    sender.send_email(args.receivers, content)
