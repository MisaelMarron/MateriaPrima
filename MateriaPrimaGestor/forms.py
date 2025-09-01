from django import forms
from .models import MateriaPrima, ProductoTerminado

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