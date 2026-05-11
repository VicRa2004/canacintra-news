from django.contrib import admin
from .models import Category, News, Comment
from unfold.admin import ModelAdmin

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ('title', 'category', 'author', 'published_at')
    list_filter = ('category', 'published_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('user', 'news', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at', 'user')
    search_fields = ('content',)
    actions = ['approve_comments']
    list_editable = ('is_approved',)

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Aprobar comentarios seleccionados"
