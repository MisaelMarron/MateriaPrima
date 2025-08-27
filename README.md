# Inicio del proyecto

## MateriaPrima 
(PK) codigo (unico) 
Nombre = String 
Cantidad en Kg = decimal con 5 digitos

## Formula
(PK) codigo (unico)
version = entero
Nombre = String 

## MateriaFormula
(PK) codigoMateriaPrima = **MateriaPrima**
(PK) codigoFormula = **Formula**
Cantidad por cada Kg = decimal con 5 digitos