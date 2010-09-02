# -*- coding: utf-8 -*-
from django.contrib import admin

from dlunch.models import Aluno
from dlunch.models import Bolsa
from dlunch.models import Curso
from dlunch.models import RefeicaoMensalDoAluno
from dlunch.models import RefeicaoMensalDoGrupo
from dlunch.models import Mes, Grupo 


class AlunoAdmin(admin.ModelAdmin):
    ordering = ('nome',)
    list_display = ('matricula', 'nome', 'situacao', 'possui_digital')
    search_fields = ('matricula', 'nome',)
    list_filter = ('situacao',)
    filter_horizontal = ('curso',)
    list_per_page = 50
    exclude = ('impressao_digital', 'possui_digital')

admin.site.register(Aluno, AlunoAdmin)

class BolsaAdmin(admin.ModelAdmin):
    list_per_page = 50

admin.site.register(Bolsa)

class CursoAdmin(admin.ModelAdmin):
    list_per_page = 50

class RefeicaoAlunoAdmin(admin.ModelAdmin):
    search_fields = ('^aluno__nome',)

admin.site.register(Curso, CursoAdmin)
admin.site.register(RefeicaoMensalDoGrupo)
admin.site.register(RefeicaoMensalDoAluno, RefeicaoAlunoAdmin)
admin.site.register(Mes)
admin.site.register(Grupo)
