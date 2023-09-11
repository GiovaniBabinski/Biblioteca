import datetime
from django.shortcuts import render, HttpResponse, redirect
from usuarios.models import Usuario
from .models import Livros, Categoria, Emprestimos
from .forms import CadastroLivroForm, CadastroCategoriaForm
from django.db.models import Q


def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id=request.session['usuario'])
        livros = Livros.objects.filter(usuario_id=usuario)
        total_livros = livros.count()

        status_cadastro_categoria = request.GET.get('cadastro_categoria')
        cadastro_livro = request.GET.get('cadastro_livro')
        cadastro_emprestimo = request.GET.get('cadastro_emprestimo')
        devolucao = request.GET.get('devolucao')
        livro_excluido = request.GET.get('livro_excluido')

        form = CadastroLivroForm()
        # acesso aos dados internos do ModelForm
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)

        form_categoria = CadastroCategoriaForm()
        form_categoria['usuario'].initial = request.session['usuario']

        usuarios = Usuario.objects.all()

        livros_emprestar = Livros.objects.filter(usuario=usuario).filter(emprestado=False)
        livros_emprestados = Livros.objects.filter(usuario=usuario).filter(emprestado=True)

        return render(request, 'home.html',
                      {'livros': livros, 'usuario_logado': request.session.get('usuario'), 'form': form,
                       'form_categoria': form_categoria,
                       'status_cadastro_categoria': status_cadastro_categoria, 'usuarios': usuarios,
                       'livros_emprestar': livros_emprestar,
                       'total_livros': total_livros, 'livros_emprestados': livros_emprestados,
                       'cadastro_livro': cadastro_livro,
                       'cadastro_emprestimo': cadastro_emprestimo, 'devolucao': devolucao,
                       'livro_excluido': livro_excluido})
    else:
        return redirect('/auth/login/?status=2')


def ver_livros(request, id):
    if request.session.get('usuario'):
        livro = Livros.objects.get(id=id)

        if request.session.get('usuario') == livro.usuario.id:
            categoria_livro = Categoria.objects.filter(usuario_id=request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro=livro)

            form = CadastroLivroForm()
            usuario = Usuario.objects.get(id=request.session['usuario'])
            form.fields['usuario'].initial = usuario
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)

            form_categoria = CadastroCategoriaForm()
            form_categoria.fields['usuario'].initial = request.session['usuario']

            usuarios = Usuario.objects.all()
            livros = Livros.objects.filter(usuario_id=usuario)

            livros_emprestar = Livros.objects.filter(usuario=usuario).filter(emprestado=False)
            livros_emprestados = Livros.objects.filter(usuario=usuario).filter(emprestado=True)

            livro_alterado = request.GET.get('livro_alterado')

            return render(request, 'ver_livro.html',
                          {'livro': livro, 'categoria_livro': categoria_livro, 'emprestimos': emprestimos,
                           'usuario_logado': request.session.get('usuario'), 'form': form, 'id_livro': id,
                           'form_categoria': form_categoria,
                           'usuarios': usuarios, 'livros_emprestar': livros_emprestar,
                           'livros_emprestados': livros_emprestados, 'livro_alterado': livro_alterado})
        else:
            return HttpResponse("Esse livro não lhe pertence!")
    return redirect('/auth/login?status=2')


def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/livro/home/?cadastro_livro=2')
        else:
            return HttpResponse("Dados invalidos")


def cadastrar_categoria(request):
    if request.method == 'POST':
        form_categoria = CadastroCategoriaForm(request.POST)
        if form_categoria.is_valid():
            form_categoria.save()
            return redirect('/livro/home/?cadastro_categoria=1')
        else:
            return HttpResponse("Dados inválidos")


def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado = request.POST.get('livro_emprestado')

        if nome_emprestado_anonimo:
            emprestimo = Emprestimos(nome_emprestado_anonimo=nome_emprestado_anonimo, livro_id=livro_emprestado)
        else:
            emprestimo = Emprestimos(nome_emprestado_id=nome_emprestado, livro_id=livro_emprestado)
        emprestimo.save()

        livro = Livros.objects.get(id=livro_emprestado)
        livro.emprestado = True
        livro.save()

        return redirect('/livro/home/?cadastro_emprestimo=3')


def devolver_livro(request):
    id = request.POST.get('id_livro_devolver')
    livro_devolver = Livros.objects.get(id=id)
    livro_devolver.emprestado = False
    livro_devolver.save()

    emprestimo_devolver = Emprestimos.objects.get(Q(livro=livro_devolver) & Q(data_devolucao=None))
    emprestimo_devolver.data_devolucao = datetime.date.today()
    emprestimo_devolver.save()
    return redirect('/livro/home/?devolucao=4')


def excluir_livro(request, id):
    livro = Livros.objects.get(id=id)
    livro.delete()
    return redirect('/livro/home/?livro_excluido=6')


def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    autor = request.POST.get('autor')
    co_autor = request.POST.get('co_autor')
    categoria_id = request.POST.get('categoria_id')
    categoria = Categoria.objects.get(id=categoria_id)
    livro = Livros.objects.get(id=livro_id)

    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        livro.categoria = categoria
        livro.save()
        return redirect(f"/livro/ver_livro/{livro_id}/?livro_alterado=5")
    else:
        return redirect('/auth/sair/')


def minhas_leituras(request):
    if request.session.get('usuario'):
        form = CadastroLivroForm()
        usuario = request.session.get('usuario')
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)

        form_categoria = CadastroCategoriaForm()
        form_categoria['usuario'].initial = request.session['usuario']

        usuarios = Usuario.objects.all()
        livros_emprestar = Livros.objects.filter(usuario=usuario).filter(emprestado=False)
        livros_emprestados = Livros.objects.filter(usuario=usuario).filter(emprestado=True)

        usuario_logado = request.session['usuario']
        usuario = Usuario.objects.get(id=usuario_logado)
        emprestimos = Emprestimos.objects.filter(nome_emprestado=usuario)
        return render(request, 'minhas_leituras.html',
                      {'usuario_logado': usuario_logado, 'emprestimos': emprestimos, 'form': form,
                       'form_categoria': form_categoria,
                       'usuarios': usuarios, 'livros_emprestar': livros_emprestar,
                       'livros_emprestados': livros_emprestados})
    else:
        return HttpResponse("Primeiro você precisa logar em sua conta.")


def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    opcoes = request.POST.get('opcoes')
    id_livro = request.POST.get('id_livro')
    emprestimo = Emprestimos.objects.get(id=id_emprestimo)
    if emprestimo.livro.usuario.id == request.session.get('usuario'):
        emprestimo.avaliacao = opcoes
        emprestimo.save()
        return redirect(f"/livro/ver_livro/{id_livro}")
    else:
        return HttpResponse("Esse emprestimo nao é seu")
