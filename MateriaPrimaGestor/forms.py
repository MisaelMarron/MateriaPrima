from django import forms
from .models import *
from django.forms import inlineformset_factory

# Proveedor 
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre"]
        labels = {"nombre": "Nombre del proveedor"}
        widgets = {"nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese nombre"})}

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if not nombre:
            raise forms.ValidationError("El nombre no puede estar vacío.")
        return nombre

# materia prima
class MateriaPrimaCreateForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ["nombre", "unidad", "cantidad", "costo"]

class MateriaPrimaUpdateForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ["codigo", "nombre", "unidad", "costo"]

class MateriaPrimaAjusteForm(forms.Form):
    TIPO = (
        ("SUMAR", "Agregar"),
        ("RESTAR", "Quitar"),
    )
    tipo = forms.ChoiceField(choices=TIPO)
    cantidad = forms.DecimalField(min_value=0.00001, max_digits=12, decimal_places=5)

# compra 
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ["proveedor", "materia_prima", "cantidad", "costo"]

# producto terminado
class ProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = ["nombre", "codigo"]

class DetalleProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ["materia_prima", "cantidad"]

DetalleProductoFormSet = inlineformset_factory(
    ProductoTerminado,
    DetalleProducto,
    form=DetalleProductoForm,
    extra=0,
    can_delete=True
)

class ProduccionAjusteForm(forms.Form):
    TIPO = (
        ("SUMAR", "Agregar"),
        ("RESTAR", "Quitar"),
    )

    tipo = forms.ChoiceField(choices=TIPO, label="Tipo de ajuste")

    cantidad = forms.IntegerField(
        min_value=1,
        label="Cantidad de unidades"
    )

# produccion 
class ProduccionForm(forms.ModelForm):
    class Meta:
        model = ProduccionProducto
        fields = ["producto", "cantidad", "cantidad_unidad"]
        labels = {
            "cantidad": "Cantidad de bulk",
            "cantidad_unidad": "Cantidad de producto"
        }