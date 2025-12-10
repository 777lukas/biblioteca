# biblioteca/test_models.py

from django.test import TestCase
from datetime import timedelta, date
from unittest.mock import patch 

# Importando Modelos (certifique-se de que os imports estão corretos)
from .models import Autor, Livro, Membro, Emprestimo, data_retorno_padrao


class ModelTests(TestCase):
    """
    Agrupa todos os testes para os modelos: Autor, Livro, Membro, Emprestimo,
    incluindo a função auxiliar data_retorno_padrao e o método salvar_devolucao.
    """

    def setUp(self):
        # Configuração inicial para os modelos
        self.autor = Autor.objects.create(nome="George Orwell", nacionalidade="Britânica")
        self.livro = Livro.objects.create(
            titulo="1984",
            autor=self.autor,
            editora="Secker & Warburg",
            ano=1949,
            quantidade_total=5,
            quantidade_disponivel=3 # Estoque inicial
        )
        self.membro = Membro.objects.create(nome="Alice Silva", contato="alice@exemplo.com", tipo="Estudante")
        
        # Empréstimo inicial (usado para testar devolução)
        self.emprestimo = Emprestimo.objects.create(
            membro=self.membro,
            livro=self.livro,
        )

    # --- Testes de Autor ---

    def test_criacao_autor(self):
        """Verifica a criação básica do Autor e seu __str__."""
        autor = Autor.objects.get(nome="George Orwell")
        self.assertEqual(autor.nacionalidade, "Britânica")
        self.assertEqual(str(autor), "George Orwell")

    # --- Testes de Livro ---

    def test_criacao_livro(self):
        """Verifica a criação básica do Livro e seu estoque."""
        livro = Livro.objects.get(titulo="1984")
        self.assertEqual(livro.quantidade_disponivel, 3)
        self.assertEqual(str(livro), "1984")

    # --- Testes de Membro ---

    def test_criacao_membro(self):
        """Verifica a criação básica do Membro."""
        membro = Membro.objects.get(nome="Alice Silva")
        self.assertEqual(membro.contato, "alice@exemplo.com")
        self.assertEqual(str(membro), "Alice Silva")

    # --- Testes de Emprestimo e Funções Auxiliares ---

    def test_data_retorno_padrao(self):
        """Testa se data_retorno_padrao calcula corretamente 7 dias no futuro."""
        data_esperada = date.today() + timedelta(days=7)
        self.assertEqual(data_retorno_padrao(), data_esperada)

    def test_criacao_emprestimo_defaults(self):
        """Verifica se o Empréstimo usa status e data_prevista padrão."""
        emprestimo = Emprestimo.objects.get(pk=self.emprestimo.pk)
        self.assertEqual(emprestimo.status, "Ativo")
        self.assertEqual(emprestimo.data_prevista, data_retorno_padrao())
        self.assertEqual(str(emprestimo), "1984 - Alice Silva")

    @patch('biblioteca.models.date') 
    def test_salvar_devolucao_e_estoque(self, mock_date):
        """Testa o método salvar_devolucao, garantindo que o status, a data e o estoque sejam atualizados."""
        
        # Define a data "atual" para simular a devolução
        data_devolucao_fixa = date(2025, 12, 17)
        mock_date.today.return_value = data_devolucao_fixa
        
        estoque_antes = self.livro.quantidade_disponivel # 3

        # Ação: Executa a devolução
        self.emprestimo.salvar_devolucao()

        # Verifica: Recarrega os objetos do DB
        self.emprestimo.refresh_from_db()
        self.livro.refresh_from_db()

        # 1. Status e Data
        self.assertEqual(self.emprestimo.status, "Devolvido")
        self.assertEqual(self.emprestimo.data_devolucao, data_devolucao_fixa)
        
        # 2. Estoque (3 + 1 = 4)
        self.assertEqual(self.livro.quantidade_disponivel, estoque_antes + 1)