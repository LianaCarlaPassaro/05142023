"""
URL configuration for ContaConmigo project.

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
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("publicaciones.urls")),
    path('register/', user_views.register, name ='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('donante/', user_views.listadoDonante, name='listadoDonante'),
    path('donante/confirmacion/<int:id>', user_views.donanteAsistencia, name='donanteAsistencia'),
    path('donante/eliminacion/<int:id>', user_views.donanteAsistenciaEliminar, name='donanteAsistenciaEliminar'),
    path('pacientes/paciente/', user_views.paciente, name='paciente'),
    path('pacientes/listadoSolicitud/', user_views.listadoSolicitud, name='listadoSolicitud'),
    path('pacientes/listadoSolicitud/editar_listadoSolicitud/<int:id>', user_views.editarListadoSolicitud, name='editarListadoSolicitud'),
    path('pacientes/listadoSolicitud/ver_listadoSolicitud/<int:id>', user_views.verListadoSolicitud, name='verListadoSolicitud'),
    path('pacientes/donante/<int:id>', user_views.donante, name='donante'),
    path('pacientes/', user_views.listadoPaciente, name='listadoPaciente'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
# Only add this when we are in debug mode.
if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
