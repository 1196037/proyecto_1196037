from django.conf.urls import url
from.views import * 

urlpatterns = [
        #aprendices
		url(r'^agregar_aprendiz/$', registrar_aprendices, name='registrar_aprendices'),#ya
		url(r'^buscar/$', buscar_ap, name='buscar'),#ya
		url(r'^$', aprendices, name='aprendices'),#vista principal
		url(r'^editar_aprendiz/(?P<pk>[0-9]+)/edit/$', editar, name='post_edit'),#ya
		url(r'^ranking$', ranking, name='ranking'),
		url(r'^eliminar_ap/(?P<pk>[0-9]+)/$', eliminar_ap, name='eliminar_ap'),#ya
		#login
		url(r'^login/$', login_view, name='vista_login'),
		url(r'^logout/$', logout_view, name='vista_logout'),

        #categorias
	   	url(r'^agregar_categoria/$',agregar_categoria, name='agregar_categoria'),#ya
	   	url(r'^lista_categoria/$', lista_categoria, name='lista_categorias'),#ya
	   	url(r'^editar_categoria/(?P<pk>[0-9]+)/$', editar_categoria, name='editar'),#ya
	   	url(r'^eliminar_categoria/(?P<pk>[0-9]+)/$', eliminar_categoria, name='eliminar_categoria'),

        #reto
		url(r'^crear_reto/$',crear_reto, name='crear_reto'),#ya
		url(r'^listar_reto/$', ver_retos, name='lista_reto'),#ya
		url(r'^editar_reto/(?P<pk>[0-9]+)/$', editar_reto, name='editar_retos'),#ya
		url(r'^detalle_reto/(?P<pk>[0-9]+)/$', detalle_reto, name='ver_detalle_reto'),
		url(r'^eliminar_reto/(?P<pk>[0-9]+)/$', eliminar_reto, name='eliminar_reto'),
		url(r'^listar_mis_retos$',listar_mis_retos, name='listar_mis_retos'),
		url(r'^listar_reto_por_calificar/$', lista_sin_c, name='lista_reto_sin_c'),
		url(r'^lista_retos_calificado/$', lista_retos_calificados, name='lista_retos_calificados'),
		
		

]