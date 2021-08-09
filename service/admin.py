from django.contrib import admin

# Register your models here.


from django.contrib import admin

from .models import Profile, Project, Product


admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Product)




