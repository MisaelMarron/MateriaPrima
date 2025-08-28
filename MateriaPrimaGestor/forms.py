from django import forms
from .models import MateriaPrima

# formulario
class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ["codigo", "nombre", "cantidad"]
