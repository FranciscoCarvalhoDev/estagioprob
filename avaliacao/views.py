from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponseNotFound
from datetime import datetime

from avaliacao.models import Criterio, Avaliacao, Funcionario, Avaliador


@login_required
def insert_avaliacao(request, id_funcionario):
    # id do usuario do ativo
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
        data=datetime.now(),
        tipo='Trimestral',
        tipo_avaliador='Chefia',
        media='0',
        periodo='2022/1',
        avaliador=avaliador,
        funcionario=funcionario_avaliado,
    )

    medias_criterios, media_avaliacao = add_criterios(request, avaliacao)

    print(medias_criterios)
    print(media_avaliacao)

    avaliacao.media = media_avaliacao
    avaliacao.save(force_update=True)

    return avaliacao



def add_criterios(request, avaliacao):
    inicio_assiduidade = 1
    inicio_disciplina = 5
    inicio_iniciativa = 10
    inicio_produtividade = 15
    inicio_responsabilidade = 20
    inicio_cooperacao = 24
    inicio_dinamismo = 29
    inicio_adaptabilidade = 31
    inicio_urbanidade = 34
    inicio_relacoes = 36

    criterio1 = Criterio

    media_avaliacao = 0

    # ASSIDUIDADE
    pontos_assiduidade = 0
    itens_assiduidade = inicio_disciplina - inicio_assiduidade

    for item in range(inicio_assiduidade, inicio_disciplina):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='1. Assiduidade Pontualidade',
            avaliacao=avaliacao
        )

        pontos_assiduidade += float(request.POST.get('pt_criterio' + str(item)))

    media_assiduidade = pontos_assiduidade / itens_assiduidade

    # DISCIPLINA
    pontos_disciplina = 0
    itens_disciplina = inicio_iniciativa - inicio_disciplina

    for item in range(inicio_disciplina, inicio_iniciativa):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='2. Disciplina',
            avaliacao=avaliacao
        )

        pontos_disciplina += float(request.POST.get('pt_criterio' + str(item)))

    media_disciplina = pontos_disciplina / itens_disciplina

    # INICIATIVA
    pontos_iniciativa = 0
    itens_iniciativa = inicio_produtividade - inicio_iniciativa

    for item in range(inicio_iniciativa, inicio_produtividade):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='3. Capacidade de Iniciativa',
            avaliacao=avaliacao
        )
        pontos_iniciativa += float(request.POST.get('pt_criterio' + str(item)))


    media_iniciativa = pontos_iniciativa / itens_iniciativa

    # PRODUTIVIDADE
    pontos_produtividade = 0
    itens_produtividade = inicio_responsabilidade - inicio_produtividade

    for item in range(inicio_produtividade, inicio_responsabilidade):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='4. Produtividade',
            avaliacao=avaliacao
        )
        pontos_produtividade += float(request.POST.get('pt_criterio' + str(item)))

    media_produtividade = pontos_produtividade / itens_produtividade

    # RESPONSABILIDADE
    pontos_responsabilidade = 0
    itens_responsabilidade = inicio_cooperacao - inicio_responsabilidade

    for item in range(inicio_responsabilidade, inicio_cooperacao):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='5. Responsabilidade',
            avaliacao=avaliacao
        )
        pontos_responsabilidade += float(request.POST.get('pt_criterio' + str(item)))


    media_responsabilidade = pontos_responsabilidade / itens_responsabilidade

    # COOPERACAO
    pontos_cooperacao = 0
    itens_cooperacao = inicio_dinamismo - inicio_cooperacao

    for item in range(inicio_cooperacao, inicio_dinamismo):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='6. Cooperação',
            avaliacao=avaliacao
        )
        pontos_cooperacao += float(request.POST.get('pt_criterio' + str(item)))


    media_cooperacao = pontos_cooperacao / itens_cooperacao

    # DINAMISMO
    pontos_dinamismo = 0
    itens_dinamismo = inicio_adaptabilidade - inicio_dinamismo

    for item in range(inicio_dinamismo, inicio_adaptabilidade):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='7. Dinamismo',
            avaliacao=avaliacao
        )
        pontos_dinamismo += float(request.POST.get('pt_criterio' + str(item)))


    media_dinamismo = pontos_dinamismo / itens_dinamismo

    # ADAPTABILIDADE
    pontos_adaptabilidade = 0
    itens_adaptabilidade = inicio_urbanidade - inicio_adaptabilidade

    for item in range(inicio_adaptabilidade, inicio_urbanidade):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='8. Adaptabilidade',
            avaliacao=avaliacao
        )
        pontos_adaptabilidade += float(request.POST.get('pt_criterio' + str(item)))


    media_adaptabilidade = pontos_adaptabilidade / itens_adaptabilidade

    # URBANIDADE
    pontos_urbanidade = 0
    itens_urbanidade = inicio_relacoes - inicio_urbanidade

    for item in range(inicio_urbanidade, inicio_relacoes):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='9. Urbanidade',
            avaliacao=avaliacao
        )
        pontos_urbanidade += float(request.POST.get('pt_criterio' + str(item)))


    media_urbanidade = pontos_urbanidade / itens_urbanidade

    # RELACOES
    pontos_relacoes = 0
    itens_relacoes = 40 - inicio_relacoes

    for item in range(inicio_relacoes, 40):
        # Cadastra cada um dos itens
        criterio1.objects.create(
            descricao=request.POST.get('txt_criterio' + str(item)),
            nota=request.POST.get('pt_criterio' + str(item)),
            categoria='10. Relações Interpessoais',
            avaliacao=avaliacao
        )
        pontos_relacoes += float(request.POST.get('pt_criterio' + str(item)))


    media_relacoes = pontos_relacoes / itens_relacoes

    medias_criterios = [media_assiduidade, media_disciplina, media_iniciativa, media_produtividade, media_responsabilidade, \
           media_cooperacao, media_dinamismo, media_adaptabilidade, media_urbanidade, media_relacoes]

    media_avaliacao = sum(medias_criterios) / len(medias_criterios)
    return medias_criterios, media_avaliacao

@login_required
def cad_avaliacao(request, id_funcionario):
    context = None

    if request.method == 'GET':
        funcionario = Funcionario
        funcionario = funcionario.objects.get(pk=id_funcionario)

        context = {'funcionario': funcionario}
        return render(request, 'form_cad_avaliacao.html', context)

    if request.method == 'POST':
        avaliacao = insert_avaliacao(request, id_funcionario)
        # insert_avaliacao(request, 3)

        print(avaliacao)
        context = {'avaliacao':avaliacao}

        return render(request,'resumo_avaliacao.html',context)

def resumo_avaliacao(request, id_avaliacao):
    avaliacao = Avaliacao.objects.get(pk=id_avaliacao)
    criterios = Criterio.objects.filter(avaliacao=avaliacao)
    # criterios = Criterio.objects.filter(categoria = '3. Capacidade de Iniciativa', avaliacao=avaliacao)


    context = {'avaliacao': avaliacao, 'criterios': criterios}
    print(criterios)
    return render(request, 'resumo_avaliacao.html', context)


@login_required
def list_avaliados(request):
    if request.user.profile.tipo == 'Chefe':
        funcionarios = Funcionario.objects.filter(
            Q(grupo_avaliacao=request.user.profile.funcionario.grupo_avaliacao, avaliavel=True))
    else:
        if request.user.profile.tipo == 'Colega':
            # funcionarios = Funcionario.objects.filter(subgrupo_avaliacao=request.user.profile.grupo_avaliado, avaliavel=True)
            funcionarios = Funcionario.objects.filter(
                Q(subgrupo_avaliacao=request.user.profile.grupo_avaliado, avaliavel=True) | Q(
                    id=request.user.profile.funcionario.id))

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
