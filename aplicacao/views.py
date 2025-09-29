from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Cliente, Perfil, Avaliacao
import io
import urllib, base64
import pandas as pd
import matplotlib.pyplot as plt

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)

@login_required
def produto(request):
    produtos = Produto.objects.all()
    context = {
        'produtos' : produtos,
    }
    return render(request, 'produtos.html', context)

def cad_produto(request):
    if request.user.is_authenticated:
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
    else:
        return redirect('url_entrar')

def atualizar_produto(request, id):
    prod = get_object_or_404(Produto, id=id)
    if request.method == "GET":
        context = {
            'prod': prod,
        }
        return render(request, 'atualizar_produto.html', context)
    elif request.method == "POST":
        nome = request.POST.get('nome')
        preco = request.POST.get('preco').replace(',', '.')
        qtd = request.POST.get('qtd')

        prod.nome = nome
        prod.preco = preco
        prod.qtd = qtd
        prod.save()
    return redirect('url_produto')

def apagar_produto(request, id):
    prod = get_object_or_404(Produto, id=id)
    prod.delete()
    return redirect('url_produto')

def entrar(request):
    if request.method == "GET":
        return render (request, "entrar.html")
    else:
        username = request.POST.get('nome')
        password = request.POST.get('senha')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('url_produto')
        else:
            return HttpResponse("PANE NO SISTEMA ALGUÉM ME DESCONFIGUROU")

def cad_user(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        
        user = User.objects.filter(username=nome).first()
        
        if user:
            return HttpResponse("Usuário já existe!")
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, "Usuário criado")
    else:
        return render(request, "cad_user.html")
    
def sair(request):
    logout(request)
    return redirect('url_entrar')

def cad_cliente(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'cad_cliente.html')
        elif request.method == "POST":
            nome = request.POST.get('nome')
            email = request.POST.get('email')

            if Cliente.objects.filter(email=email).exists():
                return HttpResponse("E-mail já cadastrado!")

            cliente = Cliente(
                nome = nome,
                email = email
            )
            cliente.save()

            rua = request.POST.get('rua')
            numero = request.POST.get('numero')
            bairro = request.POST.get('bairro')
            cidade = request.POST.get('cidade')
            estado = request.POST.get('estado')
            cep = request.POST.get('cep')
            telefone = request.POST.get('telefone')

            Perfil.objects.create(
                cliente=cliente,
                rua=rua,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cep=cep,
                telefone=telefone
            )

            return redirect('url_cliente')
    else:
        return redirect('url_entrar')
    
def get_dataframe(): 
    # Busca todos os dados do banco e retorna um DataFrame do Pandas 
    avaliacoes = Avaliacao.objects.all().values() 
    df = pd.DataFrame(list(avaliacoes)) 
    return df 
 
def plot_to_base64(fig): 
    # Converte uma figura Matplotlib para uma string base64 para ser usada no HTML 
    buf = io.BytesIO() 
    fig.savefig(buf, format='png') 
    buf.seek(0) 
    string = base64.b64encode(buf.read())
    return urllib.parse.quote(string)

def usuarios_mais_ativos_view(request):

    context = {}

    return render(request, 'aplicacao/dashboard.html', context)

def evolucao_reviews_view(request):

    context = {}

    return render(request, 'aplicacao/dashboard.html', context) 

def preco_vs_score_view(request):

    context = {}

    return render(request, 'aplicacao/dashboard.html', context) 

def sentimento_reviews_view(request):

    context = {}

    return render(request, 'aplicacao/dashboard.html', context)

def dashboard(request):

    return