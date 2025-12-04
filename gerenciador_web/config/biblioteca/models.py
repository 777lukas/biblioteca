# biblioteca/models.py

from django.db import models
from datetime import timedelta, date


# Função auxiliar para calcular o padrão de data de devolução (ex: 7 dias)
def data_retorno_padrao():
    """Calcula a data prevista de devolução, 7 dias após a data atual."""
    return date.today() + timedelta(days=7)


class Autor(models.Model):
    """Modelo para representar um Autor de livros."""
    nome = models.CharField(max_length=100)
    nacionalidade = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    """Modelo para representar um Livro no acervo."""
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE) 
    editora = models.CharField(max_length=100)
    ano = models.IntegerField()
    quantidade_total = models.IntegerField()
    quantidade_disponivel = models.IntegerField()

    def __str__(self):
        return self.titulo


class Membro(models.Model):
    """Modelo para representar um Membro (usuário) da biblioteca."""
    nome = models.CharField(max_length=100)
    contato = models.EmailField()
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


class Emprestimo(models.Model):
    """Modelo para registrar o histórico e status dos empréstimos."""
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_saida = models.DateField(auto_now_add=True)
    # Usa a função para definir o default
    data_prevista = models.DateField(default=data_retorno_padrao) 
    data_devolucao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Ativo")

    def salvar_devolucao(self):
        """Método para registrar a devolução de um livro e atualizar o estoque."""
        self.data_devolucao = date.today()
        self.status = "Devolvido"
        self.livro.quantidade_disponivel += 1 
        self.livro.save()
        self.save()

    def __str__(self):
        return f"{self.livro.titulo} - {self.membro.nome}"