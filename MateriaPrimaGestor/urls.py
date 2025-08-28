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
]