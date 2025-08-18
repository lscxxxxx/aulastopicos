from django.shortcuts import render

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)

def produto(request):
    context = {
        'produto': 'abacaxi',
    }
    return render(request, 'produtos.html', context)