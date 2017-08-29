from django.conf.urls import url
from . import views

app_name = 'ticket'

urlpatterns = [
    # pagina de inicio de usuario logeado
    url(r'^$', views.index, name='index'),

    # login y logout de usuario
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    # se aplican filtros a la lista de tickets
    url(r'^vista/(?P<tag>\w+)/$', views.vista, name='vista'),

    # para creacion de ticket
    url(r'^create_ticket/$', views.create_ticket, name='create_ticket'),

    # detalle de un ticket
    url(r'^(?P<ticket_id>[0-9]+)/$', views.detail, name='detail'),

    #se aplica una accion sobre un ticket (eliminar, restaurar, cerrar, abrir, vincular, ...)
    url(r'^(?P<ticket_id>[0-9]+)/accion/(?P<accion>\w+)/$', views.accion, name='accion'),

    #visado o no visado de data de texto y archivos
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/visar_text$', views.visar_text, name='visar_data_text'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/no_visar_text$', views.no_visar_text, name='no_visar_data_text'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/visar_file$', views.visar_file, name='visar_data_file'),
    url(r'^(?P<data_id>[0-9]+):(?P<ticket_id>[0-9]+)/no_visar_file$', views.no_visar_file, name='no_visar_data_file'),

    #creacion de data de texto o archivos
    url(r'^(?P<ticket_id>[0-9]+)/create_text_data/$', views.create_text_data, name='create_text_data'),
    url(r'^(?P<ticket_id>[0-9]+)/create_file_data/$', views.create_file_data, name='create_file_data'),

    #Click en notificacion
    url(r'^click_notificacion/(?P<notificacion_id>[0-9]+)/$', views.click_notificacion, name="click_notificacion"),

    # Estadisticas
    url(r'estadisticas/$', views.estadisticas, name='estadisticas'),
    url(r'^api/chart/data/$', views.ChartData.as_view())
]
