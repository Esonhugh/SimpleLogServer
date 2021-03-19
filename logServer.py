# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
import telegram
import json
import os
app = Flask(__name__)

bot = telegram.Bot(token='')    # there is your telegram bot token
My_chat_id=''                   # receiver id 
msgCodeFlag = True              # send the message as code in html
accessLogPassword=""            # the password to check the log
# Get log on internet method is 
# GET /check?pass=accessLogPassword&sendTG=1
# Both send to TG and you
# GET /check?pass=accessLogPassword
# Only send to you

def sendMe(msg,codeflag=msgCodeFlag):
    if (codeflag):
        bot.send_message(chat_id=My_chat_id,text="<code>"+msg+"</code>",parse_mode=telegram.ParseMode.HTML)
    else:
        bot.send_message(chat_id=My_chat_id,text=msg)

@app.before_request
def before_request():
    logfile = open("./log","a")
    log = {}
    log["ip"] = request.remote_addr
    log['method'] = request.method
    log['headers'] = str(request.headers).rstrip().replace("\r\n","\n")
    log['url']  = request.full_path
    log['form'] = request.stream.read().decode('UTF-8')
    logger = json.dumps(log)
    logfile.write(logger+"\n")
    logfile.close()
    print(logger)
    sendMe(logger)      #<----------------------------------- Very Important if you can't use the Telegram like inside GxFxW , you need # it as comment !!! repeat it is all depends on your network ENV
    print(request.headers['User-Agent'])

@app.route('/check',methods=['GET'])
def check():
    logfile = open("./log","r")
    returnlog = []
    for line in logfile:
        returnlog.append(line)
    feedback = "".join(returnlog)
    logfile.close()

    if ( request.args.get( "pass" ) ==  accessLogPassword ):
        if( request.args.get( "sendTG" ) == "1" ):
            sendMe(feedback)
        return(feedback)
    else:
        return("Permission Deny")

@app.route('/clean',methods=['DELETE'])
def clear():
    if(request.args.get("pass") == accessLogPassword):
        os.remove("./log")
        return("clear success")
    else:
        return("Permission deny")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80) 
    # server should be run as root to listen the port
