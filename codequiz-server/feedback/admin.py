from django.contrib import admin
from feedback.models import Feedback
from django.contrib.admin import SimpleListFilter


class TaskFilter(SimpleListFilter):
    """
    Filter for ForeignKey "Task"

    To be able to show just the referenced keys in the filter list.
    :DOC: http://stackoverflow.com/questions/12215751/can-i-make-list-filter-in-django-admin-to-only-show-referenced-foreignkeys
    """
    title = 'Task'
    parameter_name = 'task'

    def lookups(self, request, model_admin):
        tasks = set([t.task for t in model_admin.model.objects.all()])
        return [(t.id, t.title) for t in tasks]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(task__id__exact=self.value())
        else:
            return queryset


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['date', 'task_name', 'feedback_text']
    list_display_links = ['task_name', 'feedback_text']

    # Spans lookup into relation task --> task.author
    # :DOC: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ('task__author', TaskFilter)
    ordering = ['-date']

    def task_name(self, obj):
        return '%s' % obj.task.title

    def feedback_text(self, obj):
        feedback_lines = obj.text.splitlines()
        dots = ""
        if len(feedback_lines) > 1:
            dots = " ..."
        return '%s' % feedback_lines[0] + dots

    task_name.short_description = 'Task'
    task_name.admin_order_field = 'task__title'  # To enable ordering by custom field that has no model/DB field

    feedback_text.short_description = 'Feedback'

admin.site.register(Feedback, FeedbackAdmin)




# vim: et sw=4 sts=4
