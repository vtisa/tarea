from django.urls import path
from evento import views

urlpatterns = [
    path('eventos/crear/', views.crear, name='crear'),
    path('eliminar_registro/<int:pk>/', views.eliminar_registro, name='eliminar_registro'),
    path('eliminar_evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('actualizar_evento/<int:evento_id>/', views.actualizar_evento, name='actualizar_evento'),
    path('actualizar_registro/<int:pk>/', views.actualizar_registro, name='actualizar_registro'),
    path('', views.crear_usuario, name='crear_usuario'),
    path('eventos/registrar/', views.registrar, name='registrar'),
    path('eventos/registros/', views.listar_registros, name='listar_registros'),
    path('listar_evento/', views.listar_evento, name='listar_evento'),
    path('contar-registros/', views.contar_registros, name='contar_registros'),
    path('mes-actual/', views.contar_mes_actual, name='contar_mes_actual'),
    path('usuarios/activos/', views.usuarios_activos, name='usuarios_activos'),
    path('contar-eventos-organizados/', views.contar_eventos_organizados, name='contar_eventos_organizados'),
]