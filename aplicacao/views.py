from django.http.response import HttpResponse
from django.shortcuts import render, redirect
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
    if request.method == "GET":
        return render(request, 'cad_produto.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        preco = request.POST.get('preco').replace(',', '.')
        qtd = request.POST.get('qtd')

        produto = Produto(
            nome = nome,
            preco = preco,
            qtd = qtd
        )
        produto.save()
        return redirect('url_produto')