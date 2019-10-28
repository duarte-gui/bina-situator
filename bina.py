#!/usr/bin/python

#importando libs
import os
from time import sleep

from asterisk.ami import AMIClient
from asterisk.ami import EventListener

import requests


#Executando o cURL com as variáveis binadas
def event_notification(source, event):
        binado = ( event['ConnectedLineNum'] )
        os.system('curl -# -3 -X -k -XPOST -H "cookie: Seventh.Auth=CHAVE_DO_USER_SITUATOR" --header "Content-type: application/json" -d "{accountCode: "s%", zoneCode: 001, eventCode: "s%",  priority: 3,  join: false }" http://10.254.254.72:8080/api/remote-events' % binado)
        print ("%s" "%s" % binado)

#Login no AMI (Asterisk Manager) e escutando os "novos" eventos "Ringing", a fila "Exten" e um membro dentro da fila
#Por enquanto está desse jeito já que a fila gera n eventos que são os membros da fila + a discagem pra esses membros
client = AMIClient(address="127.0.0.1")
future = client.login(username="user", secret="password")
client.add_event_listener(
        EventListener(
                on_event=event_notification,
                white_list='Newstate',
                ChannelStateDesc='Ringing',
                Exten='100',
                CallerIDName='Supervisao Atendimento',
        )
)


if future.response.is_error():
     raise Exception(str(future.response))


try:
     while True:
         time.sleep(10)
except (KeyboardInterrupt, SystemExit):
     client.logoff()
