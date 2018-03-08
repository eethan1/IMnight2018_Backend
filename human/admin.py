from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from human.models import Profile, Relationship
from human.chat.models import Message


class RelationshipInLine(admin.TabularInline):
    model = Relationship
    # the number of extra forms the formset will display in addition to the initial forms
    extra = 0
    exclude = ('created',)


class ClientInLine(RelationshipInLine):
    fk_name = 'client'
    verbose_name = "Performer"
    verbose_name_plural = "My Performer"


class PerformerInLine(RelationshipInLine):
    fk_name = 'performer'
    verbose_name = "Client"
    verbose_name_plural = "My Client"


class ProfileInLine(admin.StackedInline):
    model = Profile
    # there must exactly have one Profile link to one User
    can_delete = False
    # the number of extra forms the formset will display in addition to the initial forms
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInLine, ClientInLine, PerformerInLine,)


class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('label', 'client', 'performer')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'handle', 'message', 'timestamp')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(Message, MessageAdmin)
