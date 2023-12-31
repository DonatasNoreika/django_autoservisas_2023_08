from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from tinymce.models import HTMLField
from PIL import Image

utc = pytz.UTC


# Create your models here.
class AutomobilioModelis(models.Model):
    marke = models.CharField(verbose_name="Markė", max_length=100)
    modelis = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.marke} {self.modelis}"

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilio modeliai'


class Automobilis(models.Model):
    valst_nr = models.CharField(verbose_name="Valstybinis numeris", max_length=20)
    vin_kodas = models.CharField(verbose_name="VIN kodas", max_length=20)
    kliento_vardas = models.CharField(verbose_name="Kliento vardas", max_length=50)
    automobilio_modelis = models.ForeignKey(to="AutomobilioModelis", verbose_name="Modelis", on_delete=models.SET_NULL,
                                            null=True)
    nuotrauka = models.ImageField(verbose_name="Nuotrauka", upload_to="autos", null=True, blank=True)
    aprasymas = HTMLField(verbose_name="Aprašymas", default="")

    def __str__(self):
        return f"{self.valst_nr} - {self.vin_kodas} ({self.automobilio_modelis}, {self.kliento_vardas})"

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'


class Uzsakymas(models.Model):
    data = models.DateField(verbose_name="Data", auto_now_add=True)
    automobilis = models.ForeignKey(to="Automobilis", verbose_name="Automobilis", on_delete=models.CASCADE,
                                    related_name='orders')
    user = models.ForeignKey(to=User, verbose_name="Vartotojas", on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateTimeField(verbose_name="Gražinimo data", null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('i', 'Įvykdyta'),
        ('a', 'Atmesta'),
    )

    status = models.CharField(verbose_name="Būsena", choices=LOAN_STATUS, default="p", max_length=1, blank=True)

    def is_overdue(self):
        return self.deadline and self.deadline.replace(tzinfo=utc) < datetime.today().replace(tzinfo=utc)

    def bendra_suma(self):
        bendra_suma = 0
        for line in self.lines.all():
            bendra_suma += line.suma()
        return bendra_suma

    def __str__(self):
        return f"{self.data} ({self.automobilis})"

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'
        ordering = ['-id']


class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", on_delete=models.CASCADE, related_name='lines')
    paslauga = models.ForeignKey(to="Paslauga", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(verbose_name="Kiekis")

    def suma(self):
        return self.paslauga.kaina * self.kiekis

    def __str__(self):
        return f"{self.uzsakymas} ({self.paslauga} - {self.kiekis}: {self.suma()})"

    class Meta:
        verbose_name = 'Eilutė'
        verbose_name_plural = 'Eilutės'


class UzsakymoKomentaras(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", verbose_name="Užsakymas", on_delete=models.CASCADE,
                                  related_name='komentarai')
    autorius = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.CASCADE)
    data = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    tekstas = models.TextField(verbose_name="Tekstas", max_length=2000)

    class Meta:
        ordering = ['-data']


class Paslauga(models.Model):
    pavadinimas = models.CharField(verbose_name="Pavadinimas", max_length=50)
    kaina = models.FloatField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.pavadinimas} ({self.kaina})"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Profile(models.Model):
    user = models.OneToOneField(to=User, verbose_name="Vartotojas", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Nuotrauka", upload_to="profile_pics", default="profile_pics/default.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)