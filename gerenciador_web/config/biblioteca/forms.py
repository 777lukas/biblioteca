# biblioteca/forms.py

from django import forms
from .models import Livro, Autor, Membro, Emprestimo


class AutorForm(forms.ModelForm):
    """Formulário para cadastro de um novo Autor."""
    class Meta:
        model = Autor
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MembroForm(forms.ModelForm):
    """Formulário para cadastro de um novo Membro."""
    class Meta:
        model = Membro
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'contato': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LivroForm(forms.ModelForm):
    """Formulário para o cadastro de novos Livros."""
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'ano', 'quantidade_total', 'quantidade_disponivel']
        labels = {
            'quantidade_total': 'Qtd. Total (Estoque Inicial)',
            'quantidade_disponivel': 'Qtd. Disponível (Estoque Inicial)'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-select'}),
            'editora': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EmprestimoForm(forms.ModelForm):
    """Formulário para registrar um novo Empréstimo."""
    class Meta:
        model = Emprestimo
        # Não incluímos data_saida, data_prevista, data_devolucao e status 
        # pois são definidos automaticamente ou na devolução.
        fields = ['membro', 'livro'] 
        widgets = {
            'membro': forms.Select(attrs={'class': 'form-select'}),
            'livro': forms.Select(attrs={'class': 'form-select'}),
        }
    
    # Validação para verificar se há estoque disponível
    def clean_livro(self):
        livro = self.cleaned_data.get('livro')
        # Verifica se o livro existe e se a quantidade disponível é maior que zero
        if livro and livro.quantidade_disponivel <= 0:
            raise forms.ValidationError("Este livro não possui mais cópias disponíveis no estoque.")
        return livro

    # Redefine o save() para atualizar o estoque do livro
    def save(self, commit=True):
        emprestimo = super().save(commit=False)
        if commit:
            # Diminui a quantidade disponível
            emprestimo.livro.quantidade_disponivel -= 1 
            emprestimo.livro.save()
            emprestimo.save()
        return emprestimo