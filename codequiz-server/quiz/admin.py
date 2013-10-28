# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User

from django import forms
from django_ace import AceWidget

from quiz.models import Task, TaskCollection, TC_Membership, QuizResult


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
    list_display = ['id', 'title', 'pub_date', 'revision']
    list_display_links = ['title']
    search_fields = ['title', 'tags']
    date_hierarchy = 'pub_date'
    inlines = (TC_MembershipInline,)
    list_filter = ['author']

    fieldsets = [
        (None, {'fields': ['title', 'body_xml', 'tags']}),
        ('Date', {'fields': ['pub_date'],
                  'description': 'Wird automatisch auf aktuelle Zeit gesetzt, kann aber geändert werden',
                  'classes': ('collapse',)}),
    ]

    # comment the following line in case of problems with Java-Script editor enhancement
    form = TaskAdminForm

    def save_model(self, request, task, form, change):
        """
        hooks into saving a task to add/change some data automatically

        specifically, the author gets set to the logged in users name/username
        and the tasks revision is incremented
        """
        if not task.author:
            user = User.objects.get(username__exact=request.user)
            name = user.get_full_name()
            if not name:
                name = user.get_short_name()
                if not name:
                    name = user.get_username()

            task.author = name
        task.revision += 1
        task.save()


class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['date', 'hash']
    list_display_links = ['date', 'hash']

class TaskCollectionAdmin(admin.ModelAdmin):
    inlines = (TC_MembershipInline,)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCollection, TaskCollectionAdmin)
admin.site.register(QuizResult, QuizResultAdmin)