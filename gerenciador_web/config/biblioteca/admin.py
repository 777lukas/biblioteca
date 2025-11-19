from django.contrib import admin
from .models import Autor, Livro, Membro, Emprestimo

admin.site.register(Autor)
admin.site.register(Livro)
admin.site.register(Membro)
admin.site.register(Emprestimo)

