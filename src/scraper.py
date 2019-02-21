'''
    Meal menu scraper

    @author: Fuad Aghazada
'''

import requests
import bs4
import sys
import re
from datetime import datetime

from pprint import pprint

# URL
URL = 'http://kafemud.bilkent.edu.tr/monu_eng.html'

'''
    Sending request to the given url
'''
def send_request(url):
    req = requests.get(url)

    try:
        req.raise_for_status()
    except Exception as e:
        print(e)
        sys.exit()

    print('Request is successful!')
    return req


'''
    Fetch today's menu
'''
def fetch_todays_menu():
    today = str(datetime.now()).split(' ')[0]
    today = datetime.strptime(today, '%Y-%m-%d').strftime('%d.%m.%Y')

    menus = fetch_menus()

    # Fix
    fix = None
    for f_menu in menus['fix']:
        if f_menu['date'] == today:
            fix = f_menu
            break

    # Alternative
    alt = None
    for alt_menu in menus['alternative']:
        if alt_menu['date'] == today:
            alt = alt_menu
            break

    return {
        'fix': fix,
        'alt': alt
    }


'''
    Fetching meals from table
'''
def fetch_meal(meal_table):
    if len(meal_table) == 0:
        return None

    meal_table.pop(0)

    meals = []
    for meal in meal_table:
        columns = meal.find_all('td')

        if columns[0].find('p'):
            date = re.search(r'\d+.\d+.\d+', columns[0].find('p').text).group()
            meal = process_meal(columns[1].get_text())
            meals.append({
                'date': date,
                'lunch': meal
            })
        else:
            meal = process_meal(columns[0].get_text())
            meals[-1]['dinner'] = meal

    return meals


'''
    Fetching menus & meals
'''
def fetch_menus():
    req = send_request(URL)

    # Scraper
    soup = bs4.BeautifulSoup(req.text, 'html.parser')

    fix_table = soup.select('body > div > center > table > tr:nth-of-type(3) > td:nth-of-type(2) > div > table > tr:nth-of-type(1) > td > table > tr:nth-of-type(2) > td > table tr')
    alt_table = soup.select('body > div > center > table > tr:nth-of-type(3) > td:nth-of-type(2) > div > table > tr:nth-of-type(1) > td > table > tr:nth-of-type(3) > td > table tr')

    fix_meals = fetch_meal(fix_table)
    alt_meals = fetch_meal(alt_table)

    return {
        'fix': fix_meals,
        'alternative': alt_meals
    }


'''
    Processing meal string
'''
def process_meal(meal_txt):

    meal_txt = replace_char(meal_txt)

    meal_txt = meal_txt.replace('\r\n', '')
    meal_txt = meal_txt.replace('\t', '')
    meal_txt = meal_txt.replace('\n', ' ')

    token1 = 'Öğle Yemeği / Lunch'
    token2 = 'Akşam Yemeği / Dinner'

    if token1 in meal_txt:
        meal_txt = meal_txt.replace(token1, '')
    elif token2 in meal_txt:
        meal_txt = meal_txt.replace(token2, '')

    meals = meal_txt.split('/')

    meal_txt = ''
    for meal in meals:
        meal = meal.strip()
        meal_txt += meal + '\n'

    return meal_txt


'''
    Replacing chars
'''
def replace_char(txt):
    '''
     ð - ğ
     ý - ı
     Þ - Ş
     þ - ş
    '''
    txt = txt.replace('ð', 'ğ')
    txt = txt.replace('ý', 'ı')
    txt = txt.replace('Þ', 'Ş')
    txt = txt.replace('þ', 'ş')


    return txt
