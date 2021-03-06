from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import reverse

class Usuario(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to="avatar")
    rol = models.CharField(max_length=20)

class Perfil_Vendedor(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="profile_vendedor")
    portada = models.ImageField(blank=True, upload_to="portada")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    direccion = models.TextField(max_length=300)
    descripcion = models.TextField(default='', max_length=500)
    estado = models.BooleanField(default=True)

class Perfil_Comprador(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="profile_comprador")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=12)
    direccion = models.TextField(max_length=300)
    descripcion = models.TextField(default='', max_length=500)
    estado = models.BooleanField(default=True)

# @receiver(post_save, sender=Usuario)
# def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        if instance.rol == "vendedor":
#             Perfil_Vendedor.objects.create(user=instance)

#        elif instance.rol == "comprador":
#            Perfil_Comprador.objects.create(user=instance)

# @receiver(post_save, sender=Usuario)
# def save_user_profile(sender, instance, **kwargs):  
#     if instance.rol == "vendedor":
#         instance.profile_vendedor.save()
#     elif instance.rol == "comprador":
#         instance.profile_comprador.save()

class Producto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    existencia = models.PositiveIntegerField(default=0)
    fecha_publicacion = models.DateField(auto_now=True)
    descripcion = models.TextField(default='', max_length=300)
    estado = models.BooleanField(default=True)
    descuento = models.FloatField(blank=True, null=True)
    slug = models.SlugField()
    
    def __str__(self):
        return self.nombre

    def get_add_to_cart_url(self):
        return reverse("mercadito:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("mercadito:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_producto(self):
        return Producto.objects.get(id=self.id)

    def get_imagen(self):
        return Imagen.objects.get(producto=self.id)

    def get_categoria(self):
        return Producto_Categoria.objects.get(producto=self.id)
    
    def get_absolute_url(self):
        return reverse("mercadito:editar_producto", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} of {self.producto.nombre}"

    def get_total_item_price(self):
        return self.cantidad * self.producto.precio

    def get_total_discount_item_price(self):
        print(self.producto.descuento)
        print(self.cantidad)
        return self.cantidad * self.producto.descuento

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.producto.descuento:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    productos = models.ManyToManyField(OrderItem)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_pedido = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    cupon = models.ForeignKey('Cupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.productos.all():
            total += order_item.get_final_price()
        if self.cupon:
            total -= self.cupon.cantidad
        return total

class Cupon(models.Model):
    codigo = models.CharField(max_length=15)
    cantidad = models.FloatField()

    def __str__(self):
        return self.codigo


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default='', max_length=200)

    def __str__(self):
        return self.nombre

class Producto_Categoria(models.Model):
    producto = models.ManyToManyField(Producto)
    categoria = models.ManyToManyField(Categoria)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("mercadito:producto", kwargs={
            'slug': self.slug
        })

    def get_imagenes(self):
        for i in Imagen.objects.all():
            if i.producto.id == self.id:
                return i


    def get_categ(self):
        return Categoria.objects.all()

class Imagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ruta = models.ImageField(upload_to="productos", null=True)

class Puntuacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario_comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.producto

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     descripcion = models.TextField(max_length=500, blank=True)
#     fecha_nacimiento = models.DateField(null=True, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

