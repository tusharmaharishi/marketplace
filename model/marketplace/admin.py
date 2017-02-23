from django.contrib import admin
from .models import User, Carpool

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class CarpoolAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Carpool, CarpoolAdmin)
