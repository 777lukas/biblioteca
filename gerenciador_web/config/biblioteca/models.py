from django.db import models
from datetime import timedelta, date


class Autor(models.Model):
    nome = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editora = models.CharField(max_length=100)
    ano = models.IntegerField()
    quantidade_total = models.IntegerField()
    quantidade_disponivel = models.IntegerField()

    def __str__(self):
        return self.titulo


class Membro(models.Model):
    nome = models.CharField(max_length=100)
    contato = models.EmailField()
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_saida = models.DateField(auto_now_add=True)
    data_prevista = models.DateField(default=date.today)
    data_devolucao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Ativo")

    def salvar_devolucao(self):
        self.data_devolucao = date.today()
        self.status = "Devolvido"
        self.livro.quantidade_disponivel += 1
        self.livro.save()
        self.save()

    def __str__(self):
        return f"{self.livro.titulo} - {self.membro.nome}"

