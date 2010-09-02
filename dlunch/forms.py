#coding: utf-8

import datetime
from django import forms
from models import Refeicao
from django.contrib.admin import widgets

def formatar_data(data):
        data_formatada = data[8:] + data[4:8] + data[0:4]
        return data_formatada.replace("-", "/")

class Relatorio(forms.Form):
    data_inicial = forms.DateField()
    data_final = forms.DateField()
    
    def __init__(self, *args, **kwargs):
        super(Relatorio, self).__init__(*args, **kwargs)
        self.fields['data_inicial'].widget = widgets.AdminDateWidget()
        self.fields['data_final'].widget = widgets.AdminDateWidget()       
    
    
    def total_de_refeicoes(self):
        return len(Refeicao.objects.filter(data__gte=self.data['data_inicial'],
                                           data__lte=self.data['data_final']))
