# Import Packages
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Open Spelling Bee webpage, and navigate to game
driver = webdriver.Chrome()
driver.get('https://www.nytimes.com/puzzles/spelling-bee')
time.sleep(0.5)
driver.find_element(By.XPATH, '//button[@class="pz-moment__button primary default"]').click()
time.sleep(0.5)

# Get all the possible letters and there associated buttons from the HTML
allButtonElements = driver.find_elements(By.CSS_SELECTOR, 'polygon.cell-fill')
allLetterElements = driver.find_elements(By.CSS_SELECTOR, 'text.cell-letter')
enterWord = driver.find_element(By.XPATH, '//div[@class="hive-action hive-action__submit sb-touch-button"]')
possibleLetters = {}
for i in range(len(allLetterElements)):
   possibleLetters[allLetterElements[i].text] = allButtonElements[i]

# Search word lists files to find words matching criteria
files = ["eight", "seven", "six", "five", "four"]
for file in files:
    letterFile = open(file + "-letter-words.txt")
    letterList = re.sub('\\d', ' ', letterFile.read()).split()
    letterFile.close()
    
    for word in letterList:
        hasMiddleLetter = False
        hasInvalidLetter = False
        
        # Check criteria (i.e., has middle letter and only available letters)
        for letter in word.upper():
            if letter not in list(possibleLetters.keys()):
                hasInvalidLetter = True
                break
            if letter == list(possibleLetters.keys())[0]:
                hasMiddleLetter = True

        # If criteria met enter all the letters
        if (hasMiddleLetter and not hasInvalidLetter):
            for letter in word.upper():
                try:
                    possibleLetters[letter].click()
                    time.sleep(0.1)
                except:
                    time.sleep(5)
            enterWord.click()
            time.sleep(0.5)