"""sigestagio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from avaliacao.views import cad_avaliacao, entrar,entrar_token, list_avaliados, resumo_avaliacao, reativar_avaliacao, \
    detalhes_avaliado, relatorio_avaliacao

urlpatterns = [
    path('', entrar, name='login'),
    path('sair', entrar, name='sair'),
    path('admin/', admin.site.urls),
    path('lista/avaliados', list_avaliados, name='list_avaliados'),
    path('cadastro/avaliacao/<int:id_funcionario>', cad_avaliacao, name='cad_avaliacao'),
    path('entrar', entrar, name='login'),
    path('entrar/<str:token_id>', entrar_token, name='login2'),
    path('resumo/avaliacao/<int:id_avaliacao>', resumo_avaliacao, name='resumo_avaliacao'),
    path('ativar/avaliacao/<int:id_funcionario>', reativar_avaliacao, name='ativar_avaliacao'),
    path('detalhe/avaliado/<int:id_avaliado>', detalhes_avaliado, name='detalhes_avaliado'),
    path('relatorio/avaliacao/<int:id_funcionario>', relatorio_avaliacao, name='relatorio_avaliacao'),

]
