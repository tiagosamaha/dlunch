# -*- coding: utf-8 -*-
from django.db import models
from fieldtypes import PostgresBinaryField


class RefeicaoEsgotada(Exception):
    pass

class Curso(models.Model):
    NIVEIS = (('medio', 'Médio'),
              ('tecnico', 'Técnico'),
              ('superior', 'Superior'),
             )

    nome = models.CharField(max_length=50)
    nivel = models.CharField(max_length=20, choices=NIVEIS)
    instituicao = models.CharField(max_length=100, default='IFF Campos') 
    
    def __unicode__(self):
        return self.nome

class Refeicao(models.Model):
    class Meta:
        verbose_name_plural = u"Refeições"
        verbose_name = u"Refeição"

    data = models.DateField(auto_now_add=True)
    aluno = models.ForeignKey('Aluno')

class Aluno(models.Model):
    SITUACOES = (('ativo', 'Ativo'),
                 ('inativo', 'Inativo'),
                )
    
    nome = models.CharField(max_length=100)
    matricula = models.IntegerField("Matrícula", unique=True)
    situacao = models.CharField("Situação", max_length="10", \
            choices=SITUACOES, default=u'ativo')
    curso = models.ManyToManyField('Curso', blank=True, null=True)
    bolsa = models.ForeignKey('Bolsa', blank=True, null=True)
    grupo = models.ForeignKey('Grupo')
    possui_digital = models.BooleanField('Impressão digital cadastrada?', default=False)
    impressao_digital = PostgresBinaryField(blank=True, null=True)
    

    def set_impressao_digital(self, impressao):
        self.impressao_digital = impressao
        self.possui_digital = True
        self.save()

    def consumir_refeicao(self):
        Refeicao.objects.create(aluno=self)
    
    def __unicode__(self):
        return self.nome
    

class Bolsa(models.Model):
    tipo = models.CharField(max_length=50)

    def __unicode__(self):
        return self.tipo
    
class Grupo(models.Model):
    REFEICOES_SEMANAIS = ((1, 1),
                          (2, 2),
                          (3, 3),
                          (4, 4),
                          (5, 5))
    
    refeicoes_por_semana = models.IntegerField('Refeições por semana',choices=REFEICOES_SEMANAIS)
    
    def __unicode__(self):
        return u"%s refeição(ões) semanal(is)" %self.refeicoes_por_semana
        
class Mes(models.Model):
    class Meta:
        verbose_name_plural = "Meses"
        verbose_name = "Mês"
        
    MESES_DO_ANO = (('janeiro', 'Janeiro'),
                    ('fevereiro', 'Fevereiro'),
                    ('marco', 'Março'),
                    ('abril', 'Abril'),
                    ('maio', 'Maio'),
                    ('junho', 'Junho'),
                    ('julho', 'Julho'),
                    ('agosto', 'Agosto'),
                    ('setembro', 'Setembro'),
                    ('outubro', 'Outubro'),
                    ('novembro', 'Novembro'),
                    ('dezembro', 'Dezembro'), )
    
    mes = models.CharField('Mês', choices=MESES_DO_ANO, max_length=15)
    ano = models.IntegerField('Ano Letivo')
    
    def __unicode__(self):
        return "%s / %s" %(self.mes, self.ano)
    
class RefeicaoMensalDoAluno(models.Model):
    class Meta:
        verbose_name_plural = "Refeições mensais do aluno"
        verbose_name = "Refeição mensal do aluno"
        
    mes = models.ForeignKey('Mes')
    aluno  = models.ForeignKey('Aluno')    
    refeicoes_restantes = models.IntegerField('Refeições restantes')
    
    @classmethod
    def deduzir_refeicao_do_aluno(cls, aluno, mes, ano):        
        mes_letivo = Mes.objects.get(ano=ano, mes=mes)
        refeicao_mensal = cls.objects.get(aluno=aluno, mes=mes_letivo)
        if refeicao_mensal.refeicoes_restantes == 0:
            raise RefeicaoEsgotada
        refeicao_mensal.refeicoes_restantes -= 1
        refeicao_mensal.save()
    
    def __unicode__(self):
        return u"%s com %d refeições restantes em %s" %(self.aluno.nome, self.refeicoes_restantes, self.mes)

    
class RefeicaoMensalDoGrupo(models.Model):
    class Meta:
        verbose_name_plural = "Refeições mensais do grupo"
        verbose_name = "Refeição mensal do grupo"
        
    mes = models.ForeignKey('Mes')
    grupo = models.ForeignKey('Grupo')
    quantidade = models.IntegerField('Quantidade de Refeições')
    
        
    def atribuir_refeicoes_aos_alunos_do_grupo(self):
        for aluno in Aluno.objects.filter(grupo=self.grupo):
            if aluno.situacao == 'ativo':
                RefeicaoMensalDoAluno.objects.filter(aluno=aluno, mes=self.mes).delete()
                RefeicaoMensalDoAluno.objects.create(aluno=aluno, mes=self.mes,
                                                     refeicoes_restantes=self.quantidade)
                
    def save(self, force_insert=False, force_update=False, commit=True):
        super(RefeicaoMensalDoGrupo, self).save()
        self.atribuir_refeicoes_aos_alunos_do_grupo()

    def __unicode__(self):
        return u"Grupo de %s com direito a %s refeições em %s" %(self.grupo,
                self.quantidade, self.mes)
    
            
    
