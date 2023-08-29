from django.db import models


# Create your models here.
class AutomobilioModelis(models.Model):
    marke = models.CharField(verbose_name="Markė", max_length=100)
    modelis = models.CharField(verbose_name="Modelis", max_length=100)

    def __str__(self):
        return f"{self.marke} {self.modelis}"


class Automobilis(models.Model):
    valst_nr = models.CharField(verbose_name="Valstybinis numeris", max_length=20)
    vin_kodas = models.CharField(verbose_name="VIN kodas", max_length=20)
    kliento_vardas = models.CharField(verbose_name="Kliento vardas", max_length=50)
    automobilio_modelis = models.ForeignKey(to="AutomobilioModelis", verbose_name="Modelis", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.valst_nr} - {self.vin_kodas} ({self.automobilio_modelis})"


class Uzsakymas(models.Model):
    data = models.DateField(verbose_name="Data", auto_now_add=True)
    automobilis = models.ForeignKey(to="Automobilis", verbose_name="Automobilis", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data} ({self.automobilis})"


class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", on_delete=models.CASCADE)
    paslauga = models.ForeignKey(to="Paslauga", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(verbose_name="Kiekis")

    def suma(self):
        return self.paslauga.kaina * self.kiekis

    def __str__(self):
        return f"{self.uzsakymas} ({self.paslauga} - {self.kiekis}: {self.suma()})"


class Paslauga(models.Model):
    pavadinimas = models.CharField(verbose_name="Pavadinimas", max_length=50)
    kaina = models.FloatField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.pavadinimas} ({self.kaina})"
