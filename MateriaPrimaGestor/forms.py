from django import forms
from .models import MateriaPrima

# formulario para Materia Prima
class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ["codigo", "nombre", "cantidad"]

class AjusteCantidadForm(forms.Form):
    ajuste = forms.DecimalField(
        max_digits=20,
        decimal_places=5,
        help_text="Ingresa un número positivo para agregar, negativo para quitar"
    )