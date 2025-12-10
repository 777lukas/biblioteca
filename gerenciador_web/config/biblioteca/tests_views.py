# biblioteca/test_views.py

from django.test import TestCase, Client
from django.urls import reverse

# Importando Modelos (necessário para criar dados de teste)
from .models import Autor, Livro, Membro, Emprestimo
# Importando Forms (não são usados diretamente, mas necessários para o contexto)
from .forms import LivroForm, AutorForm, MembroForm, EmprestimoForm 


class ViewsTests(TestCase):
    """
    Testes focados nas funções de view, rotas, templates usados e comportamento POST/GET.
    """

    def setUp(self):
        self.client = Client()
        
        # Criação de dados base para testes de view
        self.autor = Autor.objects.create(nome="Autor View")
        self.livro = Livro.objects.create(
            titulo="Livro Teste View",
            autor=self.autor,
            editora="ET",
            ano=2020,
            quantidade_total=5,
            quantidade_disponivel=2
        )
        self.membro = Membro.objects.create(nome="Membro View", contato="m@exemplo.com", tipo="Comum")
        
        # Nomes de URLs (Assumindo namespace 'biblioteca' no urls.py)
        self.index_url = reverse('biblioteca:index')
        self.add_livro_url = reverse('biblioteca:adicionar_livro')
        self.add_autor_url = reverse('biblioteca:adicionar_autor')
        self.add_membro_url = reverse('biblioteca:adicionar_membro')
        self.listar_livros_url = reverse('biblioteca:listar_livros')
        self.emprestimo_url = reverse('biblioteca:registrar_emprestimo')


    # --- Teste View Index ---

    def test_index_view_acesso(self):
        """Testa o acesso e conteúdo da view 'index' (que retorna HttpResponse)."""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bem-vindo à Biblioteca!")


    # --- Testes Views de Cadastro Genérico (criar_cadastro) ---

    def test_adicionar_livro_GET(self):
        """Testa o acesso GET e o template correto para adicionar Livro."""
        response = self.client.get(self.add_livro_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'biblioteca/adicionar_item.html')
        self.assertContains(response, 'Cadastrar Novo(a) Livro') 

    def test_adicionar_autor_POST_sucesso(self):
        """Testa o POST válido para Autor (redirecionamento e criação no DB)."""
        autor_data = {'nome': 'J.K. Rowling', 'nacionalidade': 'Britânica'}
        
        response = self.client.post(self.add_autor_url, autor_data)
        
        # 1. Redirecionamento (sucesso)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.add_autor_url) 
        
        # 2. Criação no DB
        self.assertTrue(Autor.objects.filter(nome='J.K. Rowling').exists())

    def test_adicionar_membro_POST_invalido(self):
        """Testa o POST inválido para Membro (re-renderização e falha na criação)."""
        # Dados inválidos: contato vazio (EmailField obrigatório)
        membro_data = {'nome': 'Pedro', 'contato': '', 'tipo': 'Estudante'} 
        
        response = self.client.post(self.add_membro_url, membro_data)
        
        # 1. Re-renderização (falha de validação)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'biblioteca/adicionar_item.html')
        
        # 2. Falha na criação
        self.assertFalse(Membro.objects.filter(nome='Pedro').exists())

    # --- Teste View de Listagem ---

    def test_listar_livros_view(self):
        """Testa a listagem, ordenação e o uso correto da anotação F()."""
        # Cria um segundo livro para verificar ordenação
        Livro.objects.create(
            titulo="A Livro Teste X",
            autor=self.autor,
            editora="ET",
            ano=1945,
            quantidade_total=10,
            quantidade_disponivel=5
        )
        
        response = self.client.get(self.listar_livros_url)
        self.assertEqual(response.status_code, 200)
        
        # Verifica a ordenação por 'titulo' (Livro Teste View vs A Livro Teste X)
        self.assertEqual(response.context['livros'][0].titulo, "A Livro Teste X") 
        
        # Verifica se o campo 'disponivel_hoje' anotado pela F-expression está correto
        self.assertEqual(response.context['livros'][0].disponivel_hoje, 5)

    # --- Testes View de Empréstimo ---

    def test_registrar_emprestimo_POST_sucesso(self):
        """Testa o registro bem-sucedido de um Empréstimo (criação e redirecionamento)."""

        emprestimo_data = {
            'livro': self.livro.pk,
            'membro': self.membro.pk,
        }
        
        response = self.client.post(self.emprestimo_url, emprestimo_data)
        
        # 1. Redirecionamento (sucesso)
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, self.emprestimo_url)
        
        # 2. Criação do objeto
        self.assertEqual(Emprestimo.objects.count(), 1)

    def test_registrar_emprestimo_POST_falha(self):
        """Testa o registro de Empréstimo com dados inválidos (re-renderização e mensagem de erro)."""
        
        # Dados inválidos (PK de livro que não existe, o form.is_valid() deve falhar)
        emprestimo_data = {
            'livro': 9999, 
            'membro': self.membro.pk,
        }
        
        response = self.client.post(self.emprestimo_url, emprestimo_data)
        
        # 1. Re-renderização (falha de validação)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Erro ao registrar empréstimo.') # Verifica a mensagem de erro
        
        # 2. Nenhuma criação
        self.assertEqual(Emprestimo.objects.count(), 0)