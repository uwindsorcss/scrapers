# creates list of prof emails
# get the select picker to select department
# the options there are the different departments
# then the value put through url encoding and gotten its requests
# then from there each department page scraped and
# the emails will put into a list

import requests

from pprint import pprint

from bs4 import BeautifulSoup

import urllib.parse

def get_department_page(extension):
    # get web page
    url = f'https://www.uwindsor.ca/directory/department/{extension}'
    resp = requests.get(url)

    # parse webpage into object
    return BeautifulSoup(resp.content, 'html.parser')

def get_emails_from_department(department):
    emails = []

    staff = department.select("a[href^=mailto]")
    for person in staff:
        try:
            span = person.select('span')[0]
            emails.append(span.text)
        except:
            continue

    return emails

def get_list():

    # get web page
    url = 'https://www.uwindsor.ca/directory/department'
    resp = requests.get(url)

    # parse webpage into object
    soup = BeautifulSoup(resp.content, 'html.parser')

    # get the select picker to select department
    department_select = soup.find_all('select')[0]
    #print(departments)

    departments = department_select.find_all('option')[1:]
    #pprint(departments)

    department_extensions = []

    for department in departments:
        value = department['value']
        url_safe_value = urllib.parse.quote(value)
        department_extensions.append(url_safe_value)

    emails = []
    for department_extension in department_extensions:
        page = get_department_page(department_extension)
        emails +=(get_emails_from_department(page))

    return emails




if __name__ == "__main__":
    emails = get_list()
    print(emails)
