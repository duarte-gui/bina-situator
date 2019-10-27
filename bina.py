#!/usr/bin/python
import os
import time

from asterisk.ami import AMIClient
from asterisk.ami import EventListener

import requests

def event_notification(source, event):
        binado = ( event['ConnectedLineNum'] )
        os.system('curl -# -3 -X -k -XPOST -H "cookie: Seventh.Auth=eyJuIjoidm9pcCIsImEiOm51bGx9.6tnY42e44PURICRaVFNQWnxo" --header "Content-type: application/json" -d "{accountCode: "s%", zoneCode: 001, eventCode: "s%",  priority: 3,  join: false }" http://10.254.254.72:8080/api/remote-events' % binado)
        print binado




client = AMIClient(address="127.0.0.1")
future = client.login(username="cxpanel", secret="cxmanager*con")
client.add_event_listener(EventListener(on_event=event_notification, white_list='Newstate', ChannelStateDesc='Ringing'))

if future.response.is_error():
     raise Exception(str(future.response))


try:
     while True:
         time.sleep(10)
except (KeyboardInterrupt, SystemExit):
     client.logoff()
