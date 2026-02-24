from django.db import models
from django.db.models.functions import Substr
from django.db.models import Max, IntegerField
from django.core.validators import MinValueValidator

class Proveedor(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True)
    def __str__(self):
        return f"{self.nombre}"

class MateriaPrima(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10, unique=True)
    UNIDADES = [("KG", "Kilogramos"), ("L", "Litros"), ("G", "Gramos"), ("ML", "Mililitros"), ("U", "Unidad")]
    nombre = models.CharField(max_length=150, unique=True)
    unidad = models.CharField(max_length=5, choices=UNIDADES)
    cantidad = models.DecimalField(max_digits=12, decimal_places=5, validators=[MinValueValidator(0)])
    costo = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre
    def save(self, *args, **kwargs):
        if not self.codigo:
            valid_codes = MateriaPrima.objects.filter(codigo__regex=r'^INS\d{3}$')
            if valid_codes.exists():
                max_code = valid_codes.aggregate(max_num=Max(Substr('codigo', 4, output_field=IntegerField())))['max_num']
                next_number = max_code + 1
            else:
                next_number = 1
            self.codigo = f'INS{next_number:03d}'
        super().save(*args, **kwargs)

class Compra(models.Model):
    codigo = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=12, decimal_places=5, validators=[MinValueValidator(0)])
    costo = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class ProductoTerminado(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=150, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombre

class DetalleProducto(models.Model):
    codigo = models.AutoField(primary_key=True)
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=12, decimal_places=5, validators=[MinValueValidator(0)])
    class Meta:
        constraints = [models.UniqueConstraint(fields=["producto", "materia_prima"], name="unique_materia_por_producto")]

class ProduccionProducto(models.Model):
    codigo = models.AutoField(primary_key=True)
    producto = models.ForeignKey(ProductoTerminado, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=12, decimal_places=5, validators=[MinValueValidator(0)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class ProduccionDetalle(models.Model):
    codigo = models.AutoField(primary_key=True)
    produccion = models.ForeignKey(ProduccionProducto, on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT)
    costo = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    cantidad = models.DecimalField(max_digits=12, decimal_places=5, validators=[MinValueValidator(0)])
    class Meta:
        constraints = [models.UniqueConstraint(fields=["produccion", "materia_prima"], name="unique_materia_por_produccion")]
