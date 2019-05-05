from django.contrib import admin
from todolist.models import Todo
# from import_export import resources
# Register your models here.

#admin.site.register(Todo)



# Define the admin class
class TodoAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'is_completed', 'created_time', 'last_updated')
    list_filter = ('is_completed',)
    fields = ['text', 'user', 'is_completed']
    pass



# Register the admin class with the associated model
admin.site.register(Todo, TodoAdmin)

# class TodoResource(resources.ModelResource):
#     class Meta:
#         model = Todo