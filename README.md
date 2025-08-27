# Inicio del proyecto

## MateriaPrima 
(PK) codigo (unico) 
nombre = String 
cantidad (Kg) = decimal con 5 digitos

## ProductoTerminado
(PK) codigo (unico)
nombre = String 

## DetalleProducto
(PK) codigoMateriaPrima = **MateriaPrima**
(PK) codigoProductoTerminado = **ProductoTerminado**
cantidad (Kg) = decimal con 5 digitos