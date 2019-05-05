from import_export import resources
from import_export.widgets import DateTimeWidget
from .models import Todo
from import_export.fields import Field
from datetime import datetime

class TodoExportResource(resources.ModelResource):
    user = Field(attribute='user', column_name='User')
    text = Field(attribute='text', column_name='Todo')
    is_completed = Field(attribute='is_completed', column_name='Status')
    created_time = Field(attribute='created_time', column_name='Created', widget=DateTimeWidget(format='%d-%m-%Y %H:%M:%S'))
    last_updated = Field(attribute='last_updated', column_name='Updated', widget=DateTimeWidget(format='%d-%m-%Y %H:%M:%S'))   
        
    class Meta:
        model = Todo
        exclude = ('id', )
        export_order = ('user', 'text', 'is_completed', 'created_time', 'last_updated',)

    def dehydrate_is_completed(self, todo):
        if todo.is_completed:
            return '%s' % ('Completed')
        else:
            return '%s' % ('Not Completed')






