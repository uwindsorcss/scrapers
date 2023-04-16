import json
import urllib.parse
from pprint import pprint
import requests
from bs4 import BeautifulSoup

def get_department_page(extension):
    """Returns a BS4 object for a department page"""

    # getting html
    url = f'https://www.uwindsor.ca/directory/department/{extension}'
    resp = requests.get(url, timeout=5)

    # parse webpage into object
    return BeautifulSoup(resp.content, 'html.parser')

def get_entries_from_department(department):
    output = []
    for div in department.find_all('div', {'style': 'margin-top: 20px; border-bottom: 1px solid #E7E7E7;'}):
        name_tag = div.find('div', {'class': 'staff-name'})
        if name_tag is not None:
            name = name_tag.text.strip()
        else:
            name = 'No name specified'

        position_tag = div.find('strong')
        if position_tag is not None:
            position = position_tag.text.strip()
        else:
            position = 'No position specified'

        phone_tag = div.find('span')
        if phone_tag is not None:
            phone = phone_tag.text.strip()
        else:
            phone = 'No phone number specified'

        email_tag = div.find('a')
        if email_tag is not None:
            email = email_tag.text.strip()
        else:
            email = 'No email specified'

        room_tags = div.find_all('span')
        if len(room_tags) > 1:
            room = room_tags[2].text.strip()
        else:
            room = 'No room specified'

        department_tags = div.find_all('span')
        if len(department_tags) > 2:
            dept = department_tags[3].text.strip()
        else:
            dept = 'No department specified'
        
        # Replace all newlines with spaces
        name = name.replace('\n', ' ')
        position = position.replace('\n', ' ')
        phone = phone.replace('\n', ' ')
        email = email.replace('\n', ' ')
        room = room.replace('\n', ' ')
        dept = dept.replace('\n', ' ')
        
        # Replace all occurrences of multiple spaces with a single space
        name = ' '.join(name.split())
        position = ' '.join(position.split())
        phone = ' '.join(phone.split())
        email = ' '.join(email.split())
        room = ' '.join(room.split())
        dept = ' '.join(dept.split())

        entry = {
            "name":name,
            "title":position,
            "phone":phone,
            "email":email,
            "room":room,
            "department":dept
        }
        output.append(entry)
        pprint(entry)
    return output

def get_list():
    print("Getting list...")
    # get web page
    url = 'https://www.uwindsor.ca/directory/department'
    resp = requests.get(url, timeout=5)

    # parse webpage into object
    soup = BeautifulSoup(resp.content, 'html.parser')

    # get the select picker to select department
    department_select = soup.find_all('select')[0]
    # print(departments)

    departments = department_select.find_all('option')[1:]
    pprint(departments)

    department_extensions = []

    for department in departments:
        value = department['value']
        url_safe_value = urllib.parse.quote(value)
        department_extensions.append(url_safe_value)

    pprint(department_extensions)
    entries = []
    for i, department_extension in enumerate(department_extensions):
        page = get_department_page(department_extension)

        entries +=(get_entries_from_department(page))

    return entries

if __name__ == "__main__":
    emails = get_list()
    with open('out.json', 'w') as f:
        f.write(json.dumps(emails))
    # print(json.dumps(emails))
