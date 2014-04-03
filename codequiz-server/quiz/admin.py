# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.core.urlresolvers import reverse

from builder import BuilderTextArea
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
            'body_data': BuilderTextArea()
        }


class TaskAdmin(admin.ModelAdmin):
    """
    Setup for a nicer Task admin interface

    includes a filter by author, more meta data in the list view, hides unnecessary fields,
    replaces the text field element with a sophisticated code editor
    """

    def direct_link(self, obj):
        return '<a href="' + reverse('quiz_ns:explicit_task_view', kwargs={'task_id': obj.id}) + '">Preview…</a>'

    direct_link.short_description = ''
    direct_link.allow_tags = True

    list_display = ['id', 'title', 'pub_date', 'revision', 'direct_link']
    list_display_links = ['title']
    search_fields = ['title']
    date_hierarchy = 'pub_date'
    inlines = (TC_MembershipInline,)
    list_filter = ['author', 'tags']

    fieldsets = [
        (None, {'fields': ['title', 'body_data', 'tags']}),
        ('Date', {'fields': ['pub_date'],
                  'description': 'Wird automatisch auf aktuelle Zeit gesetzt, kann aber geändert werden',
                  'classes': ('collapse',)}),
    ]

    # comment the following line in case of problems with Task Builder editor enhancement
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

    def direct_link(self, obj):
        return '<a href="' + reverse('quiz_ns:task_collection_view', kwargs={'tc_id': obj.id}) + '">Run Collection…</a>'

    direct_link.short_description = ''
    direct_link.allow_tags = True

    list_display = ['id', 'title', 'num_tasks', 'direct_link']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['author', 'tags']

    inlines = (TC_MembershipInline,)
    exclude = ('tasks',)

    fieldsets = [
        (None, {'fields': ['title', 'exam_mode', 'tags']}),
    ]

    def num_tasks(self, obj):
        return obj.tasks.count()

    num_tasks.short_description = "Number of tasks"

    def save_model(self, request, collection, form, change):
        """
        hooks into saving a collection to add/change some data automatically

        specifically, the author gets set to the logged in users name/username
        """
        if not collection.author:
            user = User.objects.get(username__exact=request.user)
            name = user.get_full_name()
            if not name:
                name = user.get_short_name()
                if not name:
                    name = user.get_username()

            collection.author = name
        collection.save()

    class Media:
        js = (
            "jquery/jquery-1.10.2.min.js",
            "jquery/jquery-ui-1.10.3.custom.min.js",
            "tasks/sortable-inline-admin.js",
        )


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCollection, TaskCollectionAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
