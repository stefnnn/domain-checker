#!/usr/bin/env python3
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import logging
import subprocess

load_dotenv()

DOMAIN_LIST_PATH = os.getenv("DOMAIN_LIST", "domain-list")
lines = open(DOMAIN_LIST_PATH).read().splitlines() 
DOMAINS = [domain for domain in lines if domain and not domain.startswith("#")]

# Email configuration
EMAIL_FROM = os.getenv("EMAIL_FROM", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Domain-Checker found a domain")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = 587

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

required_env_keys = ["EMAIL_FROM", "EMAIL_TO", "SMTP_USER", "SMTP_PASSWORD", "SMTP_HOST"]
if not all(key in os.environ for key in required_env_keys):
    raise ValueError(f"Please set all required environment variables in .env file: {required_env_keys}")


def is_domain_registered(domain):
    result = subprocess.run(['whois', domain], capture_output=True, text=True)
    output = result.stdout.lower()
    if "No match" in output or "not found" in output or "no entries found" in output or "do not have an entry" in output:
        return False
    else:
        return True


def send_email(domain):
    body = f"The domain {domain} appears to be not registered anymore."
    msg = MIMEText(body)
    msg["Subject"] = f"{EMAIL_SUBJECT} - {domain}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        logger.debug(f"Notification sent for {domain}")
    except Exception as e:
        logger.debug(f"Failed to send email for {domain}: {e}")


def main():
    for domain in DOMAINS:
        logger.debug(f"Checking {domain}...")
        if not is_domain_registered(domain):
            logger.debug(f"{domain} is available!")
            send_email(domain)
        else:
            logger.debug(f"{domain} is registered.")


if __name__ == "__main__":
    main()
