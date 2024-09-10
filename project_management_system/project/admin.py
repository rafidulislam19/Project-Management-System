from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Team, User, ProjectFile
from task.models import Task

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(ProjectFile)
admin.site.register(Team)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_manager', 'is_hod', 'team')
