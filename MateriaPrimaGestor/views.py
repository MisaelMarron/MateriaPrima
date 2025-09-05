from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import MateriaPrima, ProductoTerminado, Produccion, ConsumoMateriaPrima
from .forms import MateriaPrimaForm, AjusteCantidadForm, ProductoTerminadoForm, DetalleProducto, DetalleProductoFormSet, ProduccionForm
from .services import producir_producto
from decimal import Decimal
from django.core.exceptions import ValidationError

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
        formset = DetalleProductoFormSet(request.POST, instance=ProductoTerminado())
        if form.is_valid() and formset.is_valid():
            producto = form.save()
            formset.instance = producto
            formset.save()
            return redirect("producto_list")
    else:
        form = ProductoTerminadoForm()
        formset = DetalleProductoFormSet(instance=ProductoTerminado())
    return render(request, "producto/producto_form.html", {"form": form, "formset": formset})

# EDITAR
def producto_update(request, codigo):
    producto = get_object_or_404(ProductoTerminado, pk=codigo)
    if request.method == "POST":
        form = ProductoTerminadoForm(request.POST, instance=producto)
        formset = DetalleProductoFormSet(request.POST, instance=producto)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("producto_list")
    else:
        form = ProductoTerminadoForm(instance=producto)
        formset = DetalleProductoFormSet(instance=producto)
    return render(request, "producto/producto_form.html", {"form": form, "formset": formset})

# ELIMINAR
def producto_delete(request, codigo):
    producto = get_object_or_404(ProductoTerminado, pk=codigo)
    if request.method == "POST":
        producto.delete()
        return redirect("producto_list")
    return render(request, "producto/producto_confirm_delete.html", {"producto": producto})


@login_required
def produccion_preview(request, codigo):
    producto = get_object_or_404(ProductoTerminado, codigo=codigo)

    if request.method == "POST":
        form = ProduccionForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data["cantidad"]

            # Preparamos la receta multiplicada
            detalles = DetalleProducto.objects.filter(codigoProductoTerminado=producto)
            consumos = []
            faltante = False

            for detalle in detalles:
                requerido = detalle.cantidad * cantidad
                disponible = detalle.codigoMateriaPrima.cantidad
                consumos.append({
                    "materia": detalle.codigoMateriaPrima,
                    "requerido": requerido,
                    "disponible": disponible,
                    "suficiente": disponible >= requerido
                })
                if disponible < requerido:
                    faltante = True

            if faltante:
                messages.error(request, "No hay suficiente materia prima para esta producción")
            else:
                return render(request, "produccion/produccion_confirm.html", {
                    "producto": producto,
                    "cantidad": cantidad,
                    "consumos": consumos
                })

    else:
        form = ProduccionForm()

    return render(request, "produccion/produccion_form.html", {"form": form, "producto": producto})


@login_required
def produccion_confirm(request):
    if request.method != "POST":
        return redirect("producto_list")

    codigo = request.POST.get("codigo")
    cantidad = request.POST.get("cantidad")

    if not codigo or not cantidad:
        messages.error(request, "Faltan datos de producción")
        return redirect("producto_list")

    producto = get_object_or_404(ProductoTerminado, codigo=codigo)

    try:
        produccion = producir_producto(producto, Decimal(cantidad))
        messages.success(request, f"Producción de {cantidad} {producto.nombre} registrada correctamente")
        return redirect("produccion_detail", produccion.id)
    except ValidationError as e:
        messages.error(request, str(e))
        return redirect("produccion_preview", codigo=producto.codigo)



@login_required
def produccion_list(request):
    producciones = Produccion.objects.all().order_by("-fecha")
    return render(request, "produccion/produccion_list.html", {"producciones": producciones})


@login_required
def produccion_detail(request, pk):
    produccion = get_object_or_404(Produccion, pk=pk)
    consumos = ConsumoMateriaPrima.objects.filter(produccion=produccion)

    return render(request, "produccion/produccion_detail.html", {
        "produccion": produccion,
        "consumos": consumos
    })
