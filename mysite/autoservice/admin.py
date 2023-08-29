from django.contrib import admin
from .models import Automobilis, AutomobilioModelis, Uzsakymas, UzsakymoEilute, Paslauga

# Register your models here.
admin.site.register(Automobilis)
admin.site.register(AutomobilioModelis)
admin.site.register(Uzsakymas)
admin.site.register(UzsakymoEilute)
admin.site.register(Paslauga)
