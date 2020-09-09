import logging
from telegram.ext import Updater, CommandHandler, MessageHandler,InlineQueryHandler, Filters,CallbackContext
from telegram import Update, Bot
import telegram
import os
import re
import randfacts
from bs4 import BeautifulSoup
from urllib.request import urlopen
import random
import json
import time
import requests

PORT = int(os.environ.get('PORT', 5000))
count = 0


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1365638480:AAFfiMlS_dnXKLipzJ4lbMfe3ozDpzJRBK0'
chatid = 0
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def joke(bot,update):
    req = requests.get("https://official-joke-api.appspot.com/random_joke").json()
        
    update.message.reply_text("Q. "+req["setup"]+"\n"+"-> "+req["punchline"])


##def keepalive():
##    robot = telegram.Bot(TOKEN)
##    while True:
##        robot.sendMessage(-403832831,"Hi")
##        time.sleep(5)

def start(bot,update):#(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(bot,update):#(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def what_do_you_think(bot,update):
    contents = requests.get('https://yesno.wtf/api').json()
    url = contents["image"]
    print(url)
    chat_id = update.message.chat_id
    bot.send_animation(chat_id=chat_id, animation=url)

def data(bot, update):
    chat_id = update.message.chat.id
    print(chat_id)
    bot.send_document(chat_id=chat_id, document=open("database.txt","rb"))

def facts(bot,update):
    fact = randfacts.getFact()
    update.message.reply_text(fact)

def echo(bot,update):#, context):
    """Echo the user message."""
    global count
    chatid = update.message.chat.id
    msg = update.message.text
    print(chatid)
    cond = "@tag_ji_ka_bot"
    if chatid > 0:
        cond = ""
    if cond in msg:
        msg = msg.replace(cond,"")
        if "/train" in msg:
            if " : " in msg:
                msg = msg.replace("/train ","")
                file = open(r"database.txt","a")
                file.write(msg+"\n")
                file.close()
                update.message.reply_text("Trained")
            else:
                update.message.reply_text("Invalid command")

        elif "/clear" in msg:
            msg = msg.replace("/clear ","")
            file =  open("database.txt")
            data = file.read()
            newcont = data.replace(msg+"\n","")
            file.close()
            with open("database.txt","w") as file:
                file.write(newcont)
                file.close()
            update.message.reply_text("Command deleted")

##        elif "/facts" in msg:
##            fact = randfacts.getFact()
##            update.message.reply_text(fact)

        elif "/news" in msg:
            news_url = "https://news.google.com/topstories?"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = BeautifulSoup(xml_page, "html.parser")
            news_list = soup_page.findAll("item")
            #print("Here are top 3 news")
            news = news_list[random.randint(0,len(news_list)-1)]
            news = news.title.text
            update.message.reply_text(news)

        
            
                
        else:
            with open("database.txt") as file:
                for line in file:
                    que = line.split(" :")[0]
                    msg = msg.lower()
                    msg = msg.strip()
                    if (msg in que) or (que in msg):
                        reply = re.search(': (.+)',line).group(1)
                        update.message.reply_text(reply)
                        if count > 0:
                            count = 1
                        break
                else:
                    if count < 1:
                        update.message.reply_text("I don't understand, help me reply better.")
                        update.message.reply_text("Type '/train message : reply' to train me")
                        update.message.reply_text("Here 'message' is what user will message and 'reply' is what I am supposed to reply.")
                        update.message.reply_text("Make sure there is proper spacing before and after ':'")
                        
                    if count == 1:
                        update.message.reply_text("Consider training me")

                    if count == 2:
                        update.message.reply_text("You are not intrested in training me, right?")

                    if count == 3:
                        update.message.reply_text("-_-")
                    if count >= 4:
                        st = "-"*(count-2)+"_"*(count-2)+"-"*(count-2)
                        
                        update.message.reply_text(st)
                    count += 1

##def error(bot,update):#(update, context):
##    """Log Errors caused by Updates."""
##    pass
    #logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN)#, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("data", data))
    dp.add_handler(CommandHandler("facts", facts))
    dp.add_handler(CommandHandler("what_do_you_think", what_do_you_think))
    dp.add_handler(CommandHandler("joke", joke))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    #dp.add_error_handler(error)
##    updater.start_polling()
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://meratgkabot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    #keepalive()
    try:
        open("database.txt")

    except:
        file = open("database.txt","w")
        file.write("""hi : Hello there
how are you : I am fine Thank you
how do you do : I am fine Thank you
awesome : Glad you liked it
thank you : You're welcome
your name : My name is AnkitBot
wow : Thank you :-)
your creator : My creator is Ankit Raj Mahapatra
hello : Hi there.
birthday : I don't know, maybe 31st June.
favourite season : Winter
favourite person : You :-)
your phone number : 101100100001101011000011010110001100100101011011001000011011010101010010101010101
wonderful : Glag you liked it.
do you like me : Why wouldn't I?
/start : Hello there!
""")
        file.close()
    main()
















































##import time
##import re
##import requests
##import threading
##
##train = False
##oldid = 0
##olduserid = 0
##nolduserid = 0
##lst = []
##x = -1
##
##api = "1365638480:AAFfiMlS_dnXKLipzJ4lbMfe3ozDpzJRBK0"
##
##try:
##    open("database.txt")
##
##except:
##    file = open("database.txt","w")
##    file.write("""hi : Hello there
##how are you : I am fine Thank you
##how do you do : I am fine Thank you
##awesome : Glad you liked it
##thank you : You're welcome
##your name : My name is AnkitBot
##wow : Thank you :-)
##your creator : My creator is Ankit Raj Mahapatra
##hello : Hi there.
##birthday : I don't know, maybe 31st June.
##favourite season : Winter
##favourite person : You :-)
##your phone number : 101100100001101011000011010110001100100101011011001000011011010101010010101010101
##wonderful : Glag you liked it.
##do you like me : Why wouldn't I?
##/start : Hello there!
##""")
##    file.close()
##    
##
##def send(chatid,msg):
##    global api
##    par = {"chat_id" : chatid,"text":msg}
##    requests.post("https://api.telegram.org/bot%s/sendMessage"%api,data=par)
##    
##def get_data():
##    global api
##    res = requests.get('https://api.telegram.org/bot%s/getUpdates?offset=-1'%api)#, proxies=proxies)
##    data = res.json()
##    lst = data["result"]
####    lenth = len(lst)
##    tup = lst[0]
##    return tup
##
##
##count = 0
####def main():
####    global train, oldid, olduserid, nolduserid, lst, count
##while True:
##    try:
##        x = x+1
##        #print(x)
##        info = get_data()
##        msgid = info['message']['message_id']
##        uid = info['message']['chat']['id']
##        msgtype = info['message']['chat']["type"]
##        msg = info['message']['text']
##        expected = "@tag_ji_ka_bot"
####        if x %25 == 0:
####            send(561489747,"I am awake")
####            print("Hmm")
##        if msgtype == "private":
##            uname = info['message']['chat']['username']
##            name = info['message']['chat']['first_name']
##            expected = ""
##        #print("Here")
##        #lst.append(uid)
##        if expected in msg:
##            msg = msg.replace(expected,"")
##            msg = msg.strip()
##            if oldid != msgid:
##                oldid = msgid
##                #lst.remove(uid)
##                msg = msg.lower()
##                if "/train" in msg:
##                    if " : " in msg:
##                        msg = msg.replace("/train ","")
##                        file = open(r"database.txt","a")
##                        file.write(msg+"\n")
##                        file.close()
##                        send(uid,"Trained")
##                    else:
##                        send(uid,"Invalid command")
##
##                elif "/clear" in msg:
##                    msg = msg.replace("/clear ","")
##                    file =  open("database.txt")
##                    data = file.read()
##                    newcont = data.replace(msg+"\n","")
##                    file.close()
##                    with open("database.txt","w") as file:
##                        file.write(newcont)
##                        file.close()
##                    send(uid,"Command deleted")
##                    
##                        
##                else:
##                    with open("database.txt") as file:
##                        for line in file:
##                            que = line.split(" :")[0]
##                            if (msg in que) :#or (que in msg):
##                                reply = re.search(': (.+)',line).group(1)
##                                send(uid,reply)
##                                if count > 0:
##                                    count = 1
##                                break
##                        else:
##                            if count < 1:
##                                send(uid,"I don't understand, help me reply better.")
##                                send(uid,"Type '/train message : reply' to train me")
##                                send(uid,"Here 'message' is what user will message and 'reply' is what I am supposed to reply.")
##                                send(uid,"Make sure there is proper spacing before and after ':'")
##                                
##                            if count == 1:
##                                send(uid,"Consider training me")
##
##                            if count == 2:
##                                send(uid,"You are not intrested in training me, right?")
##
##                            if count == 3:
##                                send(uid,"-_-")
##                            if count >= 4:
##                                st = "-"*(count-2)+"_"*(count-2)+"-"*(count-2)
##                                
##                                send(uid,st)
##                            count += 1
##    except Exception as e:
##        pass
##    #print(threading.active_count())
##    
##
####while True:
####    main()
####    time.sleep(0.3)
####    ninfo = get_data()
####    nuid = ninfo['message']['chat']['id']
####    nuname = ninfo['message']['chat']['username']
####    
####    if nolduserid != nuid:
####        threading.Thread(target=main).start()
####        nolduserid = nuid
####        print("Talking to %s"%nuname)
##
##    
