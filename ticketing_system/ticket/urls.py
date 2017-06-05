from django.conf.urls import url
from . import views

app_name = 'ticket'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^mis_tickets/$', views.mis_tickets, name='mis_tickets'),
    url(r'^create_ticket/$', views.create_ticket, name='create_ticket'),
    url(r'^(?P<ticket_id>[0-9]+)/$', views.detail, name='detail'),

    url(r'^(?P<ticket_id>[0-9]+)/create_text_data/$', views.create_text_data, name='create_text_data'),
    url(r'^(?P<ticket_id>[0-9]+)/create_file_data/$', views.create_file_data, name='create_file_data'),

]