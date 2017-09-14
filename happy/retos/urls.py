from django.conf.urls import url
from.views import * 

urlpatterns = [
        #aprendices
		url(r'^agregar_aprendiz/$', registrar_aprendices, name='registrar_aprendices'),#ya
		url(r'^buscar/$', buscar_ap, name='buscar'),#ya
		url(r'^$', aprendices, name='aprendices'),#vista principal
		url(r'^editar_aprendiz/(?P<pk>[0-9]+)/edit/$', editar, name='post_edit'),#ya
		url(r'^ranking$', ranking, name='ranking'),#ya

		#login
		url(r'^login/$', login_view, name='vista_login'),
		url(r'^logout/$', logout_view, name='vista_logout'),

        #categorias
	   	url(r'^agregar_categoria/$',agregar_categoria, name='agregar_categoria'),#ya
	   	url(r'^lista_categoria/$', lista_categoria, name='lista_categorias'),#ya
	   	url(r'^editar_categoria/(?P<pk>[0-9]+)/$', editar_categoria, name='editar'),#ya

        #reto
		url(r'^crear_reto/$',crear_reto, name='crear_reto'),#ya
		url(r'^listar_reto/$', ver_retos, name='lista_reto'),#ya
		url(r'^editar_reto/(?P<pk>[0-9]+)/$', editar_reto, name='editar_retos'),#ya
		url(r'^detalle_reto/(?P<pk>[0-9]+)/$', detalle_reto, name='ver_detalle_reto'),
		
		

]