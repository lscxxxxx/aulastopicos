from django.contrib import admin
from .models import Produto, Cliente, Perfil

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'qtd')

admin.site.register(Produto, ProdutoAdm)
admin.site.register(Cliente)
