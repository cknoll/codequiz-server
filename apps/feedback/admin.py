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
    list_display = ['date', 'task_name', 'feedback_text', 'answered']
    list_display_links = ['task_name', 'feedback_text']

    # Spans lookup into relation task --> task.author
    # :DOC: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ('task__author', TaskFilter, 'answered')
    ordering = ['-date']

    def task_name(self, obj):
        return '%s' % obj.task.title

    def feedback_text(self, obj):
        feedback_lines = obj.text.splitlines()
        dots = ""
        if len(feedback_lines) > 1:
            dots = " ..."
        return '%s' % feedback_lines[0] + dots

    def show_email(self, obj):
        if obj.email:
            url = obj.email
            subject = "Regarding your Feedback on Task \"%s\"" % obj.task.title
            body = "\n" + str(obj.date) + "\n\n" + obj.text
            body = body.replace("\n", "%0D%0A> ")
            body = "\n" + body
            body = body.replace("\n", "%0D%0A")
            return "<a href='mailto:{url}?subject={subject}&body={body}'>{url}</a>".format(url=url,
                                                                                            subject=subject,
                                                                                            body=body)
        else:
            return ""
    show_email.allow_tags = True
    show_email.short_description = 'Email'

    task_name.short_description = 'Task'
    task_name.admin_order_field = 'task__title'  # To enable ordering by custom field that has no model/DB field

    feedback_text.short_description = 'Feedback'

    #fields = ['text']
    fieldsets = [
        (None, {'fields': ['show_email', 'text', 'answered']}),
    ]
    readonly_fields = ('show_email', 'text')

admin.site.register(Feedback, FeedbackAdmin)
