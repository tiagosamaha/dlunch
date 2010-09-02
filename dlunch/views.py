def index(request):
    """Interface inicial do sistema para cadastro de alunos, bolsas e cursos"""
    if request.user.is_superuser:
        return HttpResponseRedirect("/admin/")
