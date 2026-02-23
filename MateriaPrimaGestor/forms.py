from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from .models import Proveedor

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

"""# formulario para Materia Prima
class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ["codigo", "nombre", "unidad"]

class AjusteCantidadForm(forms.Form):
    agregar = forms.DecimalField(
        max_digits=20,
        decimal_places=5
    )

# formulario para ProductoTerminado
class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = ProductoTerminado
        fields = ['codigo', 'nombre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # si es edición
            self.fields['codigo'].disabled = True


class DetalleProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ['codigoMateriaPrima', 'cantidad']

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que 0")
        return cantidad

# Formset (tabla secundaria)
class BaseDetalleProductoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        materias_primas = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                mp = form.cleaned_data['codigoMateriaPrima']
                if mp in materias_primas:
                    raise forms.ValidationError("No se puede repetir la misma materia prima en un producto")
                materias_primas.append(mp)

DetalleProductoFormSet = inlineformset_factory(
    ProductoTerminado, DetalleProducto,
    form=DetalleProductoForm,
    formset=BaseDetalleProductoFormSet,
    extra=1,
    can_delete=True
)

class ProduccionForm(forms.Form):
    cantidad = forms.DecimalField(
        max_digits=20, decimal_places=5, min_value=0.00001,
        label="Cantidad a producir (kg)"
    )
"""