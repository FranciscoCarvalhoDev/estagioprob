from django.db import models


class Funcionario(models.Model):
    dt_ingresso = models.DateField()
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=255)
    cargo = models.CharField(max_length=100)
    depto = models.CharField(max_length=255)
    funcao = models.CharField(max_length=255)
    grupo = models.CharField(max_length=255)
    avaliavel = models.BooleanField()

    def __str__(self):
        return self.nome


NIVEL = [
    ('Chefia', 'Chefia'),
    ('Colega', 'Colega'),
    ('Própria', 'Própria'),

]

TIPO_AVALIACAO = [
    ('Trimestral', 'Trimestral'),
    ('Anual', 'Anual'),
]


class Avaliador(models.Model):
    TIPO_AVALIADOR = [
        ('Chefe', 'Chefe'),
        ('Colega', 'Colega'),
        ('Próprio', 'Próprio'),
    ]

    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, choices=TIPO_AVALIADOR)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='tipo_avaliadores')

    def __str__(self):
        return str(self.nome)+' - '+str(self.tipo)


class Avaliacao(models.Model):
    data = models.DateField()
    tipo = models.CharField(max_length=100, choices=TIPO_AVALIACAO)
    nivel = models.CharField(max_length=255, choices=NIVEL)
    media = models.CharField(max_length=100, null=True)
    periodo = models.CharField(max_length=255)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='avaliacao')
    avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE, related_name='avaliador')

    def __str__(self):
        return str(self.avaliador)+' - '+str(self.periodo)


# class avaliacaoFuncionario(models.Model):
#     funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='avaliacao_funcionario' )
#     avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='avaliacao_funcionario')
#

class Criterio(models.Model):

    CATEGORIA = [
        ('1. Assiduidade Pontualidade', '1. Assiduidade Pontualidade'),
        ('2. Disciplina', '2. Disciplina'),
        ('3. Capacidade de Iniciativa', '3. Capacidade de Iniciativa'),
        ('4. Produtividade', '4. Produtividade'),
        ('5. Responsabilidade', '5. Responsabilidade'),
    ]

    descricao = models.CharField(max_length=255)
    nota = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100, choices=CATEGORIA)
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='criterio_avaliacao')

    def __str__(self):
        return str(self.descricao)+' '+str(self.avaliacao.funcionario)