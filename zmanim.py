from __future__ import print_function
from bs4 import BeautifulSoup
from mechanize import Browser
import datetime
import lxml
import re
import json

# initialization
browser = Browser()


def get_shabbat_times(zip):
    base_domain = 'https://www.myzmanim.com/day.aspx?askdefault=1&vars=US'
    domain = "{}{}".format(base_domain, zip)
    print (domain)
    browser.open(domain)  # Open the page with the Zip Code from the config file

    # Get to the Friday times page
    day_of_week = datetime.datetime.today().weekday()     # 0: Monday, ... 6: Sunday
    if day_of_week == 3:      # Thursday
        browser.follow_link(text="Tomorrow")
    elif day_of_week == 5:      # Saturday
        browser.follow_link(text="Yesterday")
    elif day_of_week != 4:   # Any other day
        browser.follow_link(text="Friday")

    page = browser.response().read()
    soup = BeautifulSoup(page, "html5lib")

    candle_lighting = soup.find("span", string="Candle lighting").next_sibling.next_sibling.next_sibling.get_text().strip()
    shabbat_ends = soup.find("span", string=re.compile("Next day Shabbos ends")).next_sibling.next_sibling.next_sibling.contents[3].get_text().strip()
    times = {
        'candle_lighting': candle_lighting,
        'shabbat_ends': shabbat_ends
    }
    return times


def get_parsha():
    domain = 'http://www.aish.com/tp/'
    
    browser.open(domain)
    page = browser.response().read()
    soup = BeautifulSoup(page, "html5lib")

    div = soup.find("div", {"class": "parshaHdrRow"}).contents[1]
    # section = div.span.get_text()
    div.span.clear()
    parsha = {
        "parsha": div.get_text().strip()
    }
    return parsha


def handler(event, context):
    zip = '02906'
    if 'zip' in event:
        zip = event['zip']
    print (zip)
    shabbat_times = get_shabbat_times(zip)
    # parsha = get_parsha()
    response = {
        "times": shabbat_times,
        # "parsha": parsha
    }
    return response
