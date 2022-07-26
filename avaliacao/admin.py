from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User

from avaliacao.models import Criterio, Avaliacao, Funcionario, Avaliador

admin.site.register(Criterio)
admin.site.register(Avaliacao)
admin.site.register(Funcionario)
admin.site.register(Avaliador)



class UserProfileInline(admin.TabularInline):
    model = Avaliador


class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
