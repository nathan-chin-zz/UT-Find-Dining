'''
Name: Nathan Chin
UT EID: nhc332
Class: EE 119
Professor: Chirag Sakhuja
Date started: 3/8/18
'''

import urllib3
from bs4 import BeautifulSoup
from enum import Enum

def printName(name, symbol):
    loop = 0
    if symbol == '#': print()
    while loop < len(name) + 4:
        print(symbol, end='')
        loop += 1
    print()
    print(symbol, name.upper(), symbol)
    loop = 0
    while loop < len(name) + 4:
        print(symbol, end='')
        loop += 1
    print()

class LOCATION(Enum):
    Jester_City_Limits = 0
    Jester_City_Market = 1
    Jest_A_Pizza = 2
    J2 = 3
    J2_FAST = 4
    Kinsolving = 5
    Kins_Market = 6
    Cypress_Bend_Cafe = 7
    Littlefield_Patio_Cafe = 8
    Georges_Cafe = 9

# Constants
BASE_URL = 'http://hf-food.austin.utexas.edu/foodpro/'
LOCATIONS_URL = 'location2.asp'
LOCATIONS = list(LOCATION)


# Global variables
dining_location_urls = []   #Holds the urls for each dining location

http = urllib3.PoolManager()
page = http.request('GET', BASE_URL + LOCATIONS_URL)
page = BeautifulSoup(page.data.decode('utf-8'), 'lxml')
links = page.find_all('td', attrs={'width':'600px'})
links = links[0].find_all('a')
for l in links:
    dining_location_urls.append(l['href'])

collect = [LOCATION.J2, LOCATION.J2_FAST, LOCATION.Jest_A_Pizza, LOCATION.Kinsolving]
for count, i in enumerate(collect):
    printName(collect[count].name, '#')
    url = dining_location_urls[i.value]
    page = http.request('GET', BASE_URL + url)
    page = BeautifulSoup(page.data.decode('utf-8'), 'lxml')
    menu_data = page.find('frame', attrs={'title': 'main content window'})
    url = BASE_URL + menu_data['src']
    menu = http.request('GET', url)
    menu = BeautifulSoup(menu.data.decode('utf-8'), 'lxml')

    meals = menu.find_all('div', attrs={'class': 'menusampmeals'})
    food = menu.find_all('table', attrs={'cellspacing': '1'})
    for pos, f in enumerate(food):
        printName(meals[pos].text.strip().upper(), '-')
        item = f.find_all('div')
        for i in item:
            print(i.text.strip())
    if len(meals) == 0:
        print(collect[count].name, 'is currently closed :(')
    '''
    meals = menu.find_all('div', attrs={'class': 'menusampmeals'})
    categories = menu.find_all('div', attrs={'class': 'menusampcats'})
    food = menu.find_all('div', attrs={'class': 'menusamprecipes'})
    print('Meals: ')
    [print(m.text.strip()) for m in meals]
    print('Categories: ')
    [print(c.text.strip()) for c in categories]
    print('Food: ')
    [print(f.text.strip()) for f in food]
    print()
    '''
'''
dining_main = "http://hf-food.austin.utexas.edu/foodpro/"
j2_url = 'nutframe2.asp?sName=The+University+of+Texas+at+Austin+%2D+Housing+and+Dining&locationNum=12&locationName=Jester+2nd+Floor+Dining&naFlag=1'
j2_main = http.request('GET', str(dining_main + j2_url))
j2_main_soup = BeautifulSoup(j2_main.data.decode('utf-8'), 'lxml')
j2_frames = j2_main_soup.find('frame', attrs={'title':'main content window'})
j2_menu_url = dining_main + (j2_frames['src'])
j2_menu = http.request('GET', j2_menu_url)
j2_menu_soup = BeautifulSoup(j2_menu.data.decode('utf-8'), 'lxml')
j2_meals = j2_menu_soup.find_all('div', attrs={'class':'menusampmeals'})
j2_categories = j2_menu_soup.find_all('div', attrs={'class':'menusampcats'})
j2_food = j2_menu_soup.find_all('div', attrs={'class':'menusamprecipes'})
print('Meals:')
for m in j2_meals:
    print(m.text.strip())
print('Categories:')
for c in j2_categories:
    print(c.text.strip())
print('Food:')
for f in j2_food:
    print(f.text.strip())
'''