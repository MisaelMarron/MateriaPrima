from django import forms
from django.forms import inlineformset_factory
from .models import MateriaPrima, ProductoTerminado, DetalleProducto

# formulario para Materia Prima
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


# Formset (tabla secundaria)
DetalleProductoFormSet = inlineformset_factory(
    ProductoTerminado, DetalleProducto,
    form=DetalleProductoForm,
    extra=1, can_delete=True
)