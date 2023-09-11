from django import forms
from .models import Livros, Emprestimos, Categoria


class CadastroLivroForm(forms.ModelForm):
    class Meta:
        model = Livros
        fields = '__all__'

    # Função para acessar os dados internos do forms em BaseForm e alterar o tipo de dado do usuario, para reconhecer automaticamente a não deixar o usuario manipular

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()


class CadastroCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()
