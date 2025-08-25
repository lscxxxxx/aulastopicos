from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Produto

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)

def produto(request):
    produtos = Produto.objects.all()
    context = {
        'produtos' : produtos,
    }
    return render(request, 'produtos.html', context)

def cad_produto(request):
    return HttpResponse("tela de cadastro de produtos")