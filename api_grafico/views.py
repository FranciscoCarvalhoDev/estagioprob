from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
import ast
import pandas as pd
import numpy as np
from avaliacao.models import Avaliacao, Criterio


def _get_id_funcionario_por_acesso(request, id_funcionario):
    user = request.user.profile
    if user.tipo == 'Comissão':
        print('Permanece com o id fornecido')
        return id_funcionario
    else:
        print('Uso o proprio id')
        return user.id


@login_required()
def painel_desempenho(request, id_funcionario, ano_avaliado=0):
    context = {'msg': 'Avaliação não pode ser exibida'}
    template = 'form_auth.html'

    try:

        id_funcionario = _get_id_funcionario_por_acesso(request, id_funcionario)

        print(f'Id funcionario {id_funcionario}')

        avaliacao = Avaliacao.objects.filter(funcionario=id_funcionario, funcionario__avaliavel=True,
                                             funcionario__ativo=True).order_by('periodo_avaliado')
        if avaliacao:
            ultima_avaliacao = avaliacao.last()

            media_final_dos_anos = _get_media_geral_por_ano(avaliacao)

            print(media_final_dos_anos)

            if ultima_avaliacao:

                semestres_corridos = int(ultima_avaliacao.periodo_avaliado)
                semestres_abertos = semestres_corridos % 2

                anos_corridos = 0

                if semestres_abertos == 0:
                    anos_corridos = semestres_corridos / 2

                elif semestres_abertos > 0:
                    anos_corridos = semestres_corridos - 1

                anos_corridos = [ano + 1 for ano in range(int(anos_corridos))]

                context = {'avaliacao': ultima_avaliacao, 'ano_de_interesse': ano_avaliado,
                           'anos_corridos': anos_corridos,
                           'usuario': request.user, 'media_anos': media_final_dos_anos}

                if ano_avaliado == 0:
                    template = 'painel_desempenho.html'
                else:
                    template = 'painel_desempenho_ano.html'
    except:
        return render(request, 'form_auth.html')

    return render(request, template, context)


def _get_media_geral_por_ano(avaliacao):
    data = list(avaliacao.values())

    # print(data)

    df = pd.DataFrame(data)
    df['media'] = pd.to_numeric(df['media'], errors='coerce')

    # Função para mapear o período ao ano correspondente

    # Aplicar a função em cada linha do DataFrame para determinar o ano
    df['Ano'] = df['periodo_avaliado'].apply(_mapear_ano)

    # Agrupar por 'Ano' e calcular a média das avaliações (ou qualquer outra operação)
    df_agrupado = df.groupby('Ano').agg({
        'media': 'mean',  # Média das avaliações
        # Adicione outras colunas se necessário
    }).reset_index()

    # Exibir o DataFrame agrupado
    # print(df_agrupado)
    df_agrupado = df_agrupado.round(2)

    return df_agrupado['media']


def _mapear_ano(periodo):
    semestres_ano = {'1': [1, 2], '2': [3, 4], '3': [5, 6]}

    for ano, semestres in semestres_ano.items():
        if int(periodo) in semestres:
            return ano
    return None  # Caso o período não se encaixe em nenhum ano


@login_required()
# def relatorio_desempenho(request, id_funcionario):
#     dados = []
#     medias = []
#     tipo_avaliador = []
#
#     avaliacoes = Avaliacao.objects.filter(funcionario=id_funcionario, periodo_avaliado='1').all()
#     for avaliacao in avaliacoes:
#         avaliacao.media_criterios = ast.literal_eval(avaliacao.media_criterios)
#         dados.append(avaliacao)
#         medias_avaliacao = avaliacao.media_criterios
#         tipo_avaliador.append(avaliacao.tipo_avaliador)
#         medias.append(medias_avaliacao)
#
#     titulo = f' Média das categoria por avaliador na {avaliacao.periodo_avaliado}ª Avaliação'
#     labels = ['Assiduidade e Pontualidade', 'Disciplina', 'Capacidade de Iniciativa', 'Produtividade',
#               'Responsabilidade', 'Cooperação', 'Dinamismo', 'Adaptabilidade', 'Urbanidade', 'Relações Interpessoais']
#     json = {'labels': labels, 'data': medias_avaliacao, 'titulo': titulo, 'medias': medias,
#             'tipo_avaliador': tipo_avaliador}
#     return JsonResponse(json)

@login_required()
def relatorio_desempenho_anual_por_avaliador(request, id_funcionario, ano_avaliado=1):
    medias = []
    tipo_avaliador = []

    try:

        id_funcionario = _get_id_funcionario_por_acesso(request, id_funcionario)

        semestres_ano = {'1': [1, 2], '2': [3, 4], '3': [5, 6]}

        ano_de_interesse = semestres_ano[f'{ano_avaliado}']

        avaliacoes = Avaliacao.objects.filter(funcionario=id_funcionario,
                                              periodo_avaliado__in=ano_de_interesse).all().order_by('periodo_avaliado')

        avaliacoes_chefe = avaliacoes.filter(tipo_avaliador='Chefe Imediato')
        avaliacoes_colega = avaliacoes.filter(tipo_avaliador='Colega')
        avaliacoes_proprio = avaliacoes.filter(tipo_avaliador='Próprio')

        lista_chefe, media_chefe_do_periodo = _get_media_geral_do_ano(avaliacoes_chefe)
        lista_colega, media_colega_do_periodo = _get_media_geral_do_ano(avaliacoes_colega)
        lista_proprio, media_proprio_do_periodo = _get_media_geral_do_ano(avaliacoes_proprio)

        medias_no_ano_por_avaliador = {'chefe': media_chefe_do_periodo, 'colega': media_colega_do_periodo,
                                       'proprio': media_proprio_do_periodo}

        media_anual_geral = get_media_anual_geral(medias_no_ano_por_avaliador).tolist()

        titulo = f' Média das categoria por avaliador no {ano_avaliado}º ano de Avaliação'
        labels = ['Assiduidade e Pontualidade', 'Disciplina', 'Capacidade de Iniciativa', 'Produtividade',
                  'Responsabilidade', 'Cooperação', 'Dinamismo', 'Adaptabilidade', 'Urbanidade', 'Relações Interpessoais']
        json = {'labels': labels, 'medias_anual_chefe': media_chefe_do_periodo,
                'medias_anual_colega': media_colega_do_periodo, 'medias_anual_proprio': media_proprio_do_periodo,
                'titulo': titulo, 'medias': medias,
                'tipo_avaliador': tipo_avaliador, 'media_geral_ano': media_anual_geral}

    except:
        return render(request, 'form_auth.html')
    return JsonResponse(json)
def get_media_anual_geral(dict_medias_avaliadores):
    data = dict_medias_avaliadores

    # Criar o DataFrame
    df = pd.DataFrame(data)

    # Adicionar a coluna com a média das linhas
    df['media'] = df.mean(axis=1)

    df = df.round(2)

    return df['media']


def _get_media_geral_do_ano(avaliacoes):
    medias_semestrais_por_criterio = []
    notas_semestrais_por_criterio = []
    for criterio in range(0, 10):

        criterio_por_semestre = []
        for av in avaliacoes:
            lista_medias_da_avaliacao = ast.literal_eval(
                av.media_criterios)  # Obter a lista dos criterios na avaliação atual
            nota_do_criterio = lista_medias_da_avaliacao[criterio]  # Obter a nota do criterio x até 10
            criterio_por_semestre.append(
                nota_do_criterio)  # add a nota ao item correspondente ao criterio até compor a lista de semestre

        medias_semestrais_por_criterio.append(np.mean(criterio_por_semestre))
        notas_semestrais_por_criterio.append(criterio_por_semestre)

    return notas_semestrais_por_criterio, medias_semestrais_por_criterio


def desempenho_geral_semestre(request, id_funcionario):
    # Linha de evolução em todas as avaliações por semestre
    # periodo = []
    # media = []

    try:
        id_funcionario = _get_id_funcionario_por_acesso(request, id_funcionario)

        avaliacoes = Avaliacao.objects.filter(funcionario=id_funcionario).all().order_by('periodo_avaliado')

        avaliacoes_chefe = avaliacoes.filter(tipo_avaliador='Chefe Imediato')
        avaliacoes_colega = avaliacoes.filter(tipo_avaliador='Colega')
        avaliacoes_proprio = avaliacoes.filter(tipo_avaliador='Próprio')

        media = {
            'chefe': (_get_evolucao_semestral(avaliacoes_chefe)),
            'colega': (_get_evolucao_semestral(avaliacoes_colega)),
            'proprio': (_get_evolucao_semestral(avaliacoes_proprio)),

        }

        titulo = f'Evolução Geral por Semestre'
        labels = ['1º Semestre', '2º Semestre', '3º Semestre', '4º Semestre']
        json = {'labels': labels, 'data': media, 'titulo': titulo}
    except:
        return render(request, 'form_auth.html')

    return JsonResponse(json)


def _get_evolucao_semestral(avaliacoes_por_tipo):
    media_avaliacao = []

    for avaliacao in avaliacoes_por_tipo:
        media_avaliacao.append(avaliacao.media)
    return media_avaliacao


def _get_medias(avaliacoes, avaliador):
    avaliacoes = avaliacoes.filter(tipo_avaliador=avaliador)

    lista_criterios_em_cada_avaliacao = [ast.literal_eval(p.media_criterios) for p in avaliacoes]

    medias_criterio = []

    for criterio in range(0, 10):

        criterio_x_na_avaliacao_atual = []

        for avaliacao in lista_criterios_em_cada_avaliacao:  # São quatro avaliacoes
            criterio_x_na_avaliacao_atual.append(avaliacao[criterio])

        medias_criterio.append(criterio_x_na_avaliacao_atual)

    return medias_criterio, lista_criterios_em_cada_avaliacao


def _get_medias_dos_avaliadores_por_criterios_no_semestre(lista_chefe, lista_colega, lista_proprio,
                                                          sem_auto_avaliacao=False):
    # Para cada criterio, deve ser calculada a médias dos avaliadores no semestre

    medias = []
    for criterio in range(0, 10):

        notas_criterio = []
        for ava, dados in enumerate(lista_chefe):
            # Percorrendo as 4 avaliações
            notas_criterio_x = []
            # print(f'LISTA CHEFE {lista_chefe[ava]}')
            notas_criterio_x.append(lista_chefe[ava][criterio])

            # print(f'LISTA COLEGA {lista_colega[ava]}')
            notas_criterio_x.append(lista_colega[ava][criterio])

            if not sem_auto_avaliacao:
                # print(f'LISTA PROPRIO {lista_proprio[ava]}')
                notas_criterio_x.append(lista_proprio[ava][criterio])

            notas_criterio.append(np.mean(notas_criterio_x))

        medias.append(notas_criterio)

    print(f'array Notas do criterio 1 {notas_criterio}')

    return medias


def avaliacoes_por_semestre_avaliador(request, id_funcionario):
    # context = {'msg': 'Avaliação não pode ser exibida'}
    # dados = []

    try:

        id_funcionario = _get_id_funcionario_por_acesso(request, id_funcionario)

        avaliacoes = Avaliacao.objects.filter(funcionario=id_funcionario).all().order_by('periodo_avaliado')

        tipo_avaliador = ['Chefe Imediato', 'Próprio', 'Colega']

        lista_chefe = None
        lista_colega = None
        lista_proprio = None

        for avaliador in tipo_avaliador:
            medias_por_categorias, lista_criterio_por_avaliacao = _get_medias(avaliacoes, avaliador)

            if avaliador == 'Colega':
                lista_colega = medias_por_categorias
                lista_criterio_por_avaliacao_colega = lista_criterio_por_avaliacao

            if avaliador == 'Chefe Imediato':
                lista_chefe = medias_por_categorias
                lista_criterio_por_avaliacao_chefe = lista_criterio_por_avaliacao

            if avaliador == 'Próprio':
                lista_proprio = medias_por_categorias
                lista_criterio_por_avaliacao_proprio = lista_criterio_por_avaliacao

        media_avaliadores_criterios = _get_medias_dos_avaliadores_por_criterios_no_semestre(
            lista_criterio_por_avaliacao_chefe,
            lista_criterio_por_avaliacao_colega,
            lista_criterio_por_avaliacao_proprio)

        media_avaliadores_externos = _get_medias_dos_avaliadores_por_criterios_no_semestre(
            lista_criterio_por_avaliacao_chefe,
            lista_criterio_por_avaliacao_colega,
            lista_criterio_por_avaliacao_proprio, sem_auto_avaliacao=True)

        dados = {'criterios_chefe': lista_chefe, 'criterios_colega': lista_colega, 'criterios_proprio': lista_proprio,
                 'medias_criterios_avaliadores_avaliacao': media_avaliadores_criterios,
                 'media_avaliadores_externos': media_avaliadores_externos}
    except:
        return render(request, 'form_auth.html')

    return JsonResponse(dados, safe=False)
