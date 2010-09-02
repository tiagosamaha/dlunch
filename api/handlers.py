from django.contrib.admin.models import LogEntry
from piston.handler import BaseHandler
from piston.authentication import HttpBasicAuthentication
from dlunch.models import Aluno, RefeicaoMensalDoAluno, Mes, Refeicao
from dlunch.models import RefeicaoEsgotada
from django.http import HttpResponseForbidden, HttpResponseNotFound
import psycopg2
import datetime

ANO_LETIVO = 2010

def buscar_aluno(matricula):
    try:
        aluno = Aluno.objects.get(matricula=matricula)
        return aluno
    except Aluno.DoesNotExist:
        return None


    def read(self, request, matricula):        
        return buscar_aluno(matricula)

def mes_corrente():
    mes_atual = datetime.datetime.now().month
    return Mes.MESES_DO_ANO[mes_atual-1][0]

def aluno_nao_comeu(aluno):
    hoje = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        Refeicao.objects.get(aluno=aluno, data=hoje)
        return False
    except:
        return True

class LoginHandler(BaseHandler):
    allowed_methods = ('GET',)
    
    def read(self, request):
        basic_authentication = HttpBasicAuthentication()
        if not basic_authentication.is_authenticated(request):
            return basic_authentication.challenge()

class RefeicaoManager(BaseHandler):
    allowed_methods = ('PUT','GET')
    
    def read(self, request, matricula):
        aluno = buscar_aluno(matricula)
        mes = Mes.objects.get(mes__exact=mes_corrente())
        return RefeicaoMensalDoAluno.objects.get(aluno=aluno,mes=mes)

    def update(self, request, matricula):
        aluno = buscar_aluno(matricula)
        basic_authentication = HttpBasicAuthentication()
        if not basic_authentication.is_authenticated(request):
            return basic_authentication.challenge()
        if aluno != None:
            if aluno_nao_comeu(aluno):
                try:
                    RefeicaoMensalDoAluno.deduzir_refeicao_do_aluno(aluno, mes_corrente(), ANO_LETIVO)
                    aluno.consumir_refeicao()
                except RefeicaoEsgotada:
                    return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()

class AlunoManager(BaseHandler):
    allowed_methods = ('PUT', 'GET')
    model = Aluno
    
    def read(self, request, matricula):        
        return buscar_aluno(matricula)

    def update(self, request, matricula):
        aluno = buscar_aluno(matricula)
        impressao_digital = request.data.get('digital', None)
        if aluno is not None and impressao_digital is not None:
            basic_authentication = HttpBasicAuthentication()
            if not basic_authentication.is_authenticated(request):
                return basic_authentication.challenge()
            aluno.set_impressao_digital(psycopg2.Binary(str(impressao_digital)))
            
            
