"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from root import settings
from django.conf.urls.static import static
from apps.views import (
    IndexTemplateView, AboutTemplateView,
    ContactTemplateView, ShopListView,
    ShopDetailTemplateView, WishListCreateView,
    LoginFormView, RegisterCreateView,
    WishListListView, LogoutView, OrderCreateView,
    WishlistDeleteView, BasketListView,
    BasketCreateView, CheckoutView, BasketView,
    BasketDeleteView,
    send_email, send_msg_bot
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexTemplateView.as_view(), name='index'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('contact/', ContactTemplateView.as_view(), name='contact'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('shop_detail/<int:pk>/', ShopDetailTemplateView.as_view(), name='shop_detail'),

    # WishList
    path('like/<int:pk>/', WishListCreateView.as_view(), name='like'),
    path('wishlist/', WishListListView.as_view(), name='wishlist'),
    path('wishlist_delete/', WishlistDeleteView.as_view(), name='wishlist_delete'),

    # Basket
    path('basket', BasketListView.as_view(), name='basket'),
    path('basket_create/<int:pk>/', BasketCreateView.as_view(), name='basket_create'),
    path('basket_view/<int:pk>/', BasketView.as_view(), name='basket_view'),
    path('basket_delete/<int:pk>/', BasketDeleteView.as_view(), name='basket_delete'),

    # Order
    path('order/<int:pk>/', OrderCreateView.as_view(), name='order'),


    # SignUp / SignIn, Logout
    path('login/', LoginFormView.as_view(), name='login'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    # Sending Email
    path('email/', send_email, name='email'),

    # Sending Msg to Bot
    path('send_msg_bot/', send_msg_bot, name='send_msg_bot'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)