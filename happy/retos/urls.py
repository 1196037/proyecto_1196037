from django.conf.urls import url
from.views import * 

urlpatterns = [
url(r'^$', lista_aprendices, name='lista'),
url(r'^buscar/$', buscar_ap, name='buscar'),

]