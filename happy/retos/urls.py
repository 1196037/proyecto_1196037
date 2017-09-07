from django.conf.urls import url
from.views import * 

urlpatterns = [
		url(r'^base/nuevo/$', registrar_aprendices, name='registrar_aprendices'),
		url(r'^buscar/$', buscar_ap, name='buscar'),
		url(r'^$', aprendices, name='aprendices'),#vista principal
		url(r'^post/(?P<pk>[0-9]+)/edit/$', editar, name='post_edit'),
		url(r'^login/$', login_view, name='vista_login'),
		url(r'^logout/$', logout_view, name='vista_logout'),
		url(r'^agregar_categoria/$',agregar_categoria, name='agregar_categoria'),
		url(r'^crear_reto/$',crear_reto, name='crear_reto'),
		url(r'^ver/$', ver_retos, name='ver_reto'),
		url(r'^ranking$', ranking, name='ranking'),
		# url(r'^postnew/$', post_new, name='post_new'),
		#url(r'^$', , name='vista_login'),

]