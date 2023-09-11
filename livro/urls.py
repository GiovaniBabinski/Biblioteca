from django.urls import path
from .views import home,ver_livros,cadastrar_livro,excluir_livro,cadastrar_categoria,cadastrar_emprestimo,devolver_livro,alterar_livro,minhas_leituras, processa_avaliacao


urlpatterns = [
    path('home/', home, name='home'),
    path('ver_livro/<int:id>/', ver_livros, name='ver_livros'),
    path('cadastrar_livro/', cadastrar_livro, name='cadastrar_livro'),
    path('cadastrar_categoria/', cadastrar_categoria, name='cadastrar_categoria'),
    path('cadastrar_emprestimo/', cadastrar_emprestimo, name='cadastrar_emprestimo'),
    path('devolver_livro/', devolver_livro, name='devolver_livro'),
    path('excluir_livro/<int:id>/', excluir_livro, name='excluir_livro'),
    path('alterar_livro/', alterar_livro, name='alterar_livro'),
    path('minhas_leituras/', minhas_leituras, name='minhas_leituras'),
    path('processa_avaliacao/', processa_avaliacao, name='processa_avaliacao'),


]
