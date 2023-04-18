"""
URL configuration for tienda project.

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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from e_commer.views import order_confirmation,checkout,eliminar_del_carrito, CustomUserCreateView, CustomUserUpdateView, CustomUserDeleteView,CustomPasswordChangeView,signout,home,laptops,laptop_detail,add_to_cart, cart
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),   
    path('usuarios/nuevo/', CustomUserCreateView.as_view(), name='customuser_create'),
    path('usuarios/editar/<int:pk>/', CustomUserUpdateView.as_view(), name='customuser_update'),
    path('usuarios/eliminar/<int:pk>/', CustomUserDeleteView.as_view(), name='customuser_delete'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('logout/', signout, name='logount'),
    path('accounts/profile/', RedirectView.as_view(url='/', permanent=False)),

    path('laptops/', laptops, name='laptops'),
    path('laptops/<int:laptop_id>/', laptop_detail, name='laptop_detail'),
    path('add_to_cart/<int:laptop_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('eliminar_del_carrito/<int:carrito_id>/',eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/<int:pk>/', order_confirmation, name='order_confirmation'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
