from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import *
from .models import *

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

############## CRUD de MateriaPrima
@login_required
def listar_materias(request):
    materias = MateriaPrima.objects.all().order_by("codigo")
    return render(request, "materia/listar.html", {"materias": materias})

@login_required
def crear_materia(request):
    form = MateriaPrimaCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Materia prima creada.")
        return redirect("listar_materias")
    return render(request, "materia/form.html", {"form": form, "titulo": "Nueva Materia Prima"})

@login_required
def editar_materia(request, pk):
    materia = get_object_or_404(MateriaPrima, pk=pk)
    form = MateriaPrimaUpdateForm(request.POST or None, instance=materia)
    if form.is_valid():
        form.save()
        messages.success(request, "Materia prima actualizada.")
        return redirect("listar_materias")
    return render(request, "materia/form.html", {"form": form, "titulo": "Editar Materia Prima"})

@login_required
def ajustar_materia(request, pk):
    materia = get_object_or_404(MateriaPrima, pk=pk)
    form = MateriaPrimaAjusteForm(request.POST or None)
    if form.is_valid():
        cantidad = form.cleaned_data["cantidad"]
        tipo = form.cleaned_data["tipo"]
        if tipo == "SUMAR":
            materia.cantidad += cantidad
        else:
            if cantidad > materia.cantidad:
                messages.error(request, "No puedes dejar stock negativo.")
                return redirect("ajustar_materia", pk=pk)
            materia.cantidad -= cantidad
        materia.save()
        messages.success(request, "Stock actualizado correctamente.")
        return redirect("listar_materias")
    return render(request, "materia/ajustar.html", {"form": form, "materia": materia})

@login_required
def eliminar_materia(request, pk):
    materia = get_object_or_404(MateriaPrima, pk=pk)
    if request.method == "POST":
        materia.delete()
        messages.success(request, "Materia prima eliminada.")
        return redirect("listar_materias")
    return render(request, "materia/eliminar.html", {"materia": materia})

############## CRUD de 

############## CRUD de 