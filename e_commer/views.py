from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CustomUser, Laptop, Carrito,Order,OrderItem
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm,CustomUserCreationForm,CustomUserForm,CheckoutForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from django.shortcuts import render, redirect

from django.utils import timezone

def home(request):
    return render(request, 'home.html')

class CustomUserListView(ListView):
    model = CustomUser
    template_name = 'customuser_list.html'
    context_object_name = 'usuarios'

class CustomUserCreateView(CreateView):
    model = CustomUser
    template_name = 'customuser_form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('customuser_list')

    def form_valid(self, form):
        form.instance.username = form.cleaned_data['email']
        return super().form_valid(form)

class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'customuser_form.html'
    form_class = CustomUserForm
    success_url = reverse_lazy('customuser_list')

class CustomUserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'customuser_confirm_delete.html'
    success_url = reverse_lazy('customuser_list')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    success_url = '/'

class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('customuser_list')
    template_name = 'change_password.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response
    
def signout(request):
    logout(request)
    return redirect('home')

def laptops(request):
    laptops = Laptop.objects.all()
    print(laptops)
    return render(request, 'laptops.html', {'laptops': laptops})

def laptop_detail(request, laptop_id):
    laptop = Laptop.objects.get(pk=laptop_id)
    return render(request, 'laptop_detail.html', {'laptop': laptop})

@login_required
def agregar_al_carrito(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user, producto=laptop)
    if not creado:
        carrito.cantidad += 1
        carrito.save()
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    total = sum([item.producto.precio * item.cantidad for item in carrito])
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

@login_required
def eliminar_del_carrito(request, carrito_id):
    cart = request.session.get('cart', [])
    for i, item in enumerate(cart):
        if item['id'] == carrito_id:
            if item['cantidad'] > 1:
                item['cantidad'] -= 1
            else:
                del cart[i]
            request.session['cart'] = cart
            break
    return redirect('cart')


def add_to_cart(request, laptop_id):
    laptop = Laptop.objects.get(id=laptop_id)
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']
    for item in cart:
        if item['id'] == laptop.id:
            item['cantidad'] += 1
            break
    else:
        try:
            precio = float(laptop.precio)
        except TypeError:
            precio = float(laptop.precio.amount)
        cart.append({'id': laptop.id, 'marca': laptop.marca, 'modelo': laptop.modelo, 'precio': precio, 'cantidad': 1})
    request.session['cart'] = cart
    messages.success(request, f"{laptop.marca} {laptop.modelo} ha sido agregado al carrito.")
    return redirect('laptops')


def cart(request):
    cart = request.session.get('cart', [])
    print(cart)
    total = sum([item['precio'] for item in cart])
    return render(request, 'cart.html', {'cart': cart, 'total': total})

def checkout(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Crear un objeto Order
            order = Order(
                usuario=request.user,
                date_ordered=timezone.now(),
                total=sum([item['precio'] for item in cart]),
                direccion=form.cleaned_data['direccion'],
                ciudad=form.cleaned_data['ciudad'],
                provincia=form.cleaned_data['provincia'],
                codigo_postal=form.cleaned_data['codigo_postal'],
                pais=form.cleaned_data['pais'],
            )
            order.save()

            # Crear los objetos OrderItem relacionados con el objeto Order
            for item in cart:
                # Recuperar el objeto Laptop
                laptop = Laptop.objects.get(pk=item['id'])

                # Crear el objeto OrderItem con el objeto Laptop correspondiente
                order_item = OrderItem(
                    order=order,
                    laptop=laptop,
                    quantity=item['cantidad'],
                    subtotal=item['precio'] * item['cantidad']
                )
                order_item.save()

            # Limpiar el carrito
            request.session['cart'] = []
            messages.success(request, 'Tu pedido ha sido procesado correctamente.')
            return redirect('order_confirmation', pk=order.pk)
    else:
        form = CheckoutForm()

    total = sum([item['precio'] for item in cart])
    return render(request, 'checkout.html', {'form': form, 'total': total})


def order_confirmation(request, pk):
    order = Order.objects.get(pk=pk)
    return render(request, 'order_confirmation.html', {'order': order})
