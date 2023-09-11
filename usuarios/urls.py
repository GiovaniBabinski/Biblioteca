from django.urls import path
from .views import login,cadastro,valida_login,valida_cadastro,sair

urlpatterns = [
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('valida_cadastro', valida_cadastro, name='valida_cadastro'),
    path('valida_login/', valida_login, name='valida_login'),
    path('sair/', sair, name='sair'),

]
