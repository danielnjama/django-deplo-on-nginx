from django.contrib import admin
from . models import Post,Tags,Category,Comment

class TagsAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"url": ("name",)}


class CategotyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"url": ("name",)}
    
class PostAdmin(admin.ModelAdmin):
    list_display = ["title","created_at","published"]
    prepopulated_fields = {"url": ["title"]}


class commentAdmin(admin.ModelAdmin):
    list_display = ['name','approved']
    list_editable =['approved']
    
    
    
admin.site.register(Post,PostAdmin)
admin.site.register(Tags,TagsAdmin)
admin.site.register(Category,CategotyAdmin)
admin.site.register(Comment,commentAdmin)

# Register your models here.
