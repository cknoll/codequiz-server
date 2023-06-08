# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase

from builder import BuilderTextArea
from quiz.models import Task, TaskCollection, TC_Membership, QuizResult


class TC_MembershipInline(admin.TabularInline):
    """
    Helper class to represent one or a few TC_Memberships for each Task
    """
    model = TC_Membership
    extra = 1


class TC_MembershipSortableInline(SortableInlineAdminMixin, admin.TabularInline):
    """
    Helper class to represent many TC_Memberships for each TaskCollection.
    → This results in a widget which supports drag and drop for sorting.
    """
    model = TaskCollection.tasks.through

    extra = 1
    ordering = ("ordering",)
    fields = ("task", "title", "ordering")
    readonly_fields = ("title",)

    def title(self, obj):
        return str(obj.task.title)


class TaskAdminForm(forms.ModelForm):
    """
    Tell the form to use a fancy code editor instead of the plain text field.
    """
    pass

    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'body_data': BuilderTextArea()
        }


@admin.register(Task)
class TaskAdmin(SortableAdminBase, admin.ModelAdmin):
    """
    Setup for a nicer Task admin interface

    includes a filter by author, more meta data in the list view, hides unnecessary fields,
    replaces the text field element with a sophisticated code editor
    """

    inlines = (TC_MembershipInline,)

    def direct_link(self, obj):
        url = reverse('quiz_ns:explicit_task_view', kwargs={'task_id': obj.id})
        return mark_safe(
            f'<a href="{url}">Preview task {obj.id}</a>'
        )

    direct_link.short_description = "show task in front end view"

    list_display = ['id', 'title', 'pub_date', 'revision', 'direct_link']
    list_display_links = ['title']
    search_fields = ['title']
    date_hierarchy = 'pub_date'
    list_filter = ['author']

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



@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['date', 'hash']
    list_display_links = ['date', 'hash']


@admin.register(TaskCollection)
class TaskCollectionAdmin(SortableAdminBase, admin.ModelAdmin):

    inlines = (TC_MembershipSortableInline,)

    def direct_link(self, obj):
        url = reverse('quiz_ns:task_collection_view', kwargs={'tc_id': obj.id})
        return mark_safe(
            f'<a href="{url}">Run Collection {obj.id}</a>'
        )

    direct_link.short_description = "run task collection in front end view"

    list_display = ['id', 'title', 'num_tasks', 'direct_link']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['author']

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
