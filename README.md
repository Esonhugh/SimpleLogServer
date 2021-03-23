# SimpleLogServer
> Used Telegram bot and local document as  a receive platform.

## Usage

* git clone it

* ``` pip install flask python-telegram-bot```

* follow the comments in the head of the logServer.py  

* ```export FLASK_APP=logServer.py && flask run --host=0.0.0.0 --port=80 --with-threads```
or
you can simply use ```python logServer.py```

## Aims or Targets

it can do as request getter and logger that catchs almost any request to your server

and you can easy use as xss cookie getter / xxe infomation getter by editing the config in python script. 

i am just simply provide one common payload in both kind of attack.

Also, you can use it as the " secure tool [ as sqlmap sqlninja msf vulnmap nmap scripting ] " analyzing tools to capture the POC/EXP payloads / testing requests created in secure tools inner, especially if you not know how to get it source code or how to read source code in language you don't familiar.

## Happy To Use and Happy To Hacking

if you like it, let me know.
