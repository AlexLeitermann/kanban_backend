from django.contrib import admin
from kanban.models import Tasks, Contacts

# Register your models here.
class TasksAdmin(admin.ModelAdmin):
    fields = ["title", "description", "color", "status", "created_at", "author", "priority"]
    # list_display = ["id", "title", "color", "status", "priority", "author"]

class ContactsAdmin(admin.ModelAdmin):
    fields = ["name", "initials", "email", "phone", "user"]
    # list_display = ["id", "name", "email", "phone"]


admin.site.register(Tasks, TasksAdmin)
admin.site.register(Contacts, ContactsAdmin)