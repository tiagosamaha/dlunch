from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from dlunch.forms import Relatorio, formatar_data

@staff_member_required
def relatorio(request):    
    if request.method == "GET":
        relatorio = Relatorio()
        return render_to_response("admin/dlunch/relatorio.html", {"form": relatorio})
    elif request.method == "POST":
        return gerar_relatorio_simples(request)
    
    
def gerar_relatorio_simples(request):
    assert request.method == 'POST'
    relatorio = Relatorio(request.POST)
    if relatorio.is_valid():        
        context = {}
        context['data_inicial'] = formatar_data(relatorio.data['data_inicial'])
        context['data_final'] = formatar_data(relatorio.data['data_final'])
        context['total_de_refeicoes'] = relatorio.total_de_refeicoes()
        return render_to_response("admin/dlunch/relatorio.html", context)
    else:
        return render_to_response("admin/dlunch/relatorio.html", {"form": relatorio})

        
