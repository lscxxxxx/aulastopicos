from django.db import models
from phone_field import PhoneField
from localflavor.br.models import BRStateField, BRPostalCodeField

class Produto(models.Model):
    nome = models.CharField("Nome", max_length = 200, null = True)
    preco = models.DecimalField("Preço", decimal_places = 2, max_digits = 8)
    qtd = models.PositiveIntegerField("Quantidade", default = 0)
    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField("Nome", max_length = 200, unique = True)
    email = models.EmailField("Email", max_length = 200, unique = True)
    def __str__(self):
        return self.nome

class Perfil(models.Model):
    cliente = models.OneToOneField(
        "Cliente",
        on_delete = models.CASCADE,
        related_name = "perfil"
    )
    rua = models.CharField(max_length=255, null = True)
    numero = models.CharField(max_length=10, null = True)
    bairro = models.CharField(max_length=100, null = True)
    cidade = models.CharField(max_length=100, null = True)
    estado = BRStateField(null = True)
    cep = BRPostalCodeField(null = True)
    telefone = PhoneField("Telefone", blank = True)
    def __str__(self):
        return f"{self.cliente.nome} - {self.telefone}"


class Venda(models.Model):
    data = models.DateTimeField(auto_now_add = True)
    cliente = models.ForeignKey(
        "Cliente",
        on_delete = models.CASCADE
    )
    produto = models.ManyToManyField(
        "Produto",
        through = "ItemVenda"
    )
    def __str__(self):
        return f"Venda #{self.id} - {self.data.strftime('%d/%m/%Y %H:%M')}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(
        "Venda",
        on_delete = models.CASCADE
    )
    produto = models.ForeignKey(
        "Produto",
        on_delete = models.CASCADE
    )
    qtd = models.PositiveIntegerField("Quantidade", default = 0)
    def __str__(self):
        return f"{self.qtd}x {self.produto.nome} (Venda #{self.venda.id})"
    
class Avaliacao(models.Model): 
    id_evaluation = models.CharField(max_length=255, null=True, blank=True) 
    title = models.CharField(max_length=255, null=True, blank=True) 
    price = models.FloatField(null=True, blank=True) 
    user_id = models.CharField(max_length=100, null=True, blank=True) 
    profile_name = models.CharField(max_length=255, null=True, blank=True) 
    review_helpfulness = models.CharField(max_length=20, null=True, blank=True) 
    review_score= models.FloatField() 
    review_time = models.IntegerField() 
    review_summary = models.CharField(max_length=255, null=True, blank=True) 
    review_text = models.TextField(null=True, blank=True) 
 
    def __str__(self): 
        return f"{self.title} - Score: {self.review_score}" 