# biblioteca/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Exemplo de rota: a página inicial da aplicação 'biblioteca'
    # Será acessada em / se configurada na raiz do projeto.
    path('', views.index, name='index'), 
    
    # Você adicionará outras rotas aqui conforme desenvolver sua aplicação
    # Exemplo: path('livros/', views.lista_livros, name='lista_livros'),
]