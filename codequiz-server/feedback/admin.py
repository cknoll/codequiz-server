from django.contrib import admin
from feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_name', 'feedback_text']
    list_display_links = ['task_name', 'feedback_text']

    # Spans lookup into relation task --> task.author
    # :DOC: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ['task__author']


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
