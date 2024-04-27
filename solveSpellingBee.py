# Import Packages
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

#Open Spelling Bee webpage
driver = webdriver.Chrome()
driver.get('https://www.nytimes.com/puzzles/spelling-bee')
time.sleep(1)
driver.find_element(By.XPATH, '//button[@class="pz-moment__button primary default"]').click()
time.sleep(1)

#Get all the possible letters and there associated buttons
allButtonElements = driver.find_elements(By.CSS_SELECTOR, 'polygon.cell-fill')
allLetterElements = driver.find_elements(By.CSS_SELECTOR, 'text.cell-letter')
enterWord = driver.find_element(By.XPATH, '//div[@class="hive-action hive-action__submit sb-touch-button"]')
possibleLetters = {}
for i in range(len(allLetterElements)):
   possibleLetters[allLetterElements[i].text] = allButtonElements[i]
print(possibleLetters)

# Search word lists to find all possible words
files = ["four", "five", "six", "seven", "eight"]
possibleWords = open('allPossibleWords.txt','w')
for file in files:
    letterFile = open(file + "-letter-words.txt")
    letterList = re.sub('\\d', ' ', letterFile.read()).split()
    letterFile.close()
    
    for word in letterList:
        hasMiddleLetter=False
        hasInvalidLetter=False

        for letter in word.upper():
            if letter not in list(possibleLetters.keys()):
                hasInvalidLetter = True
                break
            if letter == list(possibleLetters.keys())[0]:
                hasMiddleLetter=True

        if (hasMiddleLetter and not hasInvalidLetter):
            possibleWords.write(word.lower()+'\n')   
possibleWords.close()

# Enter in all the discovered words
wordFile = open('allPossibleWords.txt')
wordList = re.sub('\\d', ' ', wordFile.read()).split()
wordFile.close()
for word in wordList:
    for letter in word.upper():
        try:
            possibleLetters[letter].click()
            time.sleep(0.1)
        except:
            time.sleep(10)
    enterWord.click()
    time.sleep(0.5)

time.sleep(10)