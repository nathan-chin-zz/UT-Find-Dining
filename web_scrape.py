'''
Name: Nathan Chin
UT EID: nhc332
Class: EE 119
Professor: Chirag Sakhuja
Date started: 3/8/18
'''

import urllib3
import requests
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

class DAY(Enum):
    Yesterday = 0
    Today = 1
    Tomorrow = 2
    Two = 3
    Three = 4
    Four = 5
    Five = 6

# Constants
BASE_URL = 'http://hf-food.austin.utexas.edu/foodpro/'
LOCATIONS_URL = 'location2.asp'
LOCATIONS = list(LOCATION)
DAYS = list(DAY)
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
http = urllib3.PoolManager()
dining_location_days = []
dining_location_days_urls = []

def set_up():
    page = http.request('GET', BASE_URL + LOCATIONS_URL)
    page = BeautifulSoup(page.data.decode('utf-8'), 'lxml')
    links = page.find_all('td', attrs={'width':'600px'})
    links = links[0].find_all('a')
    for l in links:
        dining_location_urls.append(l['href'])
    for pos, j in enumerate(dining_location_urls):
        page = http.request('GET', BASE_URL + j)
        page = BeautifulSoup(page.data.decode('utf-8'), 'lxml')
        day_data = page.find('frame', attrs={'name': 'AuroraContents'})
        url = BASE_URL + day_data['src']
        page = http.request('GET', url)
        page = BeautifulSoup(page.data.decode('utf-8'), 'lxml')
        day_data = page.find_all('a', attrs={'target': 'AuroraMain'})
        dining_location_days_urls.append(list())
        dining_location_days.append(list())
        for k in day_data:
            dining_location_days[pos].append(k.text.strip())
            dining_location_days_urls[pos].append(k['href'])

def introduction():
    '''
    Prints out introduction statements
    '''
    print('Thank you for using UT Find Dining, the #1 tool to help you find that fine dining at UT Austin.')
    print('This script was written by Nathan Chin for his final project in EE119, Introduction to Python (Spring 2018)')
    print('Anyways, let\'s start finding so you can start dining!')

def scrape(collect_menus, collect_days, is_all_menus, is_all_days):
    if is_all_menus and is_all_days:
        print('Menus for all locations and all days:')
    elif is_all_menus:
        print('Menus for all locations:')
    elif is_all_days:
        print('Menus for all days:')
    else:
        print('Printing requested menus for request days:')
    for count, i in enumerate(collect_menus):
        val = i.value
        printName(collect_menus[count].name, '#')
        for i2 in collect_days:
            printName(dining_location_days[val][i2.value], '+')
            url = dining_location_days_urls[val][i2.value]
            #page = http.request('GET', BASE_URL + url)
            #page = BeautifulSoup(page.data.decode('utf-8'), 'html.parser')
            r = requests.get(BASE_URL + url)
            page = BeautifulSoup(r.text, 'lxml')
            meals = page.find('table', attrs={'cellspacing': '0'})
            food = page.find_all('table', attrs={'cellspacing': '1'})
            if meals == None:
                print(collect_menus[count].name, 'is closed on', dining_location_days[val][i2.value], ':(')
            else:
                item = meals.find_all('div')
                for i in item:
                    i = i.text.strip()
                    if i.lower() == 'breakfast' or i.lower() == 'lunch' or i.lower() == 'dinner':
                        printName(i, '-')
                    else:
                        if i.startswith('-'):
                            print()
                        if len(i) > 0:
                            print(i)
            print()

def menus():
    while(True):
        collect_menus = []
        collect_days = []
        print_all_menus = print_all_days = False
        select = menu_options()
        select.sort()
        if -1 in select:
            return
        elif '9' in select and len(select) > 1:
            print('If you\'re printing multiple locations, you don\'t need to print all locations too\n')
        elif '9' in select and len(select) == 1:
            select = [0,1,2,3,4,5,6,7,8]
            print_all_menus = True
        for j in select:
            j = int(j)
            collect_menus.append(LOCATION(j))
        select2 = day_options()
        select2.sort()
        if -1 in select2:
            return
        elif '7' in select2 and len(select2) > 1:
            print('If you\'re printing multiple days, you don\'t need to print all days too\n')
        elif '7' in select2 and len(select2) == 1:
            select2 = [0,1,2,3,4,5,6]
            print_all_days = True
        for j in select2:
            j = int(j)
            collect_days.append(DAY(j))
        scrape(collect_menus, collect_days, print_all_menus, print_all_days)    
        '''for i in select:
            i = int(i)
            if i == 9 and len(select) == 1:
                print('Menus for all locations:')
                
            elif i > -1 and i < 9:
                print('Menu for :')
                
            elif i == 9 and len(select) > 1:
                print('If you\'re printing multiple locations, you don\'t need to print all locations too\n')
                break
            print()'''
        input('Press enter to continue')

def hours():
    while(True):
        select = hour_options()
        select.sort()
        for i in select:
            i = int(i)
            if i == -1:
                return
            elif i == 9 and len(select) == 1:
                print('Hours for all locations:')
                for j,k in LOCATION_HOURS.items():
                    print('Hours for %s:' % j)
                    for l in k:
                        print(l)
                    print()
            elif i > -1 and i < 9:
                print('Hours for %s:' % LOCATION(i).name)
                for j in LOCATION_HOURS[LOCATION(i).name]:
                    print(j)
            elif i == 9 and len(select) > 1:
                print('If you\'re printing multiple locations, you don\'t need to print all locations too\n')
                break
            print()
        input('Press enter to continue')

def dining_locations():
    while(True):
        print('\n-DINING LOCATIONS-')
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
        print('Which location\'s menu(s) would you like to see? If you wish to select multiple, separate them by a comma')
        print('0: Jester City Limits (JCL)')
        print('1: Jester City Market (JCM)')
        print('2: Jest A\' Pizza')
        print('3: Jester 2nd Floor Dining (J2)')
        print('4: J2 FAST Line')
        print('5: Kinsolving Dining Hall (Kins)')
        print('6: Kin\'s Market')
        print('7: Cypress Bend Cafe')
        print('8: Littlefield Patio Cafe')
        print('9: PRINT ALL MENUS')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                return [-1]
            select = str(select)
            select = select.split(',')
            for i in select:
                if int(i) < 0 or int(i) > 9:
                    raise Exception
            return select
        except Exception:
            print('Invalid input. Please select one of the options above')
            input('\nPress enter to continue')

def day_options():
    while(True):
        print('\n-DAYS-')
        print('Press \'q\' to return to the main menu')
        print('Which days\'s menu would you like to see?')
        for pos, i in enumerate(dining_location_days[0]):
            print('%d:' % pos, i)
        print('7: PRINT ALL DAYS')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                return [-1]
            select = str(select)
            select = select.split(',')
            for i in select:
                if int(i) < 0 or int(i) > 7:
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
        print('*Only prints hours for normal class days. View menus to see if location is open at all*')
        print('0: Jester City Limits (JCL)')
        print('1: Jester City Market (JCM)')
        print('2: Jest A\' Pizza')
        print('3: Jester 2nd Floor Dining (J2)')
        print('4: J2 FAST Line')
        print('5: Kinsolving Dining Hall (Kins)')
        print('6: Kin\'s Market')
        print('7: Cypress Bend Cafe')
        print('8: Littlefield Patio Cafe')
        print('9: PRINT ALL HOURS')
        try:
            select = input('>> ')
            if select.lower() == 'q':
                return [-1]
            select = str(select)
            select = select.split(',')
            for i in select:
                if int(i) < 0 or int(i) > 9:
                    raise Exception
            return select
        except Exception:
            print('Invalid input. Please select one of the options above')
            input('\nPress enter to continue')

def printName(name, symbol):
    loop = 0
    print()
    while loop < len(name) + 4:
        print(symbol, end='')
        loop += 1
    print()
    print(symbol, name.upper(), symbol)
    loop = 0
    while loop < len(name) + 4:
        print(symbol, end='')
        loop += 1

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

if __name__ == '__main__':
    main()