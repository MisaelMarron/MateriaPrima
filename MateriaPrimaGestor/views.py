from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db import transaction
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

############## CRUD de Compra 
@login_required
def listar_compras(request):
    compras = Compra.objects.select_related("proveedor", "materia_prima").all().order_by("-codigo")
    return render(request, "compra/listar.html", {"compras": compras})

@login_required
@transaction.atomic
def crear_compra(request):
    form = CompraForm(request.POST or None)
    if form.is_valid():
        compra = form.save(commit=False)
        materia = compra.materia_prima
        # Aumentar inventario
        materia.cantidad += compra.cantidad
        # Actualizar costo al último comprado
        materia.costo = compra.costo
        materia.save()
        compra.save()
        messages.success(request, "Compra registrada correctamente.")
        return redirect("listar_compras")

    return render(request, "compra/form.html", {"form": form, "titulo": "Registrar Compra"})

@login_required
@transaction.atomic
def editar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    materia = compra.materia_prima
    cantidad_anterior = compra.cantidad
    form = CompraForm(request.POST or None, instance=compra)

    if form.is_valid():
        compra_editada = form.save(commit=False)
        # Quitar efecto anterior
        materia.cantidad -= cantidad_anterior
        # Aplicar nuevo efecto
        materia.cantidad += compra_editada.cantidad
        # Actualizar costo
        materia.costo = compra_editada.costo
        materia.save()
        compra_editada.save()
        messages.success(request, "Compra actualizada correctamente.")
        return redirect("listar_compras")
    return render(request, "compra/form.html", {"form": form, "titulo": "Editar Compra"})

@login_required
def eliminar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == "POST":
        compra.delete()
        messages.success(request, "Compra eliminada.")
        return redirect("listar_compras")
    return render(request, "compra/eliminar.html", {"compra": compra})

############## CRUD de producto terminado 
@login_required
def listar_productos(request):
    productos = ProductoTerminado.objects.all().order_by("codigo")
    return render(request, "producto/listar.html", {"productos": productos})

@login_required
def crear_producto(request):
    form = ProductoForm(request.POST or None)
    formset = DetalleProductoFormSet(request.POST or None)
    if form.is_valid() and formset.is_valid():
        producto = form.save()
        formset.instance = producto
        formset.save()
        messages.success(request, "Producto y receta creados correctamente.")
        return redirect("listar_productos")
    return render(request, "producto/form.html", {
        "form": form,
        "formset": formset,
        "titulo": "Crear Producto"
    })

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(ProductoTerminado, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    formset = DetalleProductoFormSet(request.POST or None, instance=producto)
    if form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        messages.success(request, "Receta actualizada correctamente.")
        return redirect("listar_productos")
    return render(request, "producto/form.html", {
        "form": form,
        "formset": formset,
        "titulo": "Editar Producto"
    })
@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(ProductoTerminado, pk=pk)

    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado.")
        return redirect("listar_productos")

    return render(request, "producto/eliminar.html", {"producto": producto})
############## CRUD de 

