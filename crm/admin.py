from django.contrib import admin
from .models import Record

admin.site.site_header ='Zago Arena'
admin.site.index_title= 'Do the magic'

admin.site.register(Record)
