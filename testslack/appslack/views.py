import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, request
from django.conf import settings
from slackclient import SlackClient
from .models import Menu, Agenda
from .tasks import create_enqueue_message_to_slack


VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
Client_slack = SlackClient(BOT_USER_TOKEN)


create_enqueue_message_to_slack.delay()

class Verify(APIView):

    def post(self, request, *args, **kwargs):
        message = request.data

        if message.get('token') != VERIFICATION_TOKEN:
             return Response(status=status.HTTP_403_FORBIDDEN)

        if message.get('type') == 'url_verification':
             return Response(data=message, status=status.HTTP_200_OK)


        now_date = datetime.datetime.now().date()
        menu_object = Menu.objects.filter(fecha=now_date)

        if menu_object.count() > 0:
            create_enqueue_message_to_slack.delay()

            ##########PROCESO DE ENVIO DE MENSAJE SIN ENCOLAR ######################

            # menu_message = "HOLA, EL MENU DE HOY ES EL SIGUIENTE: "+ "-opcion 1:" + \
            #                menu_object[0].opcion1 + " -opcion 2: " +menu_object[0].opcion2 \
            #                + " -opcion 3: " +menu_object[0].opcion3 + " -opcion 4: " +menu_object[0].opcion4\
            #                + " .Ingresa al siguiente link y elige tu opción: http://127.0.0.1:8000/menu/userlist"
            #
            # Client_slack.api_call(method='chat.postMessage',
            #                 channel='#general',
            #                 text=menu_message)

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class MenuList(ListView):
    model = Menu
    template_name = 'appslack/list_menu.html'

class AgendaList(ListView):
    model = Agenda
    template_name = 'appslack/list_agenda.html'


class MenuAdd(CreateView):
    model = Menu
    template_name = 'appslack/add_menu.html'
    success_url = reverse_lazy('appslack:list')
    fields = ['opcion1','opcion2','opcion3','opcion4','fecha']


class MenuEdit(UpdateView):
    model = Menu
    template_name = 'appslack/add_menu.html'
    success_url = reverse_lazy('appcshopslack:list')
    fields = ['opcion1', 'opcion2', 'opcion3', 'opcion4']


class MenuDelete(DeleteView):
    model = Menu
    success_url = reverse_lazy('appslack:list')


class UserMenu(ListView):
    model = Menu
    template_name = 'appslack/user_list_menu.html'


class UserMenuAdd(CreateView):
    hour = datetime.datetime.now()
    final_hour = hour.hour - 3
    model = Agenda
    fields = ['opcion', 'especificacion']
    if final_hour < 12:
        template_name = 'appslack/user_add_menu.html'
    else:
        template_name = 'appslack/out_time_user.html'

    success_url = reverse_lazy('appslack:userlist')

    def form_valid(self, form):
        form.instance.id_cliente_id = "1-k"
        form.instance.id_menu_id = self.kwargs['fk']
        return super(UserMenuAdd, self).form_valid(form)
