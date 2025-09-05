from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"), 
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),  
    # materias
    path("materias/", views.materia_list, name="materia_list"),
    path("materias/nueva/", views.materia_create, name="materia_create"),
    path("materias/<str:codigo>/editar/", views.materia_update, name="materia_update"),
    path("materias/<str:codigo>/eliminar/", views.materia_delete, name="materia_delete"),
    # productos
    path("productos/", views.producto_list, name="producto_list"),
    path("productos/nuevo/", views.producto_create, name="producto_create"),
    path("productos/<str:codigo>/editar/", views.producto_update, name="producto_update"),
    path("productos/<str:codigo>/eliminar/", views.producto_delete, name="producto_delete"),
    # produccion
    path("produccion/confirm/", views.produccion_confirm, name="produccion_confirm"),
    path("produccion/<str:codigo>/", views.produccion_preview, name="produccion_preview"),
    path("producciones/", views.produccion_list, name="produccion_list"),
    path("producciones/<int:pk>/", views.produccion_detail, name="produccion_detail"),
]