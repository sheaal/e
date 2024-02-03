from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.views import PasswordChangeView
from .forms import RegisterUserForm
from .models import AdvUser, Order, Product
from django.views.generic import TemplateView
from django.shortcuts import redirect

@login_required
def profile(request):
    current_user = request.user
    product_list = Order.objects.filter(user=current_user)
    context = {'product_list': product_list}
    return render(request, 'app/profile.html', context)

def index(request):
    product_list = Product.objects.order_by('-pr_date')[:5]
    return render(request, 'app/index.html', {'product_list': product_list})


def product(request):
    product_list = Product.objects.all()
    return render(request, 'app/product.html', {'product_list': product_list})

class BBLoginView(LoginView):
   template_name = 'app/login.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'app/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('app:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'app/login.html'

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            # Create User object
            AdvUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                sur_name=form.cleaned_data['sur_name'],
                n_name=form.cleaned_data['n_name'],
                pat_mic=form.cleaned_data['pat_mic'],
            )
            messages.success(request, 'Registration successful.')
            return render(request, 'app/login.html')
    else:
        form = RegisterUserForm()
    return render(request, 'app/register_user.html', {'form': form})

class BBLogoutView(LoginRequiredMixin, LogoutView):
   template_name = 'app/logout.html'


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    pk_url_kwarg = 'id'
    model = Product
    template_name = 'app/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['orders'] = Order.objects.filter(user=self.request.user, product=self.object)
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = self.get_object()
            order = Order(user=request.user, product=product)
            order.save()
            messages.success(request, 'Услуга/товар успешно заказана')
            return redirect('app:profile')
        else:
            return redirect('app:login')

def search(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Product.objects.filter(pr_name__icontains=query)

    context = {'results': results}
    return render(request, "app/search.html", context)

# def ordering(request, product_id):
#
#     try:
#         service = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         return HttpResponseBadRequest('Услуга/товар не найден')
#
#
#         return HttpResponseBadRequest('Пользователь не авторизован')
#
#
#     else:
#         order = Order(user=request.user, product=product)
#         order.save()
#         messages.success(request, 'Услуга/товар успешно заказана')
#         return redirect('app:profile')