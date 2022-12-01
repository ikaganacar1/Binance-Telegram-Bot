from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from binance import Client
from telegram.ext import Updater, CommandHandler, MessageHandler,    Filters, InlineQueryHandler
import talib
from binance import Client
import csv
import os
from numpy import genfromtxt
import time

api_key = '#'
api_secret = '#' 

client = Client(api_key,api_secret)


#update.message.reply_text("İKA BOT'a hoşgeldin.\n\nXXXUSDT  yazdığınız coinin USDT indikatör verilerini gösterir.\n(Şu anlık 3 ten çok basamaklı coinlerde düzgün çalışmıyor.)")

def start(update: Update, context: CallbackContext):
    açık = True
    düğme = True
    while açık:

        if düğme:
            update.message.reply_text("%s için EMA21/55 Crossover Alarm Kuruldu"% update.message.text)
            düğme = False

        liste_close = []

        for kline in client.get_historical_klines_generator("%s" % update.message.text, Client.KLINE_INTERVAL_4HOUR, "150 days ago UTC"):

            liste_close.append(kline[4])

        with open('fiyat_liste_close2.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(liste_close)
    
        my_data_close = genfromtxt("fiyat_liste_close2.csv",delimiter = ",")
        close = my_data_close
   
        ema21 = talib.EMA(close, timeperiod=21)
        ema55 = talib.EMA(close, timeperiod=55)

        ema21_A= round(float(ema21[899]),3)
        ema55_A= round(float(ema55[899]),3)
        ema21_B= round(float(ema21[898]),3)
        ema55_B= round(float(ema55[898]),3)

        
        if ema21_A > ema55_A:
            green_A = True
            red_A = False
            cross_A = False

        if ema21_A < ema55_A:
            green_A = False
            red_A = True
            cross_A = False

        if ema21_A == ema55_A:
            green_A = False
            red_A = False
            cross_A = True
        
        if ema21_B > ema55_B:
            green_B = True
            red_B = False
            

        if ema21_B < ema55_B:
            green_B = False
            red_B = True
            

        if ema21_B == ema55_B:
            green_B = False
            red_B = False
        
        if green_A and red_A != green_B and red_B:
            update.message.reply_text("@%s"% update.message.from_user.username)
            update.message.reply_text("%s Ema21 / Ema55 Crossover Alert: "% update.message.text, + str(close[899]))
        
        if cross_A:
            update.message.reply_text("@%s"% update.message.from_user.username)
            update.message.reply_text("%s Ema21 / Ema55 Crossover !!!Alert: "% update.message.text, + str(close[899]))
        
        #if green_A:

            #update.message.reply_text("%s Yükseliş Eğiliminde: "% update.message.text + str(close[899]))

        #if red_A:
           # update.message.reply_text("%s Düşüş Eğiliminde: "% update.message.text, + str(close[899]))


        file_close = 'fiyat_liste_close2.csv'
        if(os.path.exists(file_close) and os.path.isfile(file_close)):
            os.remove(file_close)
       
        

        time.sleep(5)
        #print(str(update.message.from_user.username)+ " %s"% update.message.text)





updater = Updater("5196461583:AAG5cdvclDLaqflailR01IM2N8TNb7Dx7bU", use_context=True)

updater.dispatcher.add_handler(MessageHandler(Filters.text, start))


updater.start_polling()
updater.idle()

    
    






  
