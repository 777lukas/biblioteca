# biblioteca/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F # Para operações de banco de dados mais avançadas (como listagem)
from django.http import HttpResponse

from .forms import LivroForm, AutorForm, MembroForm, EmprestimoForm
from .models import Livro, Autor, Membro, Emprestimo


def index(request):
    # Agora o Django sabe o que é HttpResponse
    return HttpResponse("<h1>Bem-vindo à Biblioteca!</h1><p>Esta é a página inicial da sua aplicação.</p>")

# --- Views de Cadastro (C) ---

def criar_cadastro(request, form_class, template_name, redirect_url_name, item_name):
    """Função genérica para gerenciar o cadastro de Autor, Livro ou Membro."""
    if request.method == 'POST':
        form = form_class(request.POST) 
        if form.is_valid():
            novo_item = form.save() 
            messages.success(request, f'{item_name} "{novo_item}" cadastrado(a) com sucesso!')
            return redirect(redirect_url_name) 
        else:
            messages.error(request, f'Erro ao cadastrar {item_name}. Verifique os campos.')
    else:
        form = form_class()
        
    contexto = {
        'form': form,
        'titulo_pagina': f'Cadastrar Novo(a) {item_name}',
    }
    return render(request, template_name, contexto)


def adicionar_livro(request):
    return criar_cadastro(
        request, LivroForm, 'biblioteca/adicionar_item.html', 'biblioteca:adicionar_livro', 'Livro'
    )

def adicionar_autor(request):
    return criar_cadastro(
        request, AutorForm, 'biblioteca/adicionar_item.html', 'biblioteca:adicionar_autor', 'Autor'
    )

def adicionar_membro(request):
    return criar_cadastro(
        request, MembroForm, 'biblioteca/adicionar_item.html', 'biblioteca:adicionar_membro', 'Membro'
    )


# --- View de Empréstimo e Devolução ---

def registrar_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save()
            messages.success(request, f'Empréstimo de "{emprestimo.livro.titulo}" para "{emprestimo.membro.nome}" registrado com sucesso.')
            return redirect('biblioteca:registrar_emprestimo')
        else:
            messages.error(request, 'Erro ao registrar empréstimo. Verifique se o livro está disponível.', extra_tags='danger')
    else:
        form = EmprestimoForm()

    contexto = {
        'form': form,
        'titulo_pagina': 'Registrar Novo Empréstimo',
    }
    return render(request, 'biblioteca/registrar_emprestimo.html', contexto)

# --- View de Listagem (R) ---

def listar_livros(request):
    """Lista todos os livros, mostrando a disponibilidade."""
    # F() expression garante que a operação é feita no banco de dados, não na memória
    livros = Livro.objects.annotate(
        disponivel_hoje=F('quantidade_disponivel')
    ).order_by('titulo')
    
    contexto = {
        'livros': livros,
        'titulo_pagina': 'Acervo de Livros',
    }
    return render(request, 'biblioteca/listar_livros.html', contexto)
    # biblioteca/views.py (Exemplo)

def index(request):
    """
    Função de view básica para a página inicial da biblioteca.
    """
    return HttpResponse("<h1>Bem-vindo à Biblioteca!</h1><p>Esta é a página inicial da sua aplicação.</p>")