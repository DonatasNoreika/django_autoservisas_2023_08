from django.contrib import admin
from .models import Automobilis, AutomobilioModelis, Uzsakymas, UzsakymoEilute, Paslauga

class UzsakymasInLine(admin.TabularInline):
    model = UzsakymoEilute
    extra = 0

class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ['data', 'automobilis']
    inlines = [UzsakymasInLine]

# Register your models here.
admin.site.register(Automobilis)
admin.site.register(AutomobilioModelis)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(Paslauga)
