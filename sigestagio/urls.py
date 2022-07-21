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
from avaliacao.views import cad_avaliacao, entrar, list_avaliados, resumo_avaliacao

urlpatterns = [
    path('', entrar, name='login'),
    path('admin/', admin.site.urls),
    path('lista/avaliados', list_avaliados, name='list_avaliados'),
    path('cadastro/avaliacao/<int:id_funcionario>', cad_avaliacao, name='cad_avaliacao'),
    path('entrar', entrar, name='login'),
    path('resumo/avaliacao/<int:id_avaliacao>', resumo_avaliacao, name='resumo_avaliacao'),

]
