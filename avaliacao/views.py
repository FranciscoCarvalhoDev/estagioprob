from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from avaliacao.forms import AvaliacaoForm
from datetime import datetime

# def cad_avaliacao(request):
#     form = AvaliacaoForm()
#
#     context = {'form': form}
#
#     return render(request, 'form_cad_avaliacao.html', context)
from avaliacao.models import Criterio, Avaliacao, Funcionario, Avaliador


def test_cad():
    # id do usuario do ativo
    id_avaliador = 1




    # add Avaliador
    avaliador = Funcionario
    avaliador = Funcionario.objects.get(pk=id_avaliador)
    # avaliacao.avaliacao.add(avaliador)
    avaliacao = Avaliacao



    avaliacao = avaliacao.objects.create(
        data='2022-10-12',
        tipo='Trimestral',
        nivel='Chefia',
        media='0',
        periodo='2022/1',
        avaliador=avaliador
    )

    # vindo da url form
    id_funcionario = 2
    # add funcionario avaliado
    funcionario_avaliado = Funcionario
    f1 = Funcionario.objects.get(pk=id_funcionario)
    #
    f1.avaliacao.add(avaliacao)
    #


def insert_avaliacao(request, id_funcionario):
    #id do usuario do ativo
    id_avaliador = request.user.profile.id
    print(request.user.profile.id)

    # add funcionario avaliado
    funcionario_avaliado = Funcionario
    funcionario_avaliado = Funcionario.objects.get(pk=id_funcionario)

    #add Avaliador
    avaliador = Avaliador
    avaliador = Avaliador.objects.get(pk=id_avaliador)
    # avaliacao.avaliacao.add(avaliador)

    avaliacao = Avaliacao

    avaliacao = avaliacao.objects.create(
        data='2022-10-12',
        tipo='Trimestral',
        nivel='Chefia',
        media='0',
        periodo='2022/1',
        avaliador=avaliador,
        funcionario=funcionario_avaliado,
    )

    add_criterios(request, avaliacao)


def add_criterios(request, avaliacao):
    itens_assiduidade = 1
    itens_disciplina = 5
    itens_iniciativa = 10
    itens_produtividade = 15
    itens_responsabilidade = 20
    itens_cooperacao = 24
    itens_dinamismo = 29
    itens_adaptabilidade = 31
    itens_urbanidade = 34
    itens_relacoes = 36

    criterio1 = Criterio

    for item in range(itens_assiduidade, itens_disciplina):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='1. Assiduidade Pontualidade',
            avaliacao=avaliacao
        )

    for item in range(itens_disciplina, itens_iniciativa):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='2. Disciplina',
            avaliacao=avaliacao
        )

    for item in range(itens_iniciativa, itens_produtividade):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )

    for item in range(itens_produtividade,itens_responsabilidade ):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )

    for item in range(itens_responsabilidade,itens_cooperacao ):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )

    for item in range(itens_cooperacao,itens_dinamismo ):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )

    for item in range(itens_dinamismo,itens_adaptabilidade ):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )

    for item in range(itens_adaptabilidade,itens_urbanidade):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )

    for item in range(itens_urbanidade,itens_relacoes):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )

    for item in range(itens_relacoes,40):

        #Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )

def cad_avaliacao(request, id_funcionario):
    context = None


    if request.method == 'GET':
        funcionario = Funcionario
        funcionario = funcionario.objects.get(pk=id_funcionario)

        context = {'funcionario': funcionario}
        return render(request, 'form_cad_avaliacao.html', context)

    if request.method == 'POST':
        insert_avaliacao(request, id_funcionario)
        return redirect('list_avaliados')



def list_avaliados(request):
    funcionarios = Funcionario.objects.filter(grupo=request.user.profile.funcionario.grupo, avaliavel=True)

    print(funcionarios)
    context = {'funcionarios': funcionarios}

    return render(request, 'list_funcionarios.html', context)


def entrar(request):
    context = {'msg': ''}

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        user = authenticate(username=usuario, password=senha)

        if user is not None:
            if user.is_active:
                login(request, user)
                print(user.profile.funcionario.cargo)


                return redirect('/lista/avaliados')
            else:
                context = {'msg': 'Usuario não está ativo'}
        else:
            context = {'msg': 'Não foi possível logar'}

    return render(request, 'form_auth.html', context)