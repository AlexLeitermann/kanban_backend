from django.contrib import admin
from kanban.models import Tasks

# Register your models here.
class TasksAdmin(admin.ModelAdmin):
    fields = ["title", "description", "color", "status", "created_at", "author", "members"]
    list_display = ["id", "title", "color", "status", "author"]

class ContactsAdmin(admin.ModelAdmin):
    fields = ["name", "initials", "email", "phone", "user"]
    list_display = ["id", "name", "email", "phone"]


admin.site.register(Tasks, TasksAdmin)