from django.contrib.auth.models import User
from django.db import models

DEPARTAMENTOS = [
    ('DEPARTAMENTO DE INFRAESTRUTURA', 'DEPARTAMENTO DE INFRAESTRUTURA'),
    ('DEPARTAMENTO DE RECURSOS HUMANOS', 'DEPARTAMENTO DE RECURSOS HUMANOS'),
    ('DEPARTAMENTO DE COMUNICAÇÃO', 'DEPARTAMENTO DE COMUNICAÇÃO'),
    ('DEPARTAMENTO ADMINISTRATIVO', 'DEPARTAMENTO ADMINISTRATIVO'),
    ('DEPARTAMENTO DE CERIMONIAL', 'DEPARTAMENTO DE CERIMONIAL'),
    ('ESCOLA DO LEGISLATIVO', 'ESCOLA DO LEGISLATIVO'),
    ('DEPARTAMENTO LEGISLATIVO', 'DEPARTAMENTO LEGISLATIVO'),
    ('DEPARTAMENTO DE TEC. DA INFORMAÇÃO', 'DEPARTAMENTO DE TEC. DA INFORMAÇÃO'),
    ('DEPARTAMENTO JURIDÍCO', 'DEPARTAMENTO JURIDÍCO'),
    ('DEPARTAMENTO DE CONTROLE INTERNO', 'DEPARTAMENTO DE CONTROLE INTERNO'),

]

class Funcionario(models.Model):
    dt_admissao = models.DateField(default='2022-03-10')
    dt_inicio_exercicio = models.DateField(default='2022-03-10', help_text="Data Inicio efetivo para contagem do periodo probatório")
    dt_posse = models.DateField(default='2022-03-10')
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=100)
    cargo_efetivo = models.CharField(max_length=100)
    cargo_comissionado = models.CharField(max_length=100, default='Nenhum')
    depto = models.CharField(max_length=255, choices=DEPARTAMENTOS)
    funcao = models.CharField(max_length=255, default="Nenhuma")
   # periodos_avaliados = models.CharField(max_length=2, default=0)
    grupo_avaliacao = models.CharField(max_length=255, help_text="Grupo de funcionarios a ser avaliados por um Chefe Imediato")
    subgrupo_avaliacao = models.CharField(max_length=255, help_text="Grupo para avaliação do colega")
    avaliavel = models.BooleanField(default=True)
    ativo = models.BooleanField(default=True)
    avaliacao_pendente = models.BooleanField(default=True)
    avaliacao_pendente_colega = models.BooleanField(default=True)
    avaliacao_pendente_auto = models.BooleanField(default=True)


    def __str__(self):
        return self.nome


class Avaliador(models.Model):
    TIPO_AVALIADOR = [
        ('Chefe Imediato', 'Chefe Imediato'),
        ('Colega', 'Colega'),
        ('Próprio', 'Próprio'),
        ('Comissão', 'Comissão'),

    ]

    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, choices=TIPO_AVALIADOR)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='tipo_avaliadores')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    grupo_avaliado = models.CharField(max_length=255)
    token = models.CharField(max_length=40, default='44sedf')

    def __str__(self):
        return str(self.nome)+' - '+str(self.tipo)


class Avaliacao(models.Model):
    TIPO_AVALIACAO = [
        ('Quadrimestral', 'Quadrimestral'),
        ('Trimestral', 'Trimestral'),
        ('Anual', 'Anual'),
    ]

    NIVEL = [
        ('Chefe Imediato', 'Chefe Imediato'),
        ('Colega', 'Colega'),
        ('Próprio', 'Próprio'),

    ]

    data = models.DateField()
    tipo = models.CharField(max_length=100, choices=TIPO_AVALIACAO)
    tipo_avaliador = models.CharField(max_length=255, choices=NIVEL, help_text="Realizado por Chefe, Colega ou pelo proprio funcionario ")
    media = models.CharField(max_length=5, null=True)
    media_criterios = models.CharField(max_length=255, null=True)
    periodo = models.CharField(max_length=50, help_text="Periodo avaliado")
    periodo_avaliado = models.CharField(max_length=2, default=0, help_text="Trimestre a que se refere. Contador do estado atual da avaliação")
    proxima_avaliacao = models.DateField()
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='avaliacao')
    avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE, related_name='avaliador')

    def __str__(self):
        return str(self.funcionario.nome)+' - Avaliador: '+str(self.avaliador.nome)\
               +' - Trimestre '+str(self.periodo_avaliado)+'('+str(self.periodo)+')'


class Criterio(models.Model):

    CATEGORIA = [
        ('1. Assiduidade e Pontualidade', '1. Assiduidade e Pontualidade'),
        ('2. Disciplina', '2. Disciplina'),
        ('3. Capacidade de Iniciativa', '3. Capacidade de Iniciativa'),
        ('4. Produtividade', '4. Produtividade'),
        ('5. Responsabilidade', '5. Responsabilidade'),
        ('6. Cooperação', '6. Cooperação'),
        ('7. Dinamismo', '7. Dinamismo'),
        ('8. Adaptabilidade', '8. Adaptabilidade'),
        ('9. Urbanidade', '9. Urbanidade'),
        ('10. Relações Interpessoais', '10. Relações Interpessoais'),
    ]

    descricao = models.CharField(max_length=255)
    nota = models.CharField(max_length=3)
    categoria = models.CharField(max_length=100, choices=CATEGORIA)
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='criterio_avaliacao')

    def __str__(self):
        return str(self.descricao)+' '+str(self.avaliacao.funcionario)