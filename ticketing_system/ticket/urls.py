from django.conf.urls import url
from . import views

app_name = 'ticket'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^mis_tickets/$', views.mis_tickets, name='mis_tickets'),
    url(r'^create_ticket/$', views.create_ticket, name='create_ticket'),
    url(r'^tickets_no_asignados/$', views.tickets_no_asignados, name='tickets_no_asignados'),
    url(r'^tickets_cerrados/$', views.tickets_cerrados, name='tickets_cerrados'),
    url(r'^tickets_eliminados/$', views.tickets_eliminados, name='tickets_eliminados'),
    url(r'^asignar_ticket/$', views.asignar_ticket, name='asignar_ticket'),
    url(r'^(?P<ticket_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<ticket_id>[0-9]+)/cerrar$', views.cerrar, name='cerrar'),
    url(r'^(?P<ticket_id>[0-9]+)/abrir$', views.abrir, name='abrir'),
    url(r'^(?P<ticket_id>[0-9]+)/eliminar', views.eliminar, name='eliminar'),
    url(r'^(?P<ticket_id>[0-9]+):/restaurar', views.restaurar, name='restaurar'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/visar', views.visar, name='visar_data'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/no_visar', views.no_visar, name='no_visar_data'),

    url(r'^(?P<ticket_id>[0-9]+)/create_text_data/$', views.create_text_data, name='create_text_data'),
    url(r'^(?P<ticket_id>[0-9]+)/create_file_data/$', views.create_file_data, name='create_file_data'),

]