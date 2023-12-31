from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Paslauga, Uzsakymas, Automobilis, UzsakymoEilute
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from .forms import UzsakymoKomentarasForm, UserUpdateForm, ProfileUpdateForm, UzsakymasForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

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


def search(request):
    query = request.GET.get("query")
    search_results = Automobilis.objects.filter(
        Q(kliento_vardas__icontains=query) | Q(automobilio_modelis__marke__icontains=query) | Q(
            automobilio_modelis__modelis__icontains=query) | Q(valst_nr__icontains=query) | Q(
            vin_kodas__icontains=query))
    return render(request, 'search.html', context={"query": query, "automobiliai": search_results})


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
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


class MyUzsakymasListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = "my_uzsakymai.html"
    context_object_name = "uzsakymai"
    paginate_by = 5

    def get_queryset(self):
        return Uzsakymas.objects.filter(user=self.request.user)


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


class UzsakymasCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    template_name = "uzsakymas_form.html"
    success_url = "/myuzsakymai/"
    # fields = ['automobilis', 'deadline', 'status']
    form_class = UzsakymasForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class UzsakymasUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    template_name = "uzsakymas_form.html"
    # success_url = "/myuzsakymai/"
    # fields = ['automobilis', 'deadline', 'status']
    form_class = UzsakymasForm

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().user == self.request.user



class UzsakymasDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    success_url = "/myuzsakymai/"
    template_name = 'uzsakymas_delete.html'
    context_object_name = 'uzsakymas'

    def test_func(self):
        return self.get_object().user == self.request.user


class UzsakymoEiluteCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = UzsakymoEilute
    template_name = 'uzsakymoeilute_form.html'
    # success_url = "/myuzsakymai/"
    fields = ['paslauga', 'kiekis']

    def test_func(self):
        uzsakymas = self.get_object().uzsakymas
        return uzsakymas.user == self.request.user

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)


class UzsakymoEiluteDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = UzsakymoEilute
    template_name = 'uzsakymoeilute_delete.html'
    context_object_name = 'uzsakymoeilute'

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.kwargs['uzsakymas_id']})

    def test_func(self):
        uzsakymas = self.get_object().uzsakymas
        return uzsakymas.user == self.request.user


class UzsakymoEiluteUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = UzsakymoEilute
    context_object_name = 'uzsakymoeilute'
    template_name = 'uzsakymoeilute_form.html'
    fields = ['paslauga', 'kiekis']

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.kwargs['uzsakymas_id']})

    def test_func(self):
        uzsakymas = self.get_object().uzsakymas
        return uzsakymas.user == self.request.user

    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['uzsakymas_id'])
        form.save()
        return super().form_valid(form)