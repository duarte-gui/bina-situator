#!/usr/bin/python

#importando libs

from time import sleep

from asterisk.ami import AMIClient
from asterisk.ami import EventListener

import requests
#import os



def event_notification(source, event):
    binado = ( event['ConnectedLineNum'] )
    url = ('http://10.254.254.72:8080/api/remote-events')
    headers = {
        'cookie': 'Seventh.Auth=eyJuIjoidGVzdGUiLCJhIjpudWxsfQ.B917GlYR9YIoqEnL4f5plilk',
        'Content-type': 'application/json',
    }
    binadoxx = (binado[0:2])
    data = ('{accountCode: "%s", zoneCode: 001, eventCode: "%s",  priority: 3,  join: false}' % (binadoxx, binado))
    response = requests.post('http://10.254.254.72:8080/api/remote-events', headers=headers, data=data, verify=False)
    print (data)

#Login no AMI (Asterisk Manager) e escutando os "novos" eventos "Ringing", a fila "Exten" e um membro dentro da fila
#Por enquanto restringi ao Exten='100' e CallerIDName pra enviar apenas 1 evento, ja que a fila gera n eventos que sao os membros da fila + a discagem pra esses membros

client = AMIClient(address="127.0.0.1")
future = client.login(username="cxpanel", secret="cxmanager*con")
client.add_event_listener(EventListener(on_event=event_notification, white_list='Newstate', ChannelStateDesc='Ringing', Exten='100', CallerIDName='Supervisao Atendimento'))
#client.add_event_listener(EventListener(on_event=event_notification, white_list='Newstate', ChannelStateDesc='Ringing'))



if future.response.is_error():
     raise Exception(str(future.response))


try:
     while True:
         sleep(10)
except (KeyboardInterrupt, SystemExit):
     client.logoff()
