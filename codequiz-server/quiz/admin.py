# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.conf.urls import *
import admin_views as views

from django import forms
from django_ace import AceWidget

from quiz.models import Task, TaskCollection, TC_Membership


class TC_MembershipInline(admin.TabularInline):
    model = TC_Membership
    extra = 1
    ordering = ("ordering",)


class TaskAdminForm(forms.ModelForm):
    """
    Tell the form to use a fancy code editor instead of the plain text field.
    """
    pass

    class Meta:
        model = Task
        widgets = {
            'body_xml': AceWidget(mode="xml", theme="solarized_light", width="100%")
        }


class TaskAdmin(admin.ModelAdmin):
    """
    Setup for a nicer Task admin interface

    includes a filter by author, more meta data in the list view, hides unnecessary fields,
    replaces the text field element with a sophisticated code editor
    """
    add_form_template = "admin/admin_add_view.html"
    change_form_template = "admin/admin_change_view.html"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        #extra_context['osm_data'] = self.get_osm_info()
        extra_context['task'] = Task.objects.get(id=object_id)
        return super(TaskAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    #def add_view(self, request):
    #    # View for an add request
    #    return views.admin_add_view(request, self)
    #
    #def change_view(self, request, taskid):
    #    # View for a change request
    #    return views.admin_change_view(request, self, taskid)
    #
    #def get_urls(self):
    #    print("oooooooooh")
    #    urls = super(TaskAdmin, self).get_urls()
    #    my_urls = patterns('',
    #                       ('^(?P<taskid>\d+)/$', self.change_view),
    #                       ('^add/$', self.add_view))
    #    return my_urls + urls


class TaskCollectionAdmin(admin.ModelAdmin):
    inlines = (TC_MembershipInline,)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCollection, TaskCollectionAdmin)

