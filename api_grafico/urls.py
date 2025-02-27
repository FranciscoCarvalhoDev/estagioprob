from django.urls import path
from api_grafico.views import painel_desempenho, desempenho_geral_semestre, avaliacoes_por_semestre_avaliador, \
    relatorio_desempenho_anual_por_avaliador

urlpatterns = [
    path('painel/desempenho/<int:id_funcionario>/ano/<int:ano_avaliado>',
         painel_desempenho, name='painel_desempenho'),

    # path('desempenho/<int:id_funcionario>/geral/',
    # relatorio_desempenho, name='api_relatorio_desempenho'),

    path('desempenho/<int:id_funcionario>/anual/<int:ano_avaliado>',
         relatorio_desempenho_anual_por_avaliador, name='api_relatorio_desempenho_anual'),

    path('desempenho/<int:id_funcionario>/semestre',
         desempenho_geral_semestre, name='api_desempenho_semestre'),
    path('desempenho/<int:id_funcionario>/semestre/avaliador',
         avaliacoes_por_semestre_avaliador, name='api_desempenho_semestre'),
]
