import datetime
from .models import Menu
from django.conf import settings
from slackclient import SlackClient

from celery import shared_task

BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
Client_slack = SlackClient(BOT_USER_TOKEN)


@shared_task
def create_enqueue_message_to_slack():

    now_date = datetime.datetime.now().date()
    menu_object = Menu.objects.filter(fecha=now_date)

    menu_message = "HOLA, EL MENU DE HOY ES EL SIGUIENTE: " + "-opcion 1:" + \
                   menu_object[0].opcion1 + " -opcion 2: " + menu_object[0].opcion2 \
                   + " -opcion 3: " + menu_object[0].opcion3 + " -opcion 4: " + menu_object[0].opcion4 \
                   + " .Ingresa al siguiente link y elige tu opción: http://127.0.0.1:8000/menu/userlist"

    Client_slack.api_call(method='chat.postMessage',
                          channel='#chilean',
                          text=menu_message)
    return 'Mensaje procesado con exito!!!'
