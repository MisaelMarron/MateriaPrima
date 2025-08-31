from django.db import models
from django.core.exceptions import ValidationError

class MateriaPrima(models.Model):
    UNIDADES = [
        ("kg", "Kilogramo"),
        ("L", "Litro"),
        ("UNIDAD", "Unidad"),
    ]

    codigo = models.CharField(max_length=20, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=20, decimal_places=5, default=0)
    unidad = models.CharField(max_length=10, choices=UNIDADES, default="kg")
    ultima_vez_actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def clean(self):
        if self.cantidad < 0:
            raise ValidationError("La cantidad debe ser positiva")
    
class ProductoTerminado(models.Model):
    codigo = models.CharField(max_length=20, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
class DetalleProducto(models.Model):
    codigoMateriaPrima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    codigoProductoTerminado = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        unique_together = ("codigoMateriaPrima", "codigoProductoTerminado")

    def __str__(self):
        return f"{self.codigoProductoTerminado.nombre} usa {self.cantidad} de {self.codigoMateriaPrima.nombre}"