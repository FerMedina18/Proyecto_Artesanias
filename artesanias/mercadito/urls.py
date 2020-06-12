from django.urls import path
from .views import index
from  rest_framework import routers
from .viewsets import *
from .views import *
from . import views
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls import url

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registrar/', registrar, name='registrar'),
    path('inicio_sesion/', inicio_sesion),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('images/favicon.ico'),
            permanent=False),
        name='favicon'
    ),
    # path('get_usuario_vendedor', get_usuario_vendedor),
    # path('get_categoria', get_categoria)
]

router = routers.SimpleRouter()
router.register('Usuario_Vendedor', UVendedor_ViewSet),
router.register('Perfil_Vendedor', PVendedor_ViewSet),
router.register('Usuario_Comprador', UComprador_ViewSet),
router.register('Perfil_Comprador', PComprador_ViewSet),
router.register('Producto', Producto_ViewSet),
router.register('Categoria', Categoria_ViewSet),
router.register('Producto_Categoria', ProductoCat_ViewSet),
router.register('Image', Imagen_ViewSet),
router.register('Puntuacion', Puntuacion_ViewSet),
router.register('Orden', Orden_ViewSet),
router.register('Detalle_Orden', DOrden_ViewSet),
# router.register('Profile', Profile_ViewSet),

urlpatterns += router.urls