from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import ProveedorForm
from .models import Proveedor

def inicio(request):
    return render(request, "inicio.html")


# Registro
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Usuario creado correctamente")
            return redirect("inicio")
        else:
            messages.error(request, "Corrige los errores")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})
# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # obtiene al usuario autenticado
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            return redirect("inicio")
        else:
            messages.error(request, "Credenciales inválidas")
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})

# Logout
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente")
    return redirect("inicio")

############## CRUD de proveedor
@login_required
def listar_proveedores(request):
    proveedores = Proveedor.objects.all().order_by("codigo")
    return render(request, "proveedor/listar.html", {"proveedores": proveedores})

@login_required
def crear_proveedor(request):
    form = ProveedorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Proveedor creado correctamente.")
        return redirect("listar_proveedores")
    return render(request, "proveedor/form.html", {"form": form, "titulo": "Crear Proveedor"})

@login_required
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        messages.success(request, "Proveedor actualizado correctamente.")
        return redirect("listar_proveedores")
    return render(request, "proveedor/form.html", {"form": form, "titulo": "Editar Proveedor"})

@login_required
def eliminar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        proveedor.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect("listar_proveedores")
    return render(request, "proveedor/eliminar.html", {"proveedor": proveedor})

############## CRUD de 

############## CRUD de 

############## CRUD de 