from django.contrib.auth.models import User
from django.db import models


class Funcionario(models.Model):
    dt_ingresso = models.DateField()
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=255)
    cargo = models.CharField(max_length=100)
    depto = models.CharField(max_length=255)
    funcao = models.CharField(max_length=255)
    grupo_avaliacao = models.CharField(max_length=255, help_text="Grupo de funcionarios a ser avaliados por um Chefe Imediato")
    subgrupo_avaliacao = models.CharField(max_length=255, help_text="Grupo para avaliação do colega")
    avaliavel = models.BooleanField()

    def __str__(self):
        return self.nome


class Avaliador(models.Model):
    TIPO_AVALIADOR = [
        ('Chefe', 'Chefe'),
        ('Colega', 'Colega'),
        ('Próprio', 'Próprio'),
    ]

    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, choices=TIPO_AVALIADOR)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='tipo_avaliadores')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    grupo_avaliado = models.CharField(max_length=255)

    def __str__(self):
        return str(self.nome)+' - '+str(self.tipo)


class Avaliacao(models.Model):
    TIPO_AVALIACAO = [
        ('Trimestral', 'Trimestral'),
        ('Anual', 'Anual'),
    ]

    NIVEL = [
        ('Chefia', 'Chefia'),
        ('Colega', 'Colega'),
        ('Própria', 'Própria'),

    ]

    data = models.DateField()
    tipo = models.CharField(max_length=100, choices=TIPO_AVALIACAO)
    tipo_avaliador = models.CharField(max_length=255, choices=NIVEL, help_text="Realizado por Chefe, Colega ou pelo proprio funcionario ")
    media = models.CharField(max_length=100, null=True)
    media_criterios = models.CharField(max_length=255, null=True)
    periodo = models.CharField(max_length=255, help_text="Periodo avaliado")
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='avaliacao')
    avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE, related_name='avaliador')

    def __str__(self):
        return str(self.avaliador)+' - '+str(self.periodo)


class Criterio(models.Model):

    CATEGORIA = [
        ('1. Assiduidade Pontualidade', '1. Assiduidade Pontualidade'),
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
    nota = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100, choices=CATEGORIA)
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='criterio_avaliacao')

    def __str__(self):
        return str(self.descricao)+' '+str(self.avaliacao.funcionario)