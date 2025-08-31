from django import forms
from .models import MateriaPrima

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