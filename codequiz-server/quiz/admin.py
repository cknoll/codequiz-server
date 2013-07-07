from django.contrib import admin
from quiz.models import Task, TaskCollection, TC_Membership



class TC_MembershipInline(admin.TabularInline):
    model = TC_Membership
    extra = 1
    ordering = ("ordering",)


class TaskAdmin(admin.ModelAdmin):
#    list_display = ('question', 'pub_date', 'was_published_recently')
#    list_filter = ['was_published_recently']
    search_fields = ['title', 'tag_list']
    date_hierarchy = 'pub_date'
    inlines = (TC_MembershipInline,)
#    fieldsets = [
#        (None,               {'fields': ['question']}),
#        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#    ]
#
#    inlines = [ChoiceInline]

class TaskCollectionAdmin(admin.ModelAdmin):
    inlines = (TC_MembershipInline,)

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCollection, TaskCollectionAdmin)

