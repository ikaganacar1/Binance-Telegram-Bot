
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

api_key = '#'
api_secret = '#' 

client = Client(api_key,api_secret)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("İKA BOT'a hoşgeldin.\n\nXXXUSDT  yazdığınız coinin USDT indikatör verilerini gösterir.\n(Şu anlık virgülden sonra 3'ten çok basamaklı coinlerde düzgün çalışmıyor.)")
  




def unknown(update: Update, context: CallbackContext):
    liste_close = []
    liste_open = []
    liste_high = []
    liste_low = []

    for kline in client.get_historical_klines_generator("%s" % update.message.text, Client.KLINE_INTERVAL_4HOUR, "150 days ago UTC"):

        liste_close.append(kline[4])
        liste_low.append(kline[3])
        liste_high.append(kline[2])
        liste_open.append(kline[1])
        


    with open('fiyat_liste_close.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(liste_close)
    
    with open('fiyat_liste_high.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(liste_high)

    with open('fiyat_liste_low.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(liste_low)
    
    with open('fiyat_liste_open.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(liste_open)


    my_data_close = genfromtxt("fiyat_liste_close.csv",delimiter = ",")
    close = my_data_close

    my_data_high = genfromtxt("fiyat_liste_high.csv",delimiter = ",")
    high = my_data_high
    
    my_data_low = genfromtxt("fiyat_liste_low.csv",delimiter = ",")
    low = my_data_low

    my_data_open = genfromtxt("fiyat_liste_open.csv",delimiter = ",")
    open0 = my_data_open




    rsi0 = talib.RSI(close, timeperiod=14)
    ema50 = talib.EMA(close, timeperiod=50)
    ema200 = talib.EMA(close, timeperiod=200)
    upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    ma50 = talib.MA(close, timeperiod=50, matype=0)
    ma200 = talib.MA(close, timeperiod=200, matype=0)
    aroondown, aroonup = talib.AROON(high, low, timeperiod=14)
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    mom = talib.MOM(close, timeperiod=10)
    atr = talib.ATR(high, low, close, timeperiod=14)
    doji = talib.CDLDOJI(open0, high, low, close)
    dragonflydoji = talib.CDLDRAGONFLYDOJI(open0, high, low, close)
    eveningdojistar = talib.CDLEVENINGDOJISTAR(open0, high, low, close, penetration=0)
    
    
    ema21 = talib.EMA(close, timeperiod=21)
    ema55 = talib.EMA(close, timeperiod=55)



    rsi_A= round(float(rsi0[899]),3)
    ema50_A= round(float(ema50[899]),3)
    ema200_A= round(float(ema200[899]),3)
    upperband_A= round(float(upperband[899]),3)
    middleband_A= round(float(middleband[899]),3)
    lowerband_A= round(float(lowerband[899]),3)
    ma50_A= round(float(ma50[899]),3)
    ma200_A= round(float(ma200[899]),3)
    aroondown_A= round(float(aroondown[899]),3)
    aroonup_A= round(float(aroonup[899]),3)
    macd_A= round(float(macd[899]),6)
    macdsignal_A= round(float(macdsignal[899]),6)
    macdhist_A= round(macdhist[899],6)
    mom_A= round(float(mom[899]),3)
    atr_A= round(float(atr[899]),3)

    ema21_A= round(float(ema21[899]),3)
    ema55_A= round(float(ema55[899]),3)
    ema21_B= round(float(ema21[898]),3)
    ema55_B= round(float(ema55[898]),3)

    file_close = 'fiyat_liste_close.csv'
    if(os.path.exists(file_close) and os.path.isfile(file_close)):
        os.remove(file_close)
        #print("\nclose file deleted")

    file_high = 'fiyat_liste_high.csv'
    if(os.path.exists(file_high) and os.path.isfile(file_high)):
        os.remove(file_high)
        #print("\nhigh file deleted")

    file_low = 'fiyat_liste_low.csv'
    if(os.path.exists(file_low) and os.path.isfile(file_low)):
        os.remove(file_low)
        #print("\nlow file deleted")

    file_open = 'fiyat_liste_open.csv'
    if(os.path.exists(file_open) and os.path.isfile(file_open)):
        os.remove(file_open)
        #print("\nopen file deleted")

    upperband_AÜ = upperband_A+(upperband_A/100)*0.5
    

    upperband_AA = upperband_A-(upperband_A/100)*0.5
   

    lowerband_AÜ = lowerband_A+(lowerband_A/100)*0.5
    

    lowerband_AA = lowerband_A-(lowerband_A/100)*0.5
    


    if rsi_A >= 0 and rsi_A <= 15:
        rsiS = 7   
        rsiY = "StrongBuy"

    if rsi_A >15 and rsi_A <= 30:
        rsiS = 6 
        rsiY = "Buy"

    if rsi_A >30 and rsi_A <= 40:
        rsiS = 5  
        rsiY = "WeakBuy"

    if rsi_A >40 and rsi_A <= 50:
        rsiS = 4 
        rsiY = "Notr"
    
    if rsi_A >50 and rsi_A <= 60:
        rsiS = 3 
        rsiY = "WeakSell"

    if rsi_A >60 and rsi_A <= 80:
        rsiS = 2 
        rsiY = "Sell"

    if rsi_A >80 and rsi_A <= 100:
        rsiS = 1  
        rsiY = "StrongSell"

    

    if close[899] > upperband_AÜ:
        BBS = 1
        BBY = "StrongSell"
    
    if close[899] <= upperband_AÜ and close[899] >= upperband_AA:
        BBS = 2
        BBY = "Sell"

    if close[899] <= upperband_AA and close[899] >= lowerband_AÜ:
        BBS = 4
        BBY = "Notr"
    
    if close[899] < lowerband_AÜ and close[899] > lowerband_AA:
        BBS = 6
        BBY = "Buy"
    
    if close[899] < lowerband_AA:
        BBS = 7
        BBY = "StrongBuy"

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
        if green_A:
            crossoverS = 7
            crossoverY = "StrongBuy"
        if red_A:
            crossoverS = 1
            crossoverY = "StrongSell"

    if green_A:
        trend = "green"
    if red_A:
        trend= "red"
    
        
    

    
    update.message.reply_text("(4h)%s:"% update.message.text+str(close[899])+"\n"+"\n•EMA50: "+str(ema50_A)+"\n•EMA200: "+str(ema200_A)+"\n\n"+"•MA50: "+ str(ma50_A)+"\n•MA200: "+ str(ma200_A)+"\n\n"+"•RSI: "+ str(rsi_A) +"\n\n"+"•BOLINGER BANDS:\n" + "  üst: "+str(upperband_A) + ",\n" +"  orta: "+ str(middleband_A) + ",\n" + "  alt: "+str(lowerband_A)+"\n\n•AROON:\n"+" Up: %"+str(aroonup_A)+"\n Down: %" +str(aroondown_A)+"\n\n•MACD:\n"+" Macd: "+str(macd_A)+"\n Macd Signal: " +str(macdsignal_A) +"\n Macd Hist: " +  str(macdhist_A) +"\n\n•MOM: "+str(mom_A)+"\n\n•ATR: "+str(atr_A)    )
    update.message.reply_text("(4h)%s:"% update.message.text+"\nRSI: "+rsiY+"\nBolinger Bands: "+BBY+"\nTrend: "+trend+"\n")
    
    print(str(update.message.from_user.username)+ " %s"% update.message.text)


def main():

    updater = Updater("#:#", use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    
    updater.start_polling()
    updater.idle()

    
    
if __name__ == '__main__':
    main()





  
