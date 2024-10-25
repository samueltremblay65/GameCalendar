from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from Helpers import parse_datetime, parse_time
from Game import Game
from AddGamesToCalendar import create_calendar

import time

browser = webdriver.Edge()
browser.set_window_size(1024, 600)
browser.maximize_window()

# Needed to force window to be full screen
browser.get('https://www.nhl.com/senators/schedule/2024/fullseason')

# Wait until page is loaded
browser.implicitly_wait(10)
time.sleep(5)

date_elements = browser.find_elements(By.CLASS_NAME, 'sc-fhrDCu')
time_elements = browser.find_elements(By.CLASS_NAME, 'sc-eFzpJt')
matchup_elements = browser.find_elements(By.CLASS_NAME, 'sc-kIgPtV')

if(len(date_elements) != len(time_elements) or len(time_elements) != len(matchup_elements)):
    raise Exception("Failed to retrieve correct data from NHL.com")

gametimes = []
gamedates = []

games = []

for time_element in time_elements:
    try:
        parsed_time = parse_time(time_element.text)
        gametimes.append(parsed_time)
    except ValueError:
        gametimes.append("7:00 PM")
        

for date in date_elements:
    gamedates.append(date.text)

for i in range(0, len(gamedates)):
    game = Game(parse_datetime(gamedates[i], gametimes[i]))
    
    matchup_label = matchup_elements[i].get_attribute("aria-label")

    home, away = matchup_label.split(" @ ")

    game.home = home
    game.away = away

    games.append(game)

browser.quit()

create_calendar(games)