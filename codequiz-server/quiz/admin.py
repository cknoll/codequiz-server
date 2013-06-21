from django.contrib import admin
from quiz.models import Task



class TaskAdmin(admin.ModelAdmin):
#    list_display = ('question', 'pub_date', 'was_published_recently')
#    list_filter = ['was_published_recently']
    search_fields = ['title', 'tag_list']
    date_hierarchy = 'pub_date'
#    fieldsets = [
#        (None,               {'fields': ['question']}),
#        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#    ]
#    
#    inlines = [ChoiceInline]
    

admin.site.register(Task, TaskAdmin)
