from django.conf.urls.defaults import *
from handlers import RefeicaoManager, AlunoManager, LoginHandler
from piston.resource import Resource


refeicao_manager = Resource(RefeicaoManager)
aluno_manager = Resource(AlunoManager)
login = Resource(LoginHandler)

urlpatterns = patterns('',
    (r'aluno/(?P<matricula>.+)$', aluno_manager, {'emitter_format': 'json'}),
    (r'deduzir_refeicao/(?P<matricula>.+)$', refeicao_manager),
    (r'saldo/(?P<matricula>.+)$', refeicao_manager),
    (r'atualizar_digital/(?P<matricula>.+)$', aluno_manager),
    (r'login/$', login),
    )
