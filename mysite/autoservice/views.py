from django.shortcuts import render, get_object_or_404
from .models import Paslauga, Uzsakymas, Automobilis


# Create your views here.
def index(request):
    paslaugu_kiekis = Paslauga.objects.count()
    atlikti_uzsakymai = Uzsakymas.objects.filter(status__exact='i').count()
    automobiliu_kiekis = Automobilis.objects.count()

    context = {
        "paslaugu_kiekis": paslaugu_kiekis,
        "atlikti_uzsakymai": atlikti_uzsakymai,
        "automobiliu_kiekis": automobiliu_kiekis,

    }

    return render(request, "index.html", context=context)


def automobiliai(request):
    return render(request, 'automobiliai.html', context={'automobiliai': Automobilis.objects.all()})


def automobilis(request, auto_id):
    return render(request, 'automobilis.html', context={"automobilis": get_object_or_404(Automobilis, pk=auto_id)})