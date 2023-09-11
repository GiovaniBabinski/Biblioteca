import datetime

from django.db import models
from datetime import date

from usuarios.models import Usuario

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome


class Livros(models.Model):
    img = models.ImageField(upload_to='capa_livro', null=True, blank=True)
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=80)
    co_autor = models.CharField(max_length=80, blank=True,null=True)
    data_cadastro = models.DateField(default=date.today())
    emprestado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name='Livro'

    def __str__(self):
        return self.nome


class Emprestimos(models.Model):
    choices = (
        ('P', 'Péssimo'),
        ('R', 'Ruim'),
        ('B', 'Bom'),
        ('O','Otimo')
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True,null=True)
    nome_emprestado_anonimo = models.CharField(max_length=30, blank=True)
    data_emprestimo = models.DateField(default=datetime.datetime.now())
    data_devolucao = models.DateField(blank=True, null=True)
    livro = models.ForeignKey(Livros,on_delete=models.CASCADE)
    avaliacao = models.CharField(max_length=1, choices=choices, blank=True)

    class Meta:
        verbose_name = 'Emprestimo'

    def __str__(self):
        return f"{self.nome_emprestado} | {self.livro}"



