from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import MateriaPrima, ProductoTerminado
from .forms import MateriaPrimaForm, AjusteCantidadForm, ProductoTerminadoForm

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

############## CRUD de MateriaPrima

# LISTAR
@login_required
def materia_list(request):
    materias = MateriaPrima.objects.all()
    return render(request, "materia/materia_list.html", {"materias": materias})

# CREAR
@login_required
def materia_create(request):
    if request.method == "POST":
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Materia Prima creada")
            return redirect("materia_list")
    else:
        form = MateriaPrimaForm()
    return render(request, "materia/materia_form.html", {"form": form})

# AGREGAR 
@login_required
def materia_update(request, codigo):
    materia = get_object_or_404(MateriaPrima, codigo=codigo)

    if request.method == "POST":
        form = AjusteCantidadForm(request.POST)
        if form.is_valid():
            ajuste = form.cleaned_data["agregar"]
            nueva_cantidad = materia.cantidad + ajuste

            if nueva_cantidad < 0:
                messages.error(request, "No puedes dejar la cantidad en negativa")
            else:
                materia.cantidad = nueva_cantidad
                materia.save()
                messages.success(request, f"Cantidad actualizada a {materia.cantidad} de {materia.codigo} - {materia.nombre}")
                return redirect("materia_list")
    else:
        form = AjusteCantidadForm()

    return render(request, "materia/materia_form.html", {"form": form, "materia": materia})

# ELIMINAR
@login_required
def materia_delete(request, codigo):
    materia = get_object_or_404(MateriaPrima, codigo=codigo)
    if request.method == "POST":
        messages.success(request, f"Materia Prima eliminada: {materia.codigo} - {materia.nombre}")
        materia.delete()
        return redirect("materia_list")
    return render(request, "materia/materia_confirm_delete.html", {"materia": materia})


############## CRUD de ProductoTerminado
# LISTAR
def producto_list(request):
    productos = ProductoTerminado.objects.all()
    return render(request, "producto/producto_list.html", {"productos": productos})

# CREAR
def producto_create(request):
    if request.method == "POST":
        form = ProductoTerminadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("producto_list")
    else:
        form = ProductoTerminadoForm()
    return render(request, "producto/producto_form.html", {"form": form})

# EDITAR
def producto_update(request, codigo):
    producto = get_object_or_404(ProductoTerminado, pk=codigo)
    if request.method == "POST":
        form = ProductoTerminadoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("producto_list")
    else:
        form = ProductoTerminadoForm(instance=producto)
    return render(request, "producto/producto_form.html", {"form": form})

# ELIMINAR
def producto_delete(request, codigo):
    producto = get_object_or_404(ProductoTerminado, pk=codigo)
    if request.method == "POST":
        producto.delete()
        return redirect("producto_list")
    return render(request, "producto/producto_confirm_delete.html", {"producto": producto})