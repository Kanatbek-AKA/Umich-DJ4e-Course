from django.contrib import admin
from .models import Ad, Comment, Fav, Blog


class AdAdmin(admin.ModelAdmin):
    include = [Comment]
    exclude = ('picture', 'content_type')
    list_display = ['owner', "created_at"]
    list_filter = ['created_at']
    search_fields = ['title', 'updated_at']


class BlogAdmin(admin.ModelAdmin):
    include = Blog
    list_display = ['owner', "created_at"]
    list_filter = ['created_at']
    search_fields = ['title', 'updated_at']

# Register the admin class with the associated model
admin.site.register(Ad, AdAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, AdAdmin)
admin.site.register(Fav)
