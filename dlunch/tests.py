# -*- coding: utf-8 -*- 
from django.test import TestCase
from models import Curso, Bolsa, Aluno
from models import Grupo, Mes, RefeicaoMensalDoGrupo, RefeicaoMensalDoAluno, RefeicaoEsgotada, Refeicao
from django.test.client import Client
from datetime import date
import urllib2


class AtribuicaoDeRefeicoes(TestCase):
    fixtures = ['dlunch.yaml']
    
    def setUp(self):        
        self.joao = Aluno.objects.get(nome="Joao",)
        self.zezin = Aluno.objects.get(nome="Zezin")
        self.refeicoes_por_mes_do_grupo = RefeicaoMensalDoGrupo.objects.get(quantidade=14)
        
    def test_atribuicao_de_refeicoes_ao_grupo(self):
        self.refeicoes_por_mes_do_grupo.atribuir_refeicoes_aos_alunos_do_grupo()

        refeicoes_restantes_joao = RefeicaoMensalDoAluno.objects.get(aluno__exact=self.joao).refeicoes_restantes
        
        refeicao_mensal_zezin = RefeicaoMensalDoAluno.objects.filter(aluno__exact=self.zezin) or None
        
        self.assertEquals(14, refeicoes_restantes_joao)
        self.assertEquals(None, refeicao_mensal_zezin)
        
    def test_reatribuicao_de_refeicoes_ao_grupo(self):
        self.refeicoes_por_mes_do_grupo.atribuir_refeicoes_aos_alunos_do_grupo()
        nova_refeicao_mensal_do_grupo = RefeicaoMensalDoGrupo(grupo=self.grupo_3, mes=self.mes_21_dias_uteis,quantidade=21)        
        nova_refeicao_mensal_do_grupo.atribuir_refeicoes_aos_alunos_do_grupo()
        
        refeicoes_mensal_joao = RefeicaoMensalDoAluno.objects.filter(aluno__exact=self.joao,
                                                                     mes=nova_refeicao_mensal_do_grupo.mes)
        
        self.assertEquals(1, len(refeicoes_mensal_joao))    
    
    
    

class DeducaoDeRefeicoes(AtribuicaoDeRefeicoes):
    def setUp(self):
        super(DeducaoDeRefeicoes, self).setUp()
        self.refeicoes_por_mes_do_grupo.atribuir_refeicoes_aos_alunos_do_grupo()

    def test_deducao_refeicao_do_aluno(self):        
        RefeicaoMensalDoAluno.deduzir_refeicao_do_aluno(self.joao, 'novembro', 2009)        
        refeicoes_restantes_joao = RefeicaoMensalDoAluno.objects.get(aluno__exact=self.joao).refeicoes_restantes
        self.assertEquals(refeicoes_restantes_joao, 13)

    def test_refeicao_esgotada(self):        
        refeicoes_restantes_joao = RefeicaoMensalDoAluno.objects.get(aluno__exact=self.joao)
        refeicoes_restantes_joao.refeicoes_restantes = 0
        refeicoes_restantes_joao.save()
        try:
            RefeicaoMensalDoAluno.deduzir_refeicao_do_aluno(self.joao, mes='novembro', ano=2009)
            self.fail('Nao pode existir refeicao negativa.')
        except RefeicaoEsgotada:
            pass

class ConsumirRefeicaoTestCase(AtribuicaoDeRefeicoes):
    def test_registro_de_refeicao(self):
        self.joao.consumir_refeicao()
        refeicao = Refeicao.objects.get(aluno=self.joao)
        self.assertEquals(date.today(), refeicao.data)
