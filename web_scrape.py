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
LOCATION_HOURS = {
    LOCATION.Jester_City_Limits.name: ['Monday-Thursday | 7am-11pm', 'Friday | 7am-9pm', 'Saturday | 9am-8pm', 'Sunday | 9am-11pm'],
    LOCATION.Jester_City_Market.name: ['Monday-Thursday | 7am-Midnight', 'Friday | 7am-9pm', 'Saturday | 2pm-8pm', 'Sunday | 2pm-Midnight'],
    LOCATION.Jest_A_Pizza.name: ['Monday-Thursday | 11am-Midnight', 'Friday | 11am-2pm', 'Saturday | Closed', 'Sunday | 5pm-Midnight'],
    LOCATION.J2.name: ['Monday-Friday | 10:30am-8pm', 'Saturday-Sunday | Closed'],
    LOCATION.J2_FAST.name: ['Monday-Friday | 10:30am-8pm', 'Saturday-Sunday | Closed'],
    LOCATION.Kinsolving.name: ['Monday-Friday | 10:30am-8pm', 'Saturday (and non-class days) | 11am-2pm, 4:30pm-7pm', 'Sunday | 11am-2pm'],
    LOCATION.Kins_Market.name: ['Monday-Thursday | 7am-11pm', 'Friday | 7am-3pm', 'Saturday | 3pm-7pm', 'Sunday | 4pm-11pm'],
    LOCATION.Cypress_Bend_Cafe.name: ['Monday-Thursday | 7am-9pm', 'Friday | 7am-2pm', 'Saturday-Sunday | 12pm-7pm'],
    LOCATION.Littlefield_Patio_Cafe.name: ['Monday-Thursday | 7am-8pm', 'Friday | 7am-4pm', 'Saturday | Closed', 'Sunday | 2pm-8pm']
}


# Global variables
dining_location_urls = []   #Holds the urls for each dining location

def set_up():
    http = urllib3.PoolManager()
    page = http.request('GET', BASE_URL + LOCATIONS_URL)
    page = BeautifulSoup(page.data.decode('utf-8'), 'lxml')
    links = page.find_all('td', attrs={'width':'600px'})
    links = links[0].find_all('a')
    for l in links:
        dining_location_urls.append(l['href'])

def introduction():
    '''
    Prints out introduction statements
    '''
    print('Thank you for using UT Find Dining, the #1 tool to help you find that fine dining at UT Austin.')
    print('This script was written by Nathan Chin for his final project in EE119, Introduction to Python (Spring 2018)')
    print('Anyways, let\'s start finding so you can start dining!')

def menus():
    select = menu_options()
    print(select)

def hours():
    select = hour_options()
    print(select)
    '''
    for j,k in LOCATION_HOURS.items():
        print(j, 'hours:')
        for d in k:
            print(d)
    '''
def dining_locations():
    while(True):
        print('\n-DINING LOCATIONS')
        print('Press \'q\' to return to the main menu')
        print('What information would you like to see?')
        print('0: Menus')
        print('1: Hours')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                break
            select = int(select)
            if select == 0:
                menus()
            elif select == 1:
                hours()
            else:
                raise Exception
        except Exception:
            print('Invalid input. Please select one of the options above')
            input('\nPress enter to continue')
            
    print('\nPress enter to return to the main menu')

def help_choose():
    print('\n-HELP ME CHOOSE-')
    print('\nPress enter to return to the main menu')

def search():
    print('\n-SEARCH-')
    print('\nPress enter to return to the main menu')

def about():
    '''
    Window that allows users to know who made this awesome script
    '''
    print('\n-ABOUT-')
    print('Press enter to return to the main menu')
    print('ABOUT THE PROGRAMMER')
    print('This was created by Nathan Chin in the spring of 2018. At this time, Nathan was a sophomore student at The University of Texas at Austin studying electrical and computer engineering. He took a new class this semester called \'Introduction to Python\' to learn a new programming language and become a more balanced engineer through his skillset.')
    print('\nABOUT THE PROGRAM')
    print('One of the biggest problems with this generation is that they can\'t decide on anything. This is especially true when it comes to choosing where to eat. Well, for all those youngin\'s at The University of Texas at Austin, here\'s a solution for you (if you live on campus that is). This script gives you all of the information related to the dining halls given on the official UT website. By scraping the data online, I made it easy to find the information you need to make your decision. The only thing this program CAN\'T do is eat the food for you. Here\'s to indecisiveness!')
    input('\nPress enter to return to the main menu')

def help():
    '''
    Window that allows users to select FAQ questions and view their answers
    '''
    info = open('help.txt')
    info_str = info.read()
    info_str = info_str.split('\n')
    count = 0
    while(True):
        print('\n-HELP-')
        print('Press \'q\' to return to the main menu')
        print('What would you like help with?')
        for i in info_str:
            if count % 2 == 0:
                print('%d:' % (count // 2), i[2:])
            count += 1
        print('%d:' % (count // 2), 'PRINT ALL FAQ')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                break
            elif select.isalnum():
                select = int(select)
                if select < 0 or select > (count // 2):
                    raise Exception
                elif select == count // 2:
                    count = 0
                    for i in info_str:
                        if count % 2 == 0:
                            print('Q:', i[2:])
                        else:
                            print('A:', i[2:])
                        count += 1
                    input('\nPress enter to continue')
                else:
                    print('Q:', info_str[select * 2][2:])
                    print('A:', info_str[select * 2 + 1][2:])
                    input('\nPress enter to continue')
            else:
                raise Exception
        except Exception:
            print('Invalid input. Please select one of the options above')
            input('\nPress enter to continue')
        count = 0
    info.close()
        
def done():
    '''
    Prints out exit statements
    '''
    print('\n-QUIT-')
    print('Thanks for using UT Find Dining! Hope you enjoy your meal!')
    exit()

def main_menu_options():
    '''
    Prints out the main menu options and returns the user's choice

    Returns:
        int: The main menu option chosen
    '''
    while(True):
        print('\n-MAIN MENU-')
        print('What would you like to do?')
        print('0: Dining locations')
        print('1: Help me choose')
        print('2: Search')
        print('3: About')
        print('4: Help')
        print('q: Quit')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                return 5
            select = int(select)
            if select < 0 or select > 4:
                raise Exception
            return select
        except Exception:
            print('Invalid input. Please select one of the options above')
            input('\nPress enter to continue')

def menu_options():
    while(True):
        print('\n-MENUS-')
        print('Press \'q\' to return to the Dining Locations menu')
        print('Which location\'s menu would you like to see?')
        print('0: Jester City Limits (JCL)')
        print('1: Jester City Market (JCM)')
        print('2: Jest A\' Pizza')
        print('3: Jester 2nd Floor Dining (J2)')
        print('4: J2 FAST Line')
        print('5: Kinsolving Dining Hall (Kins)')
        print('6: Kin\'s Market')
        print('7: Cypress Bend Cafe')
        print('8: Littlefield Patio Cafe')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                break
            select = int(select)
            if select < 0 or select > 8:
                raise Exception
            return select
        except Exception:
            print('Invalid input. Please select one of the options above')
            input('\nPress enter to continue')

def day_options():
    while(True):
        print('\n-DAYS-')
        print('Press \'q\' to return to the main menu')
        print('Which days\'s menu would you like to see? Today\'s menu is the first on the list')
        count = 0

        print('0: Jester City Limits (JCL)')
        print('1: Jester City Market (JCM)')
        print('2: Jest A\' Pizza')
        print('3: Jester 2nd Floor Dining (J2)')
        print('4: J2 FAST Line')
        print('5: Kinsolving Dining Hall (Kins)')
        print('6: Kin\'s Market')
        print('7: Cypress Bend Cafe')
        print('8: Littlefield Patio Cafe')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                break
            select = int(select)
            if select < 0 or select > 8:
                raise Exception
            return select
        except Exception:
            print('Invalid input. Please select one of the options above')
            input('\nPress enter to continue')

def hour_options():
    while(True):
        print('\n-HOURS-')
        print('Press \'q\' to return to the Dining Locations menu')
        print('Which location\'s hours would you like to see?')
        print('0: Jester City Limits (JCL)')
        print('1: Jester City Market (JCM)')
        print('2: Jest A\' Pizza')
        print('3: Jester 2nd Floor Dining (J2)')
        print('4: J2 FAST Line')
        print('5: Kinsolving Dining Hall (Kins)')
        print('6: Kin\'s Market')
        print('7: Cypress Bend Cafe')
        print('8: Littlefield Patio Cafe')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                break
            select = int(select)
            if select < 0 or select > 8:
                raise Exception
            return select
        except Exception:
            print('Invalid input. Please select one of the options above')
            input('\nPress enter to continue')

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


def main():
    set_up()
    introduction()
    while(True):
        option = main_menu_options()
        if option == 0:     # Dining locations
            dining_locations()
        if option == 1:     # Help me choose
            help_choose()
        if option == 2:     # Search
            search()
        if option == 3:     # About
            about()
        if option == 4:     # Help
            help()
        if option == 5:     # Quit
            done()

    collect = [LOCATION.Jester_City_Limits, LOCATION.Jester_City_Market, LOCATION.Jest_A_Pizza, LOCATION.J2, LOCATION.J2_FAST] #LOCATION.Kinsolving, LOCATION.Kins_Market, LOCATION.Cypress_Bend_Cafe, LOCATION.Georges_Cafe]
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

if __name__ == '__main__':
    main()