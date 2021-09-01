from django.contrib import admin
from blog.models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tag_list')	
    search_fields = ('title', 'content')

    def get_queryset(self, request):    # 추가
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):            # 추가
        return ', '.join(o.name for o in obj.tags.all())


admin.site.register(Blog, BlogAdmin)