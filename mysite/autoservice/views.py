from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Paslauga, Uzsakymas, Automobilis
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from .forms import UzsakymoKomentarasForm
from django.contrib.auth.decorators import login_required

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


class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "uzsakymas"
    form_class = UzsakymoKomentarasForm

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.autorius = self.request.user
        form.save()
        return super().form_valid(form)


def search(request):
    query = request.GET.get("query")
    search_results = Automobilis.objects.filter(
        Q(kliento_vardas__icontains=query) | Q(automobilio_modelis__marke__icontains=query) | Q(
            automobilio_modelis__modelis__icontains=query) | Q(valst_nr__icontains=query) | Q(
            vin_kodas__icontains=query))
    return render(request, 'search.html', context={"query": query, "automobiliai": search_results})


class MyUzsakymasListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = "my_uzsakymai.html"
    context_object_name = "uzsakymai"
    paginate_by = 5

    def get_queryset(self):
        return Uzsakymas.objects.filter(user=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')

@login_required
def profile(request):
    return render(request, 'profile.html')