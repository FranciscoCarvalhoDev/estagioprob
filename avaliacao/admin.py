from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User

from avaliacao.models import Criterio, Avaliacao, Funcionario, Avaliador


class AvaliadorAdmin(admin.ModelAdmin):
    list_display = ('nome','tipo','grupo_avaliado',)
    list_filter = ('tipo','grupo_avaliado',)

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cargo_efetivo', 'grupo_avaliacao', 'subgrupo_avaliacao', 'cargo_comissionado')
    list_filter = ( 'avaliavel', 'cargo_comissionado', 'grupo_avaliacao', 'subgrupo_avaliacao', 'ativo', 'avaliacao_pendente')



admin.site.register(Criterio)
admin.site.register(Avaliacao)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Avaliador, AvaliadorAdmin)



class UserProfileInline(admin.TabularInline):
    model = Avaliador


class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline,)





admin.site.unregister(User)
admin.site.register(User, UserAdmin)
