# grupoRJF_inf225
Proyecto de sistema de tickets
 
Basado en DJANGO, paja ejecutar server:

	1.- Tener instalado python 3
	2.- Instalar Django ("pip3 install django" con "3" opcional, ver página de django)
	3.- Ir a carpeta "ticketing_system", directorio en donde se encuentra "manage.py"
	4.- En shell escribir : "python manage.py runserver" o "python3 manage.py runserver"
	
La pagina se ejecuta en localhost:8000.
Para ingresar como administrador, entra en localhost:8000/admin/ :
- **User** : admin-felix
- **Pass** : asdf1234

Los modelos se encuentran en dos diferentes zip, estos son los proyectos de modelio.

Requerimientos no fucionales implementados:

Seguriada:
	1.- Después de 30 minutos de inactividad la sesión se termina
	2.- Al cerrar el navegador la sesión de termina
