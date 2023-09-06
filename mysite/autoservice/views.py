from django.shortcuts import render, get_object_or_404
from .models import Paslauga, Uzsakymas, Automobilis
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
def index(request):
    paslaugu_kiekis = Paslauga.objects.count()
    atlikti_uzsakymai = Uzsakymas.objects.filter(status__exact='i').count()
    automobiliu_kiekis = Automobilis.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        "paslaugu_kiekis": paslaugu_kiekis,
        "atlikti_uzsakymai": atlikti_uzsakymai,
        "automobiliu_kiekis": automobiliu_kiekis,
        'num_visits': num_visits,
    }

    return render(request, "index.html", context=context)


def automobiliai(request):
    paginator = Paginator(Automobilis.objects.all(), per_page=5)
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


def search(request):
    query = request.GET.get("query")
    search_results = Automobilis.objects.filter(
        Q(kliento_vardas__icontains=query) | Q(automobilio_modelis__marke__icontains=query) | Q(
            automobilio_modelis__modelis__icontains=query) | Q(valst_nr__icontains=query) | Q(
            vin_kodas__icontains=query))
    return render(request, 'search.html', context={"query": query, "automobiliai": search_results})
