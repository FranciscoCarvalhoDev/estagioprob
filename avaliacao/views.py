from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
import datetime
import ast
import logging

logger = logging.getLogger('requestlogs')

from avaliacao.models import Criterio, Avaliacao, Funcionario, Avaliador


@login_required
def insert_avaliacao(request, id_funcionario):
    # id do usuario do ativo
    id_avaliador = request.user.profile.id
    # print(request.user.profile.id)

    # add funcionario avaliado
    # funcionario_avaliado = Funcionario
    funcionario_avaliado = Funcionario.objects.get(pk=id_funcionario)

    # add Avaliador
    avaliador = Avaliador
    avaliador = Avaliador.objects.get(pk=id_avaliador)
    # avaliacao.avaliacao.add(avaliador)

    avaliacao = Avaliacao

    id_funcionario_usuario = request.user.profile.funcionario.id

    logger.info('')

    if request.user.profile.tipo == 'Chefe Imediato':
        print('AVALIAÇÃO do Chefe--------------')
        tipo_avalicao = 'Chefe Imediato'
        funcionario_avaliado.avaliacao_pendente = False

    else:
        if id_funcionario_usuario == id_funcionario:
            print('AVALIAÇÃO PRÓPRIA--------------')
            tipo_avalicao = 'Próprio'
            funcionario_avaliado.avaliacao_pendente_auto = False

        else:
            print('AVALIAÇÃO COLEGA --------------')
            tipo_avalicao = 'Colega'
            funcionario_avaliado.avaliacao_pendente_colega = False

    # obter a ultima avaliação por tipo de avaliador
    ultima_avaliacao = Avaliacao.objects.filter(
        funcionario=funcionario_avaliado,
        tipo_avaliador=tipo_avalicao).last()

    # print(ultima_avaliacao.query)
    print('ULTIMA AVALIACAO')
    print(ultima_avaliacao)

    if ultima_avaliacao:  # dados da ultima avaliacao que diz quando a avaliacao atual começa
        inicio_periodo = ultima_avaliacao.proxima_avaliacao
        fim_periodo = ultima_avaliacao.proxima_avaliacao + datetime.timedelta(180)
        periodo = inicio_periodo.strftime('%d/%m/%Y') + ' até ' + fim_periodo.strftime(
            '%d/%m/%Y')  # 'avaliacao.proxima_avaliacao Até avaliacao.proxima_avaliacao+121'
        periodo_avaliado = int(ultima_avaliacao.periodo_avaliado) + 1
        proxima_avaliacao = ultima_avaliacao.proxima_avaliacao + datetime.timedelta(
            181)  # 'avaliacao.proxima_avaliacao + 180' #tres meses após a de hoje
    else:
        fim_periodo = funcionario_avaliado.dt_inicio_exercicio + datetime.timedelta(180)
        periodo = funcionario_avaliado.dt_inicio_exercicio.strftime('%d/%m/%Y') + ' a ' \
                  + fim_periodo.strftime('%d/%m/%Y')  # 'periodo ingresso Até perido +120'
        periodo_avaliado = 1
        proxima_avaliacao = fim_periodo + datetime.timedelta(1)  # data de hoje +120

    avaliacao = avaliacao.objects.create(
        data=datetime.datetime.now(),
        tipo='Quadrimestral',
        tipo_avaliador=tipo_avalicao,
        media='0',
        periodo=periodo,
        periodo_avaliado=periodo_avaliado,
        proxima_avaliacao=proxima_avaliacao,
        avaliador=avaliador,
        funcionario=funcionario_avaliado,
    )

    medias_criterios, media_avaliacao = add_criterios(request, avaliacao)

    # print(medias_criterios)
    # print(media_avaliacao)

    avaliacao.media = media_avaliacao
    avaliacao.media_criterios = medias_criterios
    avaliacao.save(force_update=True)

    funcionario_avaliado.save(force_update=True)

    print(funcionario_avaliado)

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
            categoria='1. Assiduidade e Pontualidade',
            avaliacao=avaliacao
        )

        pontos_assiduidade += float(request.POST.get('pt_criterio' + str(item)))

    media_assiduidade = round(pontos_assiduidade / itens_assiduidade, 2)

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

    media_disciplina = round(pontos_disciplina / itens_disciplina, 2)

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

    media_iniciativa = round(pontos_iniciativa / itens_iniciativa, 2)

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

    media_produtividade = round(pontos_produtividade / itens_produtividade, 2)

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

    media_responsabilidade = round(pontos_responsabilidade / itens_responsabilidade, 2)

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

    media_cooperacao = round(pontos_cooperacao / itens_cooperacao, 2)

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

    media_dinamismo = round(pontos_dinamismo / itens_dinamismo, 2)

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

    media_adaptabilidade = round(pontos_adaptabilidade / itens_adaptabilidade, 2)

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

    media_urbanidade = round(pontos_urbanidade / itens_urbanidade, 2)

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

    media_relacoes = round(pontos_relacoes / itens_relacoes, 2)

    medias_criterios = [media_assiduidade, media_disciplina, media_iniciativa, media_produtividade,
                        media_responsabilidade, \
                        media_cooperacao, media_dinamismo, media_adaptabilidade, media_urbanidade, media_relacoes]

    media_avaliacao = round(sum(medias_criterios) / len(medias_criterios), 2)
    return medias_criterios, media_avaliacao


@login_required
def cad_avaliacao(request, id_funcionario):
    context = None

    logger.info('')

    if request.method == 'GET':
        funcionario = Funcionario
        funcionario = funcionario.objects.get(pk=id_funcionario)

        context = {'funcionario': funcionario, 'usuario': request.user}
        return render(request, 'form_cad_avaliacao.html', context)

    if request.method == 'POST':
        avaliacao = insert_avaliacao(request, id_funcionario)
        # insert_avaliacao(request, 3)

        return redirect('/resumo/avaliacao/' + str(avaliacao.pk))
        # resumo_avaliacao(request,avaliacao.pk)

        print(avaliacao)
        context = {'avaliacao': avaliacao, 'usuario': request.user}
        # return render(request,'resumo_avaliacao.html',context)


def logout(request):
    logout(request)
    return HttpResponseRedirect('')


@login_required()
def reativar_avaliacao(request, id_funcionario):
    if request.user.profile.tipo == 'Comissão':
        funcionario = Funcionario.objects.get(pk=id_funcionario)
        funcionario.ativo = True

        funcionario.save()

        avaliacao = Avaliacao.objects.filter(funcionario=funcionario).last()

        print(avaliacao)

        logger.info('')

        if avaliacao:
            proxima_avaliacao = datetime.datetime.now() + datetime.timedelta(91)
            avaliacao.proxima_avaliacao = proxima_avaliacao
            context = {
                'msg': 'Avaliação do Funcionário foi reativada e a data da proxima avaliação será ' + proxima_avaliacao.strftime(
                    '%d/%m/%Y')}

            return render(request, 'list_funcionarios.html', context=context)

        else:
            context = {'msg': 'Avaliação do Funcionário foi reativada.'}
            return render(request, 'list_funcionarios.html', context=context)

    return render(request, 'list_funcionarios.html')


@login_required()
def relatorio_avaliacao_criterios_por_avaliacao(request, id_funcionario, n_avaliacao):
    context = {'msg': 'Avaliação não pode ser exibida'}
    dados = []

    avaliacoes = Avaliacao.objects.filter(funcionario=id_funcionario, periodo_avaliado=n_avaliacao).all()

    criterios = Criterio.objects.filter(avaliacao=avaliacoes[1])

    print(criterios)

    for avaliacao in avaliacoes:
        avaliacao.media_criterios = ast.literal_eval(avaliacao.media_criterios)
        dados.append(avaliacao)

    dados_criterio = []

    for criterio in criterios:
        # if criterio.descricao == '1 - Comparece regularmente ao trabalho':
        # print('CAT 1 - Item A')
        # criterio.descricao = criterio.categoria+' - Critérios 1'

        dados_criterio.append(criterio)

    context = {'avaliacoes': dados, 'criterios': dados_criterio}

    return render(request, 'relatorio_avaliacao.html', context)


@login_required()
def relatorio_avaliacao_media_geral(request, id_funcionario=0, p_avaliacao=0, avaliador=0):
    context = {'msg': 'Avaliação não pode ser exibida'}
    dados = []

    user = request.user.profile
    if user.tipo == 'Comissão':

        tipo_avaliadores = ['Todos', 'Próprio', 'Chefe Imediato', 'Colega']

        avaliacoes = Avaliacao.objects.filter(funcionario__ativo=True).all().order_by('funcionario__nome',
                                                                                      'periodo_avaliado')

        if avaliador in range(1, 4):
            avaliacoes = avaliacoes.filter(tipo_avaliador=tipo_avaliadores[avaliador])

        if id_funcionario > 0:
            avaliacoes = Avaliacao.filter(funcionario=id_funcionario)

        if p_avaliacao > 0:
            avaliacoes = avaliacoes.filter(periodo_avaliado=p_avaliacao)

        for avaliacao in avaliacoes:
            avaliacao.media_criterios = ast.literal_eval(avaliacao.media_criterios)
            dados.append(avaliacao)

    context = {'avaliacoes': dados}

    return render(request, 'relatorio_avaliacao.html', context)


@login_required()
def resumo_avaliacao(request, id_avaliacao):
    context = {'msg': 'Avaliação não pode ser exibida'}
    avaliacao = Avaliacao.objects.get(pk=id_avaliacao)

    if request.user.profile.id == avaliacao.avaliador.id or request.user.profile.tipo == 'Comissão':
        criterios = Criterio.objects.filter(avaliacao=avaliacao)

        logger.info('')

        try:
            chefe = Funcionario.objects.get(
                Q(depto=avaliacao.funcionario.depto, cargo_comissionado="DIR. DEPARTAMENTO") | Q(
                    depto=avaliacao.funcionario.depto, cargo_comissionado="COORD. EXEC. DA ESCOLA DO LEGISLATIVO"))
            lista_medias_criterios = ast.literal_eval(avaliacao.media_criterios)
            context = {'usuario': request.user, 'avaliacao': avaliacao, 'criterios': criterios,
                       'media_criterios': lista_medias_criterios, 'chefe': chefe}
            return render(request, 'resumo_avaliacao.html', context)

        except Funcionario.DoesNotExist:
            return redirect('list_avaliados')


@login_required
def list_avaliados(request):
    funcionarios = Funcionario.objects.filter(Q(id=request.user.profile.funcionario.id))

    if request.user.profile.tipo == 'Comissão':

        funcionarios = Funcionario.objects.filter(avaliavel=True).order_by('ativo', 'nome')
    else:
        if request.user.profile.tipo == 'Chefe Imediato':
            funcionarios = Funcionario.objects.filter(
                Q(grupo_avaliacao=request.user.profile.funcionario.grupo_avaliacao, avaliavel=True, ativo=True,
                  avaliacao_pendente=True))
        else:
            if request.user.profile.tipo == 'Colega':
                funcionarios = Funcionario.objects.filter(
                    Q(subgrupo_avaliacao=request.user.profile.grupo_avaliado, avaliavel=True, ativo=True,
                      avaliacao_pendente_colega=True) | Q(
                        id=request.user.profile.funcionario.id, avaliavel=True, avaliacao_pendente_auto=True))

    context = {'funcionarios': funcionarios, 'usuario': request.user}

    logger.info('')

    return render(request, 'list_funcionarios.html', context)


def detalhes_avaliado(request, id_avaliado):
    funcionario = Funcionario.objects.get(pk=id_avaliado)

    usuario = request.user

    print(funcionario)
    context = {'funcionario': funcionario, 'usuario': usuario}

    logger.info('')

    return render(request, 'details_funcionario.html', context)


def entrar(request):
    context = {'msg': ''}

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        user = authenticate(username=usuario, password=senha)

        if (user is not None) and (user.profile.tipo == 'Colega'):
            if user.is_active:
                login(request, user)

                return redirect('/lista/avaliados')
            else:
                context = {'msg': 'Usuario não está ativo'}
        else:
            context = {'msg': 'Não foi possível logar'}

    logger.info('')

    return render(request, 'form_auth.html', context)


def entrar_token(request, token_id):
    context = {'msg': ''}

    logger.info('')

    if (request.method == 'GET') and token_id != '44sedf':

        context = {'msg': 'Não foi possível logar'}

        try:
            user = User.objects.get(profile__token=token_id)

        except Exception:
            return render(request, 'form_auth.html', context)

        print(user)

        if user is not None:
            login(request, user)

            return redirect('/lista/avaliados')

        else:
            context = {'msg': 'Não foi possível logar'}

    return render(request, 'form_auth.html', context)
