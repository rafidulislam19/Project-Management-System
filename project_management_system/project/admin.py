from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Task, File, Team, User

# admin.site.register(Project)
# admin.site.register(Task)
# admin.site.register(File)
# admin.site.register(Team)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'is_manager', 'is_hod', 'team')
