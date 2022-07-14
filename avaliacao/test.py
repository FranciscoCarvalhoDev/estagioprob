from avaliacao.models import Criterio, Avaliacao, Funcionario

funcionario = Funcionario

f1 = funcionario.objects.create(dt_ingresso='2021-10-10',nome='Funcionario2',matricula='Mat010',cargo='Tecnico Informatica',depto='TI',funcao='Nenhuma',grupo='TI01',avaliavel='1')


av1 = funcionario.objects.create(dt_ingresso='2021-10-10',nome='Avaliador1',matricula='Mat0101',cargo='Tecnico Informatica',depto='TI',funcao='Chefe',grupo='TI01',avaliavel='0')

avaliacao = Avaliacao

avaliador = Funcionario.objects.get(pk=1)

av1 = avaliacao.objects.create(data='2022-10-12',tipo='Trimestral',nivel='Chefia',media='0',periodo='2022/1')

criterio = Criterio

criterio.objects.create(descricao='Chega no horário',nota='8',categoria='1. Assiduidade Pontualidade', avaliacao=av1)

funcionario_avaliado = Funcionario.objects.get(pk=2)
