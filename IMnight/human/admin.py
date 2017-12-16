from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Relationship


class RelationshipInLine(admin.StackedInline):
    model = Relationship
    extra = 0
    exclude = ['created']


class ClientInLine(RelationshipInLine):
    fk_name = 'client'


class PerformerInLine(RelationshipInLine):
    fk_name = 'performer'


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class UserAdmin(UserAdmin):
    inlines = (ProfileInLine, ClientInLine, PerformerInLine,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Relationship)
