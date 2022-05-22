#pip install PyTelegramBotAPI

import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime
import os


API_KEY = 'api key'
PATH = "/usr/bin/chromedriver"
checked = False


bot = telebot.TeleBot(API_KEY)



def sendMessageInd(page, data, chat_id, resources=''):

    message = f"Update from: {page}\n\n{data}\n\nresources:\n{resources}"

    bot.send_message(chat_id, message)


def lastdata(page):
    df = pd.read_excel('lastdata.xlsx')
    if page in df['page'].to_list():
        data = df[df['page'] == page]['data'][0]
    else:
        data = ''

    return data

def updatedata(page, data):
    df = pd.read_excel('lastdata.xlsx')
    if page in df['page'].to_list():
        df['data'][df['page'] == page] = data
        df.to_excel('lastdata.xlsx', index=False)

    else:
        df.loc[len(df.index)] = [page, data]
        df.to_excel('lastdata.xlsx', index=False)



@bot.message_handler(commands=['help', 'start'])
def help(message):
    return_message = 'You can try following commands\n /aboutbot - Know about the bot\n /meaning {word} - Get meaning of the provided word\n /antonym {word} - Get antonyms of the given word\n /synonym {word} - Get synonym of the given word\n /help - get help'
    bot.send_message(message.chat.id, return_message)

@bot.message_handler(commands=['aboutbot'])
def about(message):
    return_message = 'The bot can get you meaning, synonym and antonym  of a woards'
    bot.send_message(message.chat.id, return_message)
    print(message.chat.id)


# sendMessageInd(-1001552773038)
# sendMessageInd(-1001544309751)

while 1:
    
    if datetime.datetime.now().minute % 2 == 0 and checked == False:
        checked = True
        
        if not os.path.exists('lastdata.xlsx'):
            print('file not found, creating file lastdata....')
            columnNames = ['page', 'data']
            lastdataDF = pd.DataFrame(columns = columnNames)
            lastdataDF.to_excel('lastdata.xlsx', index = False)
        
        try:
            print('trying to get cuet latest data')
            driver = webdriver.Chrome(PATH)
            page = 'cuet'
            driver.get("https://cuet.samarth.ac.in/")

            newData = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "color-inherit"))
            )

            data = newData.text

            if data != lastdata(page):
                print('new data found, updating lastdata')
                updatedata(page, data)
                print('sending data to you')
                sendMessageInd(page, data, 1309831880)
                print('data sent')
                
        finally:
            print('quiting brouser')
            driver.quit()
    else:
        checked = False
            
    bot.polling()
# newData = driver.find_element_by_class_name("color-inherit")
