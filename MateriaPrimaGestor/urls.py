from django.urls import path
from . import views

urlpatterns = [
    # Usuario
    path("", views.inicio, name="inicio"), 
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),  
    # CRUD Proveedor
    path("proveedores/", views.listar_proveedores, name="listar_proveedores"),
    path("proveedores/crear/", views.crear_proveedor, name="crear_proveedor"),
    path("proveedores/<int:pk>/editar/", views.editar_proveedor, name="editar_proveedor"),
    path("proveedores/<int:pk>/eliminar/", views.eliminar_proveedor, name="eliminar_proveedor"),
    # CRUD Materia Prima
    path("materias/", views.listar_materias, name="listar_materias"),
    path("materias/crear/", views.crear_materia, name="crear_materia"),
    path("materias/<int:pk>/editar/", views.editar_materia, name="editar_materia"),
    path("materias/<int:pk>/ajustar/", views.ajustar_materia, name="ajustar_materia"),
    path("materias/<int:pk>/eliminar/", views.eliminar_materia, name="eliminar_materia"),
    # CRUD de compras
    path("compras/", views.listar_compras, name="listar_compras"),
    path("compras/crear/", views.crear_compra, name="crear_compra"),
    path("compras/<int:pk>/editar/", views.editar_compra, name="editar_compra"),
    path("compras/<int:pk>/eliminar/", views.eliminar_compra, name="eliminar_compra"),
    # CRUD de productos terminados
    path("productos/", views.listar_productos, name="listar_productos"),
    path("productos/crear/", views.crear_producto, name="crear_producto"),
    path("productos/<int:pk>/editar/", views.editar_producto, name="editar_producto"),
    path("productos/<int:pk>/eliminar/", views.eliminar_producto, name="eliminar_producto"),
]