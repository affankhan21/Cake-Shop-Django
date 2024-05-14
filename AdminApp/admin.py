from django.contrib import admin
from .models import Category,Cake

class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','cname')

class CakeAdmin(admin.ModelAdmin):
    list_display=('id','cake_name','price','description','image','qty','category')    


admin.site.register(Category,CategoryAdmin)
admin.site.register(Cake,CakeAdmin)