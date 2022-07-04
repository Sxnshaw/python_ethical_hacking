#!usr/bin/env python
import requests
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="link", help="url of the file")
    options = parser.parse_args()
    return options


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


options = get_arguments()
download(options.link)