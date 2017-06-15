from django.conf.urls import url
from . import views

app_name = 'ticket'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^vista/(?P<tag>\w+)/$', views.vista, name='vista'),
    url(r'^create_ticket/$', views.create_ticket, name='create_ticket'),
    url(r'^(?P<ticket_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<ticket_id>[0-9]+)/accion/(?P<accion>\w+)/$', views.accion, name='accion'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/visar_text', views.visar_text, name='visar_data_text'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/no_visar_text', views.no_visar_text, name='no_visar_data_text'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/visar_file', views.visar_file, name='visar_data_file'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/no_visar_file', views.no_visar_file, name='no_visar_data_file'),
    url(r'^(?P<ticket_id>[0-9]+)/create_text_data/$', views.create_text_data, name='create_text_data'),
    url(r'^(?P<ticket_id>[0-9]+)/create_file_data/$', views.create_file_data, name='create_file_data'),

]
