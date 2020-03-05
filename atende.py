#!/usr/bin/python


from time import sleep

from asterisk.ami import AMIClient
from asterisk.ami import EventListener
import os


import requests



def event_notification(source, event):
    binado = ( event['ConnectedLineNum'] )
    ext = ( event['Exten'])
    os.system("curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{call: {src: '%s', dst: '%s'}}' http://10.254.254.208:8887/api/voip/events" % (binado, ext))

    print (binado, ext)



client = AMIClient(address="127.0.0.1")
future = client.login(username="cxpanel", secret="cxmanager*con")
client.add_event_listener(EventListener(on_event=event_notification, black_list='Exten = 100', white_list='Newstate', ChannelStateDesc='Up'))



if future.response.is_error():
     raise Exception(str(future.response))


try:
     while True:
         sleep(10)
except (KeyboardInterrupt, SystemExit):
     client.logoff()

