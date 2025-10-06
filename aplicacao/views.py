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
    df = get_dataframe()

    usuarios_filtrados = df[df['profile_name'].notna() & (df['profile_name'].str.lower() != 'unknown')]
    avaliacoes_por_usuario = usuarios_filtrados['profile_name'].value_counts().nlargest(15).sort_values()

    fig = plt.figure(figsize=(10,6))
    plt.barh(avaliacoes_por_usuario.index, avaliacoes_por_usuario.values)
    plt.title('Usuários mais ativos')
    plt.xlabel('Número de avaliações')
    plt.ylabel('Usuário')
    plt.grid(True, linestyle='-', alpha=0.3)
    
    grafico_base64 = plot_to_base64(fig)
    context = {
        'grafico_usuarios_ativos': grafico_base64
    }

    return render(request, 'aplicacao/dashboard.html', context)

def evolucao_reviews_view(request):
    df = get_dataframe()

    df['data_review'] = pd.to_datetime(df['review_time'], unit='s')
    df['ano'] = df['data_review'].dt.year

    avaliacoes_por_ano = df['ano'].value_counts().sort_index()

    fig = plt.figure(figsize=(10, 6))
    plt.plot(avaliacoes_por_ano.index, avaliacoes_por_ano.values, marker='o', linestyle='-', color='blue')
    plt.title('Evolução do Número de Avaliações por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de Avaliações')
    plt.grid(True, linestyle='--', alpha=0.3)

    grafico_base64 = plot_to_base64(fig)
    context = {
        'grafico_evolucao_reviews': grafico_base64
    }

    return render(request, 'aplicacao/dashboard.html', context) 

def preco_vs_score_view(request):
    df = get_dataframe()
    df = df[df['price'] > 0]
    df = df[df['price'] < 100]
    if len(df) > 1000:
        df = df.sample(n=1000, random_state=42)

    fig = plt.figure(figsize=(10,6))
    plt.scatter(df['price'], df['review_score'], alpha=0.3, color='purple')
    plt.title('Correlação entre Preço e Nota de Avaliação')
    plt.xlabel('Preço (R$)')
    plt.ylabel('Nota (Score)')
    plt.grid(True, linestyle='--', alpha=0.3)

    grafico_base64 = plot_to_base64(fig)
    context = {
        'grafico_preco_score': grafico_base64
    }

    return render(request, 'aplicacao/dashboard.html', context) 

def sentimento_reviews_view(request):
    df = get_dataframe()

    positivo = ["good", "great", "excellent", "I loved", "I recommend"]
    negativo = ["bad", "terrible", "disappointing", "I didn't like it", "terrible"]

    def classificar_sentimento(texto):
        texto = texto.lower()
        for palavra in positivo:
            if palavra.lower() in texto:
                return 'Positivo'
        for palavra in negativo:
            if palavra.lower() in texto:
                return 'Negativo'
        return 'Neutro'

    df['review_summary'] = df['review_summary'].fillna('')
    df['sentimento'] = df['review_summary'].apply(classificar_sentimento)
    contagem = df['sentimento'].value_counts()

    cores = {
        'Positivo': '#4CAF50',
        'Negativo': '#F44336',
        'Neutro': '#2196F3'
    }
    colors = [cores.get(sent, '#CCCCCC') for sent in contagem.index]


    fig = plt.figure(figsize=(10,6))
    explode = (0.1, 0, 0)
    plt.pie(contagem, labels=contagem.index, startangle=90, autopct='%1.1f%%', explode=explode)
    plt.title("Análise de sentimentos simples")
    plt.axis('equal')

    grafico_base64 = plot_to_base64(fig)
    context = {
        'grafico_sentimento': grafico_base64
    }

    return render(request, 'aplicacao/dashboard.html', context)

def dashboard(request):

    return