from django.contrib import admin
from .models import Autor, Livro, Membro, Emprestimo

# ATENÇÃO: As linhas 'admin.site.register(...)' DUPLICADAS foram REMOVIDAS daqui.

# biblioteca/admin.py

# 1. Personalização do Autor
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nacionalidade')
    search_fields = ('nome',)


# 2. Personalização do Livro
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editora', 'ano', 'quantidade_disponivel', 'quantidade_total')
    list_filter = ('ano', 'autor', 'editora')
    search_fields = ('titulo', 'autor__nome')
    list_editable = ('quantidade_disponivel',)


# 3. Personalização do Membro
@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'contato', 'tipo')
    search_fields = ('nome', 'contato')
    list_filter = ('tipo',)


# 4. Personalização do Empréstimo
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('livro', 'membro', 'data_saida', 'data_prevista', 'data_devolucao', 'status')
    list_filter = ('status', 'data_saida', 'data_prevista')
    search_fields = ('livro__titulo', 'membro__nome')
    ordering = ('-data_saida',)
    
    # Ações disponíveis para vários itens selecionados
    actions = ['marcar_como_devolvido']

    # Action personalizada: Marcar como Devolvido
    @admin.action(description='Marcar itens selecionados como Devolvidos')
    def marcar_como_devolvido(self, request, queryset):
        livros_devolvidos = 0
        for emprestimo in queryset:
            if emprestimo.status != "Devolvido":
                # Esta linha assume que existe um método salvar_devolucao() no seu modelo Emprestimo
                # Se não existir, o código falhará em tempo de execução
                try:
                    emprestimo.salvar_devolucao()
                    livros_devolvidos += 1
                except AttributeError:
                    self.message_user(request, "Erro: O método salvar_devolucao() não existe no modelo Emprestimo.", level='error')
                    return

        if livros_devolvidos > 0:
            self.message_user(request, f'{livros_devolvidos} empréstimo(s) foram marcados como Devolvidos e o estoque atualizado.', level='success')
        else:
            self.message_user(request, 'Nenhum empréstimo ativo foi selecionado ou os itens já estavam devolvidos.', level='warning')