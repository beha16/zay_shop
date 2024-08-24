from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.views.generic import TemplateView, ListView, CreateView, FormView, View, DetailView
from httpx import post, get

from apps.form import UserSignUpForm, UserLoginForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import Product, User, Wishlist, Order, Basket

# Create your views here.

TELEGRAM_BOT_TOKEN = "7386101386:AAFkQezdAGmu4tXyX9PNWsYn0cH5puOr8sI"


def send_message(chat_id, message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = get(url, params=params)
    print(response.text, response.status_code)


class IndexTemplateView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        data = self.request.GET.get('search')

        # print(data)
        if data is not None and len(data) > 0:
            qs = qs.filter(name__icontains=data)
        # print(qs)
        return qs


def send_msg_bot(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        text = f'''
Name: {name}
Email: {email}
Subject: {subject}
Message: {message}
        '''
        send_message(867549831, text)

        return render(request, 'contact.html')


class AboutTemplateView(TemplateView):
    template_name = 'about.html'


class ContactTemplateView(TemplateView):
    template_name = 'contact.html'


class ShopListView(ListView):
    template_name = 'shop.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        data = self.request.GET.get('search')

        # print(data)
        if data is not None and len(data) > 0:
            qs = qs.filter(name__icontains=data)
        # print(qs)
        return qs


class ShopDetailTemplateView(DetailView):
    template_name = 'shop-single.html'
    model = Product


class RegisterCreateView(NotLoginRequiredMixin, CreateView):
    model = User
    form_class = UserSignUpForm
    success_url = '/'
    template_name = 'register.html'


class LoginFormView(NotLoginRequiredMixin, FormView):
    form_class = UserLoginForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(username, password)
        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            user_password = user.password
            print(user)
            print(user_password)

            print('SUCCESSFULLY LOGGED IN')
            login(self.request, user)
            return redirect('/')

        else:
            print('INCORRECT LOGIN')
            messages.error(self.request, 'Invalid username or password.')
            return redirect('login')

        return super().form_valid(form)


class WishListCreateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        pk = self.kwargs.get('pk')
        product = Product.objects.filter(pk=pk).first()
        if user and pk:
            if not Wishlist.objects.filter(user=user, product=product).exists():
                Wishlist.objects.create(
                    product=product,
                    user=user
                )
            else:
                wishlist = Wishlist.objects.filter(product=product)
                wishlist.delete()
        return redirect('/')


class WishlistDeleteView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        wishlist = Wishlist.objects.filter(user=user)
        wishlist.delete()
        return redirect('wishlist')


class WishListListView(LoginRequiredMixin, ListView):
    template_name = 'wish_list.html'
    model = Wishlist
    context_object_name = 'wishlist'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        user = self.request.user.pk
        my_wishlist = Wishlist.objects.filter(user=user)
        context['my_wishlist'] = my_wishlist
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        print(qs)
        return qs


def send_email(request):
    send_mail(
        "Test Email",
        "Test Successfully ",
        "behzod0824@gmail.com",
        ["behzod0824@gmail.com"],
        fail_silently=False,
    )
    return redirect('/')


class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('/')


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        first_name = self.request.GET.get('firstname')
        last_name = self.request.GET.get('lastname')
        xurlangan = self.request.GET.get('xurlangan')
        pk = self.request.GET.get('pk')
        print(pk)
        print(xurlangan)

        return redirect('/')


class OrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'order.html'


class BasketCreateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        pk = self.kwargs.get('pk')
        product = Product.objects.filter(pk=pk).first()

        if user and pk:
            if not Basket.objects.filter(user=user, product=product).exists():
                Basket.objects.create(
                    product=product,
                    user=user
                )
        return redirect('/')


class BasketView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        pk = self.kwargs.get('pk')
        product = Product.objects.filter(pk=pk).first()

        if user and pk:
            if not Basket.objects.filter(user=user, product=product).exists():
                Basket.objects.create(
                    product=product,
                    user=user
                )
        return redirect('basket')


class BasketDeleteView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        pk = self.kwargs.get('pk')
        product = Product.objects.filter(pk=pk).first()
        if user and pk:
            if Basket.objects.filter(user=user, product=product).exists():
                Basket.objects.filter(user=user, product=product).delete()
        return redirect('basket')


class BasketListView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'basket'
    template_name = 'basket.html'

    def get_context_data(self, **kwargs):
        l = []
        context = super(ListView, self).get_context_data(**kwargs)
        user = self.request.user.pk
        my_basket = Basket.objects.filter(user=user)
        for basket in my_basket:
            l.append(basket.id)
        context['basket_id'] = l
        context['my_basket'] = my_basket
        print(l)
        return context


class CheckoutView(LoginRequiredMixin, ListView):
    model = Basket
    context_object_name = 'basket'
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        user = self.request.user.pk
        my_basket = Basket.objects.filter(user=user)
        context['my_basket'] = my_basket
        # print(my_basket)
        return context