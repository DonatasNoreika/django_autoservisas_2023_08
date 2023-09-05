from django.shortcuts import render, get_object_or_404
from .models import Paslauga, Uzsakymas, Automobilis
from django.views import generic
from django.core.paginator import Paginator

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
    paginator = Paginator(Automobilis.objects.all(), per_page=2)
    page_number = request.GET.get('page')
    paged_automobiliai = paginator.get_page(page_number)
    return render(request, 'automobiliai.html', context={'automobiliai': paged_automobiliai})


def automobilis(request, auto_id):
    return render(request, 'automobilis.html', context={"automobilis": get_object_or_404(Automobilis, pk=auto_id)})


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    template_name = "uzsakymai.html"
    context_object_name = "uzsakymai"
    paginate_by = 5


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "uzsakymas"