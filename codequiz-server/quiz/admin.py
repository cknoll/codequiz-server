# coding=utf-8
from django.contrib import admin
import django.forms as forms
from django.conf import settings

from quiz.models import Task, TaskCollection, TC_Membership


class TC_MembershipInline(admin.TabularInline):
    model = TC_Membership
    extra = 1
    ordering = ("ordering",)


class BehaveEditor(forms.Textarea):
    def __init__(self):
        attrs = {'class': 'behave'}
        super(BehaveEditor, self).__init__(attrs)

    class Media:
        css = {'all': (settings.STATIC_URL + 'behave/behave.css',)}
        js = (settings.STATIC_URL + 'behave/behave.js', settings.STATIC_URL + 'behave/replace.js', )


class TaskAdminForm(forms.ModelForm):
    pass

    class Meta:
        model = Task
        widgets = {
            'body_xml': BehaveEditor()
        }


class TaskAdmin(admin.ModelAdmin):
    #    list_display = ('question', 'pub_date', 'was_published_recently')
    #    list_filter = ['was_published_recently']

    search_fields = ['title', 'tags']
    date_hierarchy = 'pub_date'
    inlines = (TC_MembershipInline,)
    list_filter = ['author']

    fieldsets = [
        (None, {'fields': ['title', 'body_xml', 'tags']}),
        ('Date', {'fields': ['pub_date'],
                  'description': 'Wird automatisch auf aktuelle Zeit gesetzt, kann aber geändert werden',
                  'classes': ('collapse',)}),
        #('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    form = TaskAdminForm


class TaskCollectionAdmin(admin.ModelAdmin):
    inlines = (TC_MembershipInline,)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCollection, TaskCollectionAdmin)

