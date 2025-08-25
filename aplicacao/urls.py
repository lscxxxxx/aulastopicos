from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="url_index"),
    path('produto', views.produto, name="url_produto"),
    path('cad_produto', views.cad_produto, name="url_cad_produto"),
]