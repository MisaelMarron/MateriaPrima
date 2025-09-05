from decimal import Decimal
from django.core.exceptions import ValidationError
from .models import DetalleProducto, Produccion, ConsumoMateriaPrima

def producir_producto(producto, cantidad: Decimal):
    detalles = DetalleProducto.objects.filter(codigoProductoTerminado=producto)

    if not detalles.exists():
        raise ValidationError("El producto no tiene receta definida.")

    # Verificamos stock
    for detalle in detalles:
        requerido = detalle.cantidad * cantidad
        if detalle.codigoMateriaPrima.cantidad < requerido:
            raise ValidationError(
                f"No hay suficiente {detalle.codigoMateriaPrima.nombre}. "
                f"Se requiere {requerido}, disponible {detalle.codigoMateriaPrima.cantidad}"
            )

    # Si alcanza, descontamos y registramos
    produccion = Produccion.objects.create(
        producto=producto,
        cantidad_producida=cantidad
    )

    for detalle in detalles:
        requerido = detalle.cantidad * cantidad
        materia = detalle.codigoMateriaPrima
        materia.cantidad -= requerido
        materia.save()

        # Guardamos detalle de consumo
        ConsumoMateriaPrima.objects.create(
            produccion=produccion,
            materia_prima=materia,
            cantidad_usada=requerido
        )

    return produccion
