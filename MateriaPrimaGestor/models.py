from django.db import models

class MateriaPrima(models.Model):
    codigo = models.CharField(max_length=20, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=20, decimal_places=5)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
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
        return f"{self.codigoProductoTerminado.nombre} usa {self.cantidad} Kg de {self.codigoMateriaPrima.nombre}"