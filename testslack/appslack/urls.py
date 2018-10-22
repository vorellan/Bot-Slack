from django.conf.urls import url

from .views import (
    MenuList,
    MenuAdd,
    MenuEdit,
    MenuDelete,
    UserMenu,
    UserMenuAdd,
    Verify,
    AgendaList


)

urlpatterns = [


    url(r'^list$', MenuList.as_view(), name='list'),
    url(r'^agenda$', AgendaList.as_view(), name='agenda'),
    url(r'^new$', MenuAdd.as_view(), name='new'),
    url(r'^edit/(?P<pk>\d+)$', MenuEdit.as_view(), name='edit'),
    url(r'^delete/(?P<pk>\d+)$', MenuDelete.as_view(), name='delete'),
    url(r'^userlist$', UserMenu.as_view(), name='userlist'),
    url(r'^usernew/(?P<fk>\d+)$', UserMenuAdd.as_view(), name='usernew'),
    url(r'^slack$', Verify.as_view(), name='slack'),



]