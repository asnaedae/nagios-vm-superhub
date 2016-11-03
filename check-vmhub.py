#!/usr/bin/python

import argparse
import requests
import sys
from bs4 import BeautifulSoup
import dateparser
import time
import platform

result = {}

def display_nagios_check(result):
    print "PING ok - downloaded = {}, MB, uploaded = {} MB | downloaded={}, uploaded={}, session_time={}".format(result['downloaded'], result['uploaded'], result['downloaded'], result['uploaded'], result['session_time'])

def display_nagios_graphite_metrics(result):
    now = time.strftime('%s')
    hostname = platform.node()
    for row in result:
        if row != "wan_ip_address":
            print '{}.virginmedia.{} {} {}'.format(hostname, row, result[row], now)

if __name__ == '__main__':
    secret = ""
    parser = argparse.ArgumentParser(description='retrieve data from VirginMedia Hub')
    parser.add_argument('--verbose', '-v', help='increase logging', action="store_true")
    parser.add_argument('--host', '-d', help='IP address of homehub', default='192.168.0.1')
    parser.add_argument('--password', '-p', help='Homehub login password', default='password')
    parser.add_argument('--graphite', '-g', help='return graphite instead of normal nagios check', dest='graphite', action='store_true', default=False)
    args = parser.parse_args()

    url = 'http://' + args.host + '/'
    password = args.password

    s = requests.Session()
    page = s.get(url + 'VmLogin.html')
    soup = BeautifulSoup(page.text, "lxml")
    
    for row in soup.find_all('input', id='password'):
        secret = row['name']

    if secret == "":
        print >> sys.stderr, "ERROR: unable to login to hub"
        sys.exit(1)

    data = secret + ': "' + password + '"'
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }

    # send login request
    page = s.post(url + 'cgi-bin/VmLoginCgi', data={ secret: password }, headers=headers)
    soup = BeautifulSoup(page.text, "lxml")

    page = s.get(url + 'device_connection_status.html')
    soup = BeautifulSoup(page.text, "lxml")
    failed_login = len(soup.find_all('div', id='signInForm'))

    if failed_login == 1:
        print >> sys.stderr, "ERROR: unable to login to hub, status code was ", failed_login
        sys.exit(1)

    for row in soup.find_all('div', class_='field noHint longLabel clearfix'):
        # simplify data
        data = row.span.string.replace(',', '').replace(' MB', '')

        if row.label.string.startswith("WAN IP"):
             label = "wan_ip_address"
        if row.label.string == "Session Data Downloaded":
             label = "downloaded"
        if row.label.string == "Session Data Uploaded":
                label = "uploaded"
        if row.label.string == "Session Time":
            data = dateparser.parse(data, date_formats=['%d %h:%m:%s']).strftime('%s')
            label = "session_time"
        result[label] = data


    if isinstance(result, dict):
        if args.graphite:
            display_nagios_graphite_metrics(result)
        else:
            display_nagios_check(result)
    else:
        print "Failed"

    page = s.get(url + 'VmLogout2.html')
