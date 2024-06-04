import configparser
import datetime
import smtplib
import os
import sys
from _datetime import datetime
import time
from email.message import EmailMessage
import psutil


config_file = 'config.cfg'
prohibited_words_file = 'prohibited_words.txt'


def load_config():
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def load_prohibited_words():
    with open(prohibited_words_file, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def send_email(subject, body):
    config = load_config()
    to_email = config.get('Email', 'email_to')
    from_email = config.get('Email', 'email_from')
    from_password = os.getenv('EMAIL_PASSWORD')

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, from_password)
        server.send_message(msg)

    print(f'[{datetime.now()}] Email sent to {to_email}')


def guard_dog():
    prohibited_words = load_prohibited_words()
    config = load_config()
    watched_file = config.get('System','watched_file')
    guarded_app = config.get('System', 'guarded_app')
    print(f"[{datetime.now()}] [{guarded_app}] guarding {watched_file}")
    with open(watched_file, 'r') as file:
        log_contents = file.readlines()
    matched_lines = []
    for line in log_contents:
        for word in prohibited_words:
            if word in line:
                matched_lines.append(line.strip())
                break
    if matched_lines:
        terminated = False
        for proc in psutil.process_iter():
            if proc.name() == guarded_app:
                try:
                    proc.terminate()
                    print(f"[{datetime.now()}] Process terminated: {proc.name()}")
                    terminated = True
                except Exception as e:
                    print(f"[{datetime.now()}] Failed to kill process: {proc.name()} {e}")
                    terminated = False

        subject = f'Guarddog alert in watched file'
        body = f'Checked activity in watched file: {watched_file}\n\n{matched_lines}\n\n' \
               f'Guarddog {"killed guarded app" if terminated else "was not able to kill guarded app."}'

        try:
            send_email(subject, body)
            sys.exit(0)
        except Exception as e:
            print(f"Failed to send email {e}")


def run_app():
    config = load_config()
    interval = int(config.get('App', 'check_interval_minutes'))
    print(f"[{datetime.now()}] Guarddog started for {config.get('System', 'guarded_app')}\n"
          f"[{datetime.now()}] Checking {config.get('System','watched_file')} every {interval} minutes")

    while True:
        guard_dog()
        time.sleep(interval * 60)


run_app()
