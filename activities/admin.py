from django.contrib import admin
from django.conf import settings
from activities.models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_filter = ('content_type',)
    ordering = ('-created_at',)
admin.site.register(Activity,ActivityAdmin)
