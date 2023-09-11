from django.contrib import admin
from .models import Automobilis, AutomobilioModelis, Uzsakymas, UzsakymoEilute, Paslauga, UzsakymoKomentaras

class UzsakymoEiluteInLine(admin.TabularInline):
    model = UzsakymoEilute
    extra = 0


class UzsakymoKomentarasInLine(admin.TabularInline):
    model = UzsakymoKomentaras
    extra = 0

class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ['data', 'automobilis', 'user', 'deadline']
    inlines = [UzsakymoEiluteInLine, UzsakymoKomentarasInLine]


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ['kliento_vardas', 'automobilio_modelis', 'valst_nr', 'vin_kodas']
    list_filter = ['kliento_vardas', 'automobilio_modelis__marke', 'automobilio_modelis__modelis']
    search_fields = ['valst_nr', 'vin_kodas']

class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ['pavadinimas', 'kaina']

# Register your models here.
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(AutomobilioModelis)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(Paslauga, PaslaugaAdmin)
