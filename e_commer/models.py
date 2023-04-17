from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from django.utils import timezone

# Register your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, primerNombre, apellidoPaterno, segundoNombre, apellidoMaterno, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not primerNombre:
            raise ValueError('El usuario debe tener un primer nombre')
        if not segundoNombre:
            raise ValueError('El usuario debe tener un segundo nombre')        
        if not apellidoPaterno:
            raise ValueError('El usuario debe tener un apellido paterno')
        if not apellidoMaterno:
            raise ValueError('El usuario debe tener un apellido materno')

        user = self.model(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, primerNombre, segundoNombre,apellidoPaterno,apellidoMaterno, password):
        user = self.create_user(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    primerNombre = models.CharField(max_length=100)
    segundoNombre = models.CharField(max_length=100, null=True, blank=True)
    apellidoPaterno = models.CharField(max_length=100)
    apellidoMaterno = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primerNombre','segundoNombre', 'apellidoPaterno','apellidoMaterno']

    def nombre_completos(self):
        return "{} {}, {} {}".format(self.apellidoPaterno, self.apellidoMaterno, self.primerNombre, self.segundoNombre)
    
    def __str__(self):
        return self.email
    
class Laptop(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='laptops/')

class Carrito(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    creado = models.DateField(default=timezone.now)

class Order(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_ordered = models.DateField(default=timezone.now)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100, default='Lima') # Se proporciona un valor predeterminado
    provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=50)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)